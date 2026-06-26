---
type: knowledge
入库日期: 2026-06-25
置信度: 0.87
来源: [外部-微信公众号/为什么顶尖投行都选择了 Rogo 这个金融 Agent？]
主题: 为什么顶尖投行都选择了 Rogo 这个金融 Agent？
分类: 信息挖掘/微信公众号/海外独角兽
tags: [海外独角兽, AI应用, 金融Agent, 投行, 垂直AI]
---

# 为什么顶尖投行都选择了 Rogo 这个金融 Agent？

> **来源**: [外部-微信公众号/为什么顶尖投行都选择了 Rogo 这个金融 Agent？]
> **公众号**: 海外独角兽
> **原文链接**: https://mp.weixin.qq.com/s/9Ag-Ra_TDbcMxYY6DwOEHw
> **入库日期**: 2026-06-25

---

## 核心摘要

1. Rogo 是一个专为投行设计的金融 AI 工作台，由两位普林斯顿校友（前 J.P. Morgan 和 Lazard 分析师）创立，已服务超 50 家顶级金融机构（含 J.P. Morgan、Nomura、Lazard），日活用户突破 25,000 人。
2. 产品打通 Capital IQ、FactSet、PitchBook、LSEG 等核心金融数据库的 API，集成进 Excel 和 PowerPoint，每个数据点附带可溯源的原文引用——在 FinanceBench 基准中准确率比 ChatGPT 高 2.42 倍。
3. ARR 两年增长 27 倍，16 个月内完成三轮融资累计超 1.65 亿美元，估值 7.5 亿美元，背后站着 Sequoia、Thrive Capital、Khosla Ventures 及 J.P. Morgan 等战略投资者。
4. 金融机构采用 AI 面临三重门槛：零容错准确性要求、被付费墙封锁的私有数据、极难被接管的复杂内部工作流——Rogo 同时跨越这三层。
5. 竞争格局包括 Anthropic for Financial Services（Claude 4 金融能力最强）和 OpenAI for Financial Services，但 Rogo 的壁垒在于深度嵌入投行工作流（Office 插件 + Subset 智能电子表格）+ 专业金融数据集成 + 单租户安全架构。

---

## 正文

### 一、行业痛点：投行 AI 落地的三重门槛

全球投行业每年处理超 3.5 万亿美元交易，但底层引擎是大量被当作 "Excel Monkey" 的初级分析师——每周工作超 100 小时，从事高度重复性劳动（从文件中复制数据进 Excel、调整 PowerPoint 对齐、在海量电话会议记录中扒取信息）。

金融 AI 落地迟缓的根源在于三个苛刻要求：

1. **零容错准确性**：投行财务模型关乎数十亿至上百亿美元的并购定价，小数点错误即灾难性偏差。
2. **数据壁垒**：核心数据分散在 Bloomberg（年费 $2-3 万）、AlphaSense（年费 $1-2 万）等付费墙和专业数据库中，通用 AI 无法穿透。
3. **工作流复杂度**：DCF 或 LBO 模型往往由前任或多位同事共筑，充满跨表链接、个人格式和 Hardcodes，AI 尚无法接管。

### 二、Rogo 的产品体系

Rogo 的核心是一个为金融分析师重新设计的工作台：

- **研究助手**：知识库涵盖超 5,000 万份专业金融文件（SEC 备案、sell-side research、电话会议纪要），自然语言提问 + 结构化输出 + 来源引用。
- **数据集成**：与 LSEG（实时市场数据）、PitchBook（私募交易）、S&P Capital IQ、FactSet、Crunchbase 深度集成，分析师无需在多个系统间切换。
- **Office 集成**：直接嵌入 Excel 和 PowerPoint 插件，分析师无需离开工作环境即可调用 AI——不同于通用 AI 要求改变工作习惯。
- **Subset 收购（2025.9）**：AI 驱动智能电子表格，具备从财报 PDF 自动构建金融模型、执行 roll-forward 更新、跨表公式理解和错误检测的完整能力。

在技术架构上，Rogo 采用多模型并行架构（OpenAI、Google Gemini、Anthropic），根据任务复杂度智能路由——快速检索分配给轻量模型，多步推理调用旗舰模型。采用单租户部署保障数据隔离，承诺不将客户数据用于模型训练。

### 三、客户采用与增长

Rogo 的客户名单包括 J.P. Morgan、Rothschild & Co.、Jefferies、Lazard、Moelis、Nomura 等顶级投行。日活用户从 5,000（2025.6）增至 25,000+（2026.1），ARR 在首批客户后增长 27 倍。

融资节奏：2024.2 种子轮 $7M → 2024.10 A 轮 $18.5M（Khosla Ventures 领投，Eric Schmidt 等参投） → 2025.4 B 轮 $50M（Thrive Capital 领投，J.P. Morgan 加入） → 2026.1 C 轮 $75M（Sequoia 领投），估值 7.5 亿美元。

实际使用中呈现几个现象：金融行业风控极严，AI 软件只能自上而下采购；Rogo 的权威性和准确性使其在员工中形成 "Rogo 一下" 的习惯性用语；可溯源性是灵魂——每一个数据点带原文引用和链接；复杂 model 仍无法完全替代人类分析师，尤其在部门特有的成熟 workflow 中。

### 四、竞争格局

**AI Native 玩家**：
- **Hebbia**：分布式编排引擎克服 RAG 局限，矩阵视图可横向对比几十个 deal，在非标 PDF 文件推理和提取上行业领先，客户含 KKR、Oak Hill Advisors。
- **Boosted.ai**：面向对冲基金和资管的机器学习平台，覆盖选股/对冲/Agent 监控，利用 50+ 种标准实时评分股票池。

**大模型厂商**：
- **Anthropic for Financial Services**：Claude 4 在金融代理基准测试中表现最优，与高盛深度协作，发布预建 MCP 连接器（S&P、FactSet、PitchBook），NBIM（挪威主权财富基金，管理 $1.7 万亿）已有 600+ 活跃用户。
- **OpenAI for Financial Services**：雇佣 100+ 前投行员工做提示词工程，AgentKit 支持跨应用执行任务，与 Microsoft Azure/Snowflake 深度集成实现私有化部署，BBVA 已部署 4,000+ 定制 GPT。

### 五、市场空间

由 Bloomberg、S&P Capital IQ、FactSet、AlphaSense 组成的核心金融数据与研报检索市场年营收 $250-300 亿美元。但 Rogo 的野心不限于软件费，而是将极其昂贵的人力运营成本（OpEx）转化为 AI 基础设施支出。欧美资管行业从业者超 120 万人，Rogo 目前渗透率不足 2%。

Rogo 的终极愿景是 "完全自主的 AI 分析师"——了解每位用户的思维方式、偏好习性，主动发现信息、准备材料、用使用者自己的方式呈现结论。这远非今天的 Rogo 所能达到，但正是他们正在建造的方向。

