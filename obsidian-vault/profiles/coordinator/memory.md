---
role: Coordinator
type: memory
doc_name: Coordinator 角色经验
version: 1.0
last_updated: 2026-06-24
source: 架构说明 v2.0 §7.1
---

# Coordinator 经验

## 管理类经验（跨项目可复用）

- 复杂任务先拆解为原子任务再路由，不要让一个任务跨越多个角色
- 中间材料先进 `inbox/`，最终产出进 `outputs/`
- 每次状态变更后更新项目仪表盘和协作日志
- 回退 ≥ 3 次必须升级给用户，不要自行无限重试
- 切换项目前先确认当前上下文已写入推进日志

## 注意

- 项目特定经验不存于此 → 存到 `项目空间/{项目}/`
- 临时状态不存于此 → 存到 `inbox/`
