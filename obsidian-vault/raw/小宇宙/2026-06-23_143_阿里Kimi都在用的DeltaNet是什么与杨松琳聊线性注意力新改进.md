---
source: 晚点聊LateTalk
title: 143: 阿里、Kimi都在用的DeltaNet是什么？|与杨松琳聊线性注意力新改进
url: https://podcast.latepost.com/143
author: 晚点 LatePost
published: 2025-11-30T15:45:00+00:00
fetched_at: 2026-06-23T19:34:35Z
status: raw
---

# 143: 阿里、Kimi都在用的DeltaNet是什么？|与杨松琳聊线性注意力新改进

**来源:** 晚点聊LateTalk
**链接:** https://podcast.latepost.com/143
**作者:** 晚点 LatePost
**日期:** 2025-11-30T15:45:00+00:00

---

「不仅是提效，线性注意力在数据受限情况下的更多潜力。」 今年初的两期节目（103、104 期）里也讨论过注意力机制，这是大语言模型的核心机制。 9 月 和 10 月，阿里和 Kimi 都发布了相关进展，而且都用到了一个线性注意力成果，DeltaNet。 本期嘉宾，就是 DeltaNet 的核心贡献者之一，现在在 MIT 读博士的杨松琳，她也是线性注意力开源小组 FLA 的发起者。 这期节目在 25 分钟以前很硬核，松琳讲了线性注意力和 DeltaNet 的发展脉络，为何 21 年刚被提出时没引起太多注意，后来怎么进化的。 25 分钟以后，是关注 AI 比较多的文科生，比如我也能完全跟上的部分。我们讨论了，重新去做 full attention 的 MiniMax，以及未来要在旗舰模型上用线性注意力的 Kimi 和阿里的不同选择；线性注意力的优劣势；以及一些脑洞——如果算力无限，还需要线性注意力？松琳给了很有启发的回答。 最后半小时，松琳分享了她作为研究员，怎么习得交叉技能的，怎么开始发起FLA小组等成长经历。 本期嘉宾：杨松琳，MIT 博士生在读，DeltaNet 贡献者 本期主播：程曼祺，《晚点 LatePost》科技报道负责人 时间线跳转： -DeltaNet 的诞生演进与近期动向 02:07 注意力机制是什么？ 04:21 DeltaNet 的提出，用 Delta Rule 来增强 in-context retrieval 09:41 近年的改进主要是模型架构，而非“更新规则” 14:25 阿里 Qwen 团队 apple to apple 比较几种线性注意力混合方式；Kimi Linear 对 Gated Delta 的具体改进 17:00 更新规则和模型架构改进的区别：更新规则是在算子层面“动刀” 19:50 算法出身，自学 Infra；学习 Hazy Research Group 的风格 23:28 Qwen 和 Kimi 大概率在下一代旗舰模型用线性注意力，而 MiniMax 用回 full attention；DeepSeek 目前释放的改进都是“稀疏注意力” 37:07 稀疏注意力 vs 线性注意力潜力对比 39:40 即使算力无限，线性注意力仍有价值，因为它在有限数据中的学习效率更高，而高质量数据正是当前瓶颈 42:28 线性注意力在状态追踪上也可能有效果优势，而状态追踪对 Agentic 很重要 47:33 线性注意力的“归纳偏见”和 The Bitter Lesson：先验与 scalable 并不矛盾 49:30 回应 RWKV（原始智能）彭博：从未说发明 DeltaNet，一直在给 Schmidhuber 署名 -Householder 与 DeltaNet 的联想，像运营产品一样运营技术社区 51:51 关注注意力改进的起点，数学知识、Infra，交叉能力怎么积累？ 58:48 发现 Hoseholder 累乘和 DeltaNet 关联的过程 01:02:44 AI 何时能像人这样产生联想？——Prompt 合适，大模型应该能独立发现这个算法 01:04:11 FLA 小组的产生，受 Tri Dao 做 FlashAttention 的启发，像运营产品一样运营技术社区；Kimi 从 FLA 小组招募了线性注意力研究者 -注意力改进的未来趋势 01:11:24 稀疏注意力的改进，DeepSeek 年初 NSA 到最近 DSA 的变化 01:16:44 线性注意力的改进，从线性混合全注意力，到线性混合稀疏注意力（比如混合 DeepSeek DSA 和 Kimi KDA 😀 01:21:10 更广泛来说，关注何种模型演进？——持续学习 相关链接： 图文版： 《再谈注意力：阿里、Kimi 都在用的 DeltaNet 和线性注意力新改进丨晚点播客》 晚点聊 103 期： 《用Attention串起大模型优化史，详解DeepSeek、Kimi最新注意力机制改进》 晚点聊 104 期： 《我给线性注意力找“金主”，字节 say No，MiniMax say Yes》 剪辑制作：Nick 附录，本期提到的一些论文（更多具体名词解释，见本期文字版）： Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention Linear Transformers Are Secretly Fast Weight Programmers Parallelizing Linear Transformers with the Delta Rule over Sequence Length Gated Linear Attention Transformers with Hardware-Efficient Training Recurrence-Complete Frame-based Action Models 本期主播： 小红书@ 曼祺_火柴Q 即刻@ 曼祺_火柴Q ☆《晚点聊 LateTalk》建立「 播客听友群」啦！☆ 欢迎关注科技、商业大公司动态和创业创新的小伙伴进群交流，第一时间收听新节目。 这里有更多互动，更多话题讨论。欢迎贡献选题 &amp; 推荐嘉宾。 请先添加「晚点」小助手的微信号， 备注：“晚点聊” ，我们邀请您入群。 关注公众号《晚点 LatePost》和《晚点对话》，阅读更多商业、科技文章：

