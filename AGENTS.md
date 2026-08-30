# AGENTS.md – Regeln für Coding-Agenten in diesem Projekt

Dieses Projekt wurde aus dem Harness-Template erstellt (https://github.com/hwalde/harness-template). Alles Projektwissen für Agenten steht hier; `CLAUDE.md` enthält nur `@AGENTS.md`.

## Harness einrichten (diesen Absatz nach der Einrichtung löschen)

Schlage dem Benutzer vor, diesen Harness gemeinsam mit ihm einzurichten. Lade dafür den Skill `harness` (ist er nicht ladbar, lies `.claude/skills/harness/SKILL.md`), lies ALLE dort katalogisierten Dokumente und folge dann `einrichtung.md`. Sobald die Einrichtung abgeschlossen ist, lösche diesen Absatz aus der AGENTS.md, damit dem Benutzer die Einrichtung nicht erneut vorgeschlagen wird.

## Harness-Wissen

Wenn dich der Benutzer etwas zu diesem Harness hier fragt oder den Harness verbessern oder einrichten möchte, lade den Skill `harness`; ist der Skill nicht ladbar, lies stattdessen `.claude/skills/harness/SKILL.md` und die dort verlinkte `index.md`. Halbwissen ist gefährlich: Lies die Dokumente, die dein Thema berühren, vollständig.

## Regeldateien

In jedem Ordner, in dem eine `AGENTS.md` angelegt wird, muss daneben eine `CLAUDE.md` angelegt werden, die genau eine Zeile enthält: `@AGENTS.md`. In eine `CLAUDE.md` wird nie eigener Inhalt geschrieben. Wenn du diese Datei oder einen Skill bearbeitest, schreibst du für dich selbst: kompakt, Fachbegriffe, jede Regel mit Begründung, nichts Offensichtliches.

## Projekt

<!-- Bei der Einrichtung ausfüllen: ein Satz, worum es geht; grober Aufbau (bewusst unvollständig); Sprache für Antworten, Dokumentation und Kommentare. -->

## Coding-Agenten in diesem Projekt

<!-- Bei der Einrichtung ausfüllen: je eingesetztem Agenten ein Satz – welche Features er unterstützt (Subagenten, Skills, Slash Commands, Regeldateien in Unterordnern, rules, projektlokale MCP-Konfiguration) und wo die Dateien dafür liegen. Quelle der Wahrheit für Subagenten ist `.claude/agents/`; andere Formate werden mit `python3 tools/sync-agents.py` erzeugt. -->

## Projektgedächtnis (`.my-memory/`) – librarian

Dieses Projekt hat ein persistentes Wiki-Gedächtnis in `.my-memory/` (LLM-Wiki-Muster: `wiki/` = dichte Wissensseiten mit Index je Ordner, `raw/` = unveränderliche Originale). Es wird ausschließlich vom Subagenten **librarian** bedient. Grund: Er filtert, findet und lagert ein, damit dein Kontext schlank bleibt und Wissen die Session überlebt.

1. **Arbeitsbeginn:** Braucht die Aufgabe Vorwissen (Projektfakten, frühere Entscheidungen, Zusammenhänge), konsultiere ZUERST den librarian (Modus ABFRAGE) und nenne ihm deine Intention – er liefert das Destillat und die dafür nützlichen Themen. Erst wenn er `NICHT IM WIKI` meldet, frage den Benutzer. Braucht die Aufgabe kein Vorwissen, entfällt die Konsultation. Bei jeder Planung ist die Konsultation Pflicht.
2. **Arbeitsende / Ende eines Abschnitts:** Lagere über den librarian (Modus EINLAGERUNG) nur ein, was dauerhaften, sitzungsübergreifenden Wert hat: Entscheidungen samt Begründung, stabile Erkenntnisse und Muster, hart erkämpfte Fallstricke, Betriebs-/Zugangs-/Domänenwissen, geänderte Projektfakten. NICHT einlagern: eine gerade beantwortete Nachfrage, Fortschritts-/Statusnotizen, per `grep` aus dem Code wiederbeschaffbares Detail, Log-Ausgaben, Stacktraces, Triviales. Leitfrage: „Braucht eine zukünftige Session das?" Im Zweifel nicht. Gib den Kontext mit (welches Projekt/Teilsystem/Thema); meldet er `KONTEXT UNKLAR`, kläre die Zugehörigkeit (notfalls beim Benutzer) und beauftrage erneut.
3. **Niemals direkt in `.my-memory/` lesen oder schreiben** – auch nicht aus Subagenten. Jeder Zugriff läuft über den librarian. Keine Ausnahmen.
4. **Effizienz:** Liegt einzulagerndes Wissen als Datei vor, nenne dem librarian den Pfad statt den Inhalt zu kopieren; bei Quelldokumenten legt er das Original in `raw/` ab.
5. **Kuratierung:** Das Wiki wird periodisch und bewusst angestoßen aufgeräumt (Modus WARTUNG) – nie nebenbei, Löschungen nur mit Freigabe des Benutzers.

## Qualitätssicherung – evaluator

Dieses Projekt arbeitet nach dem Generator→Evaluator-Muster. Der Subagent **evaluator** ist ein skeptischer Zweitgutachter ohne Schreibrechte: Er liest Spezifikation, Diff und Evidenz in eigenem, frischem Kontext und antwortet mit `PASS` oder `NEEDS_WORK` samt konkreten Findings. Grund: Der Builder benotet nie seine eigene Arbeit – ein zweiter Blick findet andere Fehler.

1. **Nach jeder abgeschlossenen Aufgabe oder Teilaufgabe** IMMER den evaluator ausführen, BEVOR das Ergebnis als fertig gemeldet oder akzeptiert wird. „Sieht gut aus" oder „sollte funktionieren" ersetzt keine Prüfung.
2. **Erzeuge vorher echte, beobachtbare Evidenz** (Test-Logs, Build-Output, Screenshots) und gib dem evaluator Kontext: Aufgabe bzw. Akzeptanzkriterien, geänderte Dateien, Pfade zur Evidenz. Er vertraut keinen Behauptungen.
3. **Meldet er `NEEDS_WORK`, ist dem Folge zu leisten:** alle Findings abarbeiten – keine Diskussion, kein Wegerklären, keine abgeschwächten Tests oder gelockerten Akzeptanzkriterien.
4. **Nach jeder Nachbesserung erneut prüfen lassen.** Die Schleife läuft, bis er `PASS` meldet. Erst dann gilt die Aufgabe als abgeschlossen.
5. **Schwerpunkte:** Der evaluator kann mit Fokus aufgerufen werden (Sicherheit, Performance, Clean Code, Coding-Guidelines, Architektur). <!-- Bei der Einrichtung festlegen, welche Schwerpunkte bei welchem Änderungsumfang laufen und ob eigene Schwerpunkt-Evaluatoren angelegt werden. -->

## Kontextfenster-Disziplin

Gehe sparsam mit deinem Kontextfenster um. Große Lese-, Such- und Rechercheaufgaben delegierst du an Subagenten, deren Ergebnis als knappes Destillat zurückkommt (z. B. je Datei Pfad + ein Satz + max. drei Sätze Begründung), statt Dateien auf Verdacht vollständig zu lesen. Formuliere Aufträge an Subagenten als Brief an eine gleich fähige Instanz – mit Kontext und Ziel, nicht als Befehlsliste. Bei langen Läufen bist du Orchestrator: du planst, delegierst, prüfst; Subagenten setzen um.

## Standard-Workflow

<!-- Bei der Einrichtung festlegen und auf das Projekt zuschneiden. Vorschlag: -->
1. Vorwissen holen (librarian; verlinkte Dokumente, die das Thema berühren, lesen).
2. Bei nicht-trivialen Aufgaben kurz planen; Akzeptanzkriterien abhakbar aufschreiben.
3. Umsetzen; deterministische Prüfungen per Skript (Linter, Tests, Build).
4. Evaluator-Schleife bis `PASS`.
5. Dokumentation und Wiki nachziehen (nur Bleibendes); `AGENTS.md` ergänzen, wenn ein Satz zum wiederholten Mal nötig war.

## Werkzeuge und Skripte

- `python3 tools/agent-start.py` – Coding-Agenten für rückfragefreie Läufe starten, auflisten, anhängen, beenden (tmux/psmux optional). Ohne Argumente: Hilfe.
- `python3 tools/sync-agents.py` – nach jeder Änderung in `.claude/agents/` ausführen; erzeugt die Subagent-Definitionen für andere Agenten (z. B. `.opencode/agent/`).
- Neue Skripte für diesen Harness werden nach den Prinzipien in `.claude/skills/harness/skripte.md` gebaut und hier mit je einem Satz eingetragen.
<!-- Bei der Einrichtung: MCP-Server (z. B. Playwright für Web-Apps, cua-computer-use für Desktop-Apps) und die Regel, wann sie IMMER zu verwenden sind; weitere projektspezifische Skripte. -->

## Architektur und Coding-Guidelines

<!-- Bei der Einrichtung ausfüllen: die wichtigsten Regeln in ca. 20 Zeilen (Pareto). Der vollständige Katalog gehört in einen Skill (z. B. `.claude/skills/coding-guidelines/`), der hier mit einem Satz genannt wird. -->

## Fallstricke

<!-- Nur, was wehtut, wenn es fehlt: „Nach Änderung an X muss Y, sonst Z." Jeder Eintrag ein Satz. -->
