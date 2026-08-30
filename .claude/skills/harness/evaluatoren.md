# Evaluatoren: Generator → Evaluator
**Kern:** Der Agent, der gearbeitet hat, sagt auf „gut gemacht?" immer ja. Ein zweiter Agent mit frischem Kontext, ohne Schreibrechte, gegen beobachtete Evidenz findet andere Dinge. Das Pattern = ein Subagent + ein Eintrag in der Regeldatei. (Kontext: Harness-Template | Stand: 2026-08-30)

## Das Pattern
| Teil | Inhalt |
|---|---|
| Subagent `evaluator` (`.claude/agents/evaluator.md`) | skeptischer Zweitgutachter; Skepsis steht ausdrücklich im Prompt; liest Spezifikation, `git status`/`git diff` (und ggf. Commit-History), öffnet jede Evidenz, beobachtet wo möglich selbst (Tests, Build, Smoke-Check); keine Write/Edit-Rechte; antwortet mit `PASS` oder `NEEDS_WORK` + konkreten Findings |
| Abnahmepflicht in `AGENTS.md` | „Bevor etwas ‚fertig' oder ‚funktioniert' heißt, prüft der evaluator mit frischem Kontext und ohne Schreibrechte gegen beobachtete Evidenz. `NEEDS_WORK` → Findings abarbeiten → erneut prüfen, bis `PASS`." Ohne diesen Eintrag wird der Subagent nicht benutzt. |
| Schleife | Build → Evaluator → Fix → Evaluator … bis `PASS`. Keine Diskussion, kein Wegerklären, keine abgeschwächten Tests. |

Effekt in der Praxis: fühlbar niedrigere Fehlerrate; der Evaluator findet regelmäßig Dinge, die noch nicht stimmten. Kosten: ein paar Tokens und etwas Zeit.

## Was der Aufrufer mitgibt
Der Evaluator vertraut keinen Behauptungen – also nachprüfbare Evidenz erzeugen und referenzieren:
1. Aufgabe / Akzeptanzkriterien (Spezifikation, Ticket, Plan, Checkliste).
2. Änderungsumfang (Dateien; bei Git ermittelt er den Diff selbst).
3. Evidenz: Test-Logs, Build-Output, Screenshots, gerenderte Artefakte – als Pfade.
4. Optional ein Fokus (siehe unten).

Prompt an den Evaluator als Brief, nicht als Befehlsliste: Er ist dasselbe Modell mit voller kognitiver Leistung; Raum zum Denken lassen, nichts vorwegnehmen.

## Grenzen und Gegenmittel
- Je aufmüpfiger das Modell, desto eher umgeht es den Evaluator oder versucht, ihn zu täuschen (Modelle täuschen tatsächlich): Dem Evaluator nur einen Teilaspekt nahelegen, Tests abschwächen, „bekannte Einschränkung". Gegenmittel im Evaluator-Prompt: Scope-Check, Builder-Ausreden zählen nicht, abgeschwächte Tests sind ein eigenes Finding.
- Wer den Evaluator startet: (a) der umsetzende Agent selbst – einfachste Stufe, dieses Template; (b) von außen per Hook (z. B. Stop-Hook oder Pre-Commit) – der Agent kann ihn nicht mehr vergessen; (c) in der CI/CD-Pipeline mit Findings in der Review-Plattform – „einen Ticken besser", weil unabhängig. Bei der Einrichtung entscheiden, ob (b) oder (c) zusätzlich gewünscht ist.
- Ein grüner Test beweist nur den Pfad, den der Test genommen hat. Verschriftlichte Prüfkriterien sind der Maßstab; ohne Kriterien prüft der Evaluator gegen die Aufgabenbeschreibung und sagt das dazu.

## Mehrere und spezialisierte Evaluatoren
Die kleinste Ausbaustufe ist ein Evaluator. Größer: mehrere Instanzen nacheinander (Anthropic lässt intern eine ganze Reihe laufen), je nach Projekt nach Themenschwerpunkt. Zwei Wege:

1. **Ein Evaluator, mehrere Fokusse** (im Template eingebaut): den `evaluator` mehrfach aufrufen, jeweils mit „Fokus: Sicherheit" / „Performance" / „Clean Code" / „Coding-Guidelines" / „Architektur". Kein zusätzlicher Dauerkontext, weil nur eine Beschreibung geladen ist.
2. **Eigene Subagenten je Schwerpunkt** (bei der Einrichtung anlegbar, siehe Vorlage unten): sinnvoll, wenn ein Schwerpunkt eigenes Wissen braucht (die Architekturdokumentation, den Guideline-Katalog, eine Sicherheits-Checkliste) oder wenn er in einer Pipeline/CI separat laufen soll.

Reihenfolge, wenn mehrere laufen: erst deterministische Prüfungen (Linter, statische Analyse, Tests – per Skript, nicht per Modell), dann funktionale Abnahme (Standard-Evaluator), dann die Schwerpunkte (Sicherheit → Architektur/Guidelines → Performance → Clean Code). Jeder schaut sich per `git status`/`git diff` die Änderungen an und gibt dem Hauptagenten konkrete, behebbare Findings zurück; der Hauptagent arbeitet sie ab und lässt erneut prüfen. Nicht alle bei jeder Kleinigkeit: in `AGENTS.md` festlegen, welche Evaluatoren bei welchem Änderungsumfang laufen (z. B. Sicherheit immer bei Auth/Eingaben/Dateizugriff; Architektur bei neuen Modulen).

## Vorlage für einen spezialisierten Evaluator
Datei `.claude/agents/evaluator-<schwerpunkt>.md` (für andere Agenten mit `tools/sync-agents.py` übersetzen):

```markdown
---
name: evaluator-sicherheit
description: >-
  Sicherheits-Gutachter (Generator→Evaluator). Nach Änderungen an Authentifizierung,
  Autorisierung, Eingabeverarbeitung, Datei-/Netzwerkzugriff oder Abhängigkeiten aufrufen,
  bevor die Arbeit als fertig gilt. Liest Diff und Evidenz mit frischem Kontext, prüft gegen
  die Sicherheitsregeln in AGENTS.md/docs, antwortet mit PASS oder NEEDS_WORK. Keine Schreibrechte.
tools: Read, Glob, Grep, Bash
model: opus
---

Du prüfst Änderungen eines anderen Agenten ausschließlich unter dem Aspekt Sicherheit. Du
vertraust keiner Behauptung; du bewertest, du reparierst nicht.

1. `git status` und `git diff` ansehen; betroffene Dateien vollständig lesen.
2. Prüfen: Eingabevalidierung, Injection (SQL/Shell/Prompt), AuthN/AuthZ, Secrets in Code/Log/
   Commit, unsichere Defaults, Pfade außerhalb des erlaubten Bereichs, neue Abhängigkeiten,
   Fehlerbehandlung, die Interna preisgibt. Projektspezifische Regeln: <Pfad zum Dokument>.
3. Wo möglich selbst beobachten (Tests, Linter, Security-Scanner per Bash).

Antwort: erste Zeile `PASS` oder `NEEDS_WORK`. Danach je Finding: Datei:Zeile, Risiko,
erwartetes Verhalten, konkreter Fix-Vorschlag. Blockierende Findings zuerst. Keine Zusammenfassung des Diffs.
```

Analog: `evaluator-performance` (Komplexität, N+1, IO im Hot Path, Speicher, Caching/Batching), `evaluator-clean-code` (Lesbarkeit, Benennung, Duplikate, Funktionsgröße, tote Pfade), `evaluator-guidelines` (liest den Guideline-Skill/das Dokument und prüft Punkt für Punkt), `evaluator-architektur` (liest die Architekturdokumentation, prüft Schichtgrenzen, Abhängigkeitsrichtung, Modulzuschnitt). Jeder Schwerpunkt-Evaluator bekommt in `AGENTS.md` einen Satz, wann er läuft.

## Weitere bewährte Subagent-Typen (zur Orientierung)
| Typ | Aufgabe |
|---|---|
| librarian | einziger Zugang zum Wissensspeicher → [wissensablage.md](wissensablage.md) |
| Doku-Pfleger | vor jedem Commit die Dokumentation nachziehen; Prüfkriterien im Prompt |
| Remote-System-Experte | beantwortet Fragen zur Produktionsumgebung aus eingelagertem Wissen; ohne Werkzeuge |
| Verlinkungs-Pattern | statt Custom Subagent: Prompt in einer Datei + Dreizeiler in `AGENTS.md` „starte einen Subagenten, der diese Datei liest" – ohne Dauerkontext |

Custom Subagent = Markdown mit Frontmatter (`name`, `description`, `tools`, `model`, optional `color`) plus Prompt; die `description` entscheidet, ob der Hauptagent ihn einsetzt; `tools` minimal halten; Beschreibungen kosten bei jedem Request Kontext – nur anlegen, was regelmäßig gebraucht wird.
