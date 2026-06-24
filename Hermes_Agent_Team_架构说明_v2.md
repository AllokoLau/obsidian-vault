# Agent Team 架构说明书

**Hermes 多 Profile 协作团队完整设计方案**

**v2.0 --- 新增质量保障体系**

本架构由小屿设计改进，仅供参考学习，请勿用于其他用途

修改日期：2026-06-22

适用环境：Hermes Agent

---

## 1. 核心判断

Hermes 的高级用法不是多开几个 Agent，而是用多 Profile 做角色分工，用 Wiki 做共享记忆。目标是让一个人也能管理一支稳定协作的 Agent 团队。

为什么不能单 Agent 全包？长期任务中研究、写作、实现、审查、复盘会不断挤进同一段上下文，产生三个问题：

- **幻觉**：一个 Agent 自己查、自己写、自己审，缺乏交叉视角
- **记忆污染**：内容创作经验污染工程思维，工程习惯污染写作风格
- **角色混乱**：该研究时下结论，该写作时查资料，该审查时替自己辩护

---

## 2. 四个基础概念

多 Agent 系统乱的根本原因：把长期角色、临时任务、项目空间和共享记忆混成了一件事。

| 概念 | 定义 | 特点 |
|------|------|------|
| **Profile** | **长期员工** | 有稳定身份、责任、记忆、技能和配置 |
| **Subagent** | **临时外包** | 解决局部问题，完成后结束 |
| **Project** | **项目空间** | 承接某个长期任务的上下文 |
| **Wiki** | **共享记忆层** | 跨 Agent 同步状态、知识、决策 |

---

## 3. 四角色模型

从四角色模型起步，不要一开始开十几个角色。

### 3.1 Coordinator（项目经理）

- 定义目标、拆解任务、路由任务、汇总结果、检查边界
- 最重要的职责是让整个系统有序运行，不是亲自干所有活
- **不负责**：研究、写最终稿、实现代码
- **v2 新增**：Session Gate — 每次对话先确认项目归属，不明确则主动询问
- **v2 新增**：置信度分级路由 — 根据 Researcher 置信度决定流转策略

### 3.2 Researcher（研究员）

- 收集证据、对比来源、标记不确定性、提炼事实
- 显著降低整个系统的幻觉，因为不急着写结论
- **不负责**：内容表达和润色
- **v2 新增**：产出必须附带置信度评分和来源引用

### 3.3 Writer（作家）

- 把原材料转化为清晰内容、搭建文章结构、提炼主线、优化表达、适配读者
- 当 Writer 不需要同时负责规划和查资料，就能专注于把内容讲清楚
- **不负责**：事实验证、规划
- **v2 新增**：自检清单 — 来源引用、技术一致性、事实核查、修改标注
- **v2 新增**：初稿完成后自动路由给 Researcher 做 fact-check

### 3.4 Builder（工程师）

- 实现、调试、测试、交付
- **不负责**：讲故事、从零做研究、替项目定方向
- **v2 新增**：技术驳回流程 — 发现上游材料错误时，拆分已做工作、写驳回报告、增量修正

---

## 4. Profile 文件结构

每个 Profile 包含 6 层文件，各司其职：

| 文件 | 回答的问题 | 内容范例 |
|------|------------|----------|
| **soul.md** | Agent 是谁 | 负责拆任务、规划项目、汇总结果。不负责研究、写稿、写代码 |
| **USER.md** | 对用户的理解 | 用户偏好中文、结构清晰的 Markdown、不喜欢空泛概念 |
| **memory.md** | 有什么经验 | 复杂任务先拆解、中间材料先进 inbox、最终产出进 outputs |
| **skills/** | 有什么技能 | 任务拆解、优先级判断、交接单生成、dashboard更新 |
| **config.yaml** | 怎么运行 | 模型、目录、权限、禁区 |
| **.env** | 用什么凭证 | API Key、Token、服务凭证 |

---

## 5. Wiki 共享记忆层

Wiki 同时是共享知识库、项目管理层和长期记忆层。包含 8 个部分：

| 目录 | 角色 | 说明 |
|------|------|------|
| **index.md** | 导航地图 | 不存大量具体内容，告诉人和 Agent 系统区在哪里 |
| **schema.md** | 宪法 | 规定文件命名、写入位置、读写权限、状态标记 |
| **system/** | 全局管理 | dashboard、agent-log、weekly-review、memory-routing、skill-registry、user-profile |
| **projects/** | 项目空间 | 每个长期任务独立空间，同一套 Profile 服务多个 Project |
| **pages/** | 可复用方法论 | 跨项目可用、非临时判断、经过验证或抽象 |
| **raw/** | 原始资料 | 论文、文章、网页快照、数据表、会议记录，原则只读不改 |
| **assets/** | 素材 | 图片、截图、架构图、图表 |
| **archive/** | 归档 | 不活跃、过期、废弃内容，靠分层和归档维持秩序 |

### 5.1 system/ 六个核心文件

| 文件 | 职责 | 回答的问题 |
|------|------|------------|
| **dashboard.md** | 项目当前状态 | 有哪些项目？进展如何？谁负责？ |
| **agent-log.md** | 协作追踪 | 所有 Profile 做过什么？ |
| **weekly-review.md** | 定期复盘 | 本周做了什么？下周做什么？ |
| **memory-routing.md** | 防污染总纲 | 什么信息写哪里？ |
| **skill-registry.md** | 技能分配 | 哪些技能分配给哪个 Profile？ |
| **user-profile.md** | 用户偏好 | 用户整体偏好是什么？ |

---

## 6. 信息路由规则 (Memory Routing)

这是整套 Wiki 最关键的防污染文件。规定所有类型信息的唯一存放位置：

| 信息类型 | 存放位置 | 说明 |
|----------|----------|------|
| **角色身份** | `profiles/<name>/soul.md` | Agent 是谁、做什么、不做什么 |
| **用户偏好** | `profiles/<name>/USER.md` | 对用户的理解 |
| **角色经验** | `profiles/<name>/memory.md` | 跨项目可复用的经验 |
| **项目规则** | `wiki/projects/<name>/AGENTS.md` | 这个项目应该怎么做 |
| **项目背景** | `wiki/projects/<name>/context.md` | 是什么、为什么做、当前阶段 |
| **任务状态** | `wiki/projects/<name>/tasks.md` | Doing / Todo / Done |
| **推进记录** | `wiki/projects/<name>/log.md` | 发生了什么 |
| **决策记录** | `wiki/projects/<name>/decisions.md` | 已确定方向和不做什么 |
| **临时材料** | `wiki/projects/<name>/inbox/` | 半成品、草稿、未确认结论 |
| **正式产出** | `wiki/projects/<name>/outputs/` | 已确认可交付的内容 |
| **跨项目方法论** | `wiki/pages/` | 可复用经验，非临时判断 |
| **原始资料** | `wiki/raw/` | 只读不改 |
| **过期内容** | `wiki/archive/` | 不活跃、废弃的内容 |

---

## 7. 质量保障体系（v2 新增）

v2 版本引入完整质量保障机制，解决多 Agent 协作中的信息污染和验证闭环问题。

### 7.1 Session Gate — 项目上下文确认

Coordinator 每次对话必须先确认当前项目归属，避免跨项目经验污染：

- 用户指定项目名 → 加载 `wiki/projects/<项目>/context.md` + `AGENTS.md`
- 用户未指定 → 主动询问"这个任务属于哪个项目？"
- 不特定于项目 → 使用通用上下文，产出放入 `wiki/pages/`

项目特定经验存到项目空间，Coordinator 的 `memory.md` 只存管理类经验（哪个 Researcher 响应快、哪个工具链容易出问题等）。

### 7.2 Researcher 置信度分级

每次调研产出必须附带置信度评分和来源引用，Coordinator 根据分级决定流转策略：

| 置信度 | 策略 | 说明 |
|--------|------|------|
| **> 80%** | 正常流转 | 直接进入下一环节 |
| **60-80%** | 标注不确定点 | 单 Researcher + 附带不确定点标注 |
| **40-60%** | 双盲交叉验证 | 路由给第二个 Researcher 独立调研 |
| **< 40%** | 需人工判断 | 不浪费算力，标记后等待人工介入 |

双盲冲突裁决：以来源质量更高的结论为准（一手来源 > 二手来源 > 模型推断）。

### 7.3 Builder 技术驳回

Builder 发现上游材料（Researcher 调研 / Writer 方案）存在技术错误时，执行增量修正流程：

- 立即停止基于错误部分的执行
- 将已完成的正确部分和需要修正的部分分开记录
- 写驳回报告到 `inbox/rebuttal.md`（格式：问题描述 + 正确方案 + 影响范围）
- Coordinator 只路由需要修正的部分，不重新跑全量
- 修正完成后，Builder 在已有正确基础上继续，不从零开始

### 7.4 Writer 自检与事实核查

Writer 产出必须通过以下检查才能提交为正式产出：

- **来源引用**：每个观点/数据必须有对应的来源引用，无来源的论断不得出现
- **技术一致性**：涉及技术细节的表述，必须与 `wiki/raw/` 中的原始资料一致，不得自行演绎
- **事实核查**：初稿完成后自动路由给 Researcher 做 fact-check
- **修改标注**：所有非原创的修改必须标注来源

### 7.5 写入前校验（三问原则）

任何 Profile 在写入 `memory.md`、`pages/` 或 `system/` 之前，必须先执行三问校验：

- 这条信息是否特定于某个项目？→ **是**：存到 `projects/<项目>/`，不存 memory 或 pages/
- 这条信息是否只是临时状态？→ **是**：存到 `inbox/`，不存 pages/ 或 memory/
- 这条信息六个月后还有用吗？→ **否**：存到 `log/` 或 `inbox/`，不存 pages/ 或 memory/

违反任意一条即为信息污染，应立即纠正。

### 7.6 信息污染预警

如果出现以下情况，说明信息放错了位置：

- `soul.md` 里出现项目名称 → 角色身份被项目状态污染
- `memory.md` 里出现「今天做了什么」 → 角色经验被项目进度污染
- `pages/` 里出现单次笔记 → 临时想法污染长期知识
- `outputs/` 里出现草稿 → 未验证材料混入正式产出

---

## 8. Project 项目空间结构

每个长期任务都应该有自己的项目空间，关键不是为每个项目复制一套 Profile，而是同一套 Profile 团队服务多个 Project。

| 文件 | 职责 | 说明 |
|------|------|------|
| **AGENTS.md** | 项目规则 | Researcher材料→inbox，Writer方案→inbox，Builder交付→outputs，Coordinator更新tasks+log |
| **context.md** | 项目背景 | 是什么、为什么做、当前阶段 |
| **tasks.md** | 任务池 | Doing・ Todo・ Done・负责人 |
| **log.md** | 推进记录 | 项目内发生了什么 |
| **decisions.md** | 决策记录 | 已确定方向、不做什么，防止反复摇摆 |
| **inbox/** | 中间材料 | 半成品、草稿、研究材料、未确认结论、Subagent输出、驳回报告 |
| **outputs/** | 正式产出 | 最终文章、代码、Demo、已确认可交付 |

---

## 9. 技能分配 (Skill Registry)

防止所有 Profile 都装一堆 skills 导致角色边界重新混乱。

| 技能 | 分配给 | 说明 |
|------|--------|------|
| task-decomposition | **Coordinator** | 任务拆解 |
| priority-judgment | **Coordinator** | 项目优先级判断 |
| dashboard-update | **Coordinator** | 更新 dashboard.md |
| confidence-rating | **Researcher** | 置信度评分（v2 新增） |
| Fact-check | **Researcher** | 事实核查 Writer 初稿（v2 新增） |
| source-collection | **Researcher** | 收集来源 |
| source-validation | **Researcher** | 交叉验证来源可靠性 |
| article-structure | **Writer** | 搭建文章结构 |
| self-check | **Writer** | 自检清单执行（v2 新增） |
| code-implementation | **Builder** | 代码实现 |
| testing | **Builder** | 测试 |
| technical-rebuttal | **Builder** | 技术驳回报告（v2 新增） |

---

## 10. 完整工作流

用户发布任务 → Coordinator 执行 Session Gate 确认项目 → 拆解写入 `tasks.md` → 路由到对应 Profile → 各 Profile 执行并产出 → Coordinator 按置信度分级检查 → 如有驳回则增量修正 → 汇总结果 → 更新 dashboard + agent-log → 归档决策到 `decisions.md`

**关键规则**：不要让未验证材料直接进入正式产出。Researcher 和 Writer 的产出放 `inbox/`，Builder 的交付放 `outputs/`。

---

## 11. Profile 切换决策规则

换项目不一定换 Profile，换角色才需要换 Profile。

- 这次变化是角色变化吗？→ **YES** → 职责是否变化？→ **YES** → 切换 Profile
- 这次变化是角色变化吗？→ **YES** → 职责是否变化？→ **NO** → 保留当前 Profile
- 这次变化是角色变化吗？→ **NO** → 只是项目变化？→ **YES** → 切换 Project context
- 这次变化是角色变化吗？→ **NO** → 只是项目变化？→ **NO** → 继续当前会话

---

## 12. 完整目录结构

所有文件存放在 `D:\AI项目\agent-team\` 下：

```
D:\AI项目\agent-team\
├── profiles\
│   ├── coordinator\soul.md
│   ├── researcher\soul.md
│   ├── writer\soul.md
│   └── builder\soul.md
└── wiki\
    ├── index.md
    ├── schema.md
    ├── system\
    │   ├── memory-routing.md
    │   └── skill-registry.md
    └── projects\过渡项目\
        ├── AGENTS.md
        ├── context.md
        ├── tasks.md
        ├── log.md
        ├── decisions.md
        ├── inbox\
        └── outputs\
```

---

## 附录：v2 更新日志

v2.0 相比 v1.0 新增以下内容：

- **7.1 Session Gate** — 项目上下文确认机制
- **7.2 Researcher 置信度分级** — 四级流转策略
- **7.3 Builder 技术驳回** — 增量修正流程
- **7.4 Writer 自检与事实核查** — 四项检查清单
- **7.5 写入前校验** — 三问原则
- **7.6 信息污染预警** — 污染检测指标
- Skill Registry 新增 4 项技能：confidence-rating、fact-check、self-check、technical-rebuttal
- 各 Profile soul.md 同步更新：Coordinator Session Gate + 分级路由、Writer 自检清单、Builder 驳回流程

---

*本架构由小屿设计改进，仅供参考学习，请勿用于其他用途*
