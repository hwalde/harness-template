# harness-template

[English](README.md) · [中文](README.zh-CN.md) · **Deutsch**

**Ein Projekt-Starter für die Arbeit mit Coding-Agenten.** Regeln, die immer gelten. Ein skeptischer Zweitgutachter, der jede Arbeit abnimmt. Ein Bibliothekar, der das Projektgedächtnis pflegt. Skripte, die dem Agenten zuarbeiten, und ein Start-Skript für Läufe, die nie nachfragen. Dazu die Dokumentation des Ganzen als Skill – und ein Einrichtungsleitfaden, den dein Agent selbst mit dir durchgeht.

> ### 🤖 Einrichten? Lass es deinen Agenten machen.
> Kopiere das Template in dein Projekt und starte deinen Coding-Agenten (Claude Code, Codex, Gemini CLI, Cursor, opencode …). Er liest `AGENTS.md`, schlägt dir die Einrichtung vor und führt dich durch die Entscheidungen, die nur du treffen kannst. Falls er es nicht von selbst tut:
> *„Lade den Skill `harness` und richte den Harness mit mir ein."*

## Was ein Harness ist

Alles außer dem Sprachmodell: die Umgebung, in der der Agent läuft. Regeldateien, Subagenten, Skills, MCP-Server, Skripte, ein Wissensspeicher, Start- und Überwachungsmechanik. Ein guter Harness befähigt den Agenten, sich Informationen selbst zu holen und seine Arbeit selbst zu prüfen – und er lässt einen Lauf nicht an einer Frage hängen, die niemand beantwortet. Dieses Template ist der Grundstock dafür, der in jedes Projekt passt.

## Was drin ist

```
AGENTS.md                  Alle Regeln für Coding-Agenten – das ganze Wissen steht hier
CLAUDE.md                  Enthält nur „@AGENTS.md"
.claude/agents/            evaluator (Abnahme) und librarian (Wiki) – Quelle der Wahrheit
.claude/skills/harness/    Harness-Dokumentation als LLM-Wiki + einrichtung.md
.opencode/agent/           Generierte Subagenten-Varianten für opencode
.my-memory/                Leeres LLM-Wiki – nur über den librarian
tools/agent-start.py       Rückfragefreie Läufe starten, anhängen, beenden (tmux/psmux)
tools/sync-agents.py       Subagenten-Definitionen in andere Formate übersetzen
```

**evaluator** – prüft mit frischem Kontext und ohne Schreibrechte gegen Spezifikation, Diff und Evidenz; antwortet `PASS` oder `NEEDS_WORK`. Optional mit Schwerpunkt (Sicherheit, Performance, Clean Code, Guidelines, Architektur).
**librarian** – einziger Zugang zum Projektgedächtnis; filtert, was bleibt (Entscheidungen samt Begründung, Fallstricke, Betriebswissen) und weist Grundrauschen ab.
**Harness-Skill** – zwölf kurze Dokumente: die geführte Einrichtung, was ein Harness braucht, Regeldateien, Wissensablage und ihre Alternativen, Evaluatoren, Skills, wann MCP und wann Skript, die zehn Prinzipien für agentenfreundliche Skripte, autonome Läufe, Workflow, Kompatibilität der Agenten, freilauf.

## Schnellstart

1. **Template holen:** „Use this template" auf GitHub, oder klonen, oder die Dateien in ein bestehendes Projekt kopieren.
2. **Agenten starten** im Projektordner.
3. **Einrichten lassen.** Die Einrichtung klärt der Reihe nach: Sprache · Projekt · welche Coding-Agenten arbeiten hier und was unterstützen sie (der Agent untersucht das aktuell) · Wissensablage (LLM-Wiki oder Alternativen) · MCP-Server und Zugänge (Playwright für Web-Apps, Computer Use für Desktop-Apps) · Skripte · autonome Läufe, Überwachung, Sicherheit · Architektur und Coding-Guidelines · Evaluatoren · Workflow. Am Ende steht alles in `AGENTS.md`, und der Einrichtungs-Absatz verschwindet.

Ohne Agenten geht es auch: `.claude/skills/harness/index.md` ist für Menschen genauso lesbar.

## Unterstützte Coding-Agenten

Claude Code läuft out of the box. Für opencode werden die Subagenten generiert. Alle anderen (Codex, Gemini CLI, Cursor, Copilot, hermes …) werden bei der Einrichtung angebunden: Der Agent untersucht, was der jeweilige Agent gerade unterstützt – Regeldateien und Includes, Unterordner-Regeln, rules, Subagenten, Skills, Slash Commands, projektlokale MCP-Konfiguration, Hooks, rückfragefreier Modus – und legt die Dateien dort ab, wo er sie findet. Diese Untersuchung passiert bewusst zur Einrichtungszeit, nicht im Template: So ist sie aktuell.

## Sprachen

Nur was Menschen lesen, ist dreisprachig: diese READMEs (EN/ZH/DE). Die Harness-Dateien selbst (`AGENTS.md`, Subagenten, Skill) liegen in einer Fassung auf Deutsch – Coding-Agenten lesen sie unabhängig von deiner Sprache, und eine einzige Fassung bedeutet keinen Übersetzungs-Sync. Wer sie lieber in der eigenen Sprache hätte: Schritt 0 der Einrichtung lässt den Agenten sie einmalig übersetzen. Die Skripte in `tools/` sprechen Englisch (Quellcode-Sprache).

## freilauf: der Überbau

Dieses Template ist der Starter *im* Projekt. [freilauf](https://github.com/hwalde/freilauf) ist das Gegenstück *über* den Projekten: eine selbst gehostete Weboberfläche, die ein stehendes Team von Coding-Agenten nach Zeitplan laufen lässt – eigene Worktrees und tmux-Sessions je Lauf, Budget-Gates, Überwachung von außen, ein Finish Gate, Merge nach `main`, Benachrichtigungen. Ein mit diesem Template eingerichtetes Projekt läuft dort ohne weitere Anpassung.

## Mitmachen

Pull Requests sind willkommen – Verbesserungen an Dokumenten und Subagenten, weitere Zielformate für `sync-agents.py`, Übersetzungen. Spielregeln:

- Die drei READMEs werden **gemeinsam** gepflegt.
- Jeder Ordner mit einer `AGENTS.md` hat eine `CLAUDE.md` daneben, die nur `@AGENTS.md` enthält.
- Skripte folgen `.claude/skills/harness/skripte.md`; Quellcode-Sprache ist Englisch.
- Nichts Maschinenspezifisches und keine Secrets im Repository.

## Lizenz

[CC BY 4.0](LICENSE) – nutzen, ändern, kommerziell einsetzen; Autor nennen (**Herbert Walde**), auf <https://github.com/hwalde/harness-template> verlinken, Lizenz verlinken, Änderungen kenntlich machen.
