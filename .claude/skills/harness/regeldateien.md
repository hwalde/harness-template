# Regeldateien: AGENTS.md, CLAUDE.md, Unterordner, rules
**Kern:** Die Regeldatei wird bei jedem Start gelesen – hinein gehört nur, was immer gilt, plus die Fallstricke, die wehtun. Alles Aufgabenspezifische wird ausgelagert und verlinkt. (Kontext: Harness-Template | Stand: 2026-08-30)

## Zwei Namen, eine Datei
- `AGENTS.md` ist der agentenübergreifende Standard; Claude Code liest `CLAUDE.md`. Lösung dieses Templates: **`CLAUDE.md` enthält genau eine Zeile `@AGENTS.md`** (Include-Syntax von Claude Code), alles Wissen steht in `AGENTS.md`. Regel: In jedem Ordner, in dem eine `AGENTS.md` angelegt wird, wird daneben eine `CLAUDE.md` mit `@AGENTS.md` angelegt. Im Kontext erscheinen beide als Memory-Dateien; prüfen mit `/context` (Claude Code) bzw. dem Kontext-Befehl des Agenten.
- Dateinamen in Großbuchstaben (manche Agenten akzeptieren Kleinschreibung, Best Practice ist groß).
- `CLAUDE.local.md` (bzw. das Gegenstück des Agenten): wird zum selben Zeitpunkt gelesen, bleibt aber lokal beim Entwickler (gitignored) – für persönliche Vorlieben und maschinenspezifische Werte (Ports, Pfade).
- Welche Agenten was lesen und ob sie Includes können: [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md).

## Die vier Orte
| Ort | Zweck | Wann gelesen |
|---|---|---|
| Projektwurzel | Überblick, Regeln, Workflow, Fallstricke | sofort beim Start |
| Parent-Ordner (Monorepo) | Gemeinsames für alle Unterprojekte | sofort beim Start (Unterprojekt öffnen → Parent wird mitgelesen) |
| Benutzerordner (z. B. `~/.claude/CLAUDE.md`) | projektübergreifende persönliche Regeln (Sprache, Schreibweise) | sofort beim Start |
| Unterordner | nur für Arbeit in diesem Ordner (Fachmodul) | **situativ** – erst wenn der Agent dort eine Datei liest oder arbeitet; verschachtelte Unterordner ziehen die übergeordneten Dateien mit |

Situativ geladene Regeln landen am Ende des Chats – der Position, auf die das Modell am aufmerksamsten ist. Das macht Unterordner-Regeldateien und rules-Dateien wirksamer als denselben Text in der Wurzel.

## Was hinein gehört – und was nicht
**Hinein (in ca. 20 Zeilen Kernregeln):**
- Projektbeschreibung in einem Satz; grober Aufbau (bewusst unvollständig).
- Die wichtigsten Architektur- und Coding-Regeln (Pareto: 80/20 – „wir nutzen DDD, X machen wir auf Art Y"), nicht die tausend Guidelines.
- Der Standard-Workflow (Reihenfolge der Schritte, siehe [workflow.md](workflow.md)) und die Abnahmepflicht (Evaluator).
- Werkzeuge und Skripte, die zu verwenden sind – je ein Satz, deutlich: „Für X IMMER `tools/y.py`, NICHT z."
- „Fallstricke, die Aua machen": Dinge, deren Fehlen viel Schmerz erzeugt („nach Änderung an X den Cache im Store leeren, sonst startet die App nicht"). Die einzige Ausnahme von der Sparsamkeitsregel.
- Testhinweise (dürfen etwas ausführlicher sein).
- Verweise: „Wo finde ich was?" – Dokumente, Ordner, Skills, und wer den Rest weiß (librarian).

**Nicht hinein:**
- Offensichtliches, das jedes Modell kennt (`npm run dev`, „das ist ein React-Projekt", was ein Repository ist, das Schichtenmodell).
- Situative Details, Coding-Guideline-Kataloge, Romane, lange Dokumentlisten – das gehört in verlinkte Dokumente, Unterordner-Regeldateien, rules oder Skills.
- Veraltete Regeln: Sie werden brav befolgt und machen die Datei zum Klotz. Bei jedem Fehlverhalten zuerst in die eigene Regeldatei schauen.
- Secrets, maschinenspezifische Werte (→ `CLAUDE.local.md`, Umgebungsvariablen).

Anthropic hat 90 % der eigenen Prompts in Claude Code gestrichen, weil sie nicht mehr halfen, sondern beschränkten. Haltung: klein halten, lieber Artefakte verlinken (auch komplexe: Test-Suite, Diagramm, Dokumentationsordner) – der Agent findet das Richtige darin selbst.

## Auslagern und verlinken
- Zweitdokument: „Wenn X vorkommt, lies `docs/x.md`." Inhalt steht nur dort.
- Ganzer Ordner: „Bevor du mit Arbeit in diesem Projekt beginnst, schau in den `docs`-Ordner, ob ein Dokument dein Thema berührt, und lies es dann." Gegenrichtung: Neu Erarbeitetes dort ablegen – **immer dazu sagen, was gespeichert werden soll und was nicht**, sonst speichert der Agent Unbrauchbares.
- Verlinkungs-Pattern statt Custom Subagent: Die Beschreibungen aller Custom Subagents liegen dauerhaft im Kontext (Größenordnung ein paar tausend Tokens). Ein Dreizeiler „Wenn du X wissen willst, starte einen Subagenten, der `docs/x-experte.md` liest und den Anweisungen folgt" hat denselben Effekt ohne Dauerkosten. Custom Subagent nur, wenn er ständig gebraucht wird oder viel Wissen/eine klare Rolle trägt (evaluator, librarian).
- Skill statt Regeldatei für Wissen, das nicht jeden Lauf angeht (Coding-Guidelines, Weiterentwicklungswissen eines Systems, dessen Einstiegspunkt selbst ein Agent ist) → [skills-und-commands.md](skills-und-commands.md).

## Unterordner-Regeldateien (fachliche Module)
- Voraussetzung: ein fachlich geschnittener Ordnerbaum (Screaming Architecture – von außen sieht man, worum es geht) und ein Agent, der Regeldateien in Unterordnern situativ lädt (prüfen in [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md) – der dortige Snapshot nennt es u. a. für Claude Code und Codex, verifiziert wird bei der Einrichtung).
- Hinein: nur das, was über den normalen Gebrauch hinausgeht – modulspezifische Fallstricke, Konventionen, Schnittstellen. Nicht: was ein Service oder Repository ist.
- Auch hier: `AGENTS.md` + `CLAUDE.md` mit `@AGENTS.md` nebeneinander.

## rules-Dateien (pfadgebundene Regeln)
- Was: Prompt-Dateien, deren Geltung an Dateipfade/-muster gebunden ist – sie werden nur geladen, wenn der Agent eine passende Datei anfasst. Beispiel: Gestaltungsregeln nur für Testdateien, Frontend-Konventionen nur für `src/ui/**`.
- Wo: Claude Code `.claude/rules/*.md` mit Frontmatter `paths:`; Cursor `.cursor/rules/*.mdc` mit `globs`/`alwaysApply`; GitHub Copilot `.github/instructions/*.instructions.md` mit `applyTo`. Andere Agenten: [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md).
- Faustregel: Eine Regel, die nur situativ gelesen werden soll, gehört genau dorthin – nicht in die Wurzel-Regeldatei.

## Für die KI schreiben, nicht für Menschen
- Zielgruppe ist das Modell: eigener Wortschatz, Fachbegriffe/Buzzwords statt Erklärsätze, kristallklar, keine Höflichkeitsprosa. Menschendokumente bei Bedarf in zwei Fassungen (ausführlich für Menschen, knapp für die KI).
- **Regeln begründen:** Anweisungen mit Begründung werden eher befolgt. Nie gegen den Systemprompt argumentieren („die Regel des Systemprompts ist aufgehoben") – höhere Gewichtung, Prompt-Injection-Verdacht. Stattdessen Nutzung fordern, Dringlichkeit erhöhen, begründen.
- WICHTIG / NICHT / IMMER für kritische Regeln – das fällt Agenten auf.
- Zahlen statt Adjektive: „max. drei Sätze" wirkt zuverlässiger als „kurz". Aber: „maximal drei Sätze" liefert immer drei Sätze, „tokensparend" liefert Unverständliches – Ergebnis prüfen, testen, dann committen.
- Regeln vom Agenten für sich selbst formulieren lassen (Meta-Prompting): Ziel nennen („Was muss in `AGENTS.md`, damit der librarian weiterhin konsultiert wird?") plus Rahmen: sehr kompakt, für dich geschrieben, nicht über andere Agenten reden, ein bis drei Sätze. `/init`-Ergebnisse sind fast immer zu lang – Kürze beim Aufruf verlangen.
- Wiederholst du einen Satz zum wiederholten Mal im Chat, lässt du ihn im selben Auftrag in die Regeldatei aufnehmen („bei nicht lesbaren Webseiten Playwright-MCP verwenden"). So wächst der Harness nebenbei.

## Anti-Patterns
Situative Details oder Guideline-Kataloge in der Wurzel · Offensichtliches · Romane · veraltete Regeln · Regeln ohne Begründung · Skripte/Tools nicht erwähnt · Speicheranweisung ohne „was rein, was nicht" · Evaluator ohne Abnahmepflicht-Eintrag · Menschentexte 1:1 für die KI · Kleinschreibung der Dateinamen.
