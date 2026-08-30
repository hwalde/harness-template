---
name: harness
description: >-
  本项目 Harness 的文档与设置指南：规则文件（AGENTS.md/CLAUDE.md、子目录、rules）、
  子智能体 evaluator 和 librarian、LLM-Wiki 与知识存放、Skills、MCP 服务器
  （何时用 MCP、何时用脚本）、面向智能体的脚本、自主运行（免追问模式、tmux/psmux、
  Usage、自我监控）、工作流与评估者链、编程智能体的兼容性、freilauf。当用户就这个
  Harness 提问，想设置、扩展或改进它，或需要新建、修改某个 Harness 组件（脚本、
  子智能体、Skill、MCP 配置、规则文件）时加载。
---

# Harness 知识

本 Skill 是本项目中 Harness 的文档——按小型 LLM-Wiki 的方式组织：`index.md` 是目录，
文档平铺在旁。内容是与编程智能体打交道的经验的浓缩摘录，写给作为读者的你。

## 步骤

1. 阅读本目录中的 `index.md`，选出涉及你主题的文档。
2. **一知半解是危险的。** 设置、改造或扩展 Harness 时要读全部文档，而不只是
   `einrichtung.md`。单个问题读相关的即可。
3. **设置：**`einrichtung.md` 引导用户逐步做出各项决定；结果以简洁的句子落入
   `AGENTS.md`。最后删除 `AGENTS.md` 中的设置段落。
4. 本 Harness 的**脚本**一律按 `skripte.md` 中的原则构建——无须再问，这些原则在此
   始终有效。
5. **MCP 服务器**只按 `mcp-und-werkzeuge.md` 中的决策规则引入。
6. 对 Harness 的修改和其他工作一样要经过 evaluator，并同步更新这里受影响的文档
   （加上 `index.md`）——这样文档才始终是事实。

## 本目录中的文件

| 文件 | 内容 |
|---|---|
| `index.md` | 所有文档的目录，各附一句话描述 |
| `einrichtung.md` | 与用户一起进行的引导式 Harness 设置 |
| `grundlagen.md` | 什么是 Harness，好 Harness 的检查清单 |
| `regeldateien.md` | AGENTS.md/CLAUDE.md、子目录规则文件、rules、写作风格 |
| `agenten-kompatibilitaet.md` | 各编程智能体支持什么、文件放在哪里 |
| `wissensablage.md` | 带 librarian 的 LLM-Wiki、什么该进、替代方案 |
| `evaluatoren.md` | 评估者模式、多个/专项评估者、模板 |
| `skills-und-commands.md` | Skills、Slash Commands、规范类 Skills |
| `mcp-und-werkzeuge.md` | 何时用 MCP、何时用脚本；Playwright、cua、其他服务器 |
| `skripte.md` | 为智能体服务的脚本的十条原则 |
| `autonome-laeufe.md` | 权限模式、沙箱、tmux/psmux、Usage、自我监控、`tools/agent-start.py` |
| `workflow.md` | 标准工作流、规划层级、测试、评估者链 |
| `freilauf.md` | 让智能体运行并对其监控的上层建筑 |
