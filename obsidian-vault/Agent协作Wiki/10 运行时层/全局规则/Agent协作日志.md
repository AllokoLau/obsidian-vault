---
role: Coordinator
type: 全局规则
doc_name: Agent协作日志
version: 1.0
enforced_by: Coordinator 写入
source: 架构说明 v2.0 §5.1
---

# Agent 协作日志

> 追踪所有 Profile 在系统中的活动记录。由 Coordinator 在每个操作完成后追加写入。

---

```yaml
---
log_type: 协作日志
project_id: [PRJ-YYYY-NNN]
last_updated: [ISO 8601]
---
```

## 日志条目

| 时间 | Profile | 动作 | 任务ID | 项目 | 结果摘要 |
|------|---------|------|--------|------|----------|
| [ISO 8601] | Coordinator | 路由 | T001 | [项目名] | 将研究任务路由到 Researcher |
| [ISO 8601] | Researcher | 完成 | T001 | [项目名] | 提交研究结论，置信度 0.85 |
| [ISO 8601] | Coordinator | 路由 | T002 | [项目名] | 将写作任务路由到 Writer |
| [ISO 8601] | Writer | 完成 | T002 | [项目名] | 提交成品，4重质检通过 |
| [ISO 8601] | Coordinator | 路由 | T003 | [项目名] | 将构建任务路由到 Builder |
| [ISO 8601] | Builder | 驳回 | T003 | [项目名] | 发现材料错误，提交 BR001 驳回报告 |
| [ISO 8601] | Coordinator | 重新路由 | T003 | [项目名] | 回退到 Researcher 重新调研 |

## 动作类型

| 动作 | 说明 |
|------|------|
| 路由 | Coordinator 将任务分配给某个 Profile |
| 完成 | Profile 完成任务提交产出 |
| 驳回 | Builder 发现材料错误提交驳回报告 |
| 重新路由 | Coordinator 因回退重新分配任务 |
| 升级 | 回退超过 3 次，升级给用户 |
| 归档 | 项目完成归档 |
