---
type: knowledge
入库日期: 2026-06-25
置信度: 0.85
来源: [外部-微信公众号/Harness is the New Dataset：模型智能提升的下一个关键方向]
主题: Harness is the New Dataset：模型智能提升的下一个关键方向
分类: 信息挖掘/微信公众号/海外独角兽
tags: [海外独角兽, HarnessEngineering, Agent系统, 模型训练, Context管理]
---

# Harness is the New Dataset：模型智能提升的下一个关键方向

> **来源**: [外部-微信公众号/Harness is the New Dataset：模型智能提升的下一个关键方向]
> **公众号**: 海外独角兽
> **原文链接**: https://mp.weixin.qq.com/s/9qI83Ne-Ac_R9y-yJ6SVnQ
> **入库日期**: 2026-06-25

---

## 核心摘要

1. AI 工程方法经历了三次演进：Prompt engineering（2022-2024）→ Context engineering（2025）→ Harness engineering（2026）。现在真正决定 Agent 上限的不是模型本身，而是围绕模型搭建的整套系统。
2. Harness 的 6 个关键组件：记忆与上下文管理、工具与技能、编排与协调、基础设施与保障、评估与验证、追踪与观测，可归为信息层、执行层、反馈层。
3. 核心原则包括：渐进式披露（分层加载信息）、工具越少越精、Context window 利用率控制在 60% 以下、利用 subagent 做 context 隔离、将研究/计划/执行/验证分开。
4. Deepmind 的 Philipp Schmid 提出 "The Harness is the Dataset"——真正的竞争优势在于 harness 能捕获到怎样的执行轨迹。Harness 本身已成为模型训练的数据土壤。
5. 模型和 Harness 正在被同步优化（训练即部署），许多原本属于 Harness 的能力正在被模型内生化，形成循环迭代。

---

## 正文

### 从 Prompt 到 Harness 的三次演进

AI 工程方法已经历三次演进：
- **Prompt engineering（2022-2024）**：关注如何表达需求，打磨单次对话指令。
- **Context engineering（2025）**：关注如何提供恰到好处的信息，在有限 context window 下让 AI 了解背景资料。
- **Harness engineering（2026）**：关注如何"构建系统"——模型周围的运行环境、工具调用、记忆系统、评估与回滚机制等。

Agent = LLM + Harness。模型决定了"要做什么"，Harness 决定了"能看到什么、能用什么工具、失败时该怎么办"。

Claude Opus 4.5（2025 年 11 月）的发布被视为标志性事件——模型的 agentic 能力到了一个 tipping point，"用好模型的能力"开始比"提高模型的能力"更加重要。智力本身不再是瓶颈，瓶颈转移到了系统层。

### Harness 的 6 个关键组件

1. **Memory & Context management**：解决"在当前时刻，Agent 应该看到什么信息"。
2. **Tools & Skills**：扩展 Agent 的行动能力。
3. **Orchestration & Coordination**：编排任务流程，协调分工。
4. **Infra & Guardrails**：运行环境和边界条件。
5. **Evaluation & Verification**：验证闭环，让 Agent 自行验证并修正。
6. **Tracing & Observability**：还原行为过程，使系统可调试、可管理。

这 6 个组件可归为 3 层：信息层、执行层、反馈层。

### Harness 的设计原则

**信息层**：
- **渐进式披露**：把信息做成"分层加载"系统，通过文件系统做三级分层（CLAUDE.md → SKILL.md → reference files）。
- **工具越少越精**：Agent 的强大不在于工具箱有多少把扳手，而在于是否拥有几把"万能扳手"。Claude Code 目前约 20 个工具，团队仍在审视精简。
- **Context window 甜蜜区间**：当上下文利用率超过一定区间后性能开始下降。注意力具有"稀疏性"，顶级工程师频繁进行上下文压缩，控制利用率在 60% 以下。
- **Subagent 做 Context 隔离**：主 agent 负责调度和收口，子任务分配给独立 subagent。

**执行层**：
- **研究/计划/执行/验证分开**：每个阶段是单独的 session，有单独的 context。
- **人最该介入事前规划**：人的精力应从事后 code review 前移到 research 和 plan 环节。

**反馈层**：
- **构建反馈闭环**：Mitchell Hashimoto 的工程纪律——每一次失败都是让系统永久变好的机会。
- **Harness 即数据**：每次失败被记录到 AGENTS.md，让 agent 不再犯同样错误。
- Boris Cherny 的数据：提供有效验证手段后，Claude 最终产出质量可提升 2-3 倍。

### 模型 vs Harness 的关系

**训练即部署**：Agentic RL 的训练效果在很大程度上取决于"训练场设计得好不好"。模型在训练时看到什么，就是上线后要面对什么。Cursor 训练 Composer 1.5 时并发跑数十万个沙盒，模型自发涌现了搜索、修 linter、补测试等能力。

**Harness 即数据**：真正有价值的数据不再只是静态语料，还包括 agent 在执行流程中跑出来的执行轨迹。Harness 不再是模型外面的脚手架，而是模型能力生成的土壤。

**竞争格局**：头部的模型公司在端到端做 harness，而应用公司也越来越多开始训模型。在很多垂直场景，开源模型能力已够用，接下来的差距来自于谁能在特定场景把模型、任务结构、反馈闭环和后训练结合得更好。

### 创业公司机会

- **信息层**：Edra（Context for Agents at Scale，3000 万美元 A 轮，Sequoia 领投）
- **执行层**：Temporal（Durable Execution，3 亿美元 D 轮，估值 50 亿美元）；Oasis Security（Agent 权限管理，1.2 亿美元 B 轮）；Daytona（Agent 沙箱，2400 万美元 A 轮）
- **反馈层**：Braintrust（AI Observability/Evaluation，8000 万美元 B 轮，估值 8 亿美元）
