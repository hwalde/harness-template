# 基础：什么是 Harness，好的 Harness 需要什么
**核心：** LLM 之外的一切都是 Harness——智能体运行于其中的环境：规则、知识、工具、脚本、检验者、自主性组件。目标始终是同一个问题：智能体如何能自己、自主地把这件事做成？（上下文：Harness 模板 | 截至：2026-08-30）

## 概念
- 编程智能体（Coding Agent）本身已经是一个 Harness（系统提示词、工具、权限模式）。项目专属的 Harness 是围绕它构建的一切，使运行无须人工介入也有好结果：规则文件、子智能体（Subagent）、Skills、MCP 服务器、脚本、知识库、启动与监控机制。
- Harness Engineering 是与编程智能体协作的第三阶段：在「提示词工程」和「逐任务规划流程」之后，是构建赋能并检验智能体的环境——以及反向的运动：把做法在很大程度上交给它：困难的目标 + 检验标准，放手让它跑。
- Harness 永远不会「完工」。它在日常中顺带生长：每个被反复敲入的句子进入规则文件；每项算法化的手工活变成脚本；每项重复出现的检验变成一个评估者。

## 所有组件服务于同一目标
规则文件、子智能体、Skills、MCP 服务器和脚本调控的是**哪些信息和能力在何时位于上下文窗口中**——既不让模型过载也不让它欠载。两条扩展路径：自然语言（规则文件、Skills、子智能体）和算法（脚本、MCP）。所有常驻上下文的内容（子智能体、Skills、MCP 工具的描述，规则文件）在每次请求时都产生成本——「我真的想让模型时时刻刻盯着什么？」

## 检查清单：好的 Harness 需要什么（供选择，非强制清单）
| 组件 | 用途 | 在模板中 |
|---|---|---|
| 成文的需求和规则 | 核心规则（架构、工作流、坑）进 `AGENTS.md`，其余链接 | `AGENTS.md`、[regeldateien.md](regeldateien.md) |
| 评估者 | 一个智能体检验另一个智能体；定性与功能兼顾 | `evaluator`、[evaluatoren.md](evaluatoren.md) |
| 知识管理 | 最关键的一点：需求、计划、「某事怎么做」、访问权限 | librarian + `.my-memory/`、[wissensablage.md](wissensablage.md) |
| 赋能 | 智能体自己获取信息、自己测试和调试：浏览器/桌面操控、访问权限、脚本、测试 | [mcp-und-werkzeuge.md](mcp-und-werkzeuge.md)、[skripte.md](skripte.md) |
| 脚本 | 确定性的辅助工作；输出即提示词 | `tools/`、[skripte.md](skripte.md) |
| 工作未完不得停 | Goal 命令或 Loop | [autonome-laeufe.md](autonome-laeufe.md) |
| 免追问模式 + 多路复用器 | 运行永不停下，且能挺过登出 | `tools/agent-start.py` |
| Usage 追踪 | 在配额上限前停下（仅订阅制限额时） | [autonome-laeufe.md](autonome-laeufe.md) |
| 自我监控 | 发现挂起的脚本和迷路的智能体（Cron/Loop） | [autonome-laeufe.md](autonome-laeufe.md) |
| 自我改进（可选） | 智能体续写 Skills/文档——有边界 | [skills-und-commands.md](skills-und-commands.md) |
| 安全 | 用沙箱代替禁令清单 | [autonome-laeufe.md](autonome-laeufe.md) |
| 工作流 | 读文档 → 规划 → 工作 → 检验 → 更新文档/Wiki | [workflow.md](workflow.md) |
| 上层建筑 | 时间计划、Worktrees、外部监控、合并 | [freilauf.md](freilauf.md) |

最难舍弃的是自我监控：一个在被独自留下五分钟后就卡在一个问题上的智能体，浪费的是两天。评估者以最小的投入内建，收益却最大。

## 赋能：自己的红线
凡智能体自己做不了的，都需要人。因此：Web 应用配浏览器操控，桌面应用配桌面操控，访问权限（例如一个只读邮箱，用于核对确认邮件），脚本，作为自我验证的测试。并且要有意识地划一条红线——例如：没有人工批准不发邮件，没有批准不碰生产系统。

## 秩序作为架构要求
一棵清晰、按业务切分的目录树、无歧义的术语（一个概念一个词）以及脚本、文档和配置的固定位置，都是 Harness 组件：和人一样，AI 也需要结构才能快速找到信息、不遗漏任何东西——而子目录规则文件只有在按业务切分时才能奏效。

## Spec-driven 作为补充
这里描述的路径（目标 + 标准 + Harness）并不排斥规格文档：较大的项目里，一份带实现工作包和测试要求的需求文档正好提供检验标准；Harness 薄弱时，智能体至少能在那里拿到当前任务所需的访问权限和提示（[workflow.md](workflow.md)）。
