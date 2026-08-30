# Coding-Agenten: Was sie unterstützen und wo Dateien liegen
**Kern:** Welche Harness-Bausteine ein Coding-Agent liest und wo sie liegen müssen, ändert sich laufend. Deshalb wird das bei der Einrichtung vom Agenten des Benutzers **aktuell untersucht** – die Tabelle am Ende ist nur ein datierter Orientierungs-Snapshot, keine Wahrheit. (Kontext: Harness-Template | Stand: 2026-08-30)

## Was je eingesetztem Agenten zu klären ist
| # | Frage | Warum |
|---|---|---|
| 1 | Welche **Regeldatei** liest er (`AGENTS.md`, `CLAUDE.md`, eigenes Format)? Unterstützt er `@datei`-Includes? | Ohne Regeldatei greift nichts. Kann er keine Includes, muss die Regel „CLAUDE.md = `@AGENTS.md`" für ihn nichts tun – oder er liest `AGENTS.md` direkt |
| 2 | Lädt er **Regeldateien in Unterordnern** situativ (nur wenn dort gearbeitet wird)? | entscheidet, ob modulspezifisches Wissen in Unterordner-`AGENTS.md` liegen darf ([wissensablage.md](wissensablage.md)) |
| 3 | Kennt er **rules-Dateien** mit Pfad-/Glob-Bindung? Wo, welches Frontmatter? | pfadgebundene Regeln ([regeldateien.md](regeldateien.md)) |
| 4 | Unterstützt er **Custom Subagents**? Ordner, Frontmatter-Felder (`name`, `description`, `tools`, `model`)? Liest er `.claude/agents/` mit? | evaluator und librarian müssen in seinem Format vorliegen; `tools/sync-agents.py` erzeugt Varianten |
| 5 | Unterstützt er **Skills** (SKILL.md-Standard)? Welcher Projektordner? Liest er `.claude/skills/` mit? | der Harness-Skill und Guideline-Skills müssen dort liegen, wo er sucht; sonst Rückfallebene „lies die SKILL.md" in `AGENTS.md` |
| 6 | **Custom Slash Commands / Prompts**: unterstützt, Ordner? | benutzergestartete Abläufe ([skills-und-commands.md](skills-und-commands.md)) |
| 7 | **Projektlokale MCP-Konfiguration**: Datei und Format? Lazy Loading der Tool-Beschreibungen? | MCP-Server projektweit statt pro Benutzer; Kontextkosten ([mcp-und-werkzeuge.md](mcp-und-werkzeuge.md)) |
| 8 | **Hooks** (vor/nach Werkzeugaufrufen, bei Stopp) und **Cron/Loop**-Fähigkeit? | Evaluator von außen erzwingen; Selbstüberwachung |
| 9 | **Rückfragefreier Permission-Modus** – exakte Flags? **Headless-Start** mit Prompt – exakte Syntax? | `tools/agent-start.py` (Tabelle am Skriptanfang) muss stimmen |
| 10 | Wo zeigt er seinen **Kontextverbrauch** (Memory-Dateien, Tool-Beschreibungen)? | Prüfen, ob Regeldateien geladen sind und was MCP/Subagenten kosten |

## So wird untersucht (nicht aus dem Gedächtnis)
1. **Offizielle Dokumentation** des Agenten (Web) – Abschnitte zu Konfiguration, Memory/Instructions, Subagents, Skills, Commands, MCP, Hooks, CLI-Flags. Datum/Version notieren.
2. **`<agent> --help`** und Unterbefehle auf der Maschine des Benutzers – die installierte Version ist maßgeblich, nicht die Doku.
3. **Probe:** eine Testdatei (z. B. `AGENTS.md` in einem Unterordner mit einer harmlosen, erkennbaren Anweisung) anlegen, den Agenten dort arbeiten lassen, Verhalten beobachten, Kontext-Ansicht prüfen, Testdatei wieder entfernen.
4. Für jeden Agenten **einen Satz** in `AGENTS.md` unter „Coding-Agenten in diesem Projekt" eintragen: was er unterstützt, wo die Dateien liegen, was für ihn generiert wird. Unsicheres als „(unbestätigt)" markieren.

## Regeln dieses Templates für mehrere Agenten
- Quelle der Wahrheit für Regeln: `AGENTS.md`; `CLAUDE.md` = `@AGENTS.md`. Agenten ohne Include lesen `AGENTS.md` ohnehin direkt.
- Quelle der Wahrheit für Subagenten: `.claude/agents/`. Andere Formate werden generiert (`python3 tools/sync-agents.py`, aktuell für opencode nach `.opencode/agent/`); bei weiteren Zielformaten das Skript erweitern statt Kopien von Hand zu pflegen.
- Skills liegen in `.claude/skills/<name>/` (Claude Code; von einigen Agenten mitgelesen). Für Agenten mit eigenem Skill-Ordner bei der Einrichtung kopieren oder verlinken (Symlink, wo das Betriebssystem es erlaubt) und die Rückfallebene in `AGENTS.md` behalten, falls ein Agent keine Skills kennt.
- Ein Agent lädt seine Konfiguration meist nur beim Start – nach Änderungen neu starten.
- Nur so viel Doppelstruktur wie nötig: Wird ein Agent nicht eingesetzt, wird sein Ordner nicht angelegt.

## Orientierungs-Snapshot (Stand 2026-08 – bei der Einrichtung verifizieren)
Aus dem Gedächtnis eines Modells (Wissensstand Anfang 2026) notiert, **nicht verifiziert** – als Startpunkt für die Untersuchung, nicht als Beleg. Jede Zeile wird bei der Einrichtung gegen Doku und installierte Version geprüft; „?" heißt: unklar, zuerst prüfen.

| Agent | Regeldatei | Unterordner | rules | Subagenten | Skills | Commands | MCP projektlokal | Rückfragefrei · Headless |
|---|---|---|---|---|---|---|---|---|
| Claude Code | `CLAUDE.md`, Includes mit `@datei` | ja, situativ | `.claude/rules/*.md` mit `paths:` | `.claude/agents/*.md` | `.claude/skills/<name>/SKILL.md` | `.claude/commands/*.md` | `.mcp.json` | `--permission-mode dontAsk` · `claude -p` |
| Codex CLI | `AGENTS.md`, hierarchisch | ja | ? | ? | `.agents/skills/` ? | `~/.codex/prompts/` (benutzerweit) | `.codex/config.toml` `[mcp_servers.*]` ? | `-a never -s workspace-write` · `codex exec` |
| Gemini CLI | `GEMINI.md`; `AGENTS.md` über `context.fileName`; Imports mit `@datei` | ja | ? | experimentell ? | ? | `.gemini/commands/*.toml` | `.gemini/settings.json` → `mcpServers` | `--yolo` · `gemini -p` |
| Cursor | `AGENTS.md`; liest auch `CLAUDE.md`, `.claude/skills/`, `.claude/agents/` | ja ? | `.cursor/rules/*.mdc` (globs, alwaysApply) | `.cursor/agents/` ? | `.claude/skills/` mitgelesen | `.cursor/commands/` ? | `.cursor/mcp.json` | `--force --trust` · `cursor-agent -p` |
| opencode | `AGENTS.md` (Fallback `CLAUDE.md`) | ? | ? | `.opencode/agent/*.md` | `.opencode/skill/<name>/` (liest `.claude/skills/` ?) | `.opencode/command/*.md` | `opencode.json` → `mcp` | `--auto` bzw. permission-Config · `opencode run` |
| GitHub Copilot | `AGENTS.md`; `.github/copilot-instructions.md` | ? | `.github/instructions/*.instructions.md` (`applyTo`) | `.github/agents/*.agent.md` | ? | ? | `.vscode/mcp.json` / Repo-Einstellungen | `--allow-all-tools` ? · ? |
| hermes | `~/.hermes/AGENTS.md` (global); projektlokal ? | ? | ? | ? | `~/.hermes/skills/` (benutzerweit) | ? | `~/.hermes/config.yaml` (benutzerweit) | `--yolo` · `hermes chat -q` |

Diese Tabelle veraltet von selbst – die Einrichtung verifiziert jede benötigte Zelle und trägt das Ergebnis als je einen Satz in `AGENTS.md` ein.
