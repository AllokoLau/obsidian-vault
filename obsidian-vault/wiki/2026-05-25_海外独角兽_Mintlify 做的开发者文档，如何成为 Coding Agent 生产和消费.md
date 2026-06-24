---
type: knowledge
入库日期: 2026-05-25
置信度: 0.70
主题: Mintlify 做的开发者文档，如何成为 Coding Agent 生产和消费的第一波内容？
分类: 信息挖掘/微信公众号
来源: [外部-微信公众号/海外独角兽]
tags: [海外独角兽, 微信公众号]
---

# Mintlify 做的开发者文档，如何成为 Coding Agent 生产和消费的第一波内容？

## 核心结论

（微信公众号文章，自动抓取。详见全文。）

## 详细内容

### 背景

来源：海外独角兽
原文链接：https://mp.weixin.qq.com/s/amJeRr_Be4sjBfUvuiItkw

### 正文

作者：Haozhen

编辑：Cage

当 agent 开始替开发者阅读文档、生成代码、调用 API，开发者文档就不再只是给人看的说明书，而是公司向 agent 展示产品知识和 context 的入口。如果文档有质量问题，也会直接通过 coding agent 变成分发与执行问题。

Claude Code 团队最近的一个判断很有意思：在复杂输出里，HTML 适合承载可读、可视化、for human 交互的知识产物，markdown 适合承载高信息密度、长篇幅 for agent 的文档内容。这背后其实是在探索一个更基础的问题：未来的人机协作是什么样的，复杂 context 怎样才能更好被 agent 读完、用起来。

Mintlify 抓住的正是这次读者迁移：一方面，它继续做 Git-backed 托管文档站，人类开发者可以通过他们的产品做出高可读性的文档；另一方面，又一直在活跃地融合很多 AI-native feature 比如 llms.txt、Markdown export、MCP server，加上对 Trieve、Helicone 的收购，让 agent 更容易拿到、检索和使用他们产品阅读知识。就在今年 4 月，公司以 5 亿美元估值完成 4500 万美元 B 轮融资。

如果 Mintlify 能从好看的 dev docs 工具升级为企业正式产品知识层，那 Mintlify 卖的就不是页面模板，而是人和 agent 共用的知识 context 入口。但如果未来进入“agent 写、agent 读”的时代，传统文档页的重要性可能下降，Mintlify 以 PM-friendly editor 和漂亮 docs UI 建立的部分优势会被稀释。

01


.

Key Takeaways

Mintlify 做的是一个 AI-native 开发者文档，帮助客户获得开箱即用的 stripe 级文档门面。它把文档内容放在客户自己的 GitHub repo 里，把文档维护嵌进工程师的 Code Review 流程，同时提供 PM 也能用的协作编辑器和好看的文档站 UI，


在硅谷企业（尤其是 YC 孵化的企业、Anthropic 这类早期顶级 AI 标杆客户）中有明显的产品力优势，甚至被一些客户视为现代技术公司标配的文档品牌。

Mintlify 的核心亮点，是较早抓住了“文档读者从人类开发者扩展到 agent”的变化。


通过 llms.txt、llms-full.txt、Markdown export、MCP server 等功能，以及收购 Trieve 和 Helicone，Mintlify 把开发者文档包装成一层 AI SEO / GEO 基础设施，让 ChatGPT、Claude、Cursor、Perplexity 和内部 agent 更容易读取、检索和引用文档中的产品知识。

虽然 agent-readable 叙事是很大的增量，但当前 Mintlify 真实付费价值仍有很大部分来自 GitHub-native workflow、托管、文档编辑体验和好看的 UI。商业化上，Mintlify Pro 年付高达 250 美元/月，企业级年付量级在 1 万到 10 万不等，


但客户仍然愿意买单，原因在于 Mintlify 至少能替换 1-3 个人力 hc，ROI 算得过来，而且还能提供美观且专业的文档界面，给客户带来品牌确定性。

今年 4 月 Mintlify 以 5 亿美元估值完成 4500 万美元 B 轮；Sacra 估算 2025 年 ARR 约为 1000 万美元、NRR 约 150%。

我们认为，Mintlify 主要风险是竞争壁垒偏薄。一方面，llms.txt、MCP、AI Assistant、Markdown export 等功能正在被 ReadMe、GitBook、Postman/Fern、企业自建 pipeline 或通用 coding agent 追赶；另一方面，


如果未来进入“agent 写、agent 读”的时代，Mintlify 以 PM-friendly editor 和漂亮 docs UI 建立的部分优势会被稀释。

长期看，Mintlify 如果能从外部开发者文档扩展到内部稳定知识库，就会成为公司知识 infra，不然就会停留在高质量开发者文档工具，成为 Atlassian、Postman、OpenAI、Anthropic 这类巨头的潜在收购标的。

02


.

Why Now：开发者文档变贵

文档读者从人变成 agent

理解 Mintlify，要先看一个更容易被感知到的变化：Markdown、HTML 这类内容格式正在被重新讨论。

过去，Markdown 主要用于 README、开发者文档、技术博客和少数特定写作场景。它的价值在于轻量、易写、易版本管理。但在 agent 时代，Markdown 又多了一层新价值：结构清晰、噪音少、容易切分和检索，适合直接进入 agent context。HTML 也是类似逻辑，只是承载的信息密度更高，可以表达更复杂的可视化、交互和分享场景。

这背后的本质不是 Markdown 变了，而是读者变了。过去，开发者文档主要给人类开发者看；现在，它也开始给 agent 看。

Mintlify 自己的数据也能看到这个趋势。2026 年 4 月，Mintlify 披露，过去 30 天 Mintlify-powered docs 收到约 7.9 亿次请求，其中 coding agent 贡献 45.3%，浏览器贡献 45.8%。这组数据来自 Mintlify 基于 Cloudflare 和 user-agent 的统计，虽然不能当成全行业绝对口径，但足以说明一个变化：agent 正在成为开发者文档的重要读者。

左右滑动查看完整图文

文档从发布末端变成知识层

读者变化后，文档的价值定义也会变化。

过去，高质量文档主要提升开发者体验和试用转化；现在，文档还要成为 agent 可读取、检索、引用、执行和更新的 context 入口：


在 GTM 端，最容易被 AI 理解的文档更容易被推荐；在产品和数据端，开发者文档会成为 agent 调用外部 API 时的事实来源。

这也放大了文档错误的影响。人类开发者会主动处理不完美的文档：旧截图可以猜，参数不清可以问，示例跑不通可以调试。但 agent 会更机械地把文档拆开、放进 context、转成代码、调用 API，再把结果交给下游用户。错误参数、过期示例和模糊限制不再只是体验问题，而会变成可规模化传播的执行问题。

但在很多 SaaS 公司里，开发者文档仍然是产品发布后的末端环节：工程师实现功能，产品经理写内部说明，技术写作者再转成对外文档，客服支持和 DevRel 手工同步到 Intercom、Zendesk、Confluence 等系统。这个流程主要有四类摩擦：

1. 

信息在内部说明、代码、工单和对外文档之间反复搬运；

2. 

API 规范、示例代码和截图容易不同步；

3. 

工程师不愿离开 GitHub / IDE 去维护内容管理系统；

4. 

每次发布都缺少预览、评审、回滚和责任边界。

过去，文档落后产品 1 到 2 个版本，主要影响的是人类开发者体验；现在，这会直接影响 agent 对产品知识的读取、复制和执行。

Mintlify 抓住的正是这次变化：把文档从一个漂亮的页面，升级成一套人和 agent 都能使用的产品知识层。

03


.

Mintlify 是什么？

产品：一套托管的文档生产线

Mintlify 可以理解为一套 Git-backed 的托管文档生产线，客户买的是一个开箱即用、美观的 stripe 级的开发者文档门面：客户把 Markdown / MDX、OpenAPI 规范、导航配置和图片资产保留在自己的 GitHub repo 中；Mintlify 接入 repo，负责构建品牌化文档站，并提供预览、部署、搜索、API reference、权限、分析和 agent-readable 地输出。

左右滑动查看完整图文

Mintlify 提供两种编辑路径：Web editor，以及 CLI / local editor。工程师可以继续在 IDE 里修改 Markdown / MDX、OpenAPI spec 和 docs.json，通过 Git 推送和 PR 更新文档；PM、技术写作者等可以在 Web editor 里用可视化或 Markdown 模式改页面、调导航、上传素材，Web editor 会把变更 commit 回 Git。

发布链路也更像软件发布：PR 打开后自动生成 preview deployment，后续 commit 会更新预览，合并到部署分支后发布到生产环境。

今年 3 月，公司发布 Workflows 新功能，团队可以用定时任务或代码仓库 push 事件触发 Mintlify agent，让它按预设 prompt 自动检查、更新文档、生成 changelog、同步 API reference，最后直接提交变更或发起 PR/MR。

但根据客户访谈，当前 Mintlify 的 agent 自动更新其实并不能算是完全成熟的 self-healing docs（agent 自动起草 PR、人类只做 review）。目前很多客户仍用 Claude 或者 Cursor 起草 80-90% 的内容，由人工审核合并 PR，用 Mintlify 完成预览、发布、API 同步、文档站托管和分发。

Mintlify 在 2026 年 4 月完成 4500 万美元 B 轮，估值 5 亿美元，Sacra 估算 2025 年 ARR 约 1000 万美元、NRR 约 150%。

产品亮点

Mintlify 的亮点可以拆成三层：先用高质量文档门面建立信任，再用 GitHub 原生工作流降低组织成本，最后用 agent-readable 能力承接 AI 时代的新需求。

第一层是文档门面。Mintlify 最早被客户感知到的价值，是让一家早期技术公司快速拥有接近 Stripe 风格的开发者文档体验。对 DevTools、AI infra 和 API-first 公司来说，文档站往往是产品第一界面：客户会在这里看 API、权限、代码示例、错误处理和集成细节。


一个漂亮、清晰、稳定的文档站，会让公司显得更成熟、更可靠，这也是 Mintlify 早期在 Product Hunt、X 和客户口口相传中传播最快的入口。

左右滑动查看完整图文

第二层是 GitHub 原生工作流。Mintlify 把文档维护放回工程团队熟悉的工作流里。文档像代码一样经过预览、评审、预发布、正式发布和回滚，产品经理、技术写作者和工程师可以围绕同一条发布链路协作。这让 Mintlify 区别于传统帮助中心 / 内容管理系统，也解释了它为什么能在 DevTools 和 AI infra 公司中传播。

第三层是 agent-readable 能力。Mintlify 托管文档会自动生成 /llms.txt、/llms-full.txt 和 Markdown 输出；Documentation MCP 让 Claude、Cursor、ChatGPT 等 MCP client 搜索文档并读取完整页面；Mintlify MCP 面向可信 agent，提供 branching、页面编辑、导航和 docs.json 等工具。Web editor 和 agent 生成的修改仍会回到 Git / PR / review 流程里。

llms.txt 是 Jeremy Howard 在 2024 年 9 月提出的社区标准提案；Mintlify 在 2024 年 11 月宣布为托管文档自动生成 /llms.txt 和 /llms-full.txt，把原本需要文档工程团队自建的 AI 读取入口变成默认输出。

04


.

什么样的文档是 agent-readable 的？

从通用标准看，agent-readable 文档首先要成为可靠事实来源。相比内部 wiki、论坛和过期博客，公开文档结构更清楚、承诺更稳定，也更直接连接 API、SDK、产品功能、错误处理和集成限制。对 agent 来说，真正重要的是一套可发现、可读取、可调用、可评估的知识结构。

Agent Score

Agent Score 是文档是否 agent-readable 的早期量化方式。


Fern 在 4 月 7 日推出 Agent Score，把 AFDocs 的 22 个检查项做成公开评分工具；Mintlify 在 4 月 27 日推出自己的 Agent Score，基于 Agent-Friendly Documentation Spec，并增加完整内容、agent skill、MCP 等检查。

左右滑动查看完整图文

我们选取了三类公司的文档页面进行测试。

从上表可以看出，Mintlify-built 的页面分数通常不错，说明 Mintlify 能把一部分 agent-readable 默认项产品化；Cloudflare 和 Docker 证明强文档工程团队也能自建高分文档；Atlassian 的分数则显示传统知识库页面不一定适合 agent 消费；Anthropic、Cursor、OpenAI 的分数说明 AI-native 公司的页面也未必天然 agent-readable。

总之，Agent Score 不能单独证明 Mintlify 有深护城河。它说明的是，agent-readable 已经从营销话术变成可检查的工程项；Mintlify 要防守的，是让 MCP、评审和回滚持续嵌在客户的文档发布流程里。

更难的是把碎片知识变成正式文档

Agent Score 只能评估已经发布出来的文档是否适合 agent 消费；


更上游的问题，是这些文档如何被生产出来。真实产品知识常散落在 Slack、Google Docs 评论、Zoom 会议、客户工单和工程师脑子里。真正耗时的环节，是把碎片翻译成可确认、可维护、可发布的结构化文档。Replit 的客户访谈也指出，今天仍需要理解产品的人站在中间，向用户和 agent 解释产品如何工作。

因此，


Mintlify 的 AI 机会或许更接近“翻译”和“结构化”：


把工程讨论变成产品经理能行动的需求，把专家解释变成工程师能实现的规格，把客户反馈变成客服支持和产品团队都能复用的知识。人类负责确认，AI 降低整理、改写和同步成本。Trieve 和 Helicone 的收购，或许也可以视作 Mintlify 在补齐这条链路上的能力：前者偏检索和 RAG，后者偏 LLM 可观测性和 AI Gateway。

这也解释了为什么文档页仍会存在。企业需要正式、可审计、可对外发布、可被客户引用的产品知识层：代码仓库面向内部开发，API 规范只描述接口，issue 和聊天记录也不代表稳定结论。


Mintlify 的机会，是把这层承诺做成更适合人和 agent 共同使用的基础设施。

05


.

客户与商业化

Mintlify 在定价上，Pro 为 250 美元/月，Enterprise 需要联系销售，根据客户访谈，企业客户年付从不到 1 万美元到十万美元不等。相比 Docusaurus / Fumadocs 这类开源方案，或 GitBook、ReadMe 等低价工具，这个价格有明显门槛。

左右滑动查看完整图文

客户访谈中提到，“想要 SSO 必须签年付”是 Mintlify 把 Pro 客户引导到 Enterprise 的 anchoring 机制；而 Enterprise 报价本身并没有稳定公式，Mintlify 的前 Head of Marketing 形容它更像一门“dark art”，会测试客户愿意为品牌、确定性、安全能力和未来 AI 功能支付多少。

但高价没有阻止 Mintlify 扩散，公司公开称客户已超过 2 万家，内容每年触达超过 1 亿人。

左右滑动查看完整图文

为什么客户愿意买？

如果只看“托管几份 MDX 文件”，250 美元/月的 Pro 和更高价的 Enterprise 都显得很贵；


但从访谈中，我们发现，客户往往比较的是自建和长期维护一套文档生产线的人力成本。


Mintlify 把写作、审核、PR、预览等一系列流程放进同一个托管系统，减少跨团队等待和内部工具维护的工作量。

以 Glean 为例，Glean 本身做企业搜索和 AI 知识管理，但文档站仍涉及公开 / 私有文档、权限、review flow、CI/CD、预发布和 SEO / GEO。Glean 在访谈中表示，如果自建，大约需要 1.5-2 名工程师持续负责。迁到 Mintlify 后，文档进入 GitHub 仓库，改动生成 preview，评审后发布；过去在 Google Docs、Intercom、Zendesk 和人工转换之间流转的流程，就被压缩到分钟或小时。

其他访谈也指向同一个结论。

• 

Vividly 看中的是文档站、AI search、API 同步和客户成功效率；

• 

PlanetScale 看重用不到 1 万美元年费替代自建和持续维护；

• 

Replit 更关心在团队还没到专职文档 / 开发者体验规模前，避免把文档系统变成新的内部工程项目。

综合来看，Mintlify 企业级年付量级在 1 万到 10 万不等，但至少可以替代 1-3 个工程、设计或技术写作 headcount。但边界也很清楚：当客户需要高度交互、深度自定义，或已经有成熟文档团队时，自建吸引力会上升。

此外，还有一层隐性付费理由是品牌确定性。Mintlify 的高价对应的是“现代开发者门户”的确定性，高于单纯文档 CMS。前 Head of Marketing 提到，大合同很多时候并不需要逐项证明工程小时节省，更多受品牌和 FOMO 驱动，因为 Mintlify 已经在 YC、旧金山开发者圈层和 AI-native 公司中形成了强势口碑，客户会把它视为“现代技术公司应该使用的文档平台”。

客户也在为“创新保险”付费。购买 Mintlify，相当于外包对 llms.txt、MCP、AI Assistant、agent 写文档、knowledge base 等新趋势的持续跟进。只要客户相信使用 Mintlify 能让开发者门户保持技术前沿，而自建和维护这些能力的机会成本更高，Mintlify 的溢价就仍然成立。

06


.

团队

CEO Han Wang 是 2022 届 Cornell 信息科学学士，从 11 岁开始，靠 YouTube 视频和当时质量糟糕的开发者文档自学编程，“自己被坏文档坑过”的经历贯穿 Mintlify 的产品哲学。2020 年在 Facebook 做过软件工程实习，曾共同创立 FoodFul（一家做奶牛云监测的农业科技公司，在 Cornell Digital Agriculture Hackathon 拿过 Most Market－Ready 奖）。

CTO Hahnbee Lee 曾在 Cornell Design ＆ Tech Initiative 任软件工程师与技术 PM，在 Duolingo 做软件工程实习，还在 Cornell Rocketry Team、Vera.Zone、Leidos 等公司有多份软件工程实习。

Han 和 Hahnbee 在 Cornell Design ＆ Tech Initiative 认识，一起做了 courseplan.io（至今被约一半 Cornell 本科生使用）。Mintlify 之前他们经历过多次 pivot，包括被 Bettermode 收购的 Pe.ple、Product Hunt 日榜第一的 Figstack。两人曾带 Figstack 申请 YC，面试前 4 天决定换方向、两个通宵后带新 demo 进入面试，被录取进 YC W22。

Mintlify 初始产品是周末逼自己做出来的，前 100 客户的获客方式是 Mintlify 先用自己工具帮潜在客户把文档做好，再去接触客户说“你们的文档已经在 Mintlify 上了”。团队还能做到非常及时的客户响应，多位客户提到，


Mintlify 曾做到 “P0 问题 30 分钟内修复”，以及“周末晚上 10 点报问题，5 分钟内有人响应”。

07


.

竞争格局与风险

Mintlify 的市场竞争主要来自四类力量，总的来说，


Mintlify 在 AI-readable 分发、Git workflow 和视觉体验上领先；在企业级信任、复杂权限、深度自定义等方面仍有短板。

但未来 Mintlify 如果一直停留在高质量开发者文档工具，容易成为巨头的潜在收购标的。综合公开资料和访谈，我们认为有三类买家：

1.

 Atlassian 这类 workflow / knowledge 巨头，可以用 Mintlify 补 Confluence 在外部开发者文档和 AI-readable docs 上的短板；

2.

 Postman 这类 API lifecycle 平台，可以把 Mintlify 作为 Fern 之外更横向的文档/知识层；

3.

 OpenAI、Anthropic、Cursor 这类 AI native 公司，可以把 Mintlify 视为让 agent 理解软件世界的文档 infra。

客户自建与通用 coding agent

如前文所分析的，对 Glean、Replit、Anthropic、Cursor 这样的强工程团队来说，技术可行性通常可解决，关键在组织成本。

•

 Replit 在评估 GitBook、ReadMe、Fern 和开源方案后选择 Mintlify，主要就是因为部署、预览、infra 维护等功能已被打包；如果未来需要个性化文档和更深产品交互等功能，自建吸引力会上升，Replit 预计未来 5 年内有 80%-90% 概率迁出 Mintlify，关键临界点是 docs 团队从 1 人扩大到 5-6 人。

• 

根据 Replit DevRel 在今年 1 月的访谈，Anthropic 现在已不再使用 Mintlify；Cursor 因为希望获得更强 developer experience 和更高自定义控制，也转向自建网页。

Anthropic 尤其值得关注，Han Wang 提到，两年前 Anthropic 突然要求把英文文档实时翻译成 12 种语言，Mintlify 为此专门搭建翻译流水线，这说明 Anthropic 早期承担了产品共创和 enterprise 需求验证的角色，远超过普通 logo 背书；现在它转向自控主文档，反而成为头部客户到一定规模后可能迁出的标杆案例。

此外，Mintlify 也存在一定的安全问题。Mintlify 历史上披露过 GitHub token incident 和 static asset / XSS 问题，PlanetScale 也在访谈中提到 incident 虽没有影响他们但留下不好观感。

2026 年 4 月 13 日，Letta 联合创始人在 X 上披露 prompt injection 风险，即用户使用“复制为 Markdown”时，Mintlify 会自动注入 “Built with Mintlify” 归属标记，被复制进 agent 输入流构成潜在 prompt injection 风险。

左右滑动查看完整图文

ReadMe / GitBook 等传统文档平台

ReadMe 在 API 文档和企业客户中有存量，GitBook 是轻量文档和知识库的常用选择。Mintlify 的替换机会来自更强的 Git-native 工作流、AI-readable 默认项和更现代的设计；但传统玩家也可以补齐 AI、Markdown、MCP、agent 功能和新版 UI。

•

 PlanetScale 从 ReadMe 迁出的原因在于原系统慢、维护 overhead 高；

•

 Vividly 用 ReadMe 近 5 年后迁出，核心不满是 UI/UX 笨重、API 文档更新手工、release notes 经常出问题、反馈没有响应。

Fern / Postman 等 API-first 玩家

Postman 在 2026 年 1 月收购 Fern 是一个重要信号。Fern 围绕 OpenAPI 生成接口参考文档、SDK、docs-as-code 和开发者门户。客户的诉求越靠近 API 和 SDK 同步，使用 Fern / Postman 越自然，而 Mintlify 更像外部文档门户和知识分发层。

•

 Vividly 认为 Fern 更适合 Twilio、Square 这类 API-first 公司；Replit 表示 Mintlify 的强项在于更通用的产品文档和托管 workflow；

•

 Hubspot 认为 Mintlify 专注在文档上，Fern 把精力分散在了文档、SDK 等不同领域，文档质量差异明显。

扩张边界：市场空间越大，竞争越杂

当 Mintlify 开始对外向客服支持、内部知识库、产品内引导等领域扩张，Mintlify 的市场空间和竞争压力会同时放大。

因此，短期看 20-30 亿美元级 dev-docs / API docs SaaS 市场，或许可以支撑一家高增长垂直玩家，但估值上行则依赖 Mintlify 能否从开发者文档进入企业产品知识层，切入 DevEx、客服支持和 KM 预算。


CEO 表示，目前 Mintlify 已把自身内部知识栈全部跑在 Mintlify 上。

 排版：夏悦涵

延伸阅读

从 Agent 开权限开始，Serval 想成为下一代 ServiceNow

拆解 Anthropic：最好的 AI 公司，可能也是一种组织发明

The Era of Agent：拾象 AGI 投资洞察

AI Labs 都在用，ClickHouse 能成为 AI 日志的实时分析引擎吗？

Supabase：百亿美元估值，vibe coding 的默认后端？

## 关联

- [[海外独角兽]]

## 备注

> 置信度 0.70：微信公众号文章。
