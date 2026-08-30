---
name: harness
description: >-
  Dokumentation und Einrichtungsleitfaden des Harness dieses Projekts: Regeldateien
  (AGENTS.md/CLAUDE.md, Unterordner, rules), Subagenten evaluator und librarian, LLM-Wiki
  und Wissensablage, Skills, MCP-Server (wann MCP, wann Skript), Skripte für Agenten,
  autonome Läufe (rückfragefreie Modi, tmux/psmux, Usage, Selbstüberwachung), Workflow und
  Evaluator-Ketten, Kompatibilität der Coding-Agenten, freilauf. Laden, wenn der Benutzer
  etwas zu diesem Harness fragt, ihn einrichten, erweitern oder verbessern will, oder wenn
  ein Harness-Baustein (Skript, Subagent, Skill, MCP-Konfiguration, Regeldatei) angelegt
  oder geändert werden soll.
---

# Harness-Wissen

Dieser Skill ist die Dokumentation des Harness in diesem Projekt – aufgebaut wie ein kleines
LLM-Wiki: `index.md` ist der Katalog, die Dokumente liegen flach daneben. Die Inhalte sind
verdichtete Auszüge aus Erfahrung mit Coding-Agenten, geschrieben für dich als Leser.

## Vorgehen

1. Lies `index.md` in diesem Ordner und wähle die Dokumente, die dein Thema berühren.
2. **Halbwissen ist gefährlich.** Bei Einrichtung, Umbau oder Erweiterung des Harness liest du
   ALLE Dokumente, nicht nur `einrichtung.md`. Bei einer Einzelfrage die relevanten.
3. **Einrichtung:** `einrichtung.md` führt den Benutzer Schritt für Schritt durch die
   Entscheidungen; Ergebnisse landen als knappe Sätze in `AGENTS.md`. Am Ende wird der
   Einrichtungs-Absatz aus `AGENTS.md` gelöscht.
4. **Skripte** für diesen Harness werden IMMER nach den Prinzipien in `skripte.md` gebaut –
   ohne Nachfrage, sie gelten hier.
5. **MCP-Server** nur nach der Entscheidungsregel in `mcp-und-werkzeuge.md`.
6. Änderungen am Harness gehen wie jede andere Arbeit durch den evaluator, und das betroffene
   Dokument hier (plus `index.md`) wird nachgezogen – so bleibt die Dokumentation die Wahrheit.

## Dateien in diesem Ordner

| Datei | Inhalt |
|---|---|
| `index.md` | Katalog aller Dokumente mit Ein-Satz-Beschreibung |
| `einrichtung.md` | geführte Einrichtung des Harness mit dem Benutzer |
| `grundlagen.md` | was ein Harness ist, Checkliste eines guten Harness |
| `regeldateien.md` | AGENTS.md/CLAUDE.md, Unterordner-Regeldateien, rules, Schreibstil |
| `agenten-kompatibilitaet.md` | welcher Coding-Agent was unterstützt und wo Dateien liegen |
| `wissensablage.md` | LLM-Wiki mit librarian, was hinein gehört, Alternativen |
| `evaluatoren.md` | Evaluator-Pattern, mehrere/spezialisierte Evaluatoren, Vorlage |
| `skills-und-commands.md` | Skills, Slash Commands, Guideline-Skills |
| `mcp-und-werkzeuge.md` | wann MCP, wann Skript; Playwright, cua, weitere Server |
| `skripte.md` | die zehn Prinzipien für Skripte, die Agenten zuarbeiten |
| `autonome-laeufe.md` | Permission-Modi, Sandbox, tmux/psmux, Usage, Selbstüberwachung, `tools/agent-start.py` |
| `workflow.md` | Standard-Workflow, Planungsstufen, Testing, Evaluator-Ketten |
| `freilauf.md` | der Überbau zum Laufenlassen und Überwachen von Agenten |
