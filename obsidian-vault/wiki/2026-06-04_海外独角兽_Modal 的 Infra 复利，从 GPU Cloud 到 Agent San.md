---
type: knowledge
入库日期: 2026-06-04
置信度: 0.70
主题: Modal 的 Infra 复利，从 GPU Cloud 到 Agent Sandbox
分类: 信息挖掘/微信公众号
来源: [外部-微信公众号/海外独角兽]
tags: [海外独角兽, 微信公众号]
---

# Modal 的 Infra 复利，从 GPU Cloud 到 Agent Sandbox

## 核心结论

（微信公众号文章，自动抓取。详见全文。）

## 详细内容

### 背景

来源：海外独角兽
原文链接：https://mp.weixin.qq.com/s/aL_3lNxtbYwni5mV1CCBIw

### 正文

作者：Daniel

编辑：Cage

Modal 是 Agent Infra 领域的重要公司。他们 2021 年在纽约公司成立。一开始用底层编程语言 Rust 从零构建了一套专为 AI workload 设计的 runtime。让开发者可以用 Python 直接调用云端 GPU、部署推理服务，产品体验接近“开箱即用的 AI 云”：server less 按秒计费，不运行时不收费，把复杂 AI 计算变成可可以弹性调用、低运维成本的开发者体验。

Modal 更值得关注的地方在于其近期增长极快的 Sandbox 业务，目前已经贡献了超过三分之一收入，成为清晰的第二增长曲线。飞速增长的背后，是公司多年来积累的底层 ai infra 实力：为推理优化的冷启动、为 sandbox 做的文件系统与 snapshot、为 GPU 调度做的利用率优化，能在不同产品线之间产生复利。这套底层 infra 让 Modal 的长期价值不在于转售 GPU，而是有机会成为 AI agent 时代重要的云端执行环境。

Modal 刚完成 3.55 亿美元 Series C，投后估值 46.5 亿美元。公司自 2025 年 9 月以来增长 5 倍，目前 年化收入超过 3 亿美元。客户包括 Scale AI、Ramp、Substack、Suno、Harvey、Mistral、Cognition 等一批 AI 领域最知名的公司。

我们认为，Modal 的核心壁垒不在单一业务，而在坚定自建底层 infra 产生的复利。公司早期用 Rust 自研 ，抛弃了 Kubernetes 选择了一条困难的道路，为未来的技术路线选择和应对大规模并发打下了坚实的基础。在 AI Agent 大规模爆发后，Sandbox 成为了 Agent Infra必不可少的基础设施。Modal 在几种 Sandbox 隔离路线中选择了更为复杂的 gVisor 打法，在性能取得均衡的同时复用了其 Serverless GPU 的管理能力。Modal 不只是一个模型推理时使用的 serverless GPU 平台，而是有望成为 AI agent 执行层关键的 infra 环境。

01


.

核心判断

• 

Sandbox 是 Modal 的第二增长曲线，将其从 serverless GPU 平台推向 Agent Runtime 平台。

Agent 需要一个安全、快速、有状态、可弹性扩缩的工作环境：


不能污染宿主系统，也不能每次都从零开始；既要能保持上下文和中间文件，又要能在高并发下快速启动和销毁。Modal Sandbox 正好对应这一组需求。

它继承自 Modal 自研的底层 infra，以 gVisor 作为主要隔离路线，在更好兼容内部平台的同时，于安全性与速度之间取得均衡。关键在于，Modal 的 sandbox 不是一个孤立的执行盒子，而是能与 GPU inference、batch job、volume、queue、training workflow、Python pipeline 和文件系统自然组合：这让它在复杂场景里更有优势。

• 

自研底层 infra 是 Modal 的核心壁垒，直接转化为更好的用户体验和资源效率。

Modal 的核心壁垒来自公司在 2021–2023 年期间自研的一整套底层计算基础设施。它没有简单在 Kubernetes、Docker 和云厂商 API 上封装一层开发者体验，而是围绕 AI workload 的特点，重新构建了容器启动、资源调度、文件系统加载和安全隔离等核心组件，包括 Rust container runtime、调度器、FUSE 懒加载文件系统、snapshot 机制和 gVisor 隔离层。

这些底层能力具备跨产品线复用效应。Modal 为 inference 优化 cold start，sandbox 也受益；为 sandbox 做文件系统和 snapshot，coding agent、RL evaluation 和 repo automation 也受益；为 GPU workload 优化调度和利用率，推理、小规模训练、GPU-backed sandbox 也受益。每条产品线不是孤立发展，而是在共同打磨同一套 AI compute substrate。Modal 的护城河不是某一个单点产品，而是底层 infra 的复利。其他公司要同时做好，难度要高得多。

• 

AI workload 正在从静态部署走向动态计算，Modal 受益于 serverless compute 的结构性扩张。

AI 推理和 Agent workload 的计算形态，天然不同于传统云服务和大模型训练。训练需要长时间、稳定、大规模的 GPU 集群，更接近“固定产能”；但推理、Agent 执行、sub-agent 调度、代码运行、批量评估和 RL rollout 都具有明显的


无状态、高波动、碎片化、短生命周期


特征。每一次用户请求、每一个 sub-agent、每一条 evaluation trajectory，都可能对应一个独立的 compute instance。

这类 workload 与 serverless 的“即用即走、按需扩缩、用完释放”高度契合。未来 sub-agent 的爆炸式增长，会让计算需求从“模型调用次数”扩展为“动态任务执行次数”。Modal 正处在这一变化的核心位置。它不是简单提供 GPU 资源，而是把 GPU、CPU、容器、函数、sandbox、batch job 和文件系统抽象成可以通过 Python 动态调用的计算单元。

02


.

潜在风险

• 

模型层竞争

Anthropic 于 2026 年 4 月 8 日发布的 Claude Managed Agents 是结构性事件，不是普通产品迭代：模型厂商首次正式向上吞噬"agent orchestration + sandbox"层，对 AI Infra 类初创，特别是 Sandbox 类企业造成直接冲击。而 Anthropic 选取的技术路线也与 Modal 较为相似，可能造成直接冲击。

• 

Sandbox 企业迁移成本低

Sandbox 行业尚属竞争早期，各个技术方案各有优劣。客户将一套 Sandbox 调用代码从 Modal 迁移到 E2B、Daytona、或自建 Firecracker，工程成本极低。头部客户做大后会面临 in-house 替代的风险。专家访谈里提到，如果切到自研方案或其他第三方，虽然用户体验会变差，但在一两周内能完全恢复。

• 

机群利用率、真实成本风险

在 inference 业务上，CEO Erik 在 2024 年一档播客上曾对外披露，Modal 毛利约 20–30%，显著低于 hyperscaler 软件产品的 60%+，以及 Snowflake、Databricks 等平台级公司的 70%+。


本质是 Modal 不自控上游 GPU 供给，上游租赁成本占据主要 COGS。


 这种结构下，提升毛利的唯一路径是提升机群利用率：即让闲置 GPU 尽可能接满多租户请求。负载多样性不足，则可能限制多租户调度带来的利用率收益。

03


.

主要业务

Modal 把自己定位为 High-performance AI infrastructure。公司在 2021–2023 年自研的一整套底层 infra（Rust container runtime + MIP 调度器 + FUSE 懒加载文件系统 + gVisor 隔离），同时支撑着 Modal 的全部产品。

用户不直接管理 Kubernetes、节点、容器、镜像、GPU 调度，而是用 Python 定义函数、容器、sandbox、batch job、GPU inference endpoint，Modal 负责背后的启动、调度、扩缩容、日志、存储、snapshot 和资源复用。

所以它的产品线看起来很多：Inference、Sandbox、Training、Notebook、Batch，但底层其实复用的是同一组核心能力：


冷启动、调度、容器运行时、文件系统、snapshot、存储挂载、多云资源池、日志和状态管理。

其中，最为重要的两条主线一条是 


serverless GPU compute / inference infrastructure，

另一条是

 agent runtime / sandbox infrastructure。


前者服务 AI 应用的推理、批处理、训练辅助和动态 GPU 调度；后者服务 coding agent、app generation、RL evaluation 等需要安全执行代码的场景。

Serverless Compute

训练大模型和模型推理是两种完全不同的工作负载。

训练大模型通常需要数百甚至数千块 GPU 同步工作数周甚至数月，更像一支交响乐团：所有乐手必须同时在场、持续协同，任何一个环节掉队都会影响整体效率。这类任务需要稳定、大规模、长时间运行的 GPU 集群，因此更适合 CoreWeave、Lambda、Crusoe、Nebius 等 GPU neocloud，或者 hyperscaler 提供的裸金属 / 集群型资源。Serverless 的“即用即走”模式并不是训练超大模型的最佳形态。

推理则完全不同。推理请求天然碎片化，每个用户请求通常是独立的：用户发出一次查询，模型完成一次计算，请求结束，资源即可释放。更重要的是，推理流量高度波动，白天高峰、夜间低谷、产品发布、用户活动、突发事件都会带来剧烈变化。对于 AI 应用来说，推理负载具备三个特征：


任务独立、流量波动大、资源需求难预测。


这正是 serverless 架构最适合处理的场景。

Modal 的价值在于，把 GPU 从“需要提前购买、手动部署、持续占用的稀缺资源”，抽象成“可以通过 Python 代码随时调用、按秒计费、自动扩缩的计算单元”。开发者不需要管理 Kubernetes、容器编排、GPU 调度、镜像缓存和底层云资源，只需要定义函数、选择资源、部署服务，Modal 负责后面的启动、调度、扩缩容、日志和运行环境管理。

在 GPU 编排与基础设施层，竞争力主要集中在：


容器能多快启动、GPU 能多灵活调度、模型能多顺滑部署上线。


 这三件事正是 Modal 过去几年自研容器运行时、文件系统和调度器所积累的核心能力。

Modal 的优势不是拥有最多 GPU，而是更高层次地抽象 GPU。通过开发者体验、冷启动速度、多云调度和平台组合能力，把 GPU 变成 AI 工程师可以直接编程调用的基础设施。

Sandbox

Modal Sandbox 的 v1 原型由 CTO Akshat 在 2023 年的某个周末搭出来；此后在 beta 状态打磨了大约一年，期间 Lovable、Quora（Poe）等核心客户已经在生产中跑了；2025 年 1 月 21 日正式 GA，并配套发布了 SWE-bench 原生集成、文件系统 snapshot 等关键能力。

Modal 的产品战略重心已经从 inference转向 sandbox runtime for AI agents。

目前公司更多工程资源压在 Sandbox 产品线上，而且多次 release note 明确点名 Claude Code 和 coding agents。这是个更大、更早期、竞争更激烈的市场（E2B、Daytona、Cloudflare、Vercel 直接竞争）。

进入 26 年来，随着 Agent 的爆发，Sandbox 的受关注程度指数级上升。 Sandbox 的主页浏览量在两个月内涨了 300%+。

Modal 此前积累大量底层能力，包括快速容器启动、自研文件系统、gVisor-based isolation、调度器、动态存储挂载和多云资源管理。Sandbox 只是把这些已有能力通过一个更适合 agent 的接口暴露出来。

Modal 的 Sandbox 处在 Agent 基础设施的


执行层（Runtime / Sandbox），


 负责"动手"：当编排层决定要执行一段代码时，需要一个真实的计算环境来运行它。这个环境必须满足四个条件：

•

 安全隔离：AI 生成的代码不可控，不能让它影响宿主系统。

•

 快速启动：Agent 每一步都可能触发代码执行，启动慢则整个任务链路被拖垮。

•

 有状态：Agent 的工作是多步骤连续的，第 3 步需要看到第 1 步装的依赖和第 2 步写的文件。

•

 弹性扩缩：一个用户任务可能触发 1 次执行，另一个可能触发 200 次，完全不可预测。

Modal 的优势

1. 

生态

Modal 的高明之处不在于单独提供一个 sandbox，而在于它把 sandbox 放进了一个更完整的 AI compute 生态里。如果用户接入 Modal，sandbox 不只是一个用来运行不可信代码的隔离环境，还可以直接触达 Modal 体系内的模型推理、模型训练、存储卷、队列、批处理任务和 Python workflow。换句话说，Modal 正在打破“sandbox 只是安全执行代码”的传统叙事，把它升级成一个可以被动态调用、组合、扩展的计算单元。

2. 

合规

Lovable 曾经评估过 E2B，但在安全审查中发现，截至 2025 年 6 月，E2B 对欧洲公司的支持还不够成熟：数据可能传到海外，DPA 数据处理协议和安全文档也不够完整。 这就是 Modal 的强项，他们的合规性是“开箱即用”。Modal 更早进入企业计算和 AI infrastructure 场景，因此在这部分比很多新兴 sandbox 公司更成熟。

3.

 扩展性

Modal 是一家更成熟、也更早证明自己能处理大规模 AI workload 的公司。Lovable 专家评价，Modal 虽然在某些 sandbox 细节上还略显粗糙，但在需要沙箱、挂载文件系统、日志记录和地理位置控制时，整体表现更优。Figma 评估了运行长时间会话时的故障率，以及两者提供的监控工具等。在可靠性方面，发现 Modal 稍微可靠一点。

客户对 Modal 的并行化能力印象尤其深。Modal 的强项不是单个 sandbox 的体验，而是把大量计算任务快速、稳定地扩展出去。例如，它可以同时开启大量并行 agent 去扫描 GitHub 仓库，也可以在很短时间内完成长音频的转录和总结。这类场景的本质不是“启动一个 sandbox”，而是“快速启动成千上万个计算单元，并稳定管理它们的生命周期”。

这点在 RL workload 中会更加重要。Amplify 的文章提到，Modal 的一个大型 AI lab 客户已经在 RL 工作负载中运行约 10 万个并发 sandboxes，目标是达到 100 万并发。对 coding model 的 RL 训练来说，每条 trajectory 都需要在隔离环境中执行代码、运行测试、获得可验证反馈。任务数、采样 trajectories 数量和每条 trajectory 的执行步骤数相乘后，sandbox 需求会快速放大。Modal 在这里承担的已经不是普通代码执行工具，而是大规模 agent rollout / evaluation / verification 的底层基础设施。

4. 

性价比

客户评价 Modal 的性能和可靠性是目前见过最好的之一。它的价格处于行业中游，不算最贵，但也不是最低价。真正重要的是，Modal 在性能、稳定性和成本之间取得了相对好的平衡。

这对 AI-native 应用非常关键。很多 “vibe coding” 平台收入增长很快，但利润率很薄，对计算成本极度敏感。如果 sandbox 或 agent runtime 的单位成本过高，随着用户规模扩大，毛利会很快被吞噬。专家也提到，E2B 价格偏贵，而 Daytona 这类 stateful dev environment 的成本模型在规模扩大后也可能快速上升。

当然，这个市场仍然很早。也有专家评价，整个 sandbox / agent runtime 行业还没有完全成熟，很多产品体验仍然没有准备好。Modal 擅长 GPU、serverless compute 和大规模并行任务，但在纯 sandbox 体验上可能还没有完全打磨到位。只是即便如此，它可能已经是这一行里相对领先的选择，因为其他竞品在企业可用性、可靠性、合规性或规模化能力上问题更多。

客户用例：Ramp — 内部 Background Coding Agent 的云端执行底座

Ramp 是 Modal Sandbox 在企业内部 coding agent 场景中的典型案例。Ramp 自研的 background coding agent “Inspect” 用于自动写代码、运行测试、验证前后端改动并提交 PR。它不是简单的代码执行器，而是一个拥有完整工程上下文和验证工具的云端工程 agent：


可以读取代码仓库、修改文件、运行测试、查询 telemetry、检查 feature flags，并通过浏览器完成前端视觉验证。

Modal 在其中扮演的是云端开发环境和执行底座。每个 Inspect session 都运行在独立的 Modal Sandbox 中，包含完整 full-stack development environment。根据 Ramp 和 Modal 的披露，Sandbox 环境中包含 Vite、Postgres、Redis、Temporal、RabbitMQ 等工程师本地开发常用服务，并运行 OpenCode 作为 coding agent，同时配备 VS Code server、web terminal、VNC stack 和 Chromium，支持人工编辑、终端操作和 before / after screenshots。由于这些操作都发生在隔离的 Sandbox 中，agent 不会污染工程师本地 checkout，也不会直接影响生产系统。

Ramp 选择 Modal 的关键原因之一是启动速度。


Ramp 为每个 repository 维护预构建环境：每 30 分钟通过 Modal Cron clone repo、安装依赖、运行初始化 build，并保存 filesystem snapshot。用户启动 Inspect session 时，Modal 可以直接从最新 snapshot 创建 Sandbox；由于 snapshot 最多只落后主分支 30 分钟，后续同步 head repo 几乎是即时的，session 通常可以在几秒内开始处理 prompt。

Filesystem snapshot 也让 Inspect 从一次性代码执行工具，变成可持续对话、可恢复状态的 background coding session。Agent 完成一轮修改后，环境状态可以被保存；如果 Sandbox 后续退出，用户再次发 follow-up prompt 时，可以从之前状态恢复。对真实工程任务来说，这很重要，因为 coding agent 往往需要多轮修改、测试、review 和继续修复，而不是一次 prompt 完成。Modal 在这里提供的不是简单算力，而是一个可恢复、可延续、可协作的工程环境。

高并发则是另一个关键价值。Inspect 的设计目标是让员工不需要“省着用 agent”：用户可以同时启动多个版本的同一条 prompt，尝试不同方案、切换不同模型，甚至让 agent spawn child sessions 跨 repo 并行研究。每个 session 都运行在独立的 Modal Sandbox 中，彼此隔离，不会互相抢占本地资源，也不会给用户 laptop 带来负担。Ramp 团队因此将其形容为让每个 builder 都拥有“数百台可以同时工作的电脑”。

左右滑动查看完整图文

04


.

市场竞争

GPU-as-a-Service

GPU 作为目前 AI 世界最为重要的算力基建，围绕它诞生了很多商业模式，按抽象层次从低到高，市场可以分成五层：

L3 的核心竞争，是谁能把 GPU 从传统云里的“机器资源”重新抽象成开发者可以直接调用的 AI-native runtime。Modal、RunPod、Beam、Replicate、Baseten、Fireworks、Together AI 都在这一层展开竞争：它们共同解决的是开发者不想管理集群、不想维护 Kubernetes、不想长期预留 GPU，只希望像调用函数或容器一样，按秒启动、按需扩缩、快速部署推理、训练、batch job 或 agent workload。

Baseten 和 Fireworks 是 Modal 在 


production inference 


上最直接的 AI-native 对手。Baseten 的定位非常清楚：未来会有大量专用模型在生产环境中运行，因此它主打 fast、reliable、secure inference，把模型部署、扩缩容、版本管理和生产化运维做深。官方表述也明确把自己定义为把 custom models 推向 production 的基础设施。Fireworks 的叙事类似，但更偏 


open model / enterprise inference cloud


。它由 PyTorch 背景团队创立，强调企业不会只依赖少数 closed API，而是会部署、定制和优化大量开源/自有模型。

Modal 的优势在于 DX、底层工程和平台广度。它从 Python 开发者体验出发，把 Function、Sandbox、Training、Notebook、Batch 等产品线放在同一套底层计算与调度体系上，背后包括自研 Rust container runtime、多云 GPU 池化、快速部署与弹性伸缩能力。因此，Modal 更适合 Python-heavy 的 AI 工程团队：他们不只是要把一个模型部署上线，而是要频繁实验、运行 batch jobs、调度 GPU、启动 sandbox、做 agent runtime，甚至把训练和推理流程放在同一个平台里完成。Modal 的核心不是某一个单点能力，而是把 AI workload 所需的多个 primitives 统一成一个开发者友好的计算平台。

Hyperscalers 当然也在进入这一层，但目前还没有对 AI-Native 玩家 形成直接威胁。


原因不在于它们缺少底层算力，而在于它们的产品抽象、开发者体验和灵活性，仍然更像传统云服务的延伸，而不是为 AI-native workloads 重新设计的 runtime layer。

AWS 的相关产品包括 Bedrock AgentCore 和 SageMaker Serverless Inference，方向上都可以被理解为对 L3 agent runtime / serverless inference 层的布局。但 AWS 的问题是抽象相对封闭：SageMaker Serverless Inference 并不覆盖 GPU 场景，Bedrock AgentCore 更依赖 AWS 认可的模型和服务体系，灵活性弱于 Modal 这种面向任意 Python workload、任意容器和多云 GPU 池的开发者平台。因此，AWS 在企业采购和合规层面有天然优势，但在 DX、冷启动速度和 agent sandbox 的通用性上，目前还不是 Modal 的直接替代品。

GCP 的 Cloud Run GPU 更接近 Modal 的方向：支持容器化 workload、按秒计费，并开始覆盖 L4、T4、A100 等 GPU 类型。但 Google 的短板仍然是产品推进和开发者运营能力。Cloud Run GPU 在能力形态上有竞争力，但要真正替代 Modal，还需要更好的文档、生态、销售支持和面向 AI 工程团队的端到端体验。不过，如果 Google 能持续兑现 TPU 和 AI infra 的底层优势，它在 ML workload 上的吸引力会逐渐增强。

Azure 的路径则不同。它更强调 Azure OpenAI、企业集成和既有云客户的工作流迁移，而不是打造一个通用的 serverless GPU / agent sandbox 平台。Container Apps 与 Azure OpenAI 的组合对企业用户有吸引力，但战略重心仍是 OpenAI 生态和企业云集成，而不是 Modal 这类开发者优先、workload-first 的 AI runtime。因此，短期内 Azure 对 Modal 的直接压力相对有限。

Sandbox-as-a-Service

在 AI Agent 出现之前，sandbox 只是云计算和开发者工具里的边缘需求。开发者写代码通常在本地运行，部署时交给服务器、容器或 CI/CD runner；只有在测试不可信代码、运行 notebook、执行用户提交脚本时，才需要一个隔离环境。这个市场长期存在，但并不是一个足够大的独立基础设施层。

Agent 改变了这一点。大模型不再只是生成文本，而是在生成代码、修改文件、调用工具、运行命令、读取结果，并在多轮循环中持续修正自己的行为。每一个 Agent 都需要一个“可执行的工作空间”：它要能安全运行不可信代码，要能保存上下文和中间产物，要能在失败后回滚，要能并发尝试多条路径，还要能在用户重新回来时恢复之前的状态。换句话说，sandbox 从一个偶发的安全工具，变成了 Agent 工作流中的核心运行时。

这也是为什么过去两年出现了一批 AI-native 的 sandbox / agent runtime 公司。它们和传统云厂商的差异，不在于有没有容器、虚拟机或 serverless 计算，而在于设计目标完全不同。Hyperscalers 提供的是通用计算原语：Lambda、Cloud Run、Fargate、VM、Kubernetes、Batch 等，适合一次性任务、标准化服务部署和大规模弹性计算。但 Agent 需要的是交互式、状态化、可暂停、可恢复、可复制、可观测的执行环境。

传统云可以拼出类似能力，但体验重、冷启动长、状态管理分散、权限边界和开发者接口不够 agent-native。因此，这一层给了新公司切入的机会。

隔离技术路线

AI Sandbox 的底层隔离路线，大致可以分成五类：container-based、Firecracker / microVM、gVisor、自研 VMM，以及 V8 isolate。

隔离技术路线决定了 AI sandbox 的产品边界。Modal 的 gVisor 路线介于容器和 microVM 之间，牺牲了一部分完整 Linux syscall 兼容性和 Firecracker 式硬隔离叙事，但换来了更高资源密度、更好的 GPU 结合能力，以及状态保存 能力。

如果将隔离技术路线的四大关键能力（隔离强度、资源利用率、持久化、启动速度），放到象限图中，可以看到，Modal 在其中走的是更均衡、稳妥的路线。

左右滑动查看完整图文

Sandbox 公司与模型厂商的关系

•

 Anthropic Managed Agents

4 月 8 日，Anthropic 上线 Claude Managed Agents，把"跑 agent 所需要的一切基础设施"打包成了一个托管服务。

Anthropic 的 Managed Agents，本质上是把长任务 agent 从一个脆弱的单体容器，拆成可恢复、可替换、可扩展的运行架构。


 它把 agent 拆成三层：Session 记录所有事件，是持久化状态；Harness 驱动 Claude 推理和 tool call；Sandbox / Hands 负责真正执行代码、操作文件、调用外部环境。Anthropic 官方强调，Session 不是 Claude 的上下文窗口，而是一个存在于上下文之外的 durable event log，模型可以按需读取历史事件，而不是把所有历史都塞进 context window。

这套架构的关键变化是把 brain 和 hands 解耦。


 过去 harness、session、sandbox 绑在同一个容器里，容器启动慢、失败难恢复、安全边界也弱；现在 sandbox 被抽象成一个普通工具，接口类似 execute(name, input) → string。如果 sandbox 挂了，它只是一次 tool call 失败，Claude 可以决定是否 retry，系统也可以重新 provision 一个新的执行环境。这样 inference 可以先启动，sandbox 按需启动，Anthropic 官方披露 p50 TTFT 下降约 60%，p95 TTFT 下降超过 90%。

根据 26 年 5 月 Anthropic 的更新， Execution environment 正式支持部署在客户侧。Agent loop 依然是留在 Anthropic，负责会话编排、上下文和错误恢复；而整个执行环境，工具执行、代码、文件系统、网络出口 ，可以放到企业自己的基础设施里，或者放到 


Cloudflare、Daytona、Modal、Vercel 


这些托管 sandbox provider 上。未来模型公司可能不会自己吃掉所有执行环境，而是掌握 agent control plane，再把 runtime 接到外部生态。

这一动作说明，Anthropic 在 Sandbox 上展示一个开放的态度，既提供 Sandbox 服务同时支持用户侧部署。而 Modal 作为被点名的托管商被大模型背书，也会有更多的客户曝光。

•

 OpenAI Agents SDK

左边是自己做 agent loop / tool integrations / components，右边是 SDK 包圆。

OpenAI Agents SDK 的动作，是把 sandbox 放进 agent runtime 的标准接口里。


 过去开发者做 agent，往往把 harness、agent loop、tools、filesystem 全塞进同一个执行环境里，原型快，但生产环境很脆弱：权限、密钥、文件系统、工具调用、容器生命周期都混在一起。OpenAI 新版 Agents SDK 的核心变化，是把 harness 从 compute 里拆出来：harness 负责模型调用、agent loop、tool routing、状态恢复和安全控制；sandbox 只负责执行命令、读写文件、运行代码、暴露端口和保存工作区状态。官方文档明确把这叫做 separating harness from compute。

它允许 bring your own sandbox，并内置支持 Blaxel、Cloudflare、Daytona、E2B、Modal、Runloop、Vercel 等 provider；同时用 Manifest 定义 workspace，把本地文件、输出目录，以及 S3、GCS、Azure Blob、Cloudflare R2 这类存储挂载抽象出来。换句话说，OpenAI 不需要拥有每一个 sandbox，它只要定义 agent 怎么使用 sandbox：文件放哪里、命令怎么跑、状态怎么恢复、结果怎么回到 agent loop。

OpenAI 并不下场主动做 Sandbox，而是让 sandbox 生态充分竞争、降低 agent 落地门槛，最终让更多 workload 流向 token 和 tool use 消费。

05


.

技术壁垒拆解

Modal 的核心技术壁垒，不是简单把 Kubernetes、Docker 或云厂商 GPU 实例重新包装成更好的开发者体验，而是围绕 AI workload 的动态性，重做了一整套运行时基础设施。AI 应用和传统 Web 服务不同：推理请求会突然放量，batch job 会瞬间并发上千个任务，agent sandbox 会频繁创建、执行、销毁环境。

很多组织在高峰需求下，GPU Allocation Utilization 也低于 70%，实际常见情况甚至接近 10–20%。这意味着大量 GPU 钱付出去了，但真正有效产出不高。

一个 GPU inference replica 一般拆成四步：

第一步，申请一台新的 GPU 机器，并做健康检查。这个可能要几分钟到几十分钟。GPU 不像普通 CPU 机器那么稳定，硬件故障、驱动问题、Xid error 都可能发生，所以启动前不能假设它一定健康。Modal 也特别强调，GPU 健康检查非常关键，因为 GPU 的故障率并不低。

第二步，加载应用程序和文件系统状态。说白了，就是把容器镜像、Python 环境、CUDA 库、PyTorch、模型服务代码、各种依赖文件准备好。传统方式类似 docker run，需要把完整 root filesystem 拉下来，而一个操作系统和 AI 容器可能有几万个文件、几个 GB 甚至更大。

第三步，在 CPU / host 侧启动应用。比如执行 import torch，加载 Python 包，初始化各种对象，读取文件，和驱动交互。Modal 说，光是 import torch 这类动作，就会触发大量 Python 代码和系统调用。

第四步，在 GPU / device 侧初始化应用。这个通常是最慢的。模型权重要从存储加载到 GPU 显存；推理引擎，比如 vLLM 或 SGLang，还要做 CUDA graph capture、Torch compiler 编译等准备工作。这些步骤可能需要几十秒到数分钟，甚至更久。

一篇 blog 文章解释了 Modal 管理 GPU 的能力 ，在把原本需要 2000 秒启动的推理服务器启动时间缩短至 50 秒内，他们做的关键步骤如下：

• 

cloud buffer：


Modal 不是在请求到来时才去 hyperscaler 申请 GPU，而是维护一个小规模、健康、空闲的 GPU buffer，把云厂商实例分配和健康检查从用户请求的热路径中移出去。新 replica 可以直接调度到已经通过健康检查的空闲 GPU 上，新的 GPU 则异步补充进 buffer。这个设计的难点在于 buffer 不能太大，否则浪费昂贵 GPU；也不能太小，否则无法吸收突发流量。Modal 把它描述成一个线性规划问题，本质是在可用性、成本和响应速度之间动态优化。

• 

自研 ImageFS：


Modal 自研的懒加载文件系统，叫 ImageFS。传统容器启动时，经常要把整个镜像层层下载、解压、应用。问题是，一个容器镜像里有大量文件应用根本不会读。比如时区文件、语言 locale、系统工具、某些库文件，可能都在镜像里，但本次任务完全用不到。Modal 的办法是：


启动时只加载一个很小的 metadata index，真正访问某个文件时再把文件内容拉过来。


 它说这个 metadata 通常只有几 MB，可以在 100ms 左右加载完。但光懒加载还不够。因为如果每次程序访问文件，都从远端对象存储拉，那也会很慢。Modal 因此做了一个 


content-addressed， multi-tier cache


。可以理解成“按内容寻址的多层缓存”。如果两个容器里有完全相同的文件内容，不管它们在不同路径、不同镜像层、不同应用里，Modal 都可以识别它们是同一份内容，并复用缓存。AI 应用之间重复内容很多，比如 Python、PyTorch、CUDA stack、系统库等。Modal 认为传统 Docker layer cache 或路径缓存会浪费很多复用机会。

在 Sandbox 上也有启示，Agent sandbox 经常要准备 Python、Node、Chrome、Playwright、依赖包、代码仓库。如果每次都完整下载和安装，成本和延迟都会很高。

• 

CPU memory snapshot：


从容器进程启动，到真正能处理第一个请求，中间有很多重复初始化。比如 import torch，表面上只是一行 Python，但背后会执行大量代码、读取大量文件、和驱动做大量交互。每次新 replica 都从头做一遍，非常浪费。

Modal 的思路是一个运行中的进程，大致可以理解成三类东西：内存里的数据，正在运行的线程，以及文件描述符表。文件描述符可以理解成程序已经打开的文件、socket、设备连接等。如果这些状态可以保存下来，再恢复出来，就相当于程序从“上次存档的位置”继续运行。

Modal 没有使用 Linux 的 CRIU，而是用 gVisor 的 runsc。gVisor 可以理解成一个运行在用户态的“模拟 Linux 内核”。用户程序不是直接和真实 host kernel 交互，而是和 gVisor 模拟出来的内核交互。Modal 认为这让 checkpoint/restore 更自然，因为一个 runsc container 本质上像一个可以被序列化的状态机。

• 

GPU memory snapshot / CUDA checkpoint restore：


GPU inference 启动慢，主要有两类原因。第一，模型权重要加载到 GPU 显存。现在前沿模型的权重可能从 GB 到 TB 级别。Modal 说它也会用类似文件系统的存储能力来加载权重，速度可以达到每秒几个 GB，但这个步骤本质上受吞吐限制：文件太大，你总得把它读进来，snapshot 不一定能消除这个时间。

第二类原因更适合 snapshot：推理引擎要做一些昂贵的准备工作，生成一些小但复杂的运行时状态。例如 vLLM 会 capture CUDA graphs，Torch compiler 会做编译。这些步骤可能每个都要几十秒到几分钟，而且生成的是一些小的内存结构，传统缓存方式并不好处理。

这就是 GPU snapshot 的价值。先把 GPU device memory checkpoint 到 host memory，再由 host-side checkpoint 系统把它保存到磁盘；恢复时，先恢复 host memory，再由 driver 把 device memory 恢复回 GPU。

CPU 和 GPU memory snapshot 对 agent sandbox 来说，这意味着环境不必每次从空容器开始准备，而可以从已经初始化好的 Python/Node/browser/repo/dependency 状态快速恢复。这也解释了一部分加速能力。

典型客户

除了 ramp 以外，Modal 的客户名单包括 Lovable、Quora、Substack、Decagon、Ramp、Suno 等明星公司。

06


.

商业模式

Inference

Modal 的商业本质不是单纯转售 GPU，而是用更好的调度、启动速度、资源池化和开发者抽象，把高波动 AI workload 转化为可计费、可复用、可扩展的平台收入。

Modal 运营一个


跨数千客户的多租户 GPU/CPU 大池子


，通过将不同客户的波峰波谷在时间上错开，实现远高于单租户模式的资源利用率和资本效率。它不拥有数据中心，而是从 AWS、GCP、Oracle Cloud 等供应商租 GPU，然后加价卖给客户。Modal 当前的 GPU 池子超过 20,000 块并发 GPU。

Modal 计费模式为纯 usage-based、按秒计费，零出口流量费。代码不跑时完全不收费，支持从零到数千 GPU 的自动弹性扩缩容。客户无需做容量规划、无需签长期合约、无需预留 GPU：Modal 将容量风险完全吸收到平台侧。

Modal 的商业模式其实更像是一个赚差价的中间商：


用长约低价从云供应商批发 GPU 时间，用按秒高价零售给客户，赚中间的利用率差价。

买入侧：


Modal 从 OCI/AWS 拿 GPU。以 A100 80GB 为例，OCI 的批发价可能在 $1.5-2.0/hr 左右（推测）。预留意味着不管有没有客户在用，Modal 都在付钱。

卖出侧：


Modal 按秒向客户收费。A100 80GB 标价 $2.50/hr，H100 标价 $3.95/hr。但实际有效价格更高：Modal 有区域倍率（美国/欧洲 1.25x，其他地区 2.5x）和非抢占式倍率（最高 3x），组合后最高可达基础价的 3.75 倍。

具体来说，如果是 Oracle 是一级批发商，毛利 15%。Modal 是二级批发商，在 Oracle 的价格上再加 markup 卖给终端客户。但终端客户价格敏感，天然会比对 GPU 的价格，这限制了 Modal 的加价空间。

Modal 能赚到的溢价来自软件层的价值：极致的开发者体验、自动扩缩容、零配置部署。但这意味着：如果 GPU 价格持续下降，Modal 必须不断增加软件附加值来维持定价权；如果竞品在开发者体验上追赶上来，Modal 的溢价空间也会被压缩。

•

 利润空间

不难得出，Modal 在中间的利润空间取决于机群利用率，


但 Modal 从未公开过自己的实际利用率。


 有行业估算多租户 serverless 平台可以达到 70-80%+，对比


行业平均 GPU 利用率的 30-50%有很大的优化。

但是，当客户自己的利用率持续超过 70% 


时，对于他们来说，直接买 reserved instance 更便宜。这意味着 Modal 最好的客户是那些"用量大但波动也大"的：而不是"24/7 稳定跑"的。如果一个大客户的工作负载从 bursty 变成 steady-state，它离开 Modal 的概率会大大增加。

Sandbox

Modal 按秒计费，CPU、内存分别独立计价，GPU 则沿用标准 GPU pricing。这个模式对 agent workload 很自然，因为 agent 的执行需求高度波动。

专家访谈中提到，LangChain 在 Daytona 上的年化花费约 25–50 万美元；Figma、Boeing 在 E2B 上分别约 50 万美元；Lovable 在 Modal 上的年化花费区间可能达到 50–500 万美元；Databricks 则在不同供应商之间拆分用途，RunPod 负责 GPU/主智能体，Modal 负责常规智能体评估，Vercel 负责文档和实验环境，整体花费约 20–50 万美元。

当然以上例子均是在 Agent 大爆发前或者早期的实际用量情况。如果未来 agent 使用量继续增长，企业开始为大量并行执行环境、持续运行的任务会话和可恢复的工程状态付费，那么 Modal 的 Sandbox 收入可能会成为比传统 serverless GPU 更有粘性、增长也更有爆发性。

GTM 策略

Modal 采用


典型的 PLG 策


略：和 Slack、Figma、Notion 的增长路径类似：

1.

 开发者通过 Python SDK 自助注册，免费体验。

2.

 觉得好用，在团队内推广，用量自然增长。

3. 

用量达到一定规模后，Modal 的销售团队主动联系，转化为企业客户。

Modal 通过产品使用信号（用 Segment 采集 + Attio CRM 管理）自动识别高价值用户并触发销售介入。2024 年 11 月上架 AWS Marketplace，方便企业客户通过已有的 AWS 账单支付。

07


.

团队：从 Spotify 推荐引擎到 AI 云计算

Modal 团队约 120 人（2026 年初），分布在纽约（总部）、斯德哥尔摩和旧金山。

Founder/CEO : Erik Bernhardsson

• 

竞赛编程天才

Erik 是瑞典人，高中时就是顶尖程序员：获得国际信息学奥赛（IOI）金牌，两次入围 ACM-ICPC 世界总决赛（全球大学生编程最高竞赛），还拿过瑞典全国物理竞赛冠军。在 KTH 皇家理工学院拿到物理硕士后，他没有走学术路线，而是去了一家当时只有 30 人的瑞典音乐初创公司。

•

 Spotify 早期员工

Erik 在 Spotify 待了约 6 年（2008-2014），先管斯德哥尔摩的分析团队，后搬到纽约组建并领导机器学习部门。他亲手构建了 Spotify 推荐系统的初版：今天用户熟悉的 Discover Weekly（每周发现）、Related Artists（相似歌手）、Radio（电台）等核心功能，至今仍以他设计的架构为基础。

在 Spotify 期间，Erik 开源了两个广泛使用的工具：


Luigi：


一个数据工作流引擎（GitHub 18,000+ stars，被数百家公司采用）；


Annoy：


高维空间近似最近邻搜索库，本质上是一个早期的向量数据库，被 Spotify 自身和大量推荐系统使用。这两个项目让 Erik 在数据基础设施社区建立了极高的技术信誉。

•

 Better.com CTO

2015-2021 年，Erik 在在线房贷平台 Better.com 担任 CTO，将工程团队从 1 人扩展到 300+ 人，领导 AI 技术在房贷审批中的应用，并带队经历了 SPAC 上市流程。这段经历让他补上了商业运营和大规模团队管理的经验。

•

 创业起点

在 Spotify 和 Better.com，Erik 反复经历同一个问题：每次要运行计算密集型任务，都要和基础设施搏斗。他形容这种体验是"the infrastructure the world lacked"：世界缺少一种让开发者只写代码就能获得算力的基础设施。

2021 年初，Erik 开始全职构建 Modal。他做了一个在创业者中极其罕见的决定：


前两年独自用 Rust 从零搭建了文件系统、容器运行时和调度器：


没有用任何现成的开源组件，也没有急着招人。他凭借十年的领域积累，先把技术基础打牢，再面对市场。

2022 年，Stable Diffusion 的发布验证了 serverless GPU 基础设施的产品市场契合度，Modal 的 GPU serverless 能力恰好匹配了生成式 AI 推理的需求模式（无状态、burst-heavy、GPU-attached）。 2023 年 10 月，Modal 正式 GA，同时宣布 Series A

投资机构 Amplify Partners 对 Erik 的评价是："The smartest people are those who can change your mind — so Erik is clearly among this group。"

Erik 的关键战略观点

•

 关于 DX vs GPU 效率：行业过度优化了 GPU 效率，低估了开发者体验的价值。随着工程师再次变得重要，"move fast 的能力" 将有溢价。

•

 关于 Hyperscaler 的未来：理论上 hyperscaler（AWS、Azure、GCP）将越来越聚焦于最底层（通过 API 出租容量），而纯软件提供商如 Modal 在上层构建更好的体验。

•

 关于竞争："There's a tiny sliver of the Venn diagram where we're competitive with any single competitor。 And then like 99% of the area we're not competitive." 每个竞争者都只在很窄的切面上重叠。

•

 关于 Heroku 毕业问题：明确承认客户可能 outgrow 平台的风险。解决方案是覆盖 "the entire spectrum" 从 hobbyist 到 enterprise。

•

 关于 LLM 价格战：预期 margin 压缩但视为正面信号。引用光纤泡沫的类比："VCs subsidize these things... consumers get tremendous benefits."

Co-Founder / CTO: Akshat Bubna

于 2021 年 8 月加入成为联合创始人。Akshat 同样是竞赛编程出身：MIT 数学与计算机科学毕业，2014 年获得 IOI 金牌，是


印度历史上首位 IOI 金牌获得者。


加入 Modal 前，他是 Scale AI 的 Staff Engineer，负责可扩展数据与模型基础设施。

团队构成

从当前 27 个开放职位的分布看，工程约占 60%，GTM（销售与市场）约占 22%，行政与财务约占 19%。

创始团队 7 人中有 


5 人持有 IOI 金牌


。公司早期极度偏重工程，2023 年 14 人时几乎全是工程师，GTM 团队是 2024-2025 年收入增长后才逐步搭建的。

团队成员包括多名国际奥赛奖牌得主、Seaborn（Python 最流行的数据可视化库之一）的创造者、以及来自 Scale AI、Google 等公司的高级工程师。

专家访谈中也多次提到，Modal 的基础设施人才也是世界级的，产品逻辑符合工程直觉。

根据旧金山的招聘科技公司 Paraform 基于自己招聘平台数据做的 Talent Density Index，Modal 在一众科技公司中位列第六。

Erik 的管理哲学

从多次公开访谈中，可以提炼出 Erik 几个鲜明的管理原则：

1. 

偏好竞赛编程背景的工程师：编程竞赛培养的是快速解决问题的能力和对复杂度的直觉。

2.

 不惜代价招顶尖人才："Top engineers output usually more than compensates for increased costs。"

3.

 反对 exploding offers（限时接受的 offer）：认为对候选人不公平，长期损害公司声誉

4.

 反对孤立的 ML 团队：ML 工程师应嵌入产品团队

5.

 "Engineers designed products for engineers"：产品决策始终由工程团队主导

08


.

融资进展

Modal 拥有豪华的投资人阵容，其天使投资人便高度集中在数据基础设施和 ML 工程领域。

•

 Elad Gil — 硅谷最知名的天使投资人之一

•

 Jeff Hammerbacher — Facebook 初代数据团队创始人，Cloudera 联合创始人

•

 Neha Narkhede — Confluent（Kafka 背后的公司）联合创始人

•

 Tristan Handy — dbt Labs CEO，数据工程领域最有影响力的人物之一

•

 Jordan Tigani — MotherDuck 创始人，前 Google BigQuery 工程主管

•

 Christopher Re — 斯坦福教授，Snorkel AI 联合创始人

Modal 早期由 Amplify Partners 领投 Seed，2023 年 10 月完成 $16M Series A，由 Redpoint Ventures 领投，并在平台正式 GA 时获得 Ramp、Substack、SphinxBio 等早期客户。2025 年 9 月，公司完成 $87M Series B，由 Lux Capital 领投，投后估值 $1.1B。

截至最新信息，Modal 已完成 $355M Series C，投后估值 $4.65B。本轮由 General Catalyst 与 Redpoint 领投，Menlo、Bain Capital Ventures、Accel 作为新投资人加入，原有主要投资人继续跟投。公司披露自 2025 年 9 月以来增长约 5 倍，annualized revenue 已超过 $300M；Modal 从 2025 年 9 月 Series B 的 $1.1B post-money 到 2026 年 5 月 Series C 的 $4.65B post-money，估值在约 8 个月内提升超过 4 倍。

若按 300M 的年化收入计算，～15.5x 的估值倍数在 AI infra 并不算便宜。但我们认为，Modal 的估值不能简单按统一 revenue multiple 定价，而应拆分看待：GPU / inference 收入带有较强的 compute pass-through 属性，而 Sandbox 收入更接近软件化控制平面，具备更高毛利率、更强粘性和更大的平台延展性，理应享受更高倍数。

Modal 披露 Sandboxes 已贡献超过三分之一收入，意味着其约 $300M annualized revenue 中，至少 $100M run-rate 已来自 agent runtime 相关场景。这无疑是本轮融资中传达的积极信号：


Modal 不再只是一个 serverless GPU 平台，而是在成为 AI agent 执行层的关键基础设施。


如果未来 Sandbox 收入占比继续提升，并在 agent 时代成为企业默认的安全执行环境，Modal 的估值逻辑将从“高增长 compute infra”进一步切换为“AI-native runtime platform”，从而获得更高的估值溢价。

 排版：夏悦涵

延伸阅读

Mintlify 做的开发者文档，如何成为 Coding Agent 生产和消费的第一波内容？

从 Agent 开权限开始，Serval 想成为下一代 ServiceNow

拆解 Anthropic：最好的 AI 公司，可能也是一种组织发明

The Era of Agent：拾象 AGI 投资洞察

AI Labs 都在用，ClickHouse 能成为 AI 日志的实时分析引擎吗？

## 关联

- [[海外独角兽]]

## 备注

> 置信度 0.70：微信公众号文章。
