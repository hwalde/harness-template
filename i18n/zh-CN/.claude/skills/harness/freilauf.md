# freilauf：让智能体运行并对其监控
**核心：** 本模板是项目启动器（存放在仓库里的东西）。freilauf 是其上的上层建筑：一个自托管的 Web 界面，让一支常备的编程智能体队伍按时间计划运行，并从外部对其监控。（上下文：Harness 模板 | 截至：2026-08-30 | 来源：https://github.com/hwalde/freilauf）

## freilauf 做什么
- **无人值守的运行：** 每次运行获得自己的 Git-Worktree 和自己的 tmux 会话；运行互不干扰，随时可以附着上去读取整个屏幕。
- **时间计划：**「每晚两点看一遍开放的 Issues。」一个 *Agent* 是一份保存的运行定义（编程智能体、模型、推理力度、提示词、仓库、分支规则）加名称和时间计划；一个*单次运行*是同样的东西但没有时间计划。
- **外部观察：** tmux 状态、日志、对话记录、Hooks、Provider 脉搏——即使智能体自己已经无法上报，Rate-Limits 和故障也会被发现。
- **「完成」意味着上了 `main`：** 可选由 Hub 亲自合并，在相信之前先核验智能体的断言（Finish Gate），并把还活着的智能体打发回去补齐缺漏。
- **预算闸门：** 订阅配额或余额吃紧时，计划中的启动会等待。
- 智能体的**报告**（`cc-report done|failed|help|progress|branch|pr`）、**Telegram 通知**、**No-Code-Flows**（一次运行之后发生什么：后续运行、给运行中智能体的消息、从报告中提取、分支判断）。
- **编程智能体和模型 Provider 皆为插件：** Claude Code、opencode、hermes、cursor-agent 等；更多经插件包接入。界面有英语、德语和中文。
- 内含启动/附着脚本（`cc-start`、`cc-attach`、`cc-kill`、`cc-report`），本模板中的 `tools/agent-start.py` 就是它们的项目本地精简版。

## 何时值得
- 一旦运行要定期**无人值守**或**按时间计划**进行（夜间运行、周期性维护、Issue 消化）。
- 一旦多个智能体或多个仓库并行运行，而你想知道什么时候出了岔子——又不想自己一直盯着。
- 一旦一次运行的结果要可靠地落在主分支上，且合并前要有核验。

## 与本模板的协作
| 层面 | 负责者 |
|---|---|
| 仓库内：规则（`AGENTS.md`）、子智能体（evaluator、librarian）、Skills、脚本、Wiki | 本模板 |
| 仓库之上：按时间计划启动、Worktrees、监控、预算、合并、通知 | freilauf |

用本模板设置好的项目无须进一步改动即可在 freilauf 中运行：规则和子智能体在每次运行中生效，evaluator 的 PASS 是 Finish Gate 的天然搭档。注意 freilauf 的安全模型（VPN 作为接入层；Hub 操控 tmux，那就是 Shell 访问）。

设置：freilauf 仓库中的 `README` 和 `SETUP_WITH_AGENT.md`——后者是写给编程智能体的（「读 SETUP_WITH_AGENT.md，给我把它设置好」）。
