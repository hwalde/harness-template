# Skripte für Coding-Agenten
**Kern:** Alles algorithmisch Entscheidbare gehört in ein Skript; die KI entscheidet, das Skript führt aus. Jedes Skript dieses Harness wird nach den zehn Prinzipien unten gebaut – ohne Rückfrage, sie gelten hier immer. (Kontext: Harness-Template | Stand: 2026-08-30)

## Warum Skripte
- **Determinismus:** Ein Skript liefert jeden Tag dasselbe Ergebnis; ein Fehler ist ein Bug, den man fixt. Ein Modell antwortet an manchen Tagen so, an anderen anders. Beispiel: statische Codeanalyse per Skript, nicht per „schau dir die Dateien an".
- **Arbeitsteilung:** Die KI entscheidet, *was* passieren soll und *wo*; das Skript macht es. Alles, was sich ohne KI skripten lässt, wird geskriptet.
- **Entlastung:** Ein Skript, das prüft, ob der Server läuft, der Port frei ist, der Health-Endpunkt Fehler meldet und was im Log steht, ist ein klassischer Harness-Baustein. Optimierte Skripte machen den Agenten besser.
- **Grenze:** Fachliche Abwägung („ist dieser Schnitt sinnvoll?") bleibt beim Modell. Und: Wo schon ein Werkzeug steht (Browser-Steuerung, Computer Use, `gh`), kein Skript nachbauen.
- **Bekanntmachung:** Das Modell „riecht" ein Skript nicht. Es muss erwähnt sein – in `AGENTS.md` (ein Satz), im Chat oder in einem Skill. Skript vs. MCP: [mcp-und-werkzeuge.md](mcp-und-werkzeuge.md).

## Leitbild: Ein CLI-Tool ist ein Funktionsaufruf an einen Menschen
Der Aufrufer ist ein LLM – man behandelt es wie einen klugen Kollegen: Es kennt jeden Fachbegriff und braucht keine Belehrung, verdient aber die Aufbereitung, die fehlerfreies Arbeiten ermöglicht. Der Aufruf ist so einfach, dass man ihn kaum falsch machen kann; die Ausgabe so klar, dass die Chance auf ein Missverständnis gegen null geht. Im Inneren arbeiten Algorithmen und Datenstrukturen; an der Schnittstelle wird Menschensprache gesprochen – in beide Richtungen.

## Die zehn Prinzipien (verbindlich für alle Skripte dieses Harness)

### 1. Schnell beenden
Ein Skript darf nie dauerhaft laufen – der Agent wartet auf das Ergebnis und hängt sonst. Braucht es einen Hintergrundprozess (Server), spawnt das Skript ihn abgelöst (`start_new_session=True`, Log in Datei) und beendet sich sofort mit der PID.

### 2. Selbsterklärend und einfach
- Aufruf ohne Argumente = Hilfe, die erklärt, wie das Tool zu verwenden ist.
  Ausnahme: Ein Skript mit genau einer gefahrlosen, idempotenten Aktion darf sie ohne Argumente direkt ausführen, solange die Ausgabe erklärt, was geschah (`-h/--help` bleibt trotzdem verfügbar; Beispiel: `tools/sync-agents.py`).
- Möglichst wenige Argumente; Argumente sprechen die Sprache der Aufgabe, nicht die interne Struktur (ein wörtliches Zitat oder ein Zeitstempel statt eines Index oder Objektpfads – interne IDs muss sich der Agent erst beschaffen und verwechselt sie).
- Je weniger Dokumentation in `AGENTS.md` nötig ist, desto besser: eine Zeile (`tools/check-logs.py – Fehleranalyse der Logdatei`), nicht 15.

### 3. Progressive Offenlegung
Oberste Ebene: nur die wichtigsten Unterbefehle. Details, Optionen und Unter-Hilfeseiten erst auf der jeweiligen Ebene.

### 4. Menschenlesbare Ausgabe – der Konsument bestimmt das Format
Reihenfolge: Markdown > Fließtext > XML > JSON (vermeiden). LLMs sind Leser, keine Parser; verschachteltes JSON zerreißt den Zusammenhang. Ausnahme: Ist der Konsument ein Skript (Pipeline, parsender Wrapper), bekommt genau dieser Konsument sein Format – etwa eine byte-stabile Schlusszeile oder ein `--json`-Flag. Die Formatwahl wird **nicht** dem Agenten überlassen; Modelle halten JSON fälschlich für geeignet.

### 5. Tokensparend
Die gesamte Ausgabe landet im Kontextfenster. Klarheit vor Kürze, aber wenn beides geht: kurz und klar. Keine Banner, keine Punktlinien, keine Wiederholungen. `Server läuft (Port 8080, seit 5 Min). Keine aktuellen Fehler.` statt eines Statusreports.

### 6. Navigation statt Datendump
Nie alles auf einmal. Übersicht (neueste Fehler zuerst, Zeitstempel, eine Zeile je Eintrag) plus die Befehle für Details, Blättern (`--page`), Filter (`--errors`, `--search`). Der Agent bekommt die Wahl, was er als Nächstes sehen will.

### 7. Ausgabe als Prompt – und als erste Validierung
Jeder Satz der Ausgabe landet als Anweisung im Kontext. Die Ausgabe leitet: Navigationshinweise, kontextuelle Beobachtungen, **Vorschläge statt Befehle** („Fehler #1 ist 8 s alt und stammt wahrscheinlich von deiner Änderung – Vorschlag: `tool.py logs --detail 1`"). Bei zustandsändernden Befehlen: bestätigen, was geschehen ist, die Wirkung im Kontext zeigen, den fertig ausgefüllten Umkehr-Befehl nennen – der Agent prüft seine Aktion im selben Moment. Zeitbezug liefern (Alter von Einträgen), weil Modelle kein Zeitgefühl haben und ihre eigenen Log-Einträge sonst nicht finden.

### 8. Mitdenken
- Multi-Agent-sicher: „Server wurde vor 8 s gestartet – möglicherweise arbeiten andere Agenten parallel. Erzwingen mit `--force`."
- Sinnvolle Sortierung (neueste zuerst), Vorprüfungen (kompiliert es? Port belegt? von wem?), Zählen und Messen im Skript statt im Modell.
- Daten korrelieren, statt sie einzeln hinzuwerfen (Browser-Log, Netzwerk, Server-Log je fehlgeschlagenem Test).

### 9. Verfügbare Sprache, keine Isolation
Python bevorzugt (vorher prüfen, ob vorhanden; sonst Bash). Betriebssystem-unabhängig schreiben (`pathlib`, `shutil.which`, keine Shell-Spezialitäten). **Keine virtuellen Umgebungen** – nur Standardbibliothek oder `pip install` ohne venv; fehlende Pakete beim Start erkennen und den Installationsbefehl nennen.

### 10. Fehlermeldungen sind Handlungsanweisungen
Symptom + Soll/Ist + nächster Schritt: `Abbruch: API_TOKEN fehlt in .env (erwartet: API_TOKEN=<token>). Eintragen und erneut aufrufen. Vorlage: .env.example` – kein Stacktrace ohne Deutung. Ein Agent wiederholt bei unklaren Fehlern den Aufruf oder rät; eine Meldung mit Fix macht aus dem Fehlversuch einen Ein-Schritt-Repair.

## Nach dem Bau: Eintrag in `AGENTS.md`
Ein Skript ohne Erwähnung existiert für den Agenten nicht. Der Eintrag enthält: Name und Aufruf, wann verwenden, was es ersetzt (welcher bisherige Befehl NICHT MEHR verwendet wird). Deutlich formulieren – WICHTIG/NICHT/IMMER fallen Agenten auf; kurze Sätze; nur der Hauptbefehl, Unterbefehle entdeckt der Agent durch Aufruf.

```markdown
## Server starten/stoppen
WICHTIG: Server NICHT direkt mit `npm start` starten. IMMER `python3 tools/server.py start`
verwenden – kompiliert vorher, prüft Port-Konflikte, schützt vor Doppelstarts.
- `python3 tools/server.py` – zeigt die Befehle (start, status, logs)
```

## Typische Harness-Skripte
| Skript | Zweck |
|---|---|
| `tools/agent-start.py` (im Template) | Coding-Agent rückfragefrei starten, optional in tmux/psmux; `list`, `attach`, `send`, `kill`, `doctor` → [autonome-laeufe.md](autonome-laeufe.md) |
| `tools/sync-agents.py` (im Template) | Subagent-Definitionen aus `.claude/agents/` in das Format anderer Agenten übersetzen → [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md) |
| Server-/Dienst-Steuerung | starten mit Vorprüfung, Status, Logs mit Navigation, Restart-Schutz |
| Log-Analyse | neueste Fehler zuerst, Alter, Filter, Detail-Befehl für Stacktraces |
| Test-Runner-Wrapper | E2E parallel, Fehlschläge sequentiell wiederholen, Browser-/Netzwerk-/Server-Log je Test korrelieren |
| Usage-Skript | Kontingent in Prozent + Zeitpunkt des Resets, damit ein autonomer Lauf vor dem Limit anhält → [autonome-laeufe.md](autonome-laeufe.md) |
| Überwachung | prüft hängende Skripte und verlaufene Agenten; vom Agenten per Cron/Loop periodisch aufgerufen |
| Zähl-/Messwerkzeuge | Wörter, Längen, Maße – Modelle zählen schlecht |
| Build/Release | genau ein Skript für den Release-Bau, in `AGENTS.md` als einziger Weg festgeschrieben |

## Fallstricke
- Skript existiert, ist aber nirgends erwähnt.
- Wrapper, der ganze Logdateien ausgibt (Bloat); JSON-Blob-Ausgabe; Langläufer, die den Agenten blockieren.
- Skriptausgabe ist ein Prompt – also auch ein Angriffsvektor: Fremde Inhalte (Mails, Webseiten, Tickets) in der Ausgabe klar als Daten kennzeichnen (z. B. XML-Tags), nie als Anweisung formatieren.
- Kleine/lokale Modelle vergessen Skripte eher – dort explizitere Hinweise oder MCP.
