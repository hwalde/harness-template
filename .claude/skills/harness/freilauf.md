# freilauf: Agenten laufen und überwachen lassen
**Kern:** Dieses Template ist der Projekt-Starter (was im Repo liegt). freilauf ist der Überbau darüber: eine selbst gehostete Weboberfläche, die ein stehendes Team von Coding-Agenten nach Zeitplan laufen lässt und von außen überwacht. (Kontext: Harness-Template | Stand: 2026-08-30 | Quelle: https://github.com/hwalde/freilauf)

## Was freilauf tut
- **Läufe ohne Aufsicht:** Jeder Lauf bekommt einen eigenen Git-Worktree und eine eigene tmux-Session; Läufe stören sich nicht, man kann sich jederzeit anhängen und den ganzen Bildschirm lesen.
- **Zeitpläne:** „Jede Nacht um 2 die offenen Issues ansehen." Ein *Agent* ist eine gespeicherte Lauf-Definition (Coding-Agent, Modell, Reasoning-Aufwand, Prompt, Repo, Branch-Regel) plus Name und Zeitplan; ein *Einzellauf* dasselbe ohne Zeitplan.
- **Beobachtung von außen:** tmux-Zustand, Logs, Transkripte, Hooks, Provider-Puls – Rate-Limits und Ausfälle werden erkannt, auch wenn der Agent selbst nichts mehr melden kann.
- **Fertig heißt auf `main`:** Optional merged der Hub selbst, prüft die Behauptung des Agenten vor dem Glauben (Finish Gate) und schickt den noch lebenden Agenten zurück, um Fehlendes nachzuholen.
- **Budget-Gates:** Geplante Starts warten, wenn Abo-Kontingent oder Guthaben knapp sind.
- **Reports** des Agenten (`cc-report done|failed|help|progress|branch|pr`), **Telegram-Benachrichtigungen**, **No-Code-Flows** (was nach einem Lauf passiert: Folgeläufe, Nachrichten an laufende Agenten, Extraktion aus Reports, Verzweigungen).
- **Coding-Agenten und Modell-Provider als Plugins:** Claude Code, opencode, hermes, cursor-agent u. a.; weitere per Plugin-Paket. Oberfläche in Englisch, Deutsch und Chinesisch.
- Enthält die Start-/Anhänge-Skripte (`cc-start`, `cc-attach`, `cc-kill`, `cc-report`), von denen `tools/agent-start.py` in diesem Template die projektlokale Kleinfassung ist.

## Wann es sich lohnt
- Sobald Läufe regelmäßig **unbeaufsichtigt** oder **nach Zeitplan** laufen sollen (Nachtläufe, wiederkehrende Wartung, Issue-Abarbeitung).
- Sobald mehrere Agenten oder mehrere Repos parallel laufen und man wissen will, wann etwas schiefging – ohne selbst dauernd hinzuschauen.
- Sobald das Ergebnis eines Laufs verlässlich auf dem Hauptbranch landen soll, mit Prüfung vor dem Merge.

## Zusammenspiel mit diesem Template
| Ebene | Zuständig |
|---|---|
| Im Repo: Regeln (`AGENTS.md`), Subagenten (evaluator, librarian), Skills, Skripte, Wiki | dieses Template |
| Über dem Repo: Starten nach Zeitplan, Worktrees, Überwachung, Budget, Merge, Benachrichtigung | freilauf |

Ein Projekt, das mit diesem Template eingerichtet ist, läuft in freilauf ohne weitere Anpassung: Die Regeln und Subagenten greifen in jedem Lauf, der Evaluator-Pass ist der natürliche Partner des Finish Gates. Sicherheitsmodell von freilauf beachten (VPN als Zugangsschicht; der Hub steuert tmux, das ist Shell-Zugriff).

Einrichtung: `README` und `SETUP_WITH_AGENT.md` im freilauf-Repository – letzteres ist für Coding-Agenten geschrieben („Lies SETUP_WITH_AGENT.md und richte mir das ein").
