---
role: Builder
type: memory
doc_name: Builder 角色经验
version: 1.0
last_updated: 2026-06-24
---

# Builder 经验

## 构建经验（跨项目可复用）

- 发现上游材料错误时，先拆分已做工作，再写驳回报告
- 驳回报告只包含一个原子问题，不批量提交
- 使用五步自救流程，不卡死在错误路径上
- 构建产物放 `outputs/`，驳回报告放 `inbox/`

## 注意

- 项目特定的构建产物不存于此 → 存到 `项目空间/{项目}/outputs/`
- 临时调试记录不存于此 → 存到 `inbox/`
