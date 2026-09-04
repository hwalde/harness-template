# harness – ein Skill, der den Harness für Coding-Agenten baut

[English](README.md) · [中文](README.zh-CN.md) · **Deutsch**

**Lässt Coding-Agenten autonom – und sicher – an Unternehmens-IT-Projekten arbeiten.** Dieser Skill baut einen vollständigen Harness in jedes Projekt: Regeln, die immer gelten, ein skeptischer Zweitgutachter, der jede Arbeit abnimmt, ein Bibliothekar, der das Projektgedächtnis pflegt, Skripte, die die Handarbeit übernehmen, und ein Start-Skript für Läufe, die nie nachfragen. Der Coding-Agent installiert ihn, baut ihn, führt durch die Einrichtung und hält ihn aktuell.

> ### 🤖 Eine Zeile zum Start
> ```bash
> git clone https://github.com/hwalde/harness-skill ~/.claude/skills/harness
> ```
> Anschließend im Projekt dem Coding-Agenten sagen: *„Lade den Skill `harness` und baue den Harness für dieses Projekt mit mir auf."* (Andere Agenten: in ihren Skill-Ordner klonen – der Skill sagt dem Agenten, wohin.)

## Warum ein Harness

Ein Harness ist alles außer dem Sprachmodell: die Umgebung, in der der Agent läuft. Regeldateien, Subagenten, Skills, MCP-Server, Skripte, ein Wissensspeicher, Start- und Überwachungsmechanik. Ohne Harness arbeitet ein Agent aus leerem Kontext, bewertet die eigene Arbeit selbst, vergisst, was die letzte Sitzung gelernt hat, und bleibt an der ersten Frage hängen, die niemand beantwortet. Mit diesem hier:

- **Jedes Ergebnis wird von einem zweiten Augenpaar geprüft.** Der Subagent `evaluator` liest Spezifikation, Diff und Evidenz in frischem Kontext, ohne Schreibzugriff, und antwortet mit `PASS` oder `NEEDS_WORK`. Der Ersteller nimmt die eigene Arbeit nie selbst ab.
- **Wissen überlebt die Sitzung.** Der `librarian` ist die einzige Tür zu einem LLM-Wiki im Repository: Entscheidungen samt Begründung, Fallstricke, Betriebswissen – gefiltert, damit der Kontext schlank bleibt.
- **Läufe bleiben nie stecken.** Berechtigungsmodi für rückfragefreie Läufe, ein Start-Skript für tmux-/psmux-Sitzungen, Nutzungs-Tracking, Selbstüberwachung und die Regel „erst die Fragerunde, dann das Ziel".
- **Rote Linien stehen schriftlich fest.** Was der Agent lesen, ausführen und ohne Freigabe nie anfassen darf, steht in `AGENTS.md`, die Entscheidung dahinter in `HARNESS.md` – so bleibt ein unbeaufsichtigter Lauf in einem Unternehmensprojekt innerhalb des festgelegten Korridors.
- **Er passt zu jedem Coding-Agenten.** Claude Code läuft out of the box; opencode wird generiert; Codex, Gemini CLI, Cursor, Copilot, hermes werden bei der Einrichtung angebunden, wenn der Agent untersucht, was jeder von ihnen aktuell unterstützt.

## Was der Skill in ein Projekt einbaut

```
AGENTS.md                Alle Regeln für Coding-Agenten – Projektfakten, Wiki-Regeln, QA, Workflow
CLAUDE.md                Enthält nur „@AGENTS.md"
HARNESS.md               Der Zustand dieses Harness: Skill-Version, eingesetzte Agenten, Entscheidungen, offene Punkte
.claude/agents/          evaluator (Abnahme) und librarian (Wiki) – Quelle der Wahrheit
.claude/settings.json    Minimale Allow-Liste für rückfragefreie Läufe, ein SessionStart-Hook fürs Bootstrap
.my-memory/              Leeres LLM-Wiki – nur über den librarian zugänglich
tools/agent-start.py     Rückfragefreie Läufe starten, anhängen, beenden (tmux/psmux)
tools/bootstrap.py       Lokale Einrichtung wiederherstellen, die einen Klon nicht übersteht
tools/sync-agents.py     Subagenten-Definitionen in Formate anderer Agenten übersetzen
```

Anschließend klärt die geführte Einrichtung der Reihe nach: Repository · Sprache · Projekt und Aufbau · welche Coding-Agenten hier arbeiten und was sie unterstützen · Wissensablage · MCP-Server und Zugänge (Playwright für Web-Apps, Computer Use für Desktop-Apps) · Skripte · autonome Läufe, Überwachung, Sicherheit · Architektur und Coding-Guidelines · Evaluatoren · Workflow. Alles landet in `AGENTS.md`, die Begründungen in `HARNESS.md`.

## Was im Skill steckt

```
SKILL.md                 Der Ablauf: bauen, fragen, Baustein, Review, Update, freilauf, verbessern
references/               Zwölf Dokumente – was ein Harness braucht, Regeldateien, Wissensablage,
                          Evaluatoren, Skills, MCP vs. Skript, die zehn Prinzipien für agentenfreundliche
                          Skripte, autonome Läufe, Workflow, Agentenkompatibilität, freilauf, die Einrichtung
assets/project/           Alles, was ein Projekt bekommt, am Zielpfad
scripts/build.py          Baut (oder prüft) ein Projekt gegen die Vorlagen – idempotent, überschreibt nie
CHANGELOG.md              Was sich pro Version geändert hat, und was ein gebautes Projekt von Hand braucht
```

Da der Skill ein Git-Klon bleibt, aktualisiert `git pull` ihn, und Route E des Skills trägt die Änderungen Datei für Datei in die Projekte – festgehaltene Abweichungen bleiben erhalten. Die Dokumente lassen sich genauso gut von Menschen lesen: Einstieg ist `references/index.md`.

## freilauf: der Überbau

Der Harness ist der Starter *im* Projekt. [freilauf](https://github.com/hwalde/freilauf) ist das Gegenstück *über* den Projekten: eine selbst gehostete Weboberfläche, die ein stehendes Team von Coding-Agenten nach Zeitplan laufen lässt – eigener Git-Worktree und eigene tmux-Sitzung je Lauf, Budget-Gates, Beobachtung von außen, ein Finish Gate, das die Behauptung des Agenten prüft, bevor es sie glaubt, Einbindung in `main`, Benachrichtigungen, No-Code-Flows für das, was nach einem Lauf passiert. Ein Projekt mit diesem Harness läuft dort ohne weitere Anpassung. Der Skill installiert und verbindet freilauf auf Wunsch (aktuell nur Linux).

## Über den Autor

Ich bin Herbert Walde. Ich entwickle seit 1999 Software und habe mehr als 200 Entwicklern beigebracht, ihre Produktivität mit KI drastisch zu steigern – dieser Skill ist die destillierte Form dessen, was in der Praxis funktioniert. Ich biete Schulungen für Unternehmen weltweit an, auf Deutsch und Englisch: <https://entwickler-training.de>.

## Mitmachen

Pull Requests sind willkommen – Verbesserungen an den Dokumenten und Subagenten, weitere Zielformate für `sync-agents.py`, Übersetzungen. Spielregeln (die Begründungen stehen in Route G von `SKILL.md`):

- Die drei READMEs werden **gemeinsam** gepflegt.
- Alles andere ist Englisch. Vorlagen liegen in `assets/project/` an ihrem Zielpfad; `CLAUDE.md` wird generiert, nicht gespeichert.
- Jede Änderung bekommt einen Eintrag in `CHANGELOG.md` und eine Versionserhöhung in `SKILL.md`.
- Skripte folgen `references/scripts.md`. Nichts Maschinenspezifisches und keine Secrets im Repository.

## Lizenz

[CC BY 4.0](LICENSE) – nutzen, ändern, kommerziell einsetzen; den Autor nennen (**Herbert Walde**), auf <https://github.com/hwalde/harness-skill> verlinken, die Lizenz verlinken und Änderungen kenntlich machen.
