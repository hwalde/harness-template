# Workflow: vom Auftrag zur abgenommenen Arbeit
**Kern:** Ein Standard-Workflow in `AGENTS.md` legt die Reihenfolge fest: Vorwissen holen → planen (so viel wie nötig) → umsetzen mit deterministischen Prüfungen → Evaluator-Schleife → Dokumentation und Wiki nachziehen. Der Gegenpol zu viel Planung ist ein knappes Ziel mit Prüfkriterium. (Kontext: Harness-Template | Stand: 2026-08-30)

## Der Standard-Workflow (Vorschlag für `AGENTS.md`, bei der Einrichtung zuschneiden)
1. **Vorwissen:** librarian ABFRAGE mit der Intention; verlinkte Dokumente lesen, die das Thema berühren (Unterordner-Regeldateien lädt der Agent situativ).
2. **Planen, so viel wie nötig** (Stufen unten). Akzeptanzkriterien abhakbar aufschreiben – sie sind der Maßstab des Evaluators.
3. **Umsetzen.** Deterministisches per Skript: Formatierung, Linter, statische Analyse, Tests, Build. Bei Web-/Desktop-Apps zwischendurch selbst nachsehen (Browser-/Desktop-Steuerung), am Ende wiederholbare Tests laufen lassen.
4. **Abnahme:** evaluator mit Kriterien, Diff und Evidenz; bei `NEEDS_WORK` nacharbeiten und erneut prüfen, bis `PASS`. Schwerpunkt-Evaluatoren nach Änderungsumfang ([evaluatoren.md](evaluatoren.md)).
5. **Nachziehen:** Dokumentation/Spezifikation aktualisieren; Bleibendes über den librarian einlagern (nur was eine zukünftige Session braucht); ein Satz in `AGENTS.md`, wenn er zum wiederholten Mal nötig war; Release/Deploy nur über das dafür festgelegte Skript.

Das ist die Reihenfolge, nicht ein Formular: Ein Ein-Zeilen-Fix braucht keinen Plan, aber jede Änderung braucht die Abnahme.

## Wie viel Planung eine Aufgabe braucht
| Stufe | Wann | Vorgehen |
|---|---|---|
| 1 – machen lassen | nicht kompliziert (Button umfärben, kleiner Fix) | direkt aus dem Chat umsetzen; deckt heute die meisten Fälle |
| 1+ – planen lassen | etwas mehr Struktur gewünscht | Planungsmodus des Agenten → technischer Plan → umsetzen |
| 2 – Plan in Datei | Stufe 1 trägt nicht; Kontext soll frisch sein | Plan in Datei schreiben lassen, dann **2–4 Korrekturschleifen** („geh noch einmal durch den Verlauf, fehlt etwas für die Umsetzung?") – beim ersten Nachfragen kommt immer Wesentliches nach; Umsetzung in neuem Chat nur mit dem Plan |
| 3 – Anforderungsdokument | wirklich groß; ein technischer Plan wird zum Klotz (ab ~800 Zeilen gut, 4000 schlecht) | fachliche Anforderungen mit Schlüsselnummern (was, nicht in welcher Datei) + Umsetzungspakete (jede Anforderung mindestens einem Paket zugeordnet – Korrekturschleife) + **Testinganforderungen je Paket** + bei schwachem Harness Testing-Informationen (nutzbare Werkzeuge, API-Doku, MCP-Server). Zwei Zusatzanforderungen je Paket: nach der Umsetzung das Dokument erneut lesen und abhaken; knappe Implementierungshinweise für Folgepakete nachtragen. Ein Chat oder Subagent je Paket |

Daraus der Zyklus **Dokument lesen → arbeiten → Dokument aktualisieren**: Das Anforderungs- bzw. Plandokument bleibt die fortgeschriebene Wissensquelle für den nächsten Chat oder Subagenten.

**Gegenpol (bevorzugt, wo möglich):** Ziel + Prüfkriterium statt Ablaufplan. „Die Pipeline soll unter 10 Dollar kosten; prüfe das über die Kostenabfrage bei X." Die Prompt-Arbeit verschwindet nicht, sie wandert vom Vorgehen ins Ziel und ins Kriterium ([autonome-laeufe.md](autonome-laeufe.md)). Frameworks, die Anforderungen abfragen (Spec-Kit-artige), sind Stützräder – nützlich, solange man ungeübt ist.

**Pre-Workflow:** Ticket + Braindump (alles, was der Agent nicht wissen kann: Meetings, Richtung, Bedenken, eigene Fragen) → 3–8 Subagenten parallel als Informationsbeschaffer („wie haben wir X gebaut, wäre ein Refactoring nötig?") → Lösungswege vom Agenten kommen lassen, Mensch entscheidet. Der Chat ist dann „eine Müllhalde mit Perlen"; ab Stufe 2 werden nur die Perlen weitergegeben.

## Testen im Workflow
- Die Testpyramide bleibt. Tests sind mit KI wertvoller als vorher, weil der Agent damit sein eigenes Ergebnis validiert; E2E-Tests am Ende, gern schon am Anfang geschrieben; bei Parser-artigen Aufgaben Input/Output-Paare vorgeben („bau dir daraus Unit-Tests").
- Kein manuelles Testdrehbuch zum Durchspielen geben – daraus wiederholbare E2E-Tests generieren lassen (Durchklicken ist tagesformabhängig).
- Browser-/Desktop-Steuerung ist zum Nachsehen zwischendurch da, nicht zum Testen; deterministische Zustandsprüfungen (Server läuft? Port? Health? Log?) sind Skripte.
- Testergebnisse für den Agenten aufbereiten (Skript: fehlgeschlagene Tests einzeln wiederholen, Browser-Log/Netzwerk/Server-Log je Test, Alter der Einträge) – Agenten haben kein Zeitgefühl.
- Nach Umbauten: „Tests glattziehen; findest du einen Bug, kaschiere ihn nicht, sondern schreib ihn auf."
- Menschliche Endabnahme bleibt, wo es um menschlich-optische Beurteilung geht (Sinnhaftigkeit von Oberflächen, Spezialsoftware, Video). Sie ans Ende legen und den Agenten unterwegs nicht jeden Edge Case per Screenshot prüfen lassen.

## Aufträge formulieren (Kurzfassung)
- Kristallklar, sachlich; das **Warum** und das Qualitätsniveau mitgeben (Prototyp für eine Demo vs. Produktivsystem).
- Kontext: hineinschreiben, holen lassen (und sagen wo) oder – Harness – selbst holen lassen.
- Beispiele sparsam bei Spitzenmodellen (Quelltext ist das Beispiel: „wie der User-Service"); reichlich bei kleinen Modellen.
- Vorgehen nur vorgeben, wenn eine eigene Beobachtung dahintersteht; sonst Fähigkeit nennen („nutze Subagenten") und Einsatz überlassen.
- Verhalten für Unvorhergesehenes: Grenzen und Abbruchbedingungen ([autonome-laeufe.md](autonome-laeufe.md)).
- Werkzeuge beim Namen nennen (verlangen oder verbieten); Aktionen nach außen begrenzen („ausfüllen, nicht abschicken").
- Fremden Text in XML-Tags einrahmen; „formatiere, schreibe nicht um"; „eins zu eins in eine Datei schreiben".
- Aufträge an andere Instanzen/Subagenten als **Brief**, nicht als Befehlsliste: „Bedenke, dass die Instanz dasselbe Modell ist wie du und sich vollständig damit auseinandersetzen wird – lass ihr Raum zum Denken."
- Drei Kontrollfragen: „Gib in deinen Worten wieder, was ich gesagt habe." · „Gibt es noch offene, **relevante** Fragen?" · nach Überplanung: „Gibt es Widersprüche?"
- Zahlen statt Adjektive für Umfang; Textmengen misst ein Skript.

## Rückfragen-Politik
Bei der Einrichtung festlegen: interaktiv (Rückfragen erlaubt, bevorzugt gebündelt und mit dem Fragewerkzeug des Agenten) oder vollautonom (keine Rückfragen außer auf Aufforderung; beste begründete Annahme treffen, dokumentieren, weiterarbeiten; Fragerunde nur vor dem Start). Für unbeaufsichtigte Läufe gilt immer Letzteres.

## Dynamic Workflows und Evaluator-Ketten
- Normal: Hauptagent startet Subagent → liest Report → denkt → nächster. Ein **Dynamic Workflow** (Claude Code: Workflow-Skript) spart das Dazwischen: Der Hauptagent schreibt ein Skript aus Subagent-Aufrufen (je Modell, Typ, Prompt, Ausgabeschema), führt es aus, bekommt am Ende einen Report; Ergebnisse fließen als Text in den nächsten Prompt. Vorteil: kein Nachdenken zwischen den Schritten; Nachteil: genau das fehlt. Nur mit ausdrücklicher Zustimmung des Benutzers – viele Agenten, viele Tokens.
- Mehrere Evaluatoren nacheinander lassen sich so als Kette abbilden (Findings des einen im Prompt des nächsten) oder schlicht sequenziell vom Hauptagenten aufrufen.
- Hauptagent als Manager: bei langen Läufen orchestriert er nur; Subagenten setzen um. Schwärme mit Rollen und Kommunikationsregeln haben sich nicht bewährt.

## Der Harness wächst nebenbei
Jeder Satz, den man zum zweiten Mal tippt, wird eine Regel; jede Handarbeit, die algorithmisch ist, ein Skript; jede wiederkehrende Prüfung ein Evaluator; jeder gelungene Ablauf ein Skill („Gibt es Teile, die wir als Skill wiederverwenden sollten?").
