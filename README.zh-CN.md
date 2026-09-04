# harness ——为你的编码智能体构建 harness 的技能

[English](README.md) · **中文** · [Deutsch](README.de.md)

**让编码智能体在企业 IT 项目中自主且安全地工作。** 这个技能会为任何项目构建一套完整的 harness：始终生效的规则、一个对每项工作签字把关的、持怀疑态度的第二审阅者、一个维护项目记忆的图书管理员、替智能体分担杂务的脚本，以及一个用于"永不提问"运行的启动脚本。你的智能体负责安装它、构建它、陪你完成设置，并让它保持更新。

> ### 🤖 一行命令即可开始
> ```bash
> git clone https://github.com/hwalde/harness-skill ~/.claude/skills/harness
> ```
> 然后，在你的项目中告诉你的编码智能体：*"加载 `harness` 技能，和我一起为这个项目构建 harness。"*（其他智能体：克隆到它们各自的技能目录——技能会告诉智能体具体位置。）

## 为什么需要 harness

harness 是除语言模型之外的一切：智能体运行所处的环境。规则文件、子智能体、技能、MCP 服务器、脚本、知识库、启动与监控机制。没有它，智能体只能从空白上下文开始工作，自己给自己的工作打分，忘记上一次会话学到的东西，并在第一个无人回答的问题处止步不前。有了它：

- **每项结果都由第二双眼睛检查。** `evaluator` 子智能体在全新的上下文中读取规格、diff 和证据，没有写入权限，并回答 `PASS` 或 `NEEDS_WORK`。构建者永远不能自行验收自己的工作。
- **知识能跨会话留存。** `librarian` 是通往仓库中 LLM wiki 的唯一入口：决策及其理由、踩过的坑、运维知识——经过筛选，让上下文保持精简。
- **运行永不卡死。** 面向"永不提问"运行的权限模式、按智能体和操作系统命名的启动与接入脚本（`claude-background-start`、`claude-attach`），用于在 tmux/psmux 会话中执行长时间任务、用量追踪、自我监控，以及"先问一轮问题，再定目标"的规则。
- **红线被明确写下。** 智能体可以读取什么、可以执行什么、未经批准绝不能碰什么——都写在 `AGENTS.md` 中，背后的决策理由写在 `HARNESS.md` 中——这样企业项目中的无人值守运行始终留在你设定的走廊之内。
- **适配每一种编码智能体。** Claude Code 开箱即用；opencode 由脚本生成；Codex、Gemini CLI、Cursor、Copilot、hermes 在安装时接入——届时智能体会调查它们各自当前支持什么。

## 这个技能会为你的项目构建什么

```
AGENTS.md                面向编码智能体的全部规则——项目事实、wiki 规则、QA、工作流程
CLAUDE.md                只包含 "@AGENTS.md"
HARNESS.md               这个 harness 的状态：技能版本、使用中的智能体、决策、待办事项
.claude/agents/          evaluator（签字验收）与 librarian（wiki）——唯一事实来源
.claude/settings.json    面向"永不提问"运行的最小允许列表，以及用于 bootstrap 的 SessionStart 钩子
.my-memory/              空的 LLM wiki——只能通过 librarian 访问
tools/agent-start.py     启动、接入并结束"永不提问"的运行（tmux/psmux）
tools/bootstrap.py       重新建立那些无法随克隆保留下来的本地设置
tools/sync-agents.py     将子智能体定义转换为其他智能体的格式
```

随后，引导式安装会依次确定：仓库 · 语言 · 项目与目录结构 · 哪些编码智能体在这里工作、各自支持什么 · 知识存储 · MCP 服务器与访问权限（Web 应用用 Playwright，桌面应用用 computer use）· 脚本 · 自主运行、监控、安全 · 架构与编码规范 · 评估者 · 工作流程。最终一切都写入 `AGENTS.md`，理由写入 `HARNESS.md`。

## 技能内部有什么

```
SKILL.md                 操作流程：构建、提问、构建模块、审阅、更新、freilauf、改进
references/              十二篇文档——一个 harness 需要什么、规则文件、知识存储、
                         评估者、技能、MCP 与脚本的取舍、面向智能体的脚本十项原则、
                         自主运行、工作流程、智能体兼容性、freilauf、安装指南
assets/project/          项目会收到的一切内容，均位于其目标路径
scripts/build.py         依照模板构建（或检查）项目——具有幂等性，绝不覆盖
scripts/make-start-scripts.py
                         按智能体和操作系统命名的启动/接入脚本，供不使用 freilauf 的项目使用
CHANGELOG.md             各版本的变更内容，以及已构建项目需要手动处理的事项
```

由于这个技能本身就是一次 git clone，`git pull` 即可更新它，技能的路线 E 会把变更逐个文件地带入你的项目——你记录下来的偏差会被保留。这些文档对人类同样可读：从 `references/index.md` 开始。

## freilauf：上层框架

harness 是项目*内部*的起点。[freilauf](https://github.com/hwalde/freilauf) 是它在项目*之上*的对应物：一个自托管的 Web 界面，按计划运行一支常备的编码智能体团队——每次运行拥有独立的 git worktree 与 tmux 会话、预算闸门、来自外部的观测、一个在相信智能体的说法之前先核实它的完成闸门、与 `main` 的集成、通知，以及用于定义运行结束后要做什么的无代码 flow。配置好这个 harness 的项目无需任何额外改动即可在其中运行。如果你需要，这个技能会为你安装并接通 freilauf（目前仅支持 Linux）。

## 关于作者

我是 Herbert Walde。我从 1999 年起从事软件开发，并已指导超过 200 名开发者用 AI 大幅提升生产力——这个技能就是实践中真正有效的方法的提炼。我面向全球企业提供培训，语言为德语和英语：<https://entwickler-training.de>。

## 参与贡献

欢迎提交 Pull Request——改进文档与子智能体、为 `sync-agents.py` 增加更多目标格式、翻译。基本规则如下（理由见 `SKILL.md` 的路线 G）：

- 三份 README **一同**维护。
- 其余一切内容均为英文。模板位于 `assets/project/` 中的目标路径下；`CLAUDE.md` 是生成出来的，不作为文件存储。
- 每次变更都要在 `CHANGELOG.md` 中记录一条，并在 `SKILL.md` 中提升版本号。
- 脚本遵循 `references/scripts.md`。仓库中不得包含任何机器特定信息或密钥。

## 许可证

[CC BY 4.0](LICENSE) ——可以使用、修改、并用于商业发布；须署名作者（**Herbert Walde**），链接至 <https://github.com/hwalde/harness-skill>，附上许可证链接，并注明是否作了修改。
