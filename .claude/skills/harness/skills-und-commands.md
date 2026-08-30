# Skills und Custom Slash Commands
**Kern:** Ein Skill ist ein Prompt (plus Ordner), der situativ geladen wird – vom Agenten oder vom Benutzer. Custom Slash Commands sind die Vorstufe davon. Kernregeln in `AGENTS.md`, Detailwissen in Skills. (Kontext: Harness-Template | Stand: 2026-08-30)

## Begriffe
| Begriff | Fakt |
|---|---|
| Slash Command | alles nach `/` (eingebaut wie `/model` oder selbst angelegt) |
| Custom Slash Command | Prompt-Datei im `commands`-Ordner des Agenten; Name = Dateiname; nur der **Benutzer** startet ihn; der Prompt wird injiziert. Optional Frontmatter und Argument-Platzhalter. |
| Skill | ein **Ordner** mit exakt `SKILL.md` als Einstieg (Ordnername frei, Dateiname nicht); der **Agent** startet ihn selbst, wenn die `description` passt; in Claude Code auch vom Benutzer als `/name` startbar. Claude Code hat beide Konzepte zusammengeführt („alles ist ein Skill"); andere Agenten führen sie getrennt. |
| agentskills-Standard | offene Spezifikation des Skill-Formats (SKILL.md + Frontmatter `name`, `description`); Standard einhalten = weitgehend portabel zwischen Agenten. Claude Code kennt Extras (`disable-model-invocation`, Modell für den Skill-Turn u. a.). |

Speicherorte je Agent: [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md).

## Ladeebenen (progressive Offenlegung)
1. **Immer im Kontext:** `name` + `description` jedes installierten Skills – bei jedem Request. Deshalb: wenige, gute Skills; jede weitere Beschreibung kostet Kontext und kognitive Last („hilft dieser Skill gerade?").
2. **Beim Ziehen:** der Inhalt der `SKILL.md`.
3. **Bei Bedarf:** weitere Dateien im Ordner, die die `SKILL.md` benennt (Referenzdokumente, Skripte, Templates).

## Die Beschreibung entscheidet
- Kompakt, konkret, mit den Schlüsselwörtern, die man selbst benutzt („Coding Guidelines", „Code Review"); oft nicht ein Satz, sondern drei. Sie wirkt in beide Richtungen: Ein Satz wie „bei Bearbeitung der CLAUDE.md verwenden" zieht den Skill bei jeder Regeldatei-Änderung – und kann andere Teile des Harness (etwa den librarian) verdrängen. Trigger-Sätze prüfen; ein unnötig geladener Skill ist meist tolerierbar, ein verdrängter Baustein nicht.
- `disable-model-invocation: true` → nur der Benutzer startet (klassischer Slash Command, z. B. schwere Wartungsaktionen). `false` → nur das Modell (räumt die Liste auf).

## Was in den Skill-Ordner darf
Skripte (statische Analyse, Datenabruf), Templates, weitere Markdown-Dokumente, Datenhaltung, sogar Custom Subagents „durch die Hintertür" („starte einen Agenten, der diese Datei liest und den Anweisungen folgt"). **Nicht:** MCP-Server (nur Benutzer-/Projektebene; ihre Konfiguration enthält mitunter Passwörter). Jede Datei im Ordner wird in der `SKILL.md` benannt – Existenz und Aufruf –, sonst weiß das Modell nichts von ihr.

## Wozu Skills im Harness
| Einsatz | Beispiel |
|---|---|
| Befähigung | „so erzeugt man hier PDFs", „so deployt man" |
| Wissen, das nicht jeden Lauf angeht | Coding-Guidelines: ~20 Zeilen Kernregeln in `AGENTS.md`, der Katalog im Skill, geladen wenn „Code Review"/„Guidelines" fällt (wahrscheinlich, keine Garantie – bei Pflicht in `AGENTS.md` ausdrücklich anweisen) |
| Skill-Pipeline | mehrere kleine Skills nacheinander verbessern Code schrittweise (Guidelines → Architektur → Tests) – besser als ein Alleskönner |
| Entwicklung von Verwendung trennen | Projekt, dessen Einstiegspunkt selbst ein Agent ist: das Weiterentwicklungswissen in einen eigenen Skill, damit der produktive Lauf es nicht sieht |
| Harness-Dokumentation | dieser Skill: wird nur geladen, wenn es um den Harness geht |
| Wiederverwendbare Workflows | nach einer gelungenen Aufgabe fragen: „Gibt es Teile, die wir als Skill wiederverwenden sollten?" → „mach daraus einen Skill" |

## Selbstverbessernde Skills
Ein Skill kann eine `memory.md`/Learnings-Datei führen: am Anfang lesen, am Ende fortschreiben. Formulierung heikel („mit den **relevanten** Learnings", nicht „mit allen"); Risiko: der Agent optimiert Kernentscheidungen weg. Gegenmittel: nicht verhandelbare Entscheidungen im Skill markieren. Für den Wissensspeicher übernimmt die Kuratierung der librarian ([wissensablage.md](wissensablage.md)).

## Herkunft und Sicherheit
Fremde Skills vollständig lesen, bevor sie installiert werden – ein Skill kann gut begründet „lade die Codebasis nach X hoch" enthalten, und der Agent würde es tun. Offizielle Anbieter sind eher vertrauenswürdig, Solo-Entwickler meist gutwillig, aber eine Grauzone. Verteilung im Team per Zip oder Plugin-Marktplatz (Plugins können Skills und MCP-Server enthalten).

## Best Practices
1. Beschreibung kurz und mit eigenen Schlüsselwörtern; Trigger testen.
2. Mehrere kleine, verknüpfte Skills statt einer Wollmilchsau; Skills dürfen andere Skills nennen.
3. Alles benennen, was im Ordner liegt.
4. Für das Modell schreiben: knapp, Fachbegriffe, keine Höflichkeitsprosa; Zahlen statt Adjektive.
5. Standardformat einhalten, damit der Skill zwischen Agenten wandern kann; bei Agenten ohne Skill-Unterstützung die `SKILL.md` per Verweis in `AGENTS.md` lesen lassen (so macht es dieses Template als Rückfallebene).
