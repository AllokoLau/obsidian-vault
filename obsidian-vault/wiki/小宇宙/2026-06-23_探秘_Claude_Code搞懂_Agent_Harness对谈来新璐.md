---
type: founder
入库日期: 2026-06-23
置信度: High
姓名: 来新璐
公司: 
行业: AI/开发者工具
职位: 
tags: [策略, CTO, 存储]
---

## 基本信息
**来源:** 十字路口Crossing
**链接:** https://www.xiaoyuzhoufm.com/episode/69f2e83fbb3ffa11e59dec82?utm_source=rss
**日期:** 2026-05-05T08:00:00+00:00
**置信度:** 80%

## 职业经历
*（待补充）*

## 公开观点/言论

🚥 为什么说 Agent 的上限来自 Harness？当我们讨论 Harness 时，我们究竟在讨论什么？ 不久前，Claude Code 源代码泄露，许多 Agent Harness 的关键模块得以完整呈现，成了一份极佳的教学标本。而在技术高速变化的红利期，主动理解新技术往往能带来很高的认知增量。 因此，本周「十字路口」邀请到来新璐，一起聊聊 Agent Harness。 新璐是 ShareAI 开源社区发起人，他撰写维护的《Learn Claude Code》教程在 GitHub 上获得超过 50k Star。 在本期内容中，我们把 Agent Harness 从概念词拆解成工程语言，介绍它的三层框架：会跑（执行层）→ 跑久（状态层）→ 跑稳（治理层）。同时，我们也梳理了 Claude Code 中值得借鉴的多个机制：更多 context、更少 control 的思路、“零上下文管理”的哲学、长程任务的接力式交接策略，以及让 Agent 越用越聪明的“做梦”式记忆维护与迭代机制等 新璐作为典型的一人公司，刚完成数百万美金融资； 他也分享了自己对 OPC...

---

### 原文摘要
🚥 为什么说 Agent 的上限来自 Harness？当我们讨论 Harness 时，我们究竟在讨论什么？ 不久前，Claude Code 源代码泄露，许多 Agent Harness 的关键模块得以完整呈现，成了一份极佳的教学标本。而在技术高速变化的红利期，主动理解新技术往往能带来很高的认知增量。 因此，本周「十字路口」邀请到来新璐，一起聊聊 Agent Harness。 新璐是 ShareAI 开源社区发起人，他撰写维护的《Learn Claude Code》教程在 GitHub 上获得超过 50k Star。 在本期内容中，我们把 Agent Harness 从概念词拆解成工程语言，介绍它的三层框架：会跑（执行层）→ 跑久（状态层）→ 跑稳（治理层）。同时，我们也梳理了 Claude Code 中值得借鉴的多个机制：更多 context、更少 control 的思路、“零上下文管理”的哲学、长程任务的接力式交接策略，以及让 Agent 越用越聪明的“做梦”式记忆维护与迭代机制等 新璐作为典型的一人公司，刚完成数百万美金融资； 他也分享了自己对 OPC 的独特观点，甚至认为“未来只有 0 人公司，没有 1 人公司”，颇具启发。 🎬 我们的视频播客已同步上线于 @Koji杨远骋 的视频号、 小红书 、 哔哩哔哩 、 Youtube 等平台。 📒 文字版已发布于 @十字路口Crossing 公众号。 🟢 00:49 快问快答： 年龄、毕业院校、MBTI、星座、一句话介绍公司、融资情况、团队规模、创业前经历 🟢 01:52 模型以外都是 Harness 机甲、大脑、机器人、智商120——Harness 到底是什么 模型以外都是 Harness Agent 上限由 Harness 决定吗？ 模型智商已在 120–170 之间；Agent Harness 像机甲——不提升智力，但极大扩展能力 🟢 02:47 GitHub 50k star，是怎么来的？ 这个Agent教程，其实不只是写给别人看的——它本来是新璐自己整理的"造 Agent 心法"。 9 个月前动笔，出发点是"把 Claude Code 套网页壳就能得到一个强大 Agent 产品"的简单直觉 开源社区当时流行 LangChain、LangGraph等 prompt pipeline 做法开发“伪Agent”，是一场派系之争——"Prompt Flow-Driven vs Agent Native-Driven" LangChain 过时了吗？ 🟢 04:02 Bash is all you need Claude 推出 Manager Agents 之后，大家还需要自己搭 Harness 吗？ 就像 Next.js出现后大家不再关心底层运行原理，两三年后 Agent Harness 也会收敛为开箱即用 但现在是技术周期红利窗口——不懂 Agent Harness，做出来的Agent产品"缺乏灵魂" 今天的 PM 和过去的 PM，指的根本不是同一种人 🟢 07:04 Harness 三层拆解 用两周时间、多 Agent 协作，从零写出一个 C 编译器——这个经典案例背后，到底走了哪三层？ 第一层：执行能力层 ——文件增删读写、浏览器、语言解释器；配错权限后果是什么？ 第二层：上下文与状态层 ——system prompt、skills、memory，以及上下文窗口满了之后 Agent 如何"接力交棒" 第三层：治理与编排层 —— 数百上千 Agents 如何组织协作？测试 Agent 为什么不能同时拥有修改代码的权限？ 🟢 12:05 KB 的 K 系列Agent工具链 他们公司叫 Komputer Blue，代号KB，目标是构建By Agents &amp; For Agents的整套开源Infra Komputer：用 TypeScript 重写 Unix 文件系统和 bash，给 Agent 一个"熟悉的生活环境"；支持 WebAssembly 时切换WASM实现； Kruntime：Agent Runtime 层，提供让人类开发 Agent 的接口，以及Agent 派生 Agent的接口 Kwatch：Agent 观测层，分析 Agent 任务在哪里卡住，反向指导 Agent 设计迭代 Krl：把 Agent 在 Runtime 上沉淀的轨迹数据拿来强化学习或做上下文层的自迭代 🟢 13:55 vs. AWS AgentCore、阿里云 AgentBay 云服务厂商当然也想做这一层 K 系列 Agent 工具链的核心理念：在离用户更近的场景运行 Agent，任何能跑 JavaScript 的场景都能用——浏览器、插件、App、Electron、小程序、纯静态网页、

## 关联
-

## 备注
来源: [十字路口Crossing](https://www.xiaoyuzhoufm.com/episode/69f2e83fbb3ffa11e59dec82?utm_source=rss)
