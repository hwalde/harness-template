# harness-template

[English](README.md) · **中文** · [Deutsch](README.de.md)

**一个面向编码智能体协作的项目起点。** 始终有效的规则；一个持怀疑态度、为每项工作把关的第二审阅者；一个维护项目记忆的图书管理员；为智能体分担杂务的脚本，以及一个启动"永不提问"运行的脚本。此外还有以技能（Skill）形式提供的完整文档——以及一份由你的智能体陪你逐步完成的安装指南。

> ### 🤖 要安装？交给你的智能体。
> 把模板复制到你的项目里，启动你的编码智能体（Claude Code、Codex、Gemini CLI、Cursor、opencode……）。它会读取 `AGENTS.md`，主动提议进行安装，并引导你做出那些只有你才能做的决定。如果它没有主动这样做：
> *"加载 `harness` 技能，和我一起完成 harness 的安装。"*

## 什么是 harness

除语言模型之外的一切：智能体运行所处的环境。规则文件、子智能体、技能、MCP 服务器、脚本、知识库、启动与监控机制。一个好的 harness 让智能体能够自己获取信息、自己验证工作成果——并且绝不会让一次运行卡在一个无人回答的问题上。这个模板就是这一切的基础，适用于任何项目。

## 里面有什么

```
AGENTS.md                  面向编码智能体的全部规则——所有知识都在这里
CLAUDE.md                  仅包含 "@AGENTS.md"
.claude/agents/            evaluator（验收）与 librarian（wiki）——唯一事实来源
.claude/skills/harness/    以 LLM wiki 形式组织的 harness 文档 + einrichtung.md（安装指南）
.opencode/agent/           为 opencode 生成的子智能体变体
.my-memory/                空的 LLM wiki——只能通过 librarian 访问
tools/agent-start.py       启动、连接、结束"永不提问"的运行（tmux/psmux）
tools/sync-agents.py       将子智能体定义转换为其他格式
```

**evaluator** —— 以全新上下文、无写入权限，对照规格、diff 和证据进行检查；回答 `PASS` 或 `NEEDS_WORK`。可选指定侧重点（安全、性能、整洁代码、编码规范、架构）。
**librarian** —— 通往项目记忆的唯一入口；筛选值得保留的内容（决策及其理由、坑、运维知识），拒绝噪音。
**Harness 技能** —— 十二篇简短文档：引导式设置、一个 harness 需要什么、规则文件、知识存储及其替代方案、评估者、技能、何时用 MCP 何时用脚本、面向智能体的脚本十项原则、自主运行、工作流、智能体兼容性、freilauf。

## 快速开始

1. **获取模板：** 在 GitHub 上点击"Use this template"，或克隆，或把文件复制进现有项目。
2. **在项目目录中启动你的智能体。**
3. **让它完成安装。** 安装将依次确定：语言 · 项目 · 哪些编码智能体在这里工作、各自支持什么（智能体在安装时实时调查） · 知识存储（LLM wiki 或替代方案） · MCP 服务器与访问权限（Web 应用用 Playwright，桌面应用用 computer use） · 脚本 · 自主运行、监控、安全 · 架构与编码规范 · 评估者 · 工作流。最后一切都写入 `AGENTS.md`，安装段落随之消失。

没有智能体也可以使用：`.claude/skills/harness/index.md` 对人类同样可读。

## 支持的编码智能体

Claude Code 开箱即用。opencode 的子智能体由脚本生成。其他所有智能体（Codex、Gemini CLI、Cursor、Copilot、hermes……）在安装时接入：智能体会调查各自当前支持的功能——规则文件与包含（include）、子目录规则、rules 文件、子智能体、技能、斜杠命令、项目级 MCP 配置、钩子、免提问模式——并把文件放到该智能体查找的位置。这项调查有意放在安装时而非模板中进行：这样才能保持最新。

## 语言

只有供人阅读的内容才是三语的：这三份 README（英/中/德）。harness 文件本身（`AGENTS.md`、子智能体、技能）只有一份德文版——编码智能体不受语言限制都能读懂，而且单一版本意味着没有翻译同步负担。如果你更希望它们使用你的语言：安装的第 0 步可以让你的智能体一次性完成翻译。`tools/` 中的脚本使用英文（源代码语言）。

## freilauf：上层框架

这个模板是项目*内部*的起点。[freilauf](https://github.com/hwalde/freilauf) 是项目*之上*的对应物：一个自托管的 Web 界面，按计划运行一支常备的编码智能体团队——每次运行拥有独立的 worktree 与 tmux 会话、预算闸门、外部观测、完成闸门、合并到 `main`、通知。用本模板配置好的项目无需额外改动即可在其中运行。

## 参与贡献

欢迎提交 Pull Request——改进文档与子智能体、为 `sync-agents.py` 增加目标格式、翻译。基本规则：

- 三份 README **一同**维护。
- 每个含有 `AGENTS.md` 的目录旁都有一个只包含 `@AGENTS.md` 的 `CLAUDE.md`。
- 脚本遵循 `.claude/skills/harness/skripte.md`；源代码语言为英文。
- 仓库中不得包含任何机器特定信息或密钥。

## 许可证

[CC BY 4.0](LICENSE) —— 可使用、修改、商业发布；须署名作者（**Herbert Walde**），链接至 <https://github.com/hwalde/harness-template>，链接许可证，并注明是否作了修改。
