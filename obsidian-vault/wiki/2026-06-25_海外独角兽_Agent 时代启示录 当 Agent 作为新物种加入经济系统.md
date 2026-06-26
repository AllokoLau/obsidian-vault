---
type: knowledge
入库日期: 2026-06-25
置信度: 0.85
来源: [外部-微信公众号/Agent 时代启示录: 当 Agent 作为新物种加入经济系统]
主题: Agent 时代启示录: 当 Agent 作为新物种加入经济系统
分类: 信息挖掘/微信公众号/海外独角兽
tags: [海外独角兽, Agent经济, ToAgent, 商业模式, Harness]
---

# Agent 时代启示录: 当 Agent 作为新物种加入经济系统

> **来源**: [外部-微信公众号/Agent 时代启示录: 当 Agent 作为新物种加入经济系统]
> **公众号**: 海外独角兽
> **原文链接**: https://mp.weixin.qq.com/s/9R4CknPNtq3-TsBf94tk8A
> **入库日期**: 2026-06-25

---

## 核心摘要

1. Agent 时代的关键市场坐标不再是 To B / To C，而是 To Human / To Agent。Agent 作为新物种加入经济系统，同时成为生产者和消费者，形成了一个前所未有的双边市场。
2. 传统互联网估值指标（DAU/MAU）在 Agent 时代失效。Anthropic Claude 产品 DAU 只有 ChatGPT 的 2%，但两家 ARR 已追平，因为价值集中在头部高价值任务而非用户规模。
3. 软件形态正在经历系统性格式迁移——从为人类设计的 GUI 转向为 Agent 设计的底层接口（CLI、API、语义数据层）。Claude Code 选择 CLI 而非 IDE 是这一趋势的早期信号。
4. 商业模式从 per-seat 转向 per-outcome，收费锚点从 IT 预算转向人力成本预算（美国白领工资约 6 万亿美元，全球约 18-20 万亿美元），市场规模扩大 1-2 个数量级。
5. Agent = Model + Harness，Anthropic 率先发布 Managed Agents beta，将 Harness 产品化，战略意义在于形成类似 AWS 云平台的锁定效应。

---

## 正文

### 旧尺度的失效

互联网时代的分析维度在 Agent 时代失去解释力。Anthropic 在 2025 年底年化收入约 90 亿美元，2026 年 2 月冲到 190 亿，3 月达到 300 亿，同比增长约 1400%。Claude 用户规模不到 ChatGPT 的 1%，但这 1% 是 token 消耗最密集、任务价值最高的用户。高 ARR 和低 DAU 可以同时成立，因为价值集中在头部任务，不在用户规模。

付费逻辑正在从 per-seat 走向 per-outcome。Decagon 的 per-resolution 模式只在 AI 真正解决问题时才收费；Sierra 直接把 "pay for a job well done" 写进产品 pitch。传统 SaaS 跟着企业 IT 预算走，AI-native vertical agent 瞄准的是人力成本池。IT 预算和人力成本预算的差距是 1-2 个数量级。

To B / To C 的边界已经模糊到无法分类。过去 2 年内增长最快的 AI 产品（Claude Code、Cursor、Perplexity、Manus）几乎都是 Prosumer 先自发采用，再 bottom-up 渗透到组织。工程师愿意用个人信用卡买 Claude Code 做公司项目，这已跨越了 C 和 B 的界限。

### 软件正在被重写

软件从设计之初是 To Human 的，GUI 中的每一层抽象都是为了降低人类操作的认知负担，而 Agent 不需要这些。一场系统性的格式迁移正在发生：从为人类设计的可视化界面转向为 Agent 设计的底层接口。

Claude Code 选择 CLI 而不是 IDE 的决策是这一趋势的早期信号。如果模型能力持续变强，最终的产品形态应该是更简洁、更接近底层的终端。CLI 就是 Agent 的母语。未来的软件大概率不再是一个有完整界面的应用，而是 Model + Agent Harness + 按需生成的人类审阅层。下一代 Salesforce 不再是给销售用的 CRM，而是一个 Agent 可以直接读写的客户数据语义层。

### 旧范式的漫长熊市

每一次技术平台迁移，都是新范式原生生长的公司赢，旧范式渐进迁移的公司输。雅虎不是不知道搜索重要，是它的编辑导航逻辑和 Google 的爬虫算法在产品 DNA 层面互斥。在 Agent 时代，OpenAI 的 8 亿用户可能是战略包袱而非资产——每一个面向轻度对话用户的优化，都是对 Agent 深水区的一次妥协。Anthropic 没有这个包袱，所以可以把 Claude Code 做成纯 CLI、纯 Agent-native。

### To Agent：新物种加入经济系统

Agent 作为新物种加入经济系统。To Human 的定义是服务有具体目标、具体任务的人；To Agent 的定义是 Agent 本身成为生产者和消费者——自主搜索、调用 API、开启 runtime、做采购决策、完成支付。

生产侧先发生且已发生。Anthropic 在 2026 年 2-3 月的 52 天发布了 70 多个产品 features，很多是 Agent 写、Agent 测试、Agent 部署的。边际生产成本将无限降低，一家 100 人公司的产出可以对标过去 1000 人公司的体量。

消费侧是生产侧的自然延伸。Stripe 和 Tempo 联合发布 Machine Payments Protocol，Cloudflare 在 Bot Management 中新增 AI bot 分类。Agent 写的 feature 被另一个 Agent 调用，Agent 生成的数据被另一个 Agent 消费，Agent 做的采购决策由另一个 Agent 的 API 承接——这在人类经济史上从未出现过。

### Agent = Model + Harness

Agent Harness 代表了 Agent 中除了模型之外的所有组件。Anthropic 发布 Managed Agents beta，Harness 第一次被产品化，商业模式的战略意义大于技术意义——Agent 的商业模式开始从 token 定价转向 AWS 云平台模式。

一个反直觉的事实：2026 年最好的 Harness 比 2023 年的 LangChain 薄得多。Opus 4.5 越过 Agentic 能力拐点后，越薄的 Harness 反而越强。Claude Code 核心的 Agent Loop 本身只有几十行代码，配套工程（上下文压缩、Multi-Agent 协调、工具调用）才是真正厚度。

### 看好方向

1. **Runtime 层**：Agent Infra，让 Agent 跑得更 scalable、更自由。当前 sandbox/虚拟机还是为人类设计的，Agent 需要 per-agent 状态隔离、Fork/Snapshot、Durable Execution。
2. **Context 层**：Vertical Harness，在垂直领域把行业 know-how 做到极致。Healthcare、legal、finance 三个人力成本最高的领域最先发生。
3. **Orchestration 层**：将 Agent 当作一等公民的基础设施，包括 Agent Identity 和 Agent Payment。
