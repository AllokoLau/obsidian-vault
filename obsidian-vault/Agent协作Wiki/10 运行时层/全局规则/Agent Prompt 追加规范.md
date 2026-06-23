# Agent 行为规范与写入权限

> **层级**: 运行时层 / 全局规则  
> **约束对象**: 所有接入 Obsidian 的 Agent（Coordinator、Researcher、Writer、Builder）  
> **执行方式**: Agent 每次写入前必须自检，本地桥接器二次校验

---

```yaml
---
role: Coordinator
type: 全局规则
doc_name: Agent行为规范与写入权限
version: 1.0
enforced_by: 本地桥接器 + Agent自检
violation_action: 拒绝写入并记录审计日志
---

## Obsidian 写入规范（强制执行）

### 你的可写范围
[根据角色填入对应路径]

### 每次写入前必须执行
1. 确认目标路径是否在你的可写范围内
2. 确认目标路径不包含 `00 宪法层/` 或 `20 数据层/`
3. 确认 YAML 头部包含 `role`、`timestamp`、`version`
4. 确认 version 大于该文件的旧版本号

### 禁止行为（违反将被拒绝写入）
- 禁止写入 `00 宪法层/` 和 `20 数据层/`
- 禁止写入其他角色的专属文件夹
- 禁止覆盖未归档的文件（除非你是 Coordinator）
- 禁止删除任何文件

### 命名规范
- 研究材料：`{任务ID}-{描述}.md`
- 写作成品：`{任务ID}-{描述}.md`
- 构建产物：`{任务ID}-{描述}.py`（或对应扩展名）
- 驳回报告：`BR{序号}-{任务ID}-{日期}.md`

### YAML 头部模板
```yaml
---
role: [你的角色名]
timestamp: [当前时间，ISO 8601]
version: [版本号]
project_id: [项目ID]
task_id: [任务ID]
fileClass: [对应fileClass名]
---