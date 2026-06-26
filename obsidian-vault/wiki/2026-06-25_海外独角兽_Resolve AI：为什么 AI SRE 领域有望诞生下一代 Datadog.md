---
type: knowledge
入库日期: 2026-06-25
置信度: 0.85
来源: [外部-微信公众号/Resolve AI：为什么 AI SRE 领域有望诞生下一代 Datadog]
主题: Resolve AI：为什么 AI SRE 领域有望诞生下一代 Datadog
分类: 信息挖掘/微信公众号/海外独角兽
tags: [海外独角兽, AI运维, SRE, 可观测性, AIOps]
---

# Resolve AI：为什么 AI SRE 领域有望诞生下一代 Datadog

> **来源**: [外部-微信公众号/Resolve AI：为什么 AI SRE 领域有望诞生下一代 Datadog]
> **公众号**: 海外独角兽
> **原文链接**: https://mp.weixin.qq.com/s/cr1ZLVv9eq5cbILdlQlo8g
> **入库日期**: 2026-06-25

---

## 核心摘要

1. Resolve AI 是专注"AI for Prod"的 AI SRE 公司，核心机制是环境记忆 + Multi-Agent 并行调查：从告警触发到输出完整调查报告仅需约 6 分钟，工程师只需做最终决策。
2. 创始团队是两次连续创业的老兵（OpenTelemetry 联合创始人），从 stealth 仅 16 个月获超 1.5 亿美元融资，估值 10 亿美元，天使投资人包括 Jeff Dean、李飞飞等。
3. 产品核心差异化：Satellite 本地部署架构满足金融客户数据主权要求；中央记忆系统 + 多个并行专职 Agent（Knowledge/Telemetry/Code/Infra）+ 数据飞轮（越用越准）。
4. 读操作全自主、写操作留人审批的设计是赢得 enterprise 信任的关键——完全自主执行的 AI 在生产环境尚未被大规模信任。
5. AI SRE 可能是下一代可观测性基础设施雏形，能力从 observe+store 延伸到 observe+analyze+act。但真正难点不在"读懂日志"而在"破案"——需要 long chain-of-thought 推理和大量并行 sub-agent 协同。

---

## 正文

### 产品拆解

Resolve AI 专注于"AI for Prod"，让 AI 像资深 SRE 工程师一样理解、调查和解决生产问题。核心机制是环境上下文积累：系统持续学习客户生产环境，在调查时将记忆注入给 agent。

系统架构：一个中央记忆系统 + 多个并行专职 Agent + 广泛的工具集成。

四个专职 Agent：
1. **Knowledge Agent**：搜索 Runbook、历史事故记录、Slack 历史消息（集成 PagerDuty、Azure DevOps、Slack、Notion）
2. **Telemetry Agent**：日志、指标、trace（集成 Grafana、Datadog、APM 工具）
3. **Code Agent**：GitHub/GitLab 的 commit、PR、代码变更
4. **Infra Agent**：DNS、AWS/Azure/GCP 基础设施状态

五个典型场景：Kafka 健康检查、限流设计、成本优化、事故响应、自动生成 PR。

### 与传统方案的对比

传统做法中，on-call 工程师被叫醒后逐一登录不同系统、手动翻日志，MTTR 通常在 30 分钟到数小时。Resolve AI 的流程是：
- 12:04 告警触发，系统自主启动，无需叫醒工程师
- 12:05 完成分诊
- 12:07 完成四个数据源的并行调查，生成多个假设按置信度排序
- 12:10 输出完整调查报告和修复方案
- 12:30 处置完毕（工程师花 20 分钟做最终决策）

系统只做读操作（查日志、查代码、查 metrics）的完全自主执行，但写操作（生成 PR、执行回滚、重启服务）必须人工确认。

### 持续学习的生产环境

Resolve AI 在任何事故发生前就在工作。通过 Satellite Component（部署在客户数据中心内部的本地节点）持续读取生产环境的实时状态，自动抽象成一份动态知识文档（Resolve.md）。每次事故处理完毕，新经验写回文档。

这种"Satellite"模式是赢得金融客户的关键——数据不离开客户环境，仅将脱敏后的极小量元数据传回云端。

### 行业老兵的第三次并肩作战

两位创始人 Spiros Xanthos 和 Mayank Agarwal 共同经历了从 Log Insight 到 Omnition/OpenTelemetry 再到 Resolve AI 的完整周期。OpenTelemetry 现在是 CNCF 活跃度第二高的项目（仅次于 Kubernetes），近 50% 的云原生企业用户已采用。

### 与 Traversal 的对比

Resolve 团队更像工程团队，Traversal 更像学术团队（哥伦比亚大学教授联合创立，专注因果机器学习）。Resolve 采用更务实的 Satellite 本地部署架构，Traversal 采用集中式云端架构。在根因推断深度上 Traversal 被认为更深，构建了专门针对 SRE 场景训练的推理模型。

### AI SRE 的未来

AI SRE 可能是下一代可观测性基础设施的雏形。Datadog 的 Bits AI 受制于自身存储计费模式，难以做得足够深入。Claude Code 目前离 Always-on 的 SRE 系统还比较远。SRE 的真正难点在"破案"——从一个 alert 出发，在海量 noisy 数据中追溯完整的因果链条。即便推理能力过关，更大的挑战来自 context 的组织与提取。
