# Einrichtung des Harness – geführt, Schritt für Schritt
**Kern:** Du (der Coding-Agent) richtest den Harness gemeinsam mit dem Benutzer ein. Jeder Schritt klärt eine Entscheidung, die nur der Benutzer treffen kann, und hinterlässt einen knappen Eintrag in `AGENTS.md`. Nichts wird geraten, nichts auf Vorrat installiert. (Kontext: Harness-Template | Stand: 2026-08-30)

## Bevor du beginnst
- Du hast **alle** Dokumente dieses Skills gelesen (`index.md` → jede Datei). Halbwissen ist gefährlich: Die Entscheidungen unten setzen die Zusammenhänge voraus.
- Arbeitsweise: Schritt für Schritt, je Schritt die Optionen mit einer begründeten Empfehlung vorlegen (mit dem Fragewerkzeug deines Agenten, sonst als Text), Antwort abwarten, Ergebnis sofort in `AGENTS.md` eintragen – **ein Satz je Notiz**, Fachbegriffe, mit Begründung, wo eine Regel sonst unverständlich wäre. Platzhalter-Kommentare in `AGENTS.md` ersetzt du durch Inhalt oder entfernst sie.
- Nichts installieren, was der Benutzer nicht bestätigt hat; keine Secrets in Dateien schreiben; maschinenspezifische Werte gehören in `CLAUDE.local.md` (gitignored) oder Umgebungsvariablen.
- Der Benutzer darf Schritte überspringen. Übersprungene Schritte notierst du am Ende als offene Punkte.
- Halte Ordnung: Ein neuer Harness-Baustein (Skript, Subagent, Skill, MCP-Eintrag) bekommt sofort seinen Satz in `AGENTS.md` – ein unbekannter Baustein existiert für den Agenten nicht.

## Schritt 0 – Sprache
Die Harness-Dateien (`AGENTS.md`, Subagenten, dieser Skill, Wiki-Skelett) sind auf Deutsch geschrieben – Agenten lesen das unabhängig von der Projektsprache; nur die READMEs des Templates sind dreisprachig, weil Menschen sie lesen.
- Frage, in welcher Sprache der Benutzer mit dem Agenten arbeitet und in welcher Sprache Dokumentation und Kommentare des Projekts geführt werden; notiere das unter „Projekt".
- Wünscht der Benutzer die Harness-Dateien in seiner Sprache, übersetze sie jetzt einmalig an Ort und Stelle (Struktur, Pfade, Befehle, Protokollwörter wie `NICHT IM WIKI`/`PASS`/`NEEDS_WORK` konsistent halten), danach `python3 tools/sync-agents.py` ausführen. Es gibt bewusst nur EINE Fassung – keine Sprachspiegel, kein Sync-Aufwand.
- Die Skripte in `tools/` sprechen Englisch (Quellcode-Sprache) – das bleibt so.

## Schritt 1 – Das Projekt kennenlernen
Sieh dich um (Repo-Struktur, Build-System, vorhandene Regeldateien, `docs/`, Tests, CI) und frage nach, was du nicht sehen kannst:
- Worum geht es (ein Satz)? Anwendungstyp: Kommandozeile, Bibliothek, Web-Anwendung, Desktop-Anwendung, Dienst/API, Datenpipeline – das entscheidet Schritt 4.
- Wie wird gebaut, getestet, gestartet, released? Gibt es einen einzigen richtigen Weg (→ später als IMMER/NICHT-Regel)?
- Ist der Ordnerbaum fachlich geschnitten (Module) oder technisch (Schichten)? (→ Schritt 3)
- Was tut regelmäßig weh (Fallstricke)?
Trage „Projekt" und „Fallstricke" in `AGENTS.md` ein. Ist das Template in ein bestehendes Projekt kopiert worden: vorhandene `CLAUDE.md`/`AGENTS.md`-Inhalte in die neue `AGENTS.md` einarbeiten (nur was immer gilt, siehe [regeldateien.md](regeldateien.md)), `CLAUDE.md` auf `@AGENTS.md` reduzieren.

## Schritt 2 – Coding-Agenten und ihre Fähigkeiten
1. Frage, welche Coding-Agenten in diesem Projekt arbeiten (Claude Code, Codex, Gemini CLI, Cursor, opencode, Copilot, hermes, andere) – auch die der Kollegen.
2. Untersuche **für jeden genannten Agenten aktuell** nach [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md): Regeldatei und Includes, Unterordner-Regeldateien, rules, Custom Subagents, Skills, Slash Commands, projektlokale MCP-Konfiguration, Hooks/Cron, rückfragefreier Modus, Headless-Start. Offizielle Doku plus `--help` auf dieser Maschine; im Zweifel eine Probe.
3. Setze um:
   - Subagenten: Quelle `.claude/agents/`; für jeden weiteren Agenten das Format erzeugen (`tools/sync-agents.py` erweitern, falls ein Zielformat fehlt).
   - Skills: Liegt der Harness-Skill unter `.claude/skills/harness/` dort, wo der Agent sucht? Sonst an seinen Skill-Ordner kopieren/verlinken (im Projekt bleiben, nicht auf Benutzerebene). Kennt ein Agent keine Skills, bleibt der Satz in `AGENTS.md`, die `SKILL.md` direkt zu lesen – sonst kann er auf „lade den Skill `harness`" gekürzt werden.
   - Regeldateien: Bestätige die Regel `CLAUDE.md` = `@AGENTS.md` (ein Satz steht bereits in `AGENTS.md`); für Agenten mit eigenem Dateinamen (z. B. `GEMINI.md`) dieselbe Include-Lösung oder die Konfiguration, die `AGENTS.md` liest.
   - `tools/agent-start.py`: Flags in der Tabelle am Skriptanfang gegen die installierten Versionen prüfen (`doctor`, `--dry-run`).
4. Je Agent **ein Satz** unter „Coding-Agenten in diesem Projekt".

## Schritt 3 – Wissensablage
Lies dazu [wissensablage.md](wissensablage.md) und entscheide mit dem Benutzer:
1. **LLM-Wiki mit librarian – ja oder nein?** Ja, wenn es Wissen gibt, das in keinem Repo steht (Betrieb, Zugänge, Domäne, Entscheidungen) und das Projekt lebt. Nein → `.my-memory/`, `.claude/agents/librarian.md` (und generierte Varianten) sowie den Wiki-Abschnitt in `AGENTS.md` entfernen; stattdessen einen `docs/`-Ordner mit dem Satz „Bevor du mit Arbeit in diesem Projekt beginnst, schau in den `docs`-Ordner, ob ein Dokument dein Thema berührt, und lies es dann" plus einer Zeile, was dort gespeichert wird und was nicht.
2. **Regeln schärfen:** Was gehört in diesem Projekt konkret ins Wiki (bzw. in `docs/`), was nicht? Beispiele aus dem Projekt nennen (z. B. „Deploy-Reihenfolge und ihr Warum: rein; Endpoint-Liste: raus – steht im Code"). Die geschärften Beispiele als Halbsätze in den Wiki-Abschnitt von `AGENTS.md`.
3. **Alternativen prüfen und ggf. kombinieren:**
   - Regeldateien in Unterordnern: nur wenn der Ordnerbaum fachlich geschnitten ist **und** die eingesetzten Agenten sie situativ laden (Schritt 2). Dann je Fachmodul `AGENTS.md` + `CLAUDE.md` (`@AGENTS.md`) anlegen – nur mit dem, was über den normalen Gebrauch hinausgeht.
   - Dokumente aus `AGENTS.md` verlinken (ein Satz genügt, siehe oben).
   - rules-Dateien: erklären, was das ist (pfadgebundene Regeln, nur geladen, wenn passende Dateien angefasst werden), prüfen, ob die Agenten es unterstützen, und bei Bedarf anlegen (z. B. Testregeln nur für `tests/**`).
4. Ergebnis als Sätze in `AGENTS.md`; bei Wiki: die Einrichtungsentscheidungen dieser Session am Ende über den librarian einlagern (Kontext: „Harness dieses Projekts").

## Schritt 4 – Befähigung: MCP-Server und Zugänge
Lies [mcp-und-werkzeuge.md](mcp-und-werkzeuge.md). Ziel: Der Agent kommt selbst an Informationen, kann selbst testen und sich Dinge selbst anschauen.
1. **Web-Anwendung → Playwright-MCP empfehlen:** Der Agent kann die Anwendung über den Browser bedienen, ausprobieren, Screenshots machen, Konsole und Netzwerk lesen. Hinweis geben: Das ersetzt keine Unit-/E2E-Tests. Bauform besprechen (frischer Browser vs. eigener Tab-Reihe; auf Servern headless).
2. **Desktop-Anwendung → cua-computer-use empfehlen:** dasselbe für Desktop-Apps. Regel in `AGENTS.md`, dass Computer Use zum Debuggen erlaubt ist – sonst nutzt er es nicht.
3. **Weitere Server nur mit Use Case:** Ticket-/CI-/Wiki-Systeme (erst prüfen, ob ein CLI reicht), lesendes Postfach, Datenbanken, Vision, Bildgenerierung. Für jeden Kandidaten die Entscheidungsregel MCP vs. Skript anwenden und den Kontextpreis nennen.
4. **Zugänge und rote Linien:** Was darf der Agent lesen, was ausführen, was nie ohne Freigabe (E-Mail-Versand, Deployments, Produktivsysteme, Zahlungen)?
5. Umsetzen: projektlokale MCP-Konfiguration (Dateiname je Agent aus Schritt 2), Secrets über Umgebungsvariablen, Regel „für X IMMER Werkzeug Y" in `AGENTS.md`, Kontextverbrauch vorher/nachher prüfen.

## Schritt 5 – Skripte, die dem Agenten zuarbeiten
Lies [skripte.md](skripte.md). Frage: Welche Handarbeit fällt hier regelmäßig an, die algorithmisch ist? Typische Kandidaten: Server starten/stoppen mit Vorprüfung und Restart-Schutz, Log-Analyse mit Navigation, Test-Runner mit Diagnose-Aufbereitung, Build/Release über genau einen Weg, Datenbank-Migrationen, Statusprüfungen (läuft der Dienst, ist der Port frei, meldet der Health-Endpunkt Fehler), Zählen/Messen.
- Für jeden gewünschten Kandidaten: bauen nach den zehn Prinzipien (Python bevorzugt, kein venv, Hilfe ohne Argumente, menschenlesbare Ausgabe, schnell beenden, Fehlermeldung als Handlungsanweisung) unter `tools/`, testen, mit je einem Satz in `AGENTS.md` eintragen – inklusive „ersetzt X, NICHT mehr Y", wo es einen alten Weg gibt.
- Prüfe, ob bestehende Skripte des Projekts agentenfreundlich sind (Datendumps, JSON-Blobs, Langläufer) und schlage Umbauten vor.

## Schritt 6 – Autonome Läufe, Überwachung, Sicherheit
Lies [autonome-laeufe.md](autonome-laeufe.md) und [freilauf.md](freilauf.md).
1. **Rückfragefreie Läufe:** `python3 tools/agent-start.py doctor` und einen `--dry-run` zeigen; Permission-Modus und Allow-Liste des Agenten für den Modus ohne Rückfragen einrichten (bei Claude Code `dontAsk` plus `permissions.allow` in `.claude/settings.json`). tmux (macOS/Linux) bzw. psmux (Windows) empfehlen, wenn Läufe im Hintergrund weiterlaufen und beobachtbar sein sollen. Eintrag in „Werkzeuge und Skripte" ist vorhanden – ggf. projektspezifisch ergänzen (z. B. Standard-Agent, Standard-Modell).
2. **Usage-Tracking:** nur bei Abo-Kontingenten relevant – dort aber praktisch Pflicht für lange Läufe, denn bei 100 % sterben oder hängen die Subagenten und der Lauf ist tot. Wenn ja: Datenquelle klären (Kontingent-Befehl, Statusdaten, API) und ein Usage-Skript nach [skripte.md](skripte.md) bauen; die Regeln (Intervall verkürzen, ab 90 % warten, Subagenten prüfen selbst) in `AGENTS.md` bzw. in die Prompt-Vorlage für Läufe. Kosten getrennt.
3. **Selbstüberwachung:** Braucht das Projekt jemanden, der periodisch nach hängenden Skripten und verlaufenen Agenten sieht? Wenn ja: Prüfskript (`tools/watch.py` o. ä.) und die Anweisung, per Cron/Loop-Werkzeug des Agenten (z. B. `CronCreate`, `/loop`) alle N Minuten zu prüfen; Werkzeug beim Namen nennen; vorher mit einer trivialen Aufgabe testen.
4. **Nicht anhalten:** Goal-Befehl bzw. Loop des Agenten (Schritt 2 geklärt); Reihenfolge „erst Fragerunde, dann Goal" als Regel für Läufe.
5. **Sicherheit:** Sandbox (Micro-VM/Container) oder mindestens Worktree + Git + keine Produktivzugänge; Entscheidung in `AGENTS.md` festhalten.
6. **Überbau:** Wenn Läufe regelmäßig unbeaufsichtigt oder nach Zeitplan laufen sollen, freilauf vorstellen (Zeitpläne, Worktrees, Überwachung von außen, Budget-Gates, Merge, Benachrichtigung; `SETUP_WITH_AGENT.md` dort) – und darauf hinweisen, dass ein mit diesem Template eingerichtetes Projekt ohne Anpassung darin läuft.

## Schritt 7 – Architektur und Coding-Guidelines
Das ist der wichtigste inhaltliche Schritt. Lies [regeldateien.md](regeldateien.md) und [skills-und-commands.md](skills-und-commands.md).
1. Frage nach Architektur (Stil, Schichten/Module, Abhängigkeitsrichtung, Persistenz, Fehlerbehandlung, Logging) und Coding-Guidelines (Sprache/Version, Formatierung, Benennung, Tests, Reviews). Gibt es Dokumente? Lies sie.
2. **Kernregeln (Pareto, ca. 20 Zeilen)** unter „Architektur und Coding-Guidelines" in `AGENTS.md` – nur, was immer gilt und was ein Modell nicht ohnehin weiß.
3. **Katalog als Skill** anlegen (`.claude/skills/coding-guidelines/SKILL.md`, ggf. mit Referenzdateien), Beschreibung mit den Schlüsselwörtern des Teams („Code Review", „Guidelines"); in `AGENTS.md` ein Satz, wann er zu laden ist (bei Pflicht: IMMER vor der Abnahme). Optional ein zweiter Skill für die Architektur-Dokumentation. Deterministische Regeln (Formatierung, Linter) gehören in Skripte/Konfiguration, nicht in Prosa.
4. Wenn gewünscht: `evaluator-guidelines` und `evaluator-architektur` als eigene Subagenten nach der Vorlage in [evaluatoren.md](evaluatoren.md) – oder der Standard-evaluator mit Fokus.

## Schritt 8 – Subagenten und Evaluatoren
Lies [evaluatoren.md](evaluatoren.md).
1. evaluator und librarian sind da (librarian nur bei Wiki). Prüfe, ob ihre `description` und ihr `model` zum Projekt passen (Modellwahl je Agent aus Schritt 2).
2. **Schwerpunkt-Evaluatoren:** Sicherheit, Performance, Clean Code, Coding-Guidelines, Architektur – welche braucht das Projekt, als Fokus des Standard-evaluators oder als eigene Dateien? Für jeden: bei welchem Änderungsumfang läuft er (Sicherheit bei Auth/Eingaben/Dateizugriff immer; Architektur bei neuen Modulen; Performance bei Hot Paths/Datenzugriffen)? Reihenfolge: deterministische Prüfungen → funktionale Abnahme → Schwerpunkte. Als Sätze in den Abschnitt „Qualitätssicherung".
3. **Weitere Subagenten** nur mit klarer Rolle und regelmäßigem Bedarf (Doku-Pfleger vor Commits, Experte für die Produktionsumgebung); sonst Verlinkungs-Pattern (Prompt-Datei + Dreizeiler). Jede Subagent-Beschreibung kostet dauerhaft Kontext.
4. Evaluator von außen (Hook, CI) gewünscht? Dann einrichten, wenn der Agent Hooks kennt (Schritt 2).
5. Danach `python3 tools/sync-agents.py`.

## Schritt 9 – Der Workflow
Lies [workflow.md](workflow.md). Lege mit dem Benutzer den Standard-Workflow fest und schreibe ihn als nummerierte Liste in `AGENTS.md`:
- Reihenfolge: Docs/Wiki lesen → planen (welche Stufe wann) → arbeiten → deterministische Prüfungen → Evaluator-Schleife (welche Evaluatoren) → Docs/Wiki aktualisieren → Release/Deploy über welches Skript.
- Testing-Anforderungen: Welche Tests müssen bei welcher Änderung existieren und grün sein? Wird aus manuellen Testdrehbüchern ein E2E-Test?
- Rückfragen-Politik: interaktiv oder vollautonom; für unbeaufsichtigte Läufe immer vollautonom.
- Git-Konventionen (Branch, Commit-Format, wann committen, Worktrees) – ein Satz je Konvention.
- Wann ein Dynamic Workflow oder mehrere Instanzen sinnvoll wären (optional).

## Schritt 10 – Abschluss
1. `AGENTS.md` aufräumen: alle Platzhalter-Kommentare durch Inhalt ersetzt oder entfernt; **den Absatz „Harness einrichten" löschen**; den Satz zum Harness-Skill an das Ergebnis von Schritt 2 anpassen (Rückfallebene nur, wenn ein Agent keine Skills kennt); Länge prüfen – Kernregeln kurz, Details verlinkt; jede Regel mit Begründung, keine Romane.
2. Die READMEs des Templates (`README.md`, `README.de.md`, `README.zh-CN.md`) durch die README des Projekts ersetzen oder löschen; `LICENSE` des Templates entfernen oder – wenn das Projekt veröffentlicht wird – die Attribution daraus in die eigene Lizenzdatei/README übernehmen (CC BY 4.0).
3. `python3 tools/sync-agents.py`, `python3 tools/agent-start.py doctor`, Kontext-Ansicht des Agenten prüfen (Regeldateien geladen? unerwartete Kosten?).
4. Diesen Skill nachziehen, falls die Einrichtung etwas Projektspezifisches am Harness ergeben hat (neue Skripte, eigene Evaluatoren): betroffenes Dokument + `index.md`.
5. **evaluator** aufrufen: Aufgabe „Harness-Einrichtung", Kriterien = Checkliste unten, Evidenz = `AGENTS.md`, angelegte Dateien, Ausgaben der Skripte. Bis `PASS`.
6. Bei Wiki: Entscheidungen samt Begründung über den librarian einlagern. Offene Punkte dem Benutzer als Liste nennen. Committen, wenn der Benutzer es wünscht.

## Checkliste (Kriterien für den evaluator)
- [ ] Sprache festgelegt (Harness-Dateien ggf. einmalig übersetzt); Template-READMEs ersetzt oder entfernt
- [ ] `AGENTS.md`: Projekt, Sprache, Fallstricke, Coding-Agenten (je ein Satz), Wissensablage-Regeln, Werkzeuge/Skripte, Architektur-Kernregeln, Qualitätssicherung (Evaluatoren + wann), Standard-Workflow – keine Platzhalter mehr, Einrichtungs-Absatz gelöscht
- [ ] `CLAUDE.md` = `@AGENTS.md`; Regel für Unterordner steht; Unterordner-Regeldateien (falls gewählt) haben beide Dateien
- [ ] Subagenten in allen benötigten Formaten (`sync-agents.py` gelaufen); nicht benötigte Subagenten entfernt
- [ ] Harness-Skill (und Guideline-Skill, falls angelegt) dort, wo jeder eingesetzte Agent ihn findet – oder Rückfallebene in `AGENTS.md`
- [ ] Wiki-Entscheidung umgesetzt (Skelett + librarian oder entfernt + `docs/`-Satz)
- [ ] MCP-Server nur mit Use Case, projektlokal konfiguriert, Regel „IMMER für X"; Secrets nicht im Repo
- [ ] Skripte nach den zehn Prinzipien, getestet, eingetragen
- [ ] `agent-start.py doctor` und `--dry-run` laufen; Permission-Modus/Allow-Liste eingerichtet, wenn autonome Läufe gewünscht
- [ ] Sicherheitsentscheidung (Sandbox/Worktree/rote Linien) notiert
- [ ] Offene Punkte aufgelistet
