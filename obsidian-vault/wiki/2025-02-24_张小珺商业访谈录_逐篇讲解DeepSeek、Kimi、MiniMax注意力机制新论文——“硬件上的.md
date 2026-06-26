---
type: knowledge
入库日期: 2026-06-25
置信度: 0.80
主题: 逐篇讲解DeepSeek、Kimi、MiniMax注意力机制新论文——“硬件上的暴力美学”
分类: 信息挖掘/B站
来源: [外部-Bilibili/BV1ZmAQekEMc]
tags: [杨松琳, 注意力机制, DeepSeek, Kimi, MiniMax, NSA, MoBA, 稀疏注意力, 线性注意力, 硬件对齐, 架构创新]
---

# 逐篇讲解DeepSeek、Kimi、MiniMax注意力机制新论文——“硬件上的暴力美学”

> MIT CSAIL在读博士杨松琳逐篇解读DeepSeek、Kimi、MiniMax三家公司在同周发布的注意力机制新论文，深入分析三种不同技术路线（动态稀疏注意力 vs 线性注意力混合架构）的设计哲学与硬件考量。
> [来源: [外部-Bilibili/BV1ZmAQekEMc]] [置信度: 0.80]

---

## 核心结论

1. **DeepSeek NSA首次实现动态稀疏注意力全面超越Full Attention** — Native Sparse Attention在预训练损失、下游评测、长文本能力乃至推理任务上均全程压制Full Attention，实现"既快又好"的效果。[置信度: 0.85]

2. **三家公司的注意力优化目标高度一致** — 优化注意力机制的核心驱动力都是长文本训练效率（prefilling加速）和推理效率（decoding加速），以支持更长的思维链和test-time scaling。[置信度: 0.85]

3. **DeepSeek与Kimi的论文均属Quest框架的follow-up工作** — 两者都基于MIT韩松组quest的block-wise动态稀疏注意力，但在硬件亲和性上分化出两种截然不同的设计哲学：DeepSeek走"硬件暴力美学"路线，Kimi走"极简优雅"路线。[置信度: 0.80]

4. **MiniMax-01是线性注意力混合架构最大规模的验证** — 首次将hybrid架构（7层线性注意力+1层softmax注意力循环堆叠）scale up到GPT-4o级别性能，证明该路线在大规模上的可行性。[置信度: 0.80]

5. **架构创新正成为行业新竞赛维度** — 随着pre-training data scaling遇到瓶颈，三家公司不约而同转向底层架构创新，DeepSeek坚持自研架构尤为可贵。[置信度: 0.85]

6. **NSA的kernel设计是硬件亲和性的典范** — 通过强制GQA下同一group的head选择相同的KV block，利用head维度凑矩阵乘法以调用tensor core，同时避免稀疏注意力中不同query的KV block读取并集浪费。[置信度: 0.80]

7. **MoBA的极简设计带来灵活性但也付出代价** — 砍掉压缩分支和滑动窗口分支，使用无参数的mean pooling做block表示，可在full/sparse attention间自由切换，但面临SFT时梯度稀疏问题和block size无法做小的局限。[置信度: 0.80]

8. **MiniMax的hybrid路线技术风险最低** — 因为稀疏注意力保留全部KV cache（下限有保障），而线性注意力在工业界已被反复验证约一年，MiniMax反而在risk-taking上最小。[置信度: 0.75]

---

## 详细内容

### 背景
- **来源**: [外部-Bilibili/BV1ZmAQekEMc]
- **UP主**: 张小珺Jùn｜商业访谈录
- **BV号**: BV1ZmAQekEMc
- **发布时间**: 2025-02-24
- **播放量**: 33146
- **嘉宾**: 杨松琳（MIT CSAIL博士二年级，导师为韩松教授）
- **时长**: 约156分钟
- **背景**: DeepSeek和Kimi在同一天发布注意力机制论文（中门对狙），MiniMax在春节前也已发布相关论文。三篇论文均聚焦于改进Transformer注意力机制以处理长文本任务。杨松琳的研究方向是硬件高效的序列建模和线性注意力。

### 章节速览

| 时间 | 话题 | 关键内容 |
|------|------|---------|
| 00:00 - 02:29 | 开场 | 简介三篇注意力机制论文背景 |
| 02:30 - 15:35 | 开篇问答 | 为何三家同时发注意力机制论文、注意力机制基本概念回顾 |
| 15:36 - 01:19:13 | **DeepSeek NSA** | Native Sparse Attention论文精讲 |
| 15:36 - 19:30 | NSA概述 | 第一个将动态稀疏注意力用于预训练的模型，开创性工作 |
| 19:30 - 25:30 | NSA三分支架构 | compressed attention（粗粒度）+ selected attention（细粒度）+ sliding window attention（划窗），门控机制自适应融合 |
| 25:30 - 30:00 | 与Quest对比 | NSA基于Quest框架但解决了硬件对齐问题 |
| 30:00 - 39:00 | GQA/MQA分析 | 为什么NSA在GQA下强制group内head选择相同KV block以提升decoding效率 |
| 39:00 - 48:00 | Flash Attention回顾 | Memory hierarchy讲解、为什么采用tiling策略 |
| 48:00 - 55:00 | NSA kernel创新 | 利用head维度凑矩阵乘法调用tensor core；为满足triton限制（HD≥16）暴力增加head数量 |
| 55:00 - 62:00 | 训练效果 | NSA预训练损失全程低于Full Attention；下游评测全线压制；长文本和reasoning均有提升 |
| 62:00 - 70:00 | Ablation Study | 压缩分支对可微block selection至关重要；压缩分支提供可反传的梯度信号 |
| 70:00 - 78:00 | "硬件暴力美学" | kernel设计层层相扣、刀尖舔血；在Quest框架下可以说是硬件最优解 |
| 01:19:14 - 01:44:41 | **Kimi MoBA** | Mixture of Block Attention论文讲解 |
| 01:19:14 - 81:00 | MoBA概述 | 同属Quest框架，但设计极简 |
| 81:00 - 86:00 | 主要区别 | 砍掉压缩和sliding window分支；用mean pooling替代MLP做block表示（无参数） |
| 86:00 - 93:00 | 代价分析 | block size必须较大（512）导致粒度粗；top3选择容易遗漏重要信息 |
| 93:00 - 96:00 | SFT梯度稀疏问题 | 砍掉压缩分支后梯度信号稀疏；解决方案：最后三层切换到Full Attention |
| 96:00 - 99:00 | Hybrid训练策略 | 90% token用sparse训+10%用full训；full/sparse可自由切换（无参数差异） |
| 99:00 - 01:19:13 | 两公司对比 | DeepSeek硬件暴力美学 vs Kimi极简优雅设计哲学 |
| 01:44:42 - 02:30:06 | **MiniMax-01** | Linear Attention + Hybrid架构讲解 |
| 01:44:42 - 106:00 | Hybrid架构说明 | 7层Linear Attention + 1层Softmax Attention循环堆叠（80层） |
| 106:00 - 121:00 | 线性注意力原理 | 去掉softmax后可用结合律重写为RNN形式；matryoshka hidden state（D×D矩阵） |
| 121:00 - 126:00 | Chunkwise算法 | 将序列分段并行计算，凑矩阵乘法；复杂度sub-quadratic |
| 126:00 - 135:00 | 现代线性注意力进展 | Decay + Data-dependent gating（Mamba2关键创新实为LSTM gate的现代复兴） |
| 135:00 - 143:00 | 工程优化 | 扎实的分布式优化（expert parallel、chunkwise parallel）；hybrid架构是linear attention对长文本质疑的妥协 |
| 143:00 - 148:00 | 三家公司risk对比 | Kimi/DeepSeek的sparse attention风险更小（保留完整KV cache），MiniMax的linear attention路线风险反而最大 |
| 148:00 - 156:00 | 总结讨论 | Tensor Core/MHSA对比；架构创新是scaling law遇瓶颈后的新方向；开源成为竞争新维度 |

### 关键要点

1. **注意力机制的核心矛盾** — Full Attention有平方复杂度，长文本下无法承受。三篇论文分别用稀疏注意力（省计算，不省显存）和线性注意力（省计算也省显存）两种路线解决。推理时KV cache成为主要内存瓶颈。

2. **NSA的硬件亲和性设计** — DeepSeek将GQA下同一group的多个head强制选择相同的KV block，从而避免query-level稀疏带来的内存读取浪费。这使NV cache读取量减少，在decoding阶段有天然优势。为此牺牲了不同head选择的diversity，但通过暴力增加head数量来弥补。

3. **Kimi MoBA的极简哲学** — 只用mean pooling压缩block表示（无额外参数），保留每个head自由选择不同KV block的灵活性。代价是读取效率降低（需做复杂indexing/reindexing），block size不能太小（512 vs NSA的64），且SFT时面临梯度稀疏问题。

4. **MiniMax的Hybrid路线** — 将线性注意力（高效但检索弱）与softmax注意力（精准但效率低）按7:1比例混合。线性注意力以RNN形式推理，常数复杂度；Chunkwise算法使其训练也能并行化。这是linear attention面对"长文本不可靠"质疑的务实妥协。

5. **Tensor Core驱动的硬件优化原则** — 当前GPU优化最核心原则是"尽量将操作写成矩阵乘法"，因为tensor core的矩阵乘法比其他计算单元快约16倍（A100）。NSA靠head维度、线性注意力靠chunk维度来凑这个矩阵乘法维度。

6. **"从scratch训练sparse attention"这一思路的突破性** — 此前动态稀疏注意力仅用于推理加速（对训好的full attention做后处理逼近），效果有上限。DeepSeek首次证明从零预训练动态稀疏attention可超越full attention，为社区开辟了新方向。

7. **三家公司技术风险评估** — Kimi和DeepSeek的稀疏注意力保留所有KV cache，在大海捞针等任务上有保障，风险可控。MiniMax的linear attention反而技术上更激进，因为RNN类模型的长文本检索能力一直被行业质疑。

8. **开源成为大模型竞争新维度** — 追赶者通过开源/发论文展示技术实力、吸引人才、提振市场信心。阿里因Qwen系列开源大涨，Kimi也在加速开源。论文发布已成为展示技术肌肉的"新战场"。

### 精彩引述

> "我确实被那个Native Sparse Attention他甚至比Full Attention要好这一点吸引住了。可能我之后也会做一些这种Dynamic Sparse Attention方面的研究。"

> "这个就是他（DeepSeek）在这个quest框架下面的一个最优解了，它能够非常非常高效的利用到这个硬件。可以称得上是一种硬件上的一种暴力美学了。"

> "很多人可能觉得这个模型架构不是很优雅，但是我觉得这个kernel是非常的优雅的。这几乎就是一个完美的、单就是硬件稀疏attention的一个玩法，他基本上没有什么浪费。"

> "我觉得DeepSeek他们是比较少见的、非常坚持自己做架构创新的，这一点非常可贵。因为很多公司我感觉都是排斥来做架构创新的。"

> "做架构创新是一个风险与机遇并存的。就像MLA的成功，还有可以预见到的Native Sparse Attention的成功，因为他甚至在paper里看到了他可能比Full Attention更好。"

> "在这个年代，设计算法最好还是能让他怎么硬件高效怎么来。就是尽可能把一些算法写成矩阵乘法，你就能直接看到这个效果，你不需要等到未来某些什么量子计算机。"

> "大家可能对Linear Attention的印象还停留在四五年前，那时候Linear Attention的performance确实差。但现在进展是非常快的，大家可能要update一下自己的knowledge了。"

> "开源是一种最好的方式。因为你是追赶者，所以闭源你是没有那种技术领先带来的优势的。所以追赶者经常选择的方式都是开源。"

> "现在scaling law就是数据遇到了瓶颈，所以他们其实不约而同都在改架构，都在试图通过架构的优化带来更好的结果。"

> "Attention像翻书，RN像人的大脑。人的大脑容量是固定的，但需要的时候会去翻书。一般的时候，靠着这个fix size的脑容量其实已经够用了。"

---

## 备注
置信度 0.80：基于B站AI字幕全文提取，来源可信。由AI精炼生成。原始字幕为B站自动生成，存在部分专有名词识别误差（如DeepSeek/DeepSick、attention/assize等），核心技术内容已结合上下文校正。

## 关联
<!-- 后续由 Writer 补充关联条目 -->
