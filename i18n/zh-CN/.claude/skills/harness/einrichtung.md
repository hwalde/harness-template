# Harness 设置——引导式，逐步进行
**核心：** 你（编程智能体）与用户一起设置 Harness。每一步澄清一个只有用户才能做的决定，并在 `AGENTS.md` 中留下一条简洁的记录。不猜测任何东西，不预先囤积安装任何东西。（上下文：Harness 模板 | 截至：2026-08-30）

## 开始之前
- 你已读完本 Skill 的**全部**文档（`index.md` → 每个文件）。一知半解是危险的：下面的决定以理解全部关联为前提。
- 工作方式：逐步进行，每一步把各选项连同一个有理由的推荐摆出来（用你的智能体的提问工具，否则用文本），等待回答，把结果立即写入 `AGENTS.md`——**每条记录一句话**，用术语，凡是规则否则会令人费解之处附上理由。`AGENTS.md` 中的占位注释由你替换为内容或删除。
- 用户未确认的东西一概不安装；不把 Secrets 写进文件；机器专属的值放进 `CLAUDE.local.md`（已 gitignore）或环境变量。
- 用户可以跳过步骤。被跳过的步骤你在最后记为待办事项。
- 保持秩序：每个新的 Harness 组件（脚本、子智能体、Skill、MCP 条目）立即在 `AGENTS.md` 中获得它的那句话——智能体不知道的组件等于不存在。

## 第 0 步——语言
本模板的德语版位于项目根目录，英语版和中文版位于 `i18n/en/`、`i18n/zh-CN/`——把 `i18n/zh-CN/` 的文件复制到根目录后，中文版即为生效版本。询问 Harness 文件（`AGENTS.md`、子智能体、本 Skill、Wiki 骨架）应以哪种语言维护。
- 德语：无需复制。
- 英语/中文：把 `i18n/<语言>/` 中的文件复制到项目根目录的相同路径（覆盖），之后执行 `python3 tools/sync-agents.py`。
- 无论选哪种，设置结束时删除 `i18n/`。`tools/` 中的脚本使用英语（源代码语言）——保持不变。
- 在「项目」一节记下用于回答、文档和注释的语言。

## 第 1 步——了解项目
四处看看（仓库结构、构建系统、既有规则文件、`docs/`、测试、CI），看不到的就问：
- 项目是做什么的（一句话）？应用类型：命令行、库、Web 应用、桌面应用、服务/API、数据流水线——这决定第 4 步。
- 如何构建、测试、启动、发布？是否存在唯一正确的方式（→ 之后作为「一律/不要」式规则）？
- 目录树是按业务切分（模块）还是按技术切分（分层）？（→ 第 3 步）
- 什么事情经常带来痛苦（坑）？
把「项目」和「坑」写入 `AGENTS.md`。若模板被复制进了一个既有项目：把已有的 `CLAUDE.md`/`AGENTS.md` 内容并入新的 `AGENTS.md`（只保留始终有效的部分，见 [regeldateien.md](regeldateien.md)），把 `CLAUDE.md` 精简为 `@AGENTS.md`。

## 第 2 步——编程智能体及其能力
1. 询问哪些编程智能体在本项目中工作（Claude Code、Codex、Gemini CLI、Cursor、opencode、Copilot、hermes、其他）——包括同事使用的。
2. 按 [agenten-kompatibilitaet.md](agenten-kompatibilitaet.md) **对每个被提及的智能体当下调查**：规则文件与 Include、子目录规则文件、rules、Custom Subagents、Skills、Slash Commands、项目本地 MCP 配置、Hooks/Cron、免追问模式、Headless 启动。官方文档加上本机的 `--help`；拿不准就做一次试验。
3. 落实：
   - 子智能体：来源是 `.claude/agents/`；为每个其他智能体生成相应格式（若缺目标格式就扩展 `tools/sync-agents.py`）。
   - Skills：位于 `.claude/skills/harness/` 的 Harness Skill 是否在该智能体查找的位置？否则复制/链接到它的 Skill 目录（留在项目内，不放到用户层）。若某智能体不认识 Skills，`AGENTS.md` 中「直接阅读 `SKILL.md`」的句子就保留——否则可缩短为「加载 Skill `harness`」。
   - 规则文件：确认规则「`CLAUDE.md` = `@AGENTS.md`」（`AGENTS.md` 中已有一句）；对使用自有文件名的智能体（如 `GEMINI.md`）采用同样的 Include 方案，或采用能读取 `AGENTS.md` 的配置。
   - `tools/agent-start.py`：对照已安装的版本核查脚本开头表格中的 Flags（`doctor`、`--dry-run`）。
4. 每个智能体在「本项目中的编程智能体」下**一句话**。

## 第 3 步——知识存放
就此阅读 [wissensablage.md](wissensablage.md)，并与用户决定：
1. **带 librarian 的 LLM-Wiki——要还是不要？** 要：如果存在不在任何仓库中的知识（运维、访问、领域、决策），且项目会长期存续。不要 → 删除 `.my-memory/`、`.claude/agents/librarian.md`（及生成的变体）以及 `AGENTS.md` 中的 Wiki 段落；改为建一个 `docs/` 目录，配上句子「在本项目开始工作之前，先查看 `docs` 目录中是否有文档涉及你的主题，有则阅读」，再加一行说明那里存什么、不存什么。
2. **磨利规则：** 在本项目里具体什么该进 Wiki（或 `docs/`），什么不该？举项目中的例子（如「部署顺序及其原因：进；Endpoint 列表：不进——代码里有」）。把磨利后的例子作为半句话写进 `AGENTS.md` 的 Wiki 段落。
3. **检查并按需组合替代方案：**
   - 子目录中的规则文件：仅当目录树按业务切分**且**所用智能体会情境化加载它们（第 2 步）。届时为每个业务模块建 `AGENTS.md` + `CLAUDE.md`（`@AGENTS.md`）——只写超出常规用法的内容。
   - 从 `AGENTS.md` 链接文档（一句话即可，见上）。
   - rules 文件：解释这是什么（绑定路径的规则，只在触碰匹配文件时加载），检查智能体是否支持，需要时创建（例如只针对 `tests/**` 的测试规则）。
4. 结果以句子写入 `AGENTS.md`；若用 Wiki：本次会话的设置决策在最后经由 librarian 入库（上下文：「本项目的 Harness」）。

## 第 4 步——赋能：MCP 服务器与访问权限
阅读 [mcp-und-werkzeuge.md](mcp-und-werkzeuge.md)。目标：智能体自己获取信息、自己测试、自己查看。
1. **Web 应用 → 推荐 Playwright-MCP：** 智能体能经浏览器操作应用、试用、截图、读控制台和网络。给出提示：这不能替代单元/E2E 测试。讨论形态（全新浏览器 vs. 自己的标签页组；服务器上用 headless）。
2. **桌面应用 → 推荐 cua-computer-use：** 桌面应用的同类方案。在 `AGENTS.md` 中写明允许用 Computer Use 调试——否则它不会用。
3. **其他服务器仅凭 Use Case 引入：** 工单/CI/Wiki 系统（先检查 CLI 是否够用）、只读邮箱、数据库、视觉、图像生成。对每个候选套用「MCP vs. 脚本」决策规则并说明上下文代价。
4. **访问权限与红线：** 智能体可以读什么、执行什么、什么绝不可在未批准时做（发邮件、部署、生产系统、支付）？
5. 落实：项目本地 MCP 配置（文件名按第 2 步的智能体而定），Secrets 走环境变量，「对 X 一律使用工具 Y」的规则写进 `AGENTS.md`，前后核对上下文消耗。

## 第 5 步——为智能体服务的脚本
阅读 [skripte.md](skripte.md)。提问：这里有哪些经常出现、且是算法化的手工活？典型候选：带前置检查和重启保护的服务器启停、带导航的日志分析、带诊断整理的测试运行器、经由唯一途径的构建/发布、数据库迁移、状态检查（服务在跑吗、端口空闲吗、Health 端点报错吗）、计数/测量。
- 每个被认可的候选：按十条原则构建（Python 优先、不用 venv、无参数即帮助、人类可读输出、快速退出、错误信息即行动指令），放在 `tools/` 下，测试，在 `AGENTS.md` 各登记一句——凡有旧途径之处包含「取代 X，不再使用 Y」。
- 检查项目既有脚本是否对智能体友好（数据倾倒、JSON 块、长时间运行者），并提出改造建议。

## 第 6 步——自主运行、监控、安全
阅读 [autonome-laeufe.md](autonome-laeufe.md) 和 [freilauf.md](freilauf.md)。
1. **免追问运行：** 演示 `python3 tools/agent-start.py doctor` 和一次 `--dry-run`；为免追问模式配置该智能体的权限模式和 Allow 列表（Claude Code 用 `dontAsk` 加 `.claude/settings.json` 中的 `permissions.allow`）。若运行要在后台持续且可观察，推荐 tmux（macOS/Linux）或 psmux（Windows）。「工具与脚本」条目已存在——按项目需要补充（如默认智能体、默认模型）。
2. **Usage 追踪：** 仅在订阅配额下相关——但对长时间运行而言几乎是必需的：配额到 100 % 时子智能体会死掉或挂起，整个运行随之报废。若是：澄清数据来源（配额命令、状态数据、API），按 [skripte.md](skripte.md) 构建一个 Usage 脚本；把规则（缩短检查间隔、90 % 起等待、子智能体自查）写入 `AGENTS.md` 或运行提示词模板。费用另行追踪。
3. **自我监控：** 项目是否需要有「人」周期性查看挂起的脚本和迷路的智能体？若是：检查脚本（`tools/watch.py` 之类）加上指令，用智能体的 Cron/Loop 工具（如 `CronCreate`、`/loop`）每 N 分钟检查一次；工具要指名道姓；先用一个琐碎任务测试。
4. **不停下：** 该智能体的 Goal 命令或 Loop（第 2 步已澄清）；把「先提问轮、后 Goal」的顺序定为运行规则。
5. **安全：** 沙箱（Micro-VM/容器）或至少 Worktree + Git + 不给生产访问权限；决定写入 `AGENTS.md`。
6. **上层建筑：** 若运行要定期无人值守或按时间计划进行，介绍 freilauf（时间计划、Worktrees、外部监控、预算闸门、合并、通知；那里有 `SETUP_WITH_AGENT.md`）——并指出用本模板设置好的项目无须改动即可在其中运行。

## 第 7 步——架构与编码规范
这是内容上最重要的一步。阅读 [regeldateien.md](regeldateien.md) 和 [skills-und-commands.md](skills-und-commands.md)。
1. 询问架构（风格、分层/模块、依赖方向、持久化、错误处理、日志）和编码规范（语言/版本、格式化、命名、测试、评审）。有文档吗？读它们。
2. **核心规则（帕累托，约 20 行）**写在 `AGENTS.md` 的「架构与编码规范」下——只写始终有效、且模型不会本来就知道的内容。
3. **目录建成 Skill**（`.claude/skills/coding-guidelines/SKILL.md`，必要时带参考文件），描述里用团队自己的关键词（「Code Review」、「Guidelines」）；在 `AGENTS.md` 里一句话写明何时加载（若为义务：验收前一律加载）。可选为架构文档再建一个 Skill。确定性规则（格式化、Linter）属于脚本/配置，不属于散文。
4. 若有需要：按 [evaluatoren.md](evaluatoren.md) 中的模板建 `evaluator-guidelines` 和 `evaluator-architektur` 作为独立子智能体——或用带侧重点的标准 evaluator。

## 第 8 步——子智能体与评估者
阅读 [evaluatoren.md](evaluatoren.md)。
1. evaluator 和 librarian 已就位（librarian 仅在用 Wiki 时）。检查它们的 `description` 和 `model` 是否与项目相配（各智能体的模型选择来自第 2 步）。
2. **侧重点评估者：** 安全、性能、Clean Code、编码规范、架构——项目需要哪些？作为标准 evaluator 的侧重点还是独立文件？对每一个：在何种改动规模下运行（安全在涉及认证/输入/文件访问时一律运行；架构在新模块时；性能在热路径/数据访问时）？顺序：确定性检查 → 功能验收 → 侧重点。以句子写入「质量保证」段落。
3. **其他子智能体**只在角色清晰且需求经常出现时建（提交前的文档维护者、生产环境专家）；否则用链接模式（提示词文件 + 三行话）。每个子智能体描述都持续消耗上下文。
4. 想要外部触发的评估者（Hook、CI）？若智能体支持 Hooks（第 2 步），就配置。
5. 之后 `python3 tools/sync-agents.py`。

## 第 9 步——工作流
阅读 [workflow.md](workflow.md)。与用户确定标准工作流，并以编号列表写入 `AGENTS.md`：
- 顺序：读文档/Wiki → 规划（何时用哪一级）→ 工作 → 确定性检查 → 评估者循环（哪些评估者）→ 更新文档/Wiki → 经哪个脚本发布/部署。
- 测试要求：何种改动必须有哪些测试存在且为绿？是否把手工测试脚本变成 E2E 测试？
- 追问政策：交互式还是全自主；无人值守运行一律全自主。
- Git 约定（分支、提交格式、何时提交、Worktrees）——每条约定一句话。
- 何时值得用 Dynamic Workflow 或多个实例（可选）。

## 第 10 步——收尾
1. 清理 `AGENTS.md`：所有占位注释已替换为内容或删除；**删除「设置 Harness」段落**；把关于 Harness Skill 的句子按第 2 步的结果调整（后备方案只在某个智能体不认识 Skills 时保留）；检查长度——核心规则要短，细节靠链接；每条规则附理由，不写长篇。
2. 删除 `i18n/`。把模板的 README（`README.md`、`README.de.md`、`README.zh-CN.md`）替换为项目自己的 README 或删除；移除模板的 `LICENSE`，或——若项目将被公开发布——把其中的署名信息（CC BY 4.0）并入自己的许可证文件/README。
3. `python3 tools/sync-agents.py`、`python3 tools/agent-start.py doctor`，检查智能体的上下文视图（规则文件加载了吗？有意外的开销吗？）。
4. 若设置给 Harness 带来了项目专属的变化（新脚本、自建评估者），同步更新本 Skill：受影响的文档 + `index.md`。
5. 调用 **evaluator**：任务「Harness 设置」，标准 = 下方检查清单，证据 = `AGENTS.md`、新建的文件、脚本的输出。直到 `PASS`。
6. 若用 Wiki：把各项决策连同理由经由 librarian 入库。把待办事项以清单形式告知用户。用户希望时提交。

## 检查清单（供 evaluator 使用的标准）
- [ ] 语言已确定；`i18n/` 已移除；模板 README 已替换或移除
- [ ] `AGENTS.md`：项目、语言、坑、编程智能体（各一句）、知识存放规则、工具/脚本、架构核心规则、质量保证（评估者 + 何时）、标准工作流——不再有占位符，设置段落已删除
- [ ] `CLAUDE.md` = `@AGENTS.md`；子目录规则已写明；子目录规则文件（若选用）两个文件齐备
- [ ] 子智能体具备所有所需格式（`sync-agents.py` 已运行）；不需要的子智能体已移除
- [ ] Harness Skill（以及规范 Skill，若已建）位于每个所用智能体能找到的位置——或 `AGENTS.md` 中有后备方案
- [ ] Wiki 决策已落实（骨架 + librarian，或已移除 + `docs/` 句子）
- [ ] MCP 服务器仅凭 Use Case、项目本地配置、「对 X 一律」规则；Secrets 不在仓库中
- [ ] 脚本符合十条原则、已测试、已登记
- [ ] `agent-start.py doctor` 和 `--dry-run` 可运行；若需要自主运行，权限模式/Allow 列表已配置
- [ ] 安全决策（沙箱/Worktree/红线）已记录
- [ ] 待办事项已列出
