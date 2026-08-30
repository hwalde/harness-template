# Wissensablage: LLM-Wiki, Alternativen, Regeln
**Kern:** Arbeit mit Coding-Agenten ist zum großen Teil Wissensmanagement. In den Speicher gehört nur, was nicht im Quelltext steht; jede Information gehört zu genau einem Kontext; wer einen Speicher betreibt, kauft eine Pflegepflicht. (Kontext: Harness-Template | Stand: 2026-08-30)

## Sechs Wege, einem Agenten Wissen zu geben (beliebig mischbar)
| Weg | Beschreibung | Wann |
|---|---|---|
| 1. Dokumente von `AGENTS.md` aus verlinken | „Bevor du mit Arbeit in diesem Projekt beginnst, schau in den `docs`-Ordner, ob ein Dokument dein Thema berührt, und lies es dann." Gegenrichtung: Neu Erarbeitetes dort ablegen – mit Anweisung, was speicherwürdig ist und was nicht | kleine bis mittlere Projekte, wenige Dokumente, Team pflegt Docs ohnehin |
| 2. Regeldateien in Unterordnern | modulspezifisches Wissen liegt beim Modul und wird situativ geladen | fachlich geschnittener Ordnerbaum + Agent, der das unterstützt ([regeldateien.md](regeldateien.md)) |
| 3. rules-Dateien | pfadgebundene Regeln (nur für `tests/**`, nur für `src/ui/**`) | Agent unterstützt rules; Regeln hängen an Dateitypen/Bereichen |
| 4. Skills | Wissen wird erst geladen, wenn es gebraucht wird | Guideline-Kataloge, Weiterentwicklungswissen, Anleitungen ([skills-und-commands.md](skills-und-commands.md)) |
| 5. LLM-Wiki mit librarian | strukturierter Speicher mit einem Subagenten als einzigem Zugang | Wissen über viele Systeme/Repos hinweg, Entscheidungen samt Begründung, Betriebswissen, Domänenwissen; langlebige Projekte |
| 6. MCP-Server / Skripte als Wissensquelle | Confluence-MCP, Skript, das Doku liefert | wenn die Quelle außerhalb liegt; Confluence-Inhalte sind für Menschen geschrieben und oft eine Müllhalde – Agenten scheitern daran genauso |

Voraussetzung für alle: **Das Modell muss davon erfahren** – ein Satz in `AGENTS.md`. Kein RAG/Embedding-Chunking: Auffindbarkeit über Ordnerbaum + Indexdateien funktioniert besser.

## Was in einen Wissensspeicher gehört – und was nicht
**Rein:**
- Wissen, das **nicht aus den Quelldateien ersichtlich** ist: Entscheidungen samt Begründung (das Warum), Fallstricke, die man dem Code nicht ansieht, Betriebs-/Zugangs-/Infrastrukturwissen, Domänen- und Geschäftswissen, Konventionen, Zeiger auf die Quelle der Wahrheit.
- Eigenes Expertenwissen in Bereichen, in denen Modelle noch dünn sind.

**Raus:**
- Was ohnehin im Quelltext steht: „Wer aufschreibt, was im Quelltext steht, hat zwei Wahrheiten – und die gehen auseinander." Codebase-ableitbares Detail (Inventare, Feldlisten, Endpoint-Kataloge, Zählstände) driftet und wird falsch → höchstens ein Zeiger.
- Was das Modell ohnehin weiß.
- Transientes Laufzeit-Wissen: eine gerade beantwortete Nachfrage, Fortschritts-/Statusnotizen, Log-Ausgaben, Zwischenstände, Triviales.
- Secrets – nur der Verweis, wo sie liegen.

Leitfrage: **„Braucht eine zukünftige Session das?"** Im Zweifel nicht einlagern. Je klüger das Modell, desto weniger Wissensdokumente braucht es; bei kleinen/lokalen Modellen sind sie umso wertvoller.

## Das LLM-Wiki (Karpathy-Muster) in diesem Template
```
.my-memory/
├── raw/    unveränderliche Originale (append-only)
└── wiki/   verdichtete, querverlinkte Seiten; index.md je Ordner (ein Satz je Eintrag); log.md
```
- Navigation top-down: immer zuerst die `index.md`, dann gezielt weiter; Querverweise wie in einer Enzyklopädie. Zwei Qualitätsregeln: Index-Beschreibungen knapp und präzise (Wegweiser, kein Changelog); nichts, was das Modell ohnehin kennt.
- **librarian** (`.claude/agents/librarian.md`) ist das einzige Tor: Er holt Wissen (ABFRAGE) und lagert es ein (EINLAGERUNG), filtert als Gatekeeper (Library- vs. Laufzeit-Wissen), erzwingt Context Scoping und liefert nur die Essenz zurück – der Hauptagent liest keine Wiki-Dateien und muss nicht überlegen, was wohin gehört. Zwei Haltungsregeln: Er argumentiert nie gegen Entscheidungen, und er kennzeichnet altes Wissen als möglicherweise überholt.
- Regeln in `AGENTS.md` (kompakt, begründet): zu Arbeitsbeginn fragen, bevor der Benutzer gefragt wird; am Ende Bleibendes einlagern; nie direkt in `.my-memory/` lesen oder schreiben. Ignoriert der Agent den librarian, die Regel vom Modell selbst neu formulieren lassen – kompakt, begründet, ohne gegen den Systemprompt zu argumentieren.
- **Context Scoping:** Jede Information gehört zu einem Kontext (Projekt, Teilsystem, Zielgruppe, Kunde, Werkzeug) – als Ordner-Teilbaum abgebildet; sonst verknüpft der Agent Unzusammenhängendes.
- **Kuratierung** (Dauerpflicht): Wissen veraltet und arbeitet dann gegen einen. Periodisch, bewusst angestoßen (Modus WARTUNG, bei großen Wikis ein eigener Kuratierungs-Skill): Redundanz zusammenführen, driftendes Detail in Zeiger umwandeln, Überholtes markieren, Index-Beschreibungen glattziehen, tote Links entfernen. Nie nebenbei, nie ohne Freigabe für Löschungen.
- Bilanz aus der Praxis: projektübergreifend (Verbund mehrerer Repos/Systeme) sehr bewährt; bei einem einzelnen, stark codezentrierten Projekt kann ein `docs`-Ordner reichen.

## Entscheidungshilfe bei der Einrichtung
| Frage | Ja → | Nein → |
|---|---|---|
| Gibt es Wissen, das in keinem Repo steht (Betrieb, Zugänge, Domäne, Entscheidungen), und lebt das Projekt länger als ein paar Wochen? | LLM-Wiki mit librarian | `docs`-Ordner + Verlinkung aus `AGENTS.md` |
| Ist der Ordnerbaum fachlich geschnitten und lädt der Agent Unterordner-Regeldateien? | modulspezifisches Wissen in Unterordner-`AGENTS.md` | in `docs/` oder Wiki |
| Hängen Regeln an Dateitypen/Bereichen und unterstützt der Agent rules? | rules-Dateien | Unterordner-Regeldatei oder `AGENTS.md`-Abschnitt |
| Gibt es einen großen Guideline-/Anleitungskatalog? | Skill | kurzer Abschnitt in `AGENTS.md` |

Wird das Wiki nicht genutzt: `.my-memory/`, den librarian und die Wiki-Regeln in `AGENTS.md` entfernen (halbe Installationen verwirren den Agenten mehr, als sie helfen).
