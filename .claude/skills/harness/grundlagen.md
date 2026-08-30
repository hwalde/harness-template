# Grundlagen: Was ein Harness ist und was ein guter braucht
**Kern:** Alles außer dem LLM ist der Harness – die Umgebung, in der der Agent läuft: Regeln, Wissen, Werkzeuge, Skripte, Prüfer, Autonomie-Bausteine. Ziel ist immer dieselbe Frage: Wie kann der Agent das selbst und autonom machen? (Kontext: Harness-Template | Stand: 2026-08-30)

## Begriff
- Der Coding-Agent selbst ist schon ein Harness (Systemprompt, Werkzeuge, Permission-Modi). Der projektspezifische Harness ist alles, was man darum herum baut, damit Läufe ohne Zutun gut ausgehen: Regeldateien, Subagenten, Skills, MCP-Server, Skripte, Wissensspeicher, Start- und Überwachungsmechanik.
- Harness Engineering ist die dritte Phase der Arbeit mit Coding-Agenten: Nach „Prompting" und „Prozesse pro Aufgabe planen" kommt die Umgebung, die den Agenten befähigt und prüft – und die Gegenbewegung, ihm das Vorgehen weitgehend zu überlassen: schwieriges Ziel + Prüfkriterium, laufen lassen.
- Ein Harness wird nie fertig. Er wächst nebenbei: Jeder Satz, den man zum wiederholten Mal tippt, wandert in die Regeldatei; jede Handarbeit, die algorithmisch ist, wird ein Skript; jede wiederkehrende Prüfung ein Evaluator.

## Alle Bausteine dienen demselben Ziel
Regeldateien, Subagenten, Skills, MCP-Server und Skripte steuern, **welche Informationen und Fähigkeiten wann im Kontextfenster liegen** – das Modell weder über- noch unterfordern. Zwei Erweiterungswege: natürliche Sprache (Regeldateien, Skills, Subagenten) und Algorithmen (Skripte, MCP). Alles, was dauerhaft im Kontext liegt (Beschreibungen von Subagenten, Skills, MCP-Tools, Regeldateien), kostet bei jedem Request – „was will ich dem Modell wirklich die ganze Zeit ins Gesicht halten?"

## Checkliste: Was ein guter Harness braucht (Auswahl, nicht Pflichtliste)
| Baustein | Zweck | Im Template |
|---|---|---|
| Verschriftlichte Anforderungen und Regeln | Kernregeln (Architektur, Workflow, Fallstricke) in `AGENTS.md`, Rest verlinkt | `AGENTS.md`, [regeldateien.md](regeldateien.md) |
| Evaluator | ein Agent prüft einen Agenten; qualitativ und funktional | `evaluator`, [evaluatoren.md](evaluatoren.md) |
| Wissensmanagement | der kritischste Punkt: Anforderungen, Pläne, „wie geht was", Zugänge | librarian + `.my-memory/`, [wissensablage.md](wissensablage.md) |
| Befähigung | der Agent kommt selbst an Informationen, testet und debuggt selbst: Browser-/Desktop-Steuerung, Zugänge, Skripte, Tests | [mcp-und-werkzeuge.md](mcp-und-werkzeuge.md), [skripte.md](skripte.md) |
| Skripte | deterministische Zuarbeit; Ausgabe als Prompt | `tools/`, [skripte.md](skripte.md) |
| Nicht vor erledigter Arbeit aufhören | Goal-Befehl oder Loop | [autonome-laeufe.md](autonome-laeufe.md) |
| Rückfragefreier Modus + Multiplexer | der Lauf hält nie an und überlebt das Ausloggen | `tools/agent-start.py` |
| Usage-Tracking | vor dem Kontingent-Limit anhalten (nur bei Abo-Limits) | [autonome-laeufe.md](autonome-laeufe.md) |
| Selbstüberwachung | hängende Skripte und verlaufene Agenten erkennen (Cron/Loop) | [autonome-laeufe.md](autonome-laeufe.md) |
| Selbstverbesserung (optional) | der Agent schreibt Skills/Doku fort – mit Grenzen | [skills-und-commands.md](skills-und-commands.md) |
| Sicherheit | Sandbox statt Verbotsliste | [autonome-laeufe.md](autonome-laeufe.md) |
| Workflow | Docs lesen → planen → arbeiten → prüfen → Docs/Wiki aktualisieren | [workflow.md](workflow.md) |
| Überbau | Zeitpläne, Worktrees, Überwachung von außen, Merge | [freilauf.md](freilauf.md) |

Auf die Selbstüberwachung lässt sich am schlechtesten verzichten: Ein Agent, der fünf Minuten nach dem Alleinlassen eine Frage hatte, hat zwei Tage verschenkt. Der Evaluator ist mit dem geringsten Aufwand eingebaut und bringt am meisten.

## Befähigung: die eigene rote Linie
Alles, was der Agent nicht selbst kann, braucht den Menschen. Deshalb: Browser-Steuerung für Web-Apps, Desktop-Steuerung für Desktop-Apps, Zugänge (z. B. ein nur lesendes Postfach, um Bestätigungsmails zu prüfen), Skripte, Tests als Selbstvalidierung. Und bewusst eine rote Linie ziehen – etwa: keine E-Mails ohne menschliche Freigabe, kein Zugriff auf Produktivsysteme ohne Freigabe.

## Ordnung als Architekturvorgabe
Ein klarer, fachlich geschnittener Ordnerbaum, eindeutige Begriffe (ein Wort pro Konzept) und feste Orte für Skripte, Dokumente und Konfiguration sind Harness-Bausteine: Wie Menschen braucht die KI Struktur, um Informationen schnell zu finden und nichts zu übersehen – und Unterordner-Regeldateien funktionieren nur mit einem fachlichen Schnitt.

## Spec-driven als Ergänzung
Der hier beschriebene Weg (Ziel + Kriterien + Harness) schließt Spezifikationsdokumente nicht aus: Bei größeren Vorhaben liefert ein Anforderungsdokument mit Umsetzungspaketen und Testing-Anforderungen die Prüfkriterien; bei schwachem Harness bekommt der Agent dort die Zugänge und Hinweise wenigstens für die anstehende Aufgabe ([workflow.md](workflow.md)).
