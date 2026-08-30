# 编程智能体：它们支持什么、文件放在哪里
**核心：** 一个编程智能体读取哪些 Harness 组件、这些文件必须放在哪里，是不断变化的。因此这要在设置时由用户的智能体**当下调查**——文末的表格只是一份带日期的定位快照，不是真理。（上下文：Harness 模板 | 截至：2026-08-30）

## 对每个投入使用的智能体要澄清什么
| # | 问题 | 为什么 |
|---|---|---|
| 1 | 它读哪个**规则文件**（`AGENTS.md`、`CLAUDE.md`、自有格式）？支持 `@datei` 式 Include 吗？ | 没有规则文件，一切都不生效。若不支持 Include，「CLAUDE.md = `@AGENTS.md`」这条规则对它无用——或它本来就直接读 `AGENTS.md` |
| 2 | 它会情境化加载**子目录中的规则文件**（只在那里工作时）吗？ | 决定模块专属知识是否可以放进子目录 `AGENTS.md`（[wissensablage.md](wissensablage.md)） |
| 3 | 它认识带路径/Glob 绑定的 **rules 文件**吗？在哪、什么 Frontmatter？ | 绑定路径的规则（[regeldateien.md](regeldateien.md)） |
| 4 | 它支持 **Custom Subagents** 吗？目录、Frontmatter 字段（`name`、`description`、`tools`、`model`）？它会连带读取 `.claude/agents/` 吗？ | evaluator 和 librarian 必须以它的格式存在；`tools/sync-agents.py` 生成变体 |
| 5 | 它支持 **Skills**（SKILL.md 标准）吗？项目目录是哪个？它会连带读取 `.claude/skills/` 吗？ | Harness Skill 和规范 Skills 必须放在它查找的位置；否则在 `AGENTS.md` 中用「读 SKILL.md」的后备方案 |
| 6 | **Custom Slash Commands / Prompts**：支持吗，目录？ | 用户启动的流程（[skills-und-commands.md](skills-und-commands.md)） |
| 7 | **项目本地 MCP 配置**：文件和格式？工具描述是否懒加载？ | MCP 服务器按项目而非按用户配置；上下文成本（[mcp-und-werkzeuge.md](mcp-und-werkzeuge.md)） |
| 8 | **Hooks**（工具调用前后、停止时）和 **Cron/Loop** 能力？ | 从外部强制评估者；自我监控 |
| 9 | **免追问权限模式**——精确的 Flags？**Headless 启动**并携带提示词——精确的语法？ | `tools/agent-start.py`（脚本开头的表格）必须正确 |
| 10 | 它在哪里显示**上下文消耗**（Memory 文件、工具描述）？ | 检查规则文件是否已加载、MCP/子智能体花费多少 |

## 如何调查（不凭记忆）
1. 该智能体的**官方文档**（Web）——关于配置、Memory/Instructions、Subagents、Skills、Commands、MCP、Hooks、CLI-Flags 的章节。记下日期/版本。
2. 在用户机器上运行 **`<agent> --help`** 及各子命令——以已安装的版本为准，不以文档为准。
3. **试验：** 建一个测试文件（例如放在某个子目录里、含一条无害且可辨识指令的 `AGENTS.md`），让智能体在那里工作，观察行为，检查上下文视图，再删除测试文件。
4. 对每个智能体在 `AGENTS.md` 的「本项目中的编程智能体」下写**一句话**：它支持什么、文件在哪、为它生成什么。不确定的标注为「（未确认）」。

## 本模板面向多智能体的规则
- 规则的事实来源：`AGENTS.md`；`CLAUDE.md` = `@AGENTS.md`。不支持 Include 的智能体本来就直接读 `AGENTS.md`。
- 子智能体的事实来源：`.claude/agents/`。其他格式由生成产生（`python3 tools/sync-agents.py`，目前为 opencode 生成到 `.opencode/agent/`）；有新目标格式时扩展脚本，而不是手工维护副本。
- Skills 位于 `.claude/skills/<name>/`（Claude Code；部分智能体会连带读取）。对有自有 Skill 目录的智能体，设置时复制或链接（操作系统允许之处用 Symlink），并保留 `AGENTS.md` 中的后备方案，以防某个智能体不认识 Skills。
- 智能体大多只在启动时加载其配置——修改后要重启。
- 只保留必要程度的双重结构：不投入使用的智能体，就不建它的目录。

## 定位快照（截至 2026-08——设置时核实）
出自一个模型的记忆（知识截至 2026 年初），**未经核实**——作为调查的起点，不作为依据。每一行都在设置时对照文档和已安装版本检验；「?」表示：不明，先查。

| 智能体 | 规则文件 | 子目录 | rules | 子智能体 | Skills | Commands | MCP 项目本地 | 免追问 · Headless |
|---|---|---|---|---|---|---|---|---|
| Claude Code | `CLAUDE.md`，Include 用 `@datei` | 是，情境化 | `.claude/rules/*.md` 带 `paths:` | `.claude/agents/*.md` | `.claude/skills/<name>/SKILL.md` | `.claude/commands/*.md` | `.mcp.json` | `--permission-mode dontAsk` · `claude -p` |
| Codex CLI | `AGENTS.md`，层级式 | 是 | ? | ? | `.agents/skills/` ? | `~/.codex/prompts/`（用户级） | `.codex/config.toml` `[mcp_servers.*]` ? | `-a never -s workspace-write` · `codex exec` |
| Gemini CLI | `GEMINI.md`；经 `context.fileName` 读 `AGENTS.md`；Import 用 `@datei` | 是 | ? | 实验性 ? | ? | `.gemini/commands/*.toml` | `.gemini/settings.json` → `mcpServers` | `--yolo` · `gemini -p` |
| Cursor | `AGENTS.md`；也读 `CLAUDE.md`、`.claude/skills/`、`.claude/agents/` | 是 ? | `.cursor/rules/*.mdc`（globs、alwaysApply） | `.cursor/agents/` ? | 连带读取 `.claude/skills/` | `.cursor/commands/` ? | `.cursor/mcp.json` | `--force --trust` · `cursor-agent -p` |
| opencode | `AGENTS.md`（后备 `CLAUDE.md`） | ? | ? | `.opencode/agent/*.md` | `.opencode/skill/<name>/`（读 `.claude/skills/` ?） | `.opencode/command/*.md` | `opencode.json` → `mcp` | `--auto` 或 permission 配置 · `opencode run` |
| GitHub Copilot | `AGENTS.md`；`.github/copilot-instructions.md` | ? | `.github/instructions/*.instructions.md`（`applyTo`） | `.github/agents/*.agent.md` | ? | ? | `.vscode/mcp.json` / 仓库设置 | `--allow-all-tools` ? · ? |
| hermes | `~/.hermes/AGENTS.md`（全局）；项目本地 ? | ? | ? | ? | `~/.hermes/skills/`（用户级） | ? | `~/.hermes/config.yaml`（用户级） | `--yolo` · `hermes chat -q` |

这张表会自行过时——设置过程会核实每个需要的单元格，并把结果以每条一句话写进 `AGENTS.md`。
