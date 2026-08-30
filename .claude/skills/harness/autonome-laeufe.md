# Autonome Läufe: ohne Rückfragen, ohne Anhalten, ohne Aufsicht
**Kern:** Ein autonomer Lauf scheitert an jeder Nachfrage, die niemand beantwortet, an jeder Session, die beim Ausloggen stirbt, und an jedem Limit, das ihn still abwürgt. Der Harness beseitigt alle drei. (Kontext: Harness-Template | Stand: 2026-08-30)

## Bausteine im Überblick
| Baustein | Wozu | Wo im Template |
|---|---|---|
| Rückfragefreier Permission-Modus | der Agent hält nie an, um zu fragen | `tools/agent-start.py` kennt den Modus je Agent |
| Terminal-Multiplexer (tmux / psmux unter Windows) | Lauf überlebt das Ausloggen; man kann sich anhängen und zuschauen | `tools/agent-start.py start/attach/send` |
| Zielhierarchie + abhakbare Abnahme-Checkliste im Prompt | der Agent weiß, was Vorrang hat und wann er fertig ist | [workflow.md](workflow.md), unten |
| Etwas, das ihn nicht vor erledigter Arbeit aufhören lässt | `/goal`-Befehl (Claude Code) bzw. ein Loop | unten |
| Usage-Tracking | vor dem Kontingent-Limit anhalten statt sterben | Usage-Skript, siehe unten |
| Selbstüberwachung | hängende Skripte und verlaufene Agenten erkennen | Cron/Loop des Agenten + Prüfskript |
| Evaluator | die Abnahme prüft ein Zweiter | [evaluatoren.md](evaluatoren.md) |
| Sandbox | Sicherheit über die Grenze der Umgebung, nicht über Verbotslisten | unten |
| Überbau für Zeitpläne und Überwachung von außen | wenn Läufe regelmäßig unbeaufsichtigt laufen | [freilauf.md](freilauf.md) |

## Permission-Modi (am Beispiel Claude Code; Gegenstücke anderer Agenten in [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md))
| Modus | Verhalten |
|---|---|
| manuell | fragt bei jeder Kleinigkeit, darf nicht einmal in Dateien schreiben |
| acceptEdits | schreibt Dateien im Projektordner ohne Nachfrage; fragt bei Befehlen, außer sie sind freigegeben (dauerhaft erlaubte Befehle merkt er sich) |
| plan | nur planen, fokussiert auf einen technischen Plan |
| auto | führt aus, wo er sicher ist, dass der Befehl sicher ist; bei Unsicherheit (z. B. Löschbefehl mit Variablen) fragt er |
| bypassPermissions | fragt bei Shell-Befehlen nicht; bei wenigen Dingen (eigene Konfigurationsdateien) trotzdem. In Unternehmen unbeliebt – `auto` tut es meist genauso |
| **dontAsk** | **der Schlüssel zur Autonomie:** fragt nie; nicht Erlaubtes wird still verweigert und dem Modell mitgeteilt, das sich einen anderen Weg sucht. Sperrt alle interaktiven Nachfragewerkzeuge (auch `AskUserQuestion`). Subagenten laufen ohnehin so. Braucht eine Allow-Liste der erlaubten Befehle in den Settings, sonst verweigert er zu viel. |

Alternative: `acceptEdits` plus vorab freigegebene Befehle. Bei jedem anderen Agenten das Gegenstück suchen – ohne einen Modus, in dem er nicht mehr fragen *kann*, läuft er nicht wirklich autonom.

## Sicherheit: Sandbox statt Rechteentzug
Wer einen Agenten tagelang laufen lässt, will weder, dass er hängen bleibt, noch, dass er seine eigenen Skills nicht bearbeiten darf. Das spricht gegen „möglichst wenig erlauben". Das richtige Konzept: **alles erlauben, dafür in eine Sandbox** (z. B. eine Micro-VM wie die Docker-Sandbox für Coding-Agenten, oder ein Container/Worktree mit begrenztem Netz). Innerhalb der Grenze darf der Agent alles; die Sicherheit kommt aus der Grenze der Umgebung, nicht aus der Länge der Verbotsliste. Ohne Sandbox spielt man mit dem Feuer – dann wenigstens Worktree, Git als Sicherheitsnetz und keine Produktivzugänge.

## Der Startablauf (bewährte Reihenfolge)
1. **Prompt schreiben** – kurz, von Hand, präzise. Inhaltlicher Kern ist eine **Zielhierarchie**: Ziel 1, Ziel 2, plus ein ausdrücklicher Satz zur Reihenfolge („wenn Ziel 1 erreicht ist, fahre mit Ziel 2 fort"). Ziele so formulieren, dass er sie rigoros verfolgt, aber erreichbar sind.
2. **Streichen**, was der Agent ohnehin tut oder was für diesen Lauf keine Rolle spielt („Dokumente aktuell halten", „Learnings notieren" – das steht im Harness). Übrig bleibt der Kern: Ziele, Rahmenbedingungen (Usage, Kosten), Befähigungen.
3. **Fähigkeit vorgeben, nicht den Einsatzplan:** „Nutze Subagenten" bleibt; „starte pro Fehler einen" wird gestrichen. Eine Vorgabe zum Vorgehen ist nur berechtigt, wenn eine eigene Beobachtung dahintersteht (z. B. „erst ein vollständiger Durchlauf, dann die gesammelten Fehler beheben", weil Neustarts messbar Geld gekostet haben). Die Grenze liegt dort, wo Vorgabe zu Beaufsichtigung wird.
4. **Meta-Ebenen sauber halten:** Arbeitet das Projekt selbst mit Agenten, gibt es Agenten *im* Projekt und Agenten *des* Coding-Agenten – Wortwahl im Prompt eindeutig halten. Für solche Läufe ein klügeres Modell wählen.
5. **Formatieren lassen** in einem leeren Chat: „Formatiere diesen Text als Markdown, schreibe nichts um" – den Text in XML-Tags einrahmen, damit Daten und Anweisung getrennt sind.
6. **Abnahme-Checkliste erzeugen lassen:** „Schreibe die Anforderungen in abhakbarer Form, geordnet nach Ziel 1 und Ziel 2." Jede Formulierung auf zweite Lesarten prüfen („verpflichtende Abhängigkeit" ≠ „verpflichtend zu nutzen") – im Lauf hakt niemand mehr nach.
7. **Starten** per Skript in einer benannten Session: `python3 tools/agent-start.py start --prompt-file lauf.md --name nachtlauf`. Erster Auftrag an eine neue Instanz bei mehreren Skripten: die Hilfe der Skripte aufrufen und sie verstehen.
8. **Erst Fragerunde, dann Goal:** „Stelle innerhalb der nächsten zehn Minuten relevante Fragen; danach arbeite vollautonom." Antworten. **Erst danach** das Goal setzen – ein aktives Goal hindert den Agenten daran, für eine Rückfrage anzuhalten. Das Fragewerkzeug beim Namen nennen (verlangen oder verbieten).
9. **Goal setzen:** Zusammenfassung + Checkliste + Arbeitsweise („vollautonom, keine Fragen, nicht auf Antworten warten"). Token-Länge grob prüfen; den Befehl im Zielfenster frisch eintippen (kopierte Befehle bekommen gern ein Leerzeichen zu viel).
10. **Loslassen.** Fenster schließen, Session läuft weiter. Nicht ständig hineinschauen – Zuschauen ist der schwierige Teil.

## Nicht vor erledigter Arbeit aufhören
- Claude Code: `/goal` – Bedingungen in abhakbarer Form; der Agent bricht nicht ab, bevor sie erfüllt sind (endlos läuft er trotzdem nicht).
- Alternativ ein Loop, der den Agenten mit derselben Aufgabe neu startet, bis ein Prüfskript „fertig" meldet (vorsichtig: Loops ohne Abbruchkriterium und ohne Usage-Prüfung sind gefährlich).
- Große Ziele: ausführlich im normalen Chat beschreiben, in das Goal nur die zu erfüllenden Bedingungen setzen.

## Usage-Tracking (nur bei Abo-Kontingenten relevant)
- Ein Session-Fenster (z. B. 5 Stunden) plus Wochen- und Modell-Limits. Bei 100 % ist der Lauf faktisch tot: Subagenten sterben oder hängen; einziger Ausweg wäre zusätzliches, teures Extra-Kontingent.
- Lösung: ein **Usage-Skript**, das Prozentwert und Reset-Zeitpunkt zurückgibt (Datenquelle je Agent verschieden – bei Claude Code z. B. die Statusline-/Quota-Daten im Konfigurationsordner; sonst der Kontingent-Befehl des Agenten oder die Provider-API). Ausgabe menschenlesbar, für Wrapper zusätzlich eine byte-stabile Schlusszeile.
- Anweisungen im Prompt: das Skript nutzen; Prüfintervall verkürzen, je näher der Wert an 90 % rückt; über 90 % bis zum Reset warten; **Subagenten pausieren und prüfen ihr Usage selbst mit demselben Skript** – ein Subagent, der nichts vom Limit weiß, verbraucht das Budget des Hauptagenten ungebremst.
- **Kosten getrennt tracken** (API-Kosten ≠ Kontingent).

## Selbstüberwachung
- Lang laufende Skripte hängen manchmal; Agenten verlaufen sich. Es braucht jemanden, der von Zeit zu Zeit hinschaut, wenn niemand vor dem Bildschirm sitzt.
- Der Agent legt sich die Überwachung selbst an: bei Claude Code per `CronCreate`-Tool bzw. `/loop` („lege dir mit deinem CronCreate-Tool einen Job an, der alle 30 Minuten `tools/watch.py` ausführt"). Werkzeug beim Namen nennen, damit aus dem Cron-Tool kein Chrome-Tool wird; mit einer trivialen Aufgabe (minütlich „Hallo Welt") vorher testen, danach den Job wieder löschen.
- Was der Job prüft: laufen die Prozesse noch, gibt es Fortschritt, läuft die Platte voll, hängt ein Skript, ist ein Subagent ohne Ergebnis stehen geblieben. Bei Befund: eingreifen oder den Lauf neu anstoßen.
- Für Überwachung von außen (auch bei Rate-Limits, die der Agent selbst nicht mehr melden kann) und Zeitpläne: [freilauf.md](freilauf.md).

## Verhalten für Unvorhergesehenes: Boundaries und Abbruchbedingungen
Modelle wollen ihr Ziel erreichen und nehmen den kürzesten Weg – im Normalfall die eingebaute Bremse, unter Zieldruck („denke out of the box") aber auch der Grund für unerwünschte Wege. Wer autonom laufen lässt, gibt deshalb ein Verhalten für unvorhergesehene Situationen mit:
- **Harte Grenzen:** „Nur die Controller migrieren, sonst nichts." „Keine Änderungen außerhalb von `src/api/`." „Keine E-Mails, keine Deployments, keine Produktivsysteme." Sonst schreibt der Agent das halbe System um, weil „dann muss auch das und das".
- **Abbruchbedingung:** „Stellst du fest, dass du außerhalb von X etwas ändern müsstest, hör auf und schreib auf, was fehlt."
- **Bei Zeit:** die ersten Fälle gemeinsam, die nächsten allein, bei Erfolg alle.
- **Tests glattziehen ohne Bugs zu kaschieren:** „Zieh die Tests glatt, die wegen der Codeänderung brechen; findest du dabei einen Bug, kaschiere ihn nicht, sondern schreib ihn auf." Ohne den Zusatz werden Tests grün und Fehler verschwinden.
- Grobe Ziele haben Kanten: „Pipeline debuggen" braucht den Satz „gefixte Bugs aus der Bug-Liste entfernen", sonst wächst die Liste endlos.
- Loops (Agent wird mit derselben Aufgabe neu gestartet) nur mit Abbruchkriterium und Usage-Prüfung.

## Steuern ohne zu stören
- Direkt in den Chat getippte Hinweise ändern den Kontext und wirken auf alles Folgende – so steuert man absichtlich (Steering). Mitten im Lauf „benutze jetzt den librarian" ist dagegen sinnlos; angebotene Werkzeuge werden in autonomen Läufen seltener genutzt als erwartet.
- Stille Diagnose: Der ganze Verlauf plus eine Frage an ein zweites Modell (Claude Code: `/by the way`) beantwortet „wo steht er?", ohne dass der Agent etwas merkt. Muster: still diagnostizieren → Problem außerhalb des Laufs beheben → nur die eine nötige Information in den Chat.
- Verläuft sich der Hauptagent in Detailarbeit: „Starte dafür lieber einen Subagenten, damit du dich nicht ablenken lässt." Bei langen Läufen gleich am Anfang: „Du orchestrierst nur; Subagenten setzen um – so schützt du dein Kontextfenster."
- Modell und Reasoning-Aufwand sind keine Einmal-Einstellungen: Für Zwischenaufgaben ohne Denkbedarf ein kleineres Modell und niedrigeren Effort; für Läufe, in denen Meta-Ebenen und Werkzeuge verstanden werden müssen, das klügste Modell.

## Selbstverbesserung (optional)
Der Agent darf den Skill, aus dem er das Wissen zur Weiterentwicklung des Systems zieht, mit **relevanten** Learnings fortschreiben. Risiko: Er optimiert den Skill kaputt und wirft Kernentscheidungen über Bord. Gegenmittel: nicht verhandelbare Entscheidungen im Skill als solche markieren; „mit den relevanten Learnings", nicht „mit allen". Ein Rest bleibt Kontrollabgabe.

## Verifikation ans Ende verlagern
Manche Ergebnisse kann nur ein Mensch abnehmen. Dann lohnt es sich, die Endabnahme verlässlich ans Ende zu legen (z. B. eine Kommentarfunktion mit Zeitmarke, deren Rückmeldung der Agent gezielt abarbeitet) und unterwegs nicht jede Kleinigkeit per Screenshot prüfen zu lassen – laufende Zwischenprüfung ist teuer, Edge Cases sind beim Menschen am Ende besser aufgehoben.

## `tools/agent-start.py` in Kürze
`doctor` (welche Agenten/Multiplexer da sind) · `start --prompt/--prompt-file [--agent] [--name] [--dir] [--model] [--headless] [--attach] [--dry-run]` · `list` · `attach NAME` · `send NAME "Text"` · `kill NAME`. Mit Multiplexer entsteht eine interaktive Session `hx-<name>`; ohne (oder mit `--headless`) läuft der Agent im Hintergrund mit Log unter `.harness/runs/`. Die Flags je Agent stehen in einer Tabelle am Anfang des Skripts – der einzige Ort, der bei Flag-Änderungen anzupassen ist.
