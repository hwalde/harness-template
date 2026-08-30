# Harness 知识 – 索引
本 Skill 文档的目录。每个文件一句话：讲什么、涉及哪些主题（截至：2026-08-30）。设置、改造或扩展 Harness 时全部阅读；单个问题读相关的即可。

- [einrichtung.md](einrichtung.md) – 十一个步骤（0–10）的引导式设置：语言、项目、编程智能体与特性调查、知识存放（Wiki 或替代方案）、MCP/访问权限、脚本、自主运行/监控/安全、架构与规范、子智能体/评估者、工作流、以检查清单收尾。
- [grundlagen.md](grundlagen.md) – 什么是 Harness（LLM 之外的一切）、为什么所有组件都在调控上下文、好 Harness 的检查清单、赋能与红线、秩序作为架构要求。
- [regeldateien.md](regeldateien.md) – AGENTS.md/CLAUDE.md（`@AGENTS.md`）、四个位置、什么该进什么不该进（帕累托、坑）、外移与链接、子目录规则文件、rules 文件、写给 AI 的写作风格、反模式。
- [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md) – 设置时每个编程智能体要当下调查的十个问题（规则文件、子目录、rules、子智能体、Skills、Commands、MCP 配置、Hooks、免追问模式、Headless）、如何调查、多智能体规则、带日期的定位快照。
- [wissensablage.md](wissensablage.md) – 向智能体供给知识的途径、什么该进知识库什么不该、带 librarian 的 LLM-Wiki（结构、Context Scoping、策展）、替代方案（子目录 AGENTS.md、docs 目录、rules、Skills）及决策辅助。
- [evaluatoren.md](evaluatoren.md) – 生成者→评估者模式（子智能体 + 验收义务）、调用方要提供什么、局限与欺骗、多个与专项评估者（安全、性能、Clean Code、规范、架构）及顺序和模板、其他子智能体类型。
- [skills-und-commands.md](skills-und-commands.md) – Skills 与 Custom Slash Commands 之别、加载层级、作为触发器的描述、Skill 目录里可以放什么、规范类 Skills 与 Skill 流水线、自我改进的 Skills、来源审查、最佳实践。
- [mcp-und-werkzeuge.md](mcp-und-werkzeuge.md) – MCP 是什么、代价几何，MCP 服务器 vs. CLI/脚本的决策规则、「提供不等于使用」、按应用类型的赋能（Playwright、cua-computer-use、只读邮箱、其他服务器）、坑。
- [skripte.md](skripte.md) – 为什么要脚本、「CLI 工具是对一个人的函数调用」的指导思想、本 Harness 脚本的十条强制原则、建成后的 AGENTS.md 条目、典型 Harness 脚本、坑。
- [autonome-laeufe.md](autonome-laeufe.md) – 组件、权限模式（dontAsk）、沙箱、启动流程（目标层级、检查清单、Goal 前的提问轮）、Goal/Loop、Usage 追踪、经 Cron 的自我监控、边界与中止条件、不打扰的调控、`tools/agent-start.py`。
- [workflow.md](workflow.md) – AGENTS.md 的标准工作流、规划层级 1–3 及其对极「目标 + 检验标准」、工作流中的测试、任务的表述（信而非提示词、XML 隔离、控制性提问）、追问政策、Dynamic Workflows 与评估者链。
- [freilauf.md](freilauf.md) – 本模板之上的上层建筑：时间计划、Worktrees、外部监控、预算闸门、合并、报告、通知；何时值得以及它与模板如何协作。
