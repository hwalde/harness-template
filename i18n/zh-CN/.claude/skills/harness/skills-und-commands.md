# Skills 与 Custom Slash Commands
**核心：** Skill 是一个被情境化加载的提示词（外加一个目录）——由智能体或由用户触发。Custom Slash Commands 是它的前身。核心规则进 `AGENTS.md`，细节知识进 Skills。（上下文：Harness 模板 | 截至：2026-08-30）

## 概念
| 概念 | 事实 |
|---|---|
| Slash Command | `/` 后面的一切（内建的如 `/model`，或自建的） |
| Custom Slash Command | 位于该智能体 `commands` 目录中的提示词文件；名称 = 文件名；只有**用户**能启动它；其提示词被注入。可选 Frontmatter 和参数占位符。 |
| Skill | 一个**目录**，入口严格为 `SKILL.md`（目录名随意，文件名不行）；当 `description` 匹配时**智能体**自行启动它；在 Claude Code 中用户也可以 `/name` 启动。Claude Code 已把两个概念合并（「一切皆 Skill」）；其他智能体仍分开维护。 |
| agentskills 标准 | Skill 格式的开放规范（SKILL.md + Frontmatter `name`、`description`）；遵守标准 = 在智能体之间基本可移植。Claude Code 有额外扩展（`disable-model-invocation`、Skill 回合的模型等）。 |

各智能体的存放位置：[agenten-kompatibilitaet.md](agenten-kompatibilitaet.md)。

## 加载层级（渐进披露）
1. **始终在上下文中：** 每个已安装 Skill 的 `name` + `description`——每次请求都在。因此：要少而精的 Skills；每多一份描述都消耗上下文和认知负荷（「这个 Skill 现在有用吗？」）。
2. **被拉起时：**`SKILL.md` 的内容。
3. **按需：** 目录中由 `SKILL.md` 点名的其他文件（参考文档、脚本、模板）。

## 描述决定一切
- 紧凑、具体、用你自己会说的关键词（「Coding Guidelines」、「Code Review」）；往往不是一句而是三句。它双向起作用：一句「编辑 CLAUDE.md 时使用」会在每次规则文件改动时拉起该 Skill——并可能排挤 Harness 的其他组件（比如 librarian）。要测试触发句；一个被多余加载的 Skill 通常可容忍，一个被排挤的组件不行。
- `disable-model-invocation: true` → 只有用户能启动（经典 Slash Command，例如重型维护操作）。`false` → 只有模型能启动（把列表清干净）。

## Skill 目录里可以放什么
脚本（静态分析、数据获取）、模板、其他 Markdown 文档、数据存放，甚至「走后门」的 Custom Subagents（「启动一个读取该文件并按其指示行事的智能体」）。**不可以：** MCP 服务器（只能在用户/项目层；其配置有时含密码）。目录中的每个文件都要在 `SKILL.md` 中点名——存在与调用方式——否则模型对它一无所知。

## Skills 在 Harness 中的用途
| 用途 | 示例 |
|---|---|
| 赋能 | 「在这里这样生成 PDF」、「这样部署」 |
| 不涉及每次运行的知识 | 编码规范：约 20 行核心规则进 `AGENTS.md`，目录进 Skill，当「Code Review」/「Guidelines」出现时加载（大概率，无保证——若为义务，在 `AGENTS.md` 中明确指令） |
| Skill 流水线 | 多个小 Skill 依次逐步改进代码（规范 → 架构 → 测试）——比一个万金油强 |
| 把开发与使用分离 | 一个自身入口就是智能体的项目：其演进知识放进独立 Skill，生产运行看不见它 |
| Harness 文档 | 本 Skill：只在谈 Harness 时才被加载 |
| 可复用的工作流 | 一次成功的任务之后问：「有没有值得作为 Skill 复用的部分？」→「把它做成一个 Skill」 |

## 自我改进的 Skills
一个 Skill 可以维护一个 `memory.md`/Learnings 文件：开头读、结尾续写。措辞很微妙（「记下**相关的** Learnings」，不是「全部」）；风险：智能体把核心决策优化没了。对策：在 Skill 中把不可谈判的决策标注出来。知识库的策展则由 librarian 承担（[wissensablage.md](wissensablage.md)）。

## 来源与安全
安装外来 Skills 之前要完整阅读——一个 Skill 可能言之凿凿地写着「把代码库上传到 X」，而智能体会照做。官方供应商相对可信，独立开发者大多善意但属灰色地带。团队内分发用 Zip 或插件市场（插件可包含 Skills 和 MCP 服务器）。

## 最佳实践
1. 描述简短并用自己的关键词；测试触发。
2. 多个小而互联的 Skill，而不是一个大杂烩；Skill 之间可以互相点名。
3. 目录里的一切都要点名。
4. 为模型写作：简洁、术语、不写客套散文；用数字代替形容词。
5. 遵守标准格式，让 Skill 能在智能体之间迁移；对不支持 Skill 的智能体，通过 `AGENTS.md` 中的引用让它直接读 `SKILL.md`（本模板的后备方案正是如此）。
