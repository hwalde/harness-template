# MCP-Server und Werkzeuge: wann MCP, wann nicht
**Kern:** MCP-Server geben dem Agenten Werkzeuge (Browser, Desktop, fremde Systeme); sie kosten Kontext und laufen mit deinen Rechten. Die Konkurrenz zum MCP-Server ist das Skript. (Kontext: Harness-Template | Stand: 2026-08-30)

## Was MCP ist (in drei Sätzen)
- Model Context Protocol: Client-Server-Protokoll (kein REST). Der Coding-Agent ist der Client, der Server ein laufendes Programm, das Funktionen als „Tools" anbietet.
- Beim Start liest der Agent seine Konfiguration, verbindet sich, sammelt die Tool-Liste ein und hängt sie an seine eigenen Werkzeuge an. Ruft das Modell ein MCP-Tool auf, reicht der Agent den Aufruf an den Server weiter; das Ergebnis kommt als Text zurück.
- Konfiguration = Command + Argumente + Umgebungsvariablen, auf Benutzer- oder Projektebene (Dateiname je Agent, siehe [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md)). MCP-Server können **nicht** in einen Skill gelegt werden; verteilbar sind sie über Plugins.

## Was sie kosten
| Kostenart | Fakt |
|---|---|
| Kontextfenster | Ohne Lazy Loading werden alle Tool-Beschreibungen bei **jedem** Request mitgeschickt: fünf Server ≈ 50k Tokens, mit Browser-Server schnell 100k. Claude Code lädt Tool-Beschreibungen inzwischen lazy (Tool-Search): ≈ 90 Tokens pro tatsächlich genutztem Tool plus ≈ 3 Zeilen pro Server. Andere Agenten (z. B. GitHub Copilot) schicken sie dauerhaft mit (Computer-Use-Server ≈ 12k, Playwright ≈ 4k). Prüfen mit `/context` bzw. dem Kontext-Befehl des Agenten. |
| Ungenutzte Server | kosten trotzdem bei jedem Request → Server für gerade nicht genutzte Plattformen abschalten. |
| Arbeitsspeicher | Standardbauweise: eine Server-Instanz pro Agent-Instanz. Viele offene Agenten = viel RAM; Extremfall 12 GB für einen Server. |
| Sicherheit | Ein MCP-Server läuft **mit deinen Rechten** und ist praktisch nicht prüfbar (vollständige Anwendung, bei jedem Update von vorn). Ein Server, der Quelltext ins Netz lädt, wird von keinem Virenscanner erkannt. Unbekannte Herkunft → nicht installieren. Secrets landen mitunter in der MCP-Konfiguration – nie ins Repo committen. |
| Massen-Installation | Verzeichnisse listen tausende Server. Jeder zusätzliche Server (wie jeder Skill, jeder Subagent) senkt die Modellleistung und erhöht die Kosten. Installiert wird, was das Projekt braucht – nichts „auf Vorrat". |

## Entscheidungsregel: MCP-Server oder CLI/Skript?
Vorfrage vor jeder Erweiterung: **Ist die Aufgabe algorithmisch entscheidbar?** Dann Skript (deterministisch, ein Fehler ist ein reparierbarer Bug). Braucht sie Fachlichkeit oder Abwägung, bleibt sie beim Modell. Erst danach die Frage MCP oder CLI:

| Kriterium | → MCP-Server | → CLI-Tool / Skript |
|---|---|---|
| Zustand | zustandshaltend: offene Browser-Tabs, Sitzung, Fenster, das so lange lebt wie der Server | zustandslos: „läuft der Server, ist der Port frei, was steht im Log", kleine wiederverwendete Algorithmen |
| Entfernung | Funktion läuft auf einem anderen Rechner; eigene Anwendung soll von außen benutzbar sein | REST-API direkt ansprechen oder ein Skript über die API bauen |
| Nutzungshäufigkeit | ständig gebraucht (Browser-Steuerung täglich) | situativ gebraucht |
| Sichtbarkeit | Werkzeug soll omnipräsent im Blick des Modells sein | ein Satz in `AGENTS.md` an der richtigen Stelle genügt |
| Vorhandenes CLI | – | gibt es ein Kommandozeilen-Tool (`gh`, Hersteller-CLIs, `kubectl`, `aws`, `psql` …), ist ein MCP-Server überflüssig – der Agent kennt diese Tools oft besser als der Entwickler |
| Prüfbarkeit | kaum prüfbar, volle Rechte | lesbar, prüfbar, im Repo versioniert |
| Modellstärke | kleine/lokale Modelle vergessen Skripte → MCP | starke Modelle merken sich einen Hinweis |
| Paketierung | nur Benutzer-/Projektebene, nicht im Skill; Secrets in der Konfiguration | Skript liegt im Repo oder Skill-Ordner |

Faustregel: **Zustand, Entfernung oder tägliche Nutzung → MCP. Alles andere → Skript** ([skripte.md](skripte.md)). Ein MCP-Server, der einen vorhandenen CLI-Befehl nachbaut, ist ein Fehler.

## Bereitstellen ist nicht Benutzen
Ein installiertes Werkzeug wird nicht automatisch verwendet. Soll es verwendet werden, steht das ausdrücklich in `AGENTS.md`: „Für X IMMER Werkzeug Y verwenden" – bei Bedarf mit dem Gegenstück „NICHT Z". Beispiele: „Kann eine Webseite nicht gelesen werden (Fetch geblockt), Playwright-MCP zum Lesen verwenden." · „Computer Use darf zum Debuggen der Desktop-App eingesetzt werden."

## Empfohlene Befähigung je Anwendungstyp
Ziel der Befähigung: Der Agent kommt selbst an Informationen, testet und schaut sich Dinge selbst an – jede Schleife „Mensch klickt durch und schreibt einen Prompt, dass etwas nicht geht" kostet Zeit.

| Anwendung | Empfehlung |
|---|---|
| Kommandozeile / Bibliothek | keine Browser-/Desktop-Steuerung nötig; Tests und Skripte reichen |
| Web-Anwendung | **Playwright-MCP** (oder Selenium/Puppeteer-Äquivalent): Seite öffnen, durchklicken, Formulare ausfüllen, Screenshots machen, Browser-Konsole und Netzwerk lesen. Auf Servern headless. Bauformen: eigener leerer Browser (keine Logins, sicher) · Tab-Reihe im echten Browser (Logins vorhanden, viel Zugriff – abwägen) · Hybrid mit gesperrten Seiten. **Ersetzt keine Tests** – es dient dem Ausprobieren und Anschauen während der Arbeit; am Ende läuft ein E2E-Test. |
| Desktop-Anwendung | **cua-computer-use** (Open-Source-Computer-Use-MCP): dasselbe für Desktop-Apps, Anwendung darf im Hintergrund laufen. Der Agent nutzt es als Debug-Werkzeug nur, wenn `AGENTS.md` es ausdrücklich erlaubt. |
| Layout-/Design-Arbeit | Multimodale Modelle sehen Screenshots ohnehin; ein Vision-Server (Positionen, Abstände) nur bei konkretem Bedarf |
| Bilder erzeugen | Bildgenerierungs-Server nur, wenn das Projekt Bilder braucht |
| E-Mail | nur **lesend** (List/Read, keine Send-Funktion) – z. B. um Bestätigungsmails/Newsletter-Anmeldungen zu prüfen. Rote Linie: kein Versand ohne menschliche Freigabe. |
| Ticket-/Wiki-/Pipeline-Systeme (Jira, Confluence, CI) | prüfen, ob ein CLI existiert; Confluence-Inhalte sind für Menschen geschrieben und oft eine Müllhalde – ein agentengerechtes Wiki ([wissensablage.md](wissensablage.md)) ist meist die bessere Quelle |

## Konfigurationsorte (Kurzfassung)
Projektlokal, damit jeder Klon dieselben Werkzeuge hat; Secrets über Umgebungsvariablen, nie im Repo. Dateinamen je Agent in [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md). Vor und nach dem Hinzufügen den Kontextverbrauch prüfen.

## Fallstricke
- MCP-Server nur, weil er im Verzeichnis steht – ohne Use Case. Erst der Use Case, dann der Server.
- GitHub-/GitLab-MCP installiert, obwohl `gh`/`glab` da sind.
- Hersteller-CLIs bringen MCP-Server ungefragt mit → Kontext-Ansicht prüfen.
- Browser-Steuerung als Testersatz missverstanden.
- Tab-Reihe im echten Browser: der Agent darf dann nie den Browser schließen oder fremde Tabs anfassen – gehört als Regel in `AGENTS.md`, wenn diese Bauform gewählt wird.
- Computer Use ohne ausdrückliche Erlaubnis wird nicht als Debug-Werkzeug genutzt.
