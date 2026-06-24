---
type: knowledge
入库日期: 2026-05-21
置信度: 0.70
主题: 从 Agent 开权限开始，Serval 想成为下一代 ServiceNow
分类: 信息挖掘/微信公众号
来源: [外部-微信公众号/海外独角兽]
tags: [海外独角兽, 微信公众号]
---

# 从 Agent 开权限开始，Serval 想成为下一代 ServiceNow

## 核心结论

（微信公众号文章，自动抓取。详见全文。）

## 详细内容

### 背景

来源：海外独角兽
原文链接：https://mp.weixin.qq.com/s/7U92Rhlzvr2PRIhOybQcVw

### 正文

作者：Haina

一个员工想开 Cursor 权限。过去的流程大概是：去 Jira、Freshservice 或 ServiceNow 提一个 ticket，写清楚理由，等 IT 分派，再等审批，再等有人进后台配置。对员工来说，这是等待；对 IT 来说，这是重复劳动；对公司来说，这是每天都在发生的组织摩擦。

Serval 想把这件事变成一句话：在 Slack、Teams、email 或 web portal 里说“帮我开 Cursor”。系统判断员工身份、权限、审批规则和访问时长，调用对应 workflow，留下日志，到期自动回收权限。

这类场景看起来很小，却是 enterprise agent 最早成立的地方。原因很简单：请求高频，动作明确，权限重要，结果可验证，ROI 直接。Serval 正在把 IT help desk 从工单系统推向企业里的 governed execution layer。

01


.

Thesis

Serval 所处的机会，可以从四个层面理解。

Serval 直接切入的市场是 IT help desk 的人工处理、Jira 承载的 IT 工单流转，以及一部分流程配置和实施服务；ServiceNow 作为主系统，暂时更像第二层竞争边界。


它的早期客户大多是云原生公司，IT 资产主要是 SaaS 许可、云资源、身份与访问配置。这些资源可以通过 API 操作，不需要传统 CMDB 先跑起来。员工从“去一个单独系统提工单”变成“在 Slack 里说一句话”，IT 团队从手动配置变成让 agent 调用流程。这个重新定位会直接改变市场判断：Serval 的预算池既来自 ITSM 软件，也来自一线 / 二线服务台、IT 工程师、ServiceNow 管理员和流程自动化。

Serval 的架构 alpha 在白盒执行。


很多 AI help desk 产品把大模型放在前台回答、分流、搜索知识库。Serval 把 AI 放在流程创建和请求处理两端，中间用可审计的 TypeScript 流程承接执行。Builder Agent 生成流程，Help Desk Agent 调用已经发布的流程；前者创建工具，后者使用工具。流程一旦发布，执行过程受 RBAC、审批、API 权限范围、团队隔离、审计日志限制。企业不需要相信每一次执行时的大模型推理都可靠，只需要审计和控制已经发布的执行逻辑。

Serval 进大企业的路径更像部门级部署，区别于整体替换 ServiceNow。


集团主系统可以继续跑 ServiceNow，新业务线、创新部门、高变化运营单元可以独立采购更轻、更快的 ITSM / 自动化工具。Serval 不需要等集团 CIO 做一次 12-18 个月的大替换，可以从一个部门开始，把流程模板和内部口碑带到更多团队。

Serval 的更大想象空间，是成为面向 AI agent 的 ITSM。


企业里会有越来越多 AI agent、服务账号和其他非人类身份。它们都要申请权限、调用 API、改系统状态、触发审批、留下审计记录。Serval 现在的产品架构，已经贴近企业管理 agent 群所需要的基础能力。而短板可能在叙事，和 agent 治理相关功能尚不完整。

Serval 的长期问题是：它会停在 AI-native help desk，还是升级成企业 agent 的执行和治理层？

02


.

Serval 是什么

Serval 官方的定位是 AI-native ITSM。它把 IT 帮助台、权限开通/回收和流程自动化放到同一个入口，并内置一组 AI agent 来接手原本由 IT 团队处理的工单任务。

拆开看，它有三类 agent：

•

 Help Desk Agent：面向员工，回答问题、处理请求、开权限、触发 workflow；

•

 Automation Agent：面向管理员，用自然语言创建 enterprise-grade workflow；

•

 Insights Agent：面向运营和安全团队，建议新的 workflow、更新知识库、优化配置。

产品形态上，Serval 覆盖几个模块：

•

 处理请求：自动处理员工请求，入口包括 Slack、Teams、邮件和网页门户；

•

 搭建工作流：用自然语言描述流程，系统生成工作流；

•

 改造工单系统：替代或同步现有工单系统；

•

 管理权限：处理权限申请、审批、即时授权、权限回收；

•

 管理资产：从 MDM、采购系统、IdP、HRIS 等系统汇总资产数据；

•

 企业级控制：支持云部署、混合部署、私有化部署、团队隔离、治理、Git 版本管理、SOC 2 / HIPAA / GDPR、SIEM 日志。

产品里最值得展开的是 workflow as code。Serval 的 workflow 可以由 AI 生成，也可以在 no-code UI 里查看。技术团队还能直接检查 workflow code，并把 workflow 放进 Git 管理。官网把这件事叫 “vibe coding for IT automation”：让 IT admin 用自然语言生成流程，同时保留代码的透明度、可靠性和可审计性。


普通 service bot 往往到回答和分流为止。

Serval 继续往后走，把一批重复、可控、可审计的 IT 动作变成可运行的 workflow。

03


.

为什么 ServiceNow 时代的抽象开始不够用

ServiceNow 那一代产品抓住了一个好抽象：workflow on top of database。

ServiceNow 这一代产品把 IT 流程、资产、审批、权限、工单、合规记录放进一个系统。大企业的记录系统不会快速消失。它们沉淀了标准数据、权限体系、审批逻辑、异常处理方式和组织记忆。a16z 在《为什么世界仍然运行在 SAP 上》


（Why the World Still Runs on SAP）


里讲到的判断很类似：AI 更现实的路径，是让这些系统变得更可编程、更容易使用。

问题出在另一层：创建和维护 workflow 太重。很多自动化需要管理员、实施顾问、开发资源一起配置。一个 onboarding flow、access policy、approval path，从需求到上线常常按周计算。业务变化速度开始快于自动化建设速度。结果是，很多人仍然选择手动做事，因为做一次手动操作比搭一套自动化更快。

Jake Stauch 在最近一次访谈里讲了一个生动的例子：IT admin 面前有两种选择，去 Google Workspace 点一下 reset password，或者打开 workflow builder 拖 trigger、response、approval。大多数人会直接手动 reset。


自动化要真正发生，构建自动化本身必须比手动操作更简单。

这是 AI-native ITSM 的第一性问题。

04


.

产品架构：AI 生成 workflow，代码执行 workflow

过去很多 IT support 产品把 AI 用在前台：理解员工问题、搜索知识库、分类工单、总结对话、推荐回复。这些能力能减少一部分 L1 helpdesk 压力，也能提升 ticket deflection。

Serval 更早把重点放在 execution。它押注的产品路线，是让 AI 负责生成和维护 workflow，让已经发布的代码负责执行 workflow。这个设计决定了 Serval 和普通 AI help desk 的区别。

企业不会把 mission-critical 的执行权完全交给一个每次都重新推理的模型。Serval 把系统拆成两个角色：Builder / Automation Agent 负责根据自然语言生成 workflow，Help Desk Agent 负责在员工提出请求时调用已经发布的 workflow。前者创建工具，后者使用工具；前者能改流程，后者只能在管理员设定的边界内执行。


Serval 的产品最大的特点是 Slack native，员工可以在 Slack 里直接调用。

Workflow 一旦发布，就变成可读、可审计、可版本控制的 TypeScript。管理员可以在 no-code UI 里查看，也可以让工程团队直接读代码，放进 Git，接入 SIEM。我们在调研中看到，一些医疗、金融和大型企业客户关心的问题，从“AI 能不能回答员工问题”变成“这段自动化逻辑能不能被审计、回滚、解释”。

Jake 把这个说成“产品就是边界”。模型能力越来越强，企业真正缺的东西，开始回到那些看起来很老派的企业软件基础能力：权限、审批、范围限制、可见性、审计、报表、日志、告警。当模型足够聪明，产品价值会从“让模型更会说话”转向“让企业敢让模型做事”。在企业级智能体里，控制层本身就是产品。

这也解释了 Serval 的单位经济结构。对于密码重置、Google 群组创建、即时权限申请这类高频工作流，昂贵的模型调用主要发生在工作流创建和打磨阶段。工作流一旦发布，后续请求运行的是已经生成好的逻辑，不需要每次都重新生成代码。

这条路线还有一个好处：模型升级会影响 workflow builder 的效率，但不会直接改变每一次已发布 workflow 的执行行为。新模型变强，Serval 可以更快生成、更好重构 workflow；旧 workflow 的执行仍然由已发布代码约束。这是应用层公司抵抗模型波动的一种方式。

05


.

客户证据：AI-native 创业公司、Enterprise 和反向验证

Serval 的客户证据可以分三层看。第一层是公开的 AI-native 客户；第二层是部门级大企业试点；第三层是传统大企业 IT 负责人给出的反向验证。第三层会把 Serval 还没解决的问题暴露出来。

先看第一层。Serval 早期客户很集中：Perplexity、Together AI、Mercor、Verkada、Cribl、Bilt、Clay 等快速增长的 AI 原生或 SaaS 占比较高的公司。它们的 IT 资产更偏 SaaS 许可证、云资源、身份配置、内部工具权限，天然更适合通过 API 管理。相比有大量自有路由器、防火墙、数据中心、历史 CMDB 的传统企业，这类公司更适合从第一天采用 AI 原生工作流。

几个公开客户案例能说明 Serval 先在哪里跑通。

• 

Perplexity：从手动入职到超过 50% 的工单自动化。

Perplexity 在 12 个月内员工数增长 3 倍，IT 团队需要支撑入职、软件权限、Google 群组、Slack 频道等大量请求。Perplexity 用 Serval 自动化了超过 50% 的 IT 请求和全部员工入职流程，每个管理员每天节省 1-2 小时。Perplexity 的安全负责人还把 Serval 描述成安全团队的延伸，因为它帮助团队实践最小权限原则，并把访问权限限制在必要时长内。

•

 Together AI：95% 的即时权限申请自动化。

Together AI 的问题更偏安全运营。工程师需要快速访问基础设施和应用，但手动授权慢、容易出错，还会增加安全风险。Serval 的公开案例显示，Together AI 用 Serval 自动化了 95% 的即时权限申请，同时保留业务理由、授权时长、审批记录和审计轨迹。对安全团队来说，这里的价值超过省时间：访问控制变成了一个可追踪的系统。

• 

Mercor：从帮助台扩展到跨团队自动化平台。

Mercor 的案例说明 Serval 的横向扩展潜力。公司内部支持 250 名员工、150 名外包人员和 30,000 多名外部专家。Mercor 起初用 Serval 解决 IT 支持和外包人员入职，后来扩展到基础设施、支付、工程、安全、人力、办公室支持七个团队。结果包括 4,000 多名外包人员完成入职、超过 60% 的工单被自动化，以及 24/7 全球支持覆盖。Serval 从 IT 切入后，开始成为内部业务团队的自动化层。支付团队可以做支付问题排查，基础设施团队可以做数据库权限流程，人力团队可以做外包人员入职。帮助台可能只是入口，更大的机会在内部运营自动化。

在我们做的一次客户访谈里，有一个很 sharp 的说法：很多 AI 支持工具像一个被产品化的支持工程师，Serval 更像一个被产品化的 IT 工程师。


这组词的差别在于：前者主要减少一线支持人力，后者开始替代一部分 IT 工程师、工作流实施人员和 ServiceNow 管理员的工作。比如构建权限流程、写授权逻辑、连接多个系统、保留审计记录。这类工作原来需要更高技能的人去做，价值密度也更高。这个客户还提到，Serval 让他们推迟了一个 ServiceNow / IT 自动化工程岗位的招聘计划。这比“减少工单”更能说明问题：Serval 的价值开始从一线帮助台进入工作流实施。

第二层证据来自大企业部门级 land。


我们访谈到的大型咨询公司 ITSM 负责人提到，Serval 已经在一个全球消费品公司的仓储物流中心被局部采用，使用场景集中在一个变化很快的运营单元，而非全集团 ITSM 替换。传统系统太重，流程配置跟不上订单、货位、货品协同的变化。Serval 的接入周期按十几天到几十天计算，传统工具常常按数月计算。这个案例后来成为内部优秀案例向其他团队传播。

一家医疗 SaaS 公司的运维负责人也给了类似反馈。公司在 500 人左右时，Jira license 成本上升，自建 ITSM 又需要持续投入工程师维护，于是开始重新考虑商业产品。它的一个事业部已经试用 Serval，其他事业部也在跟进。这个规模很典型：企业已经大到不能靠 Excel / 多维表格管理流程，又还没有到必须采购 ServiceNow 的复杂度。

第三层证据来自反向验证。


一位跨国集团 IT 负责人表示，对 6-10 万人规模的全球企业来说，ServiceNow + Moveworks 的统一性和兼容性仍然很强。大企业有自研 CMDB、历史资产数据、混合云、地区合规和长期积累的流程关系。任何新产品要进入，都要能接上这些底层数据。Serval 在这类客户心智里更像“AI 增强型产品”，还没有成为员工每天使用的主入口。

这类反馈把 Serval 的边界拉回现实。Serval 的短期机会集中在部门级 land、新业务线、创新团队、云原生公司和中型企业。大企业主系统仍然可能是 ServiceNow，Serval 可以先成为某些高变化场景里的执行层，再通过内部口碑横向扩展。

06


.

市场机会：ITSM 之外的四层预算

如果只看 ITSM 软件，Serval 面对的是一个已经很大的市场。Grand View Research 预计全球 ITSM 市场到 2030 年接近 300 亿美元。

但 Serval 更有意思的地方，是它可能把预算池拉宽。


它吃到的第一笔预算未必来自 ServiceNow replacement，更可能来自 Jira IT ticketing、help desk 人力、ServiceNow admin、workflow implementation 和 access governance。

第一层是 ITSM / ticketing 软件。


Jira Service Management、Freshservice、ManageEngine、BMC、ServiceNow 都在这一层。Serval 在 AI-native 客户里的直接替代对象，很多时候更像 Jira IT ticketing，而非整个 ServiceNow。

第二层是 help desk 人力。


大量 L1 / L2 support request 原来由人工处理。AI-native 自动化如果能端到端解决 30%-50% 的 routine tickets，客户的 ROI 会从“省软件费”升级成“省人力时间”。我们访谈到的医疗 SaaS 运维负责人提到，公司已经因为 AI 上线优化了一线运维人力；跨国集团 IT 负责人也提到，现有 AI 入口已经替代了相当一部分一线 help desk 工作。

第三层是 workflow 的自动实施。


传统 ServiceNow 实施、Okta Workflows、Workato、Zapier、internal scripts 都在帮企业做自动化。一位客户在访谈里说，如果 Serval 能覆盖更多重复 workflow，他会重新评估 Zapier 和 Okta Workflows 的预算。Serval 的替代对象已经从 help desk 扩展到 iPaaS / workflow automation。

第四层是权限控制和更广泛的员工支持。


JIT access、least privilege、deprovisioning、audit trail、access review 本来分别落在 IAM、ITSM、security operations 之间。Serval 把这些动作放到统一请求和执行界面里，预算边界会从 IT support 外溢到 security 和 compliance。IT 是入口，HR、Finance、Legal、Workplace、Security 都有类似请求：我要开权限、查政策、申请资源、走审批、追状态、更新系统。Mercor 七个团队的扩展，就是这条路径的早期证据。

所以 Serval 的市场很难用一个 ITSM replacement TAM 概括。更准确的看法是：它先从 IT help desk 切入，再进入 employee support、access governance 和 workflow automation 的交叉区域。

07


.

Why Now?

Serval 这类公司在 3 年前很难成立，原因在于 workflow 的创建本身太难。上一代系统要么依赖拖拽式 workflow builder，要么依赖 SI / consultant，要么依赖内部工程师写脚本。AI 的变化在于，它把 workflow 的创建的门槛降到了自然语言描述。

这带来一个新的 product wedge：自动化本身也被自动化了。IT admin 不需要先成为 workflow engineer。业务方也不需要等一个排期几周的自动化项目。一个重复请求解决过一次，就可以被系统建议沉淀成 reusable workflow。

Jake 访谈里提到的 “slop automation” 也来自这里。自动化太容易，系统会产生重复 workflow：第 20 个 password reset flow、第 10 个 onboarding variant、第 30 个相似 access policy。Serval 为此做了一层 agent，理解已有 workflow、建议合并、删除、重构、加入 approvals。

这其实是 AI-native enterprise software 的第二阶段：


第一阶段，AI 帮你创建自动化。第二阶段，AI 帮你治理自动化。企业缺的是一套能持续维护、去重、审计、解释、更新的 operational system。

08


.

团队：为什么他们会从 IT 这个角度切入

Serval 的创始团队来自 Verkada，这影响了它对 IT buyer 的理解。CEO Jake Stauch 曾在 Verkada 做产品，CTO Alex McLeod 来自 Verkada 工程体系。Verkada 本身面向 IT 和 security buyer，产品涉及硬件、云、安全、权限和企业部署。这类背景让 Serval 团队对 IT leader 的真实痛点更敏感：他们的出发点接近企业 IT 如何采购、部署、审计、承担责任。

COO Tatiana Birgisson 来自 Rippling。Rippling 背后的思路是把 HR、IT、finance 等 employee lifecycle 系统连接起来。这个背景也贴近 Serval 的扩展路径：从 IT support 进入 employee operations。

这个团队组合有一个特点：产品、工程和 GTM 从一开始就放在一起。


Jake 带来 enterprise IT buyer 的产品直觉，Alex 负责双代理隔离和 TypeScript workflow 这样的底层架构判断，Tatiana 带来 Rippling 式的 multi-module enterprise GTM 经验。Serval 看起来像 AI-native ITSM，组织能力上更像一个早期 enterprise platform company。

Jake 的 customer obsession 也值得写进来。


他在访谈里提到自己在 100+ customer Slack channels 里，每天和客户交流。这个细节很不像传统企业软件 CEO 的公关表达，更像这一代 AI application founder 的工作方式。模型能力变化太快，产品每天都可能需要调整。离客户越近，越能把新能力翻译成真实流程。


他对应用层公司的护城河也有一个朴素判断：要保证新模型发布时，自己的产品变得更好，替代风险降低。对 Serval 来说，产品价值落在模型之外的边界、权限、审批、日志、workflow、客户流程和部署信任上。

Serval 还有一个值得注意的组织设计：FDE。


企业 automation 产品很难完全靠 self-serve 推开，因为每个客户的审批、权限、系统、历史流程都不同。Serval 自己也承认，很多时候 revenue 的瓶颈在 deployment capacity，而非 demand。它后来推出 Serval Start，招募有创业意图的人做 FDE，本质上是在用 founder-density 的人去抽取客户 workflow，再把这些 workflow 变成可复用资产。

09


.

竞争格局

这个市场会非常拥挤，因为它同时碰到 ITSM、employee service、IAM、workflow automation 和 agent platform。

•

 ServiceNow + Moveworks

ServiceNow 是最强的在位者。它有 ITSM 客户基础、CMDB、工作流、审批、审计和企业信任。2025 年，ServiceNow 宣布以 28.5 亿美元收购 Moveworks，把员工 AI 助手和自己的工作流平台结合起来。前台对话入口和后台工作流执行，正在被放到同一套平台里。ServiceNow 的优势是大企业兼容性。很多超大型客户已经把 CMDB、事件、变更、资产、审批都放在 Now Platform 上。Serval 要进入这些客户，必须和已有系统共存。

•

 Salesforce Agentforce IT Service

Salesforce 也在进攻 ITSM。Salesforce 


2026 年公开表示，已有 180 个组织选择 Agentforce IT Service，用统一的智能体平台替换传统支持工具。Salesforce 的优势是 CRM、Service Cloud、Data Cloud，以及中型企业和大企业渠道。它天然会把 IT 服务、人力服务、客户服务放在同一个智能体平台叙事里。

•

 Console、Ravenna、eesel AI 等 AI-native / lightweight 竞品

Console 更接近 AI-native ITSM 直接竞品。Ravenna 是 Slack-first internal support，2025 年融资 1500 万美元，定位也很贴近 internal IT / ops teams。eesel AI 更像 layer-on-existing-ticketing philosophy，覆盖 Zendesk、Freshdesk、Jira、Slack 等系统。这些 lightweight 工具在 SMB 和 mid-market 里有威胁：部署轻、价格低、替换成本小。Serval 如果走更 enterprise 的 workflow / access / audit 路线，需要证明自己的复杂度换来了更高自动化率和更强安全治理。

•

 Glean、Workato、Zapier、Okta Workflows

另一类竞争来自更 horizontal 的 workflow / enterprise context 平台。Glean 从 enterprise search 和 assistant 往 agent platform 走，Workato / Zapier / Okta Workflows 原本就承载很多企业自动化。Serval 如果只做 workflow automation，会遇到这些玩家；它的差异必须来自 IT / access / audit / employee support 的原生场景。

所以 Serval 的竞争定位不只是 “next-gen ServiceNow”。更准确地说，它在争夺一块新的交叉地带：AI-native 员工支持 + 权限控制 + workflow 自动化。

10


.

更大的可能：ITSM for AI Agents

Serval 更长期的想象空间，来自企业 agent 自身的管理问题。


现在企业已经有大量 service accounts、API keys、workload identities。未来每个员工、每个团队、每个系统旁边都会有 agent。一个 agent 要替人工作，就必须拥有身份、权限、上下文和审计记录。它会读数据、调用 API、修改系统、触发审批、创建工单、访问文件、写入系统。

这听起来像 ITSM，也像 IAM，也像 workflow automation，也像 agent governance。

Serval 当前的几个设计自然贴近这层需求：

•

 workflow 以代码形式存在，可审计、可版本化；

•

 action 通过 approvals 和 API scopes 限制；

•

 access request 和 JIT provisioning 是核心场景；

•

 agent 被分成构建侧和执行侧；

•

 workflow 可以接入 Git、SIEM、SSO、SCIM、HRIS、IdP、MDM、ticketing system；

•

 管理员可以定义每个团队、每个工具、每个 agent 能做什么。

如果 enterprise agents 真的成为下一代工作接口，企业需要一个地方回答这些问题：

•

 哪些 agent 可以调用哪些工具？

•

 谁批准了这些工具？

•

 每一次 action 执行了什么？

•

 哪些 workflow 正在重复创建？

•

 哪些权限应该自动过期？

•

 哪些失败应该进入新的 guardrail？

• 

哪些流程可以从手工 ticket 迁移到自动执行？

这个位置可能会成为 ITSM for AI agents 或 agent governance OS 的早期形态。


这也是 Serval 最有意思的观察角度：它现在服务的是人类员工的请求，将来可能服务的是企业里所有 human 和 non-human workers 的请求。

11


.

风险

第一，CMDB 和 legacy enterprise mess。


AI-native 公司没有太多历史包袱，IT 资产以 SaaS 和 cloud resources 为主。大型跨国企业有复杂 CMDB、legacy device data、hybrid cloud、regional compliance 和自研系统。一位大型集团 IT 负责人把 CMDB 表示：大量基础设备和历史资产数据都在自有库里，重新治理不经济。Serval 要进入这类客户，必须补强 asset / CMDB / data integration。

第二，incumbent 的系统优势。


ServiceNow、Salesforce、Microsoft、Atlassian、Okta 都已经在 agent 化自己的平台。它们拥有安装基础、权限数据、工作流和采购关系。对大型跨国企业来说，ServiceNow + Moveworks 的兼容性和单一供应商管理便利性仍然很强。Serval 必须在速度、产品体验和 white-box automation 上维持领先。

第三，AI-native 客户到 traditional enterprise 的跨越。


Perplexity、Together AI、Mercor 这类客户很愿意尝试新工具，也更 API-first。传统企业的采购、合规、数据驻留、系统兼容都更重。部门级 land 到扩张到集团级需要时间。

第四，GTM 和渠道。


Serval 早期客户很多来自 SF AI 圈层、Verkada network 和投资人网络。这个圈层质量很高，但数量有限。要进入 mid-market 和传统企业，它需要更强的 content marketing、community、SI/channel 和区域伙伴。大型咨询公司专家给出的建议也很明确：与埃森哲这类渠道建立合作，能更快获得市场信任。

第六，模型迁移风险。


Jake 在访谈里提到，新模型发布经常很难 plug-and-play。一些能力变好，一些行为变差，过去围绕旧模型 quirks 建的 prompts 和 infra 需要调整。Serval 需要持续投入 eval、slow rollout 和 model routing。

12


.

怎么判断 Serval 是否真的走出来

Serval 已经证明了一件事：AI-native 公司愿意让它处理真实的 IT 请求。接下来要证明的，是这套东西能不能从一个好用的 help desk，变成企业内部的执行系统。

我们会重点看五件事。

第一，自动化有没有做到最后一步。很多产品能回答问题、分类 ticket、推荐下一步，真正难的是完成动作：权限开了，access 到期回收了，onboarding 账号建好了，审批和日志都留下来了。Serval 应该被看的指标是端到端完成率，而非 deflection rate。

第二，新 workflow 上线速度有没有持续变快。AI 生成 workflow 的承诺很直接：业务流程变了，系统也能跟着变。好的信号是，第 100 个 workflow 比第 10 个更容易建，客户自己能改，重复流程能被合并，workflow 越用越干净。

第三，access governance 会不会成为主线。JIT access、deprovisioning、least privilege、approval、audit trail，如果只是 help desk 的一个功能，天花板有限；如果成为 IT 和 security 共用的动作层，Serval 在企业里的位置会重很多。

第四，能否从 AI-native 客户，进入更复杂的大企业。Perplexity、Together AI、Mercor 是很好的早期客户，因为它们 API-first，也愿意拥抱新工具。更大的企业有旧 CMDB、混合部署、地区合规、自研系统和复杂采购。Serval 不需要一次性替换所有东西，但需要和这些系统共存，读到正确的数据，写回正确的状态，并给安全团队足够完整的审计。

第五，能否从 IT 走向员工运营。Mercor 把 Serval 用到 infrastructure、payments、engineering、security、HR 和 office support。这个扩展如果能在更多客户里重复，Serval 就会更接近内部运营自动化 layer。

Serval 的故事有意思，正因为它从很小的请求开始。开一个 SaaS 权限、重置一个密码、创建一个 Google Group、处理一次 JIT access，这些事情不性感，但它们是 enterprise agent 进入生产前必须通过的基本测试：能不能识别用户身份，能不能理解权限边界，能不能执行稳定动作，能不能留下记录，能不能在出错后追溯和修正。

如果一个 agent 不能可靠地开权限，它也很难承担更复杂的企业工作。所以 Serval 的价值，会从 help desk 的聊天体验，移向一个受控的 action surface：员工在这里提出请求，管理员在这里定义边界，agent 在这里执行动作，安全团队在这里审计结果。

模型公司会继续把模型做强。企业客户要解决的下一层问题，是怎么让这些能力进入组织，又不让组织失控。Serval 最值得跟踪的问题也在这里：它能否成为企业定义“谁可以让哪个 agent 做什么事”的地方。这个问题一旦成立，机会会比 ITSM 本身更大。

 排版：夏悦涵

延伸阅读

拆解 Anthropic：最好的 AI 公司，可能也是一种组织发明

The Era of Agent：拾象 AGI 投资洞察

AI Labs 都在用，ClickHouse 能成为 AI 日志的实时分析引擎吗？

Supabase：百亿美元估值，vibe coding 的默认后端？

深度讨论新一轮模型发布：当智能进入月更时代 | Best Ideas

## 关联

- [[海外独角兽]]

## 备注

> 置信度 0.70：微信公众号文章。
