---
role: Coordinator
timestamp: 2026-06-27T16:30:00+08:00
version: 1.0
project_id: PRJ-2026-002
type: 跨会话记忆
fileClass: 项目记忆
---

# 项目记忆

## 待办事项

- 事件：login.py 中的用户查询仍是硬编码演示骨架，需替换为真实数据库调用
- 上下文：PRJ-2026-002 微信小程序后端 /api/v1/auth/login 接口开发
- 决策：当前使用 `_authenticate_user()` 内的硬编码 `user_record` 字典作为占位，标注了 TODO，后续接入用户表后替换为数据库查询
- 教训：骨架代码中的 TODO 必须在合并到主分支前解决，否则容易遗漏上线前的关键替换；建议在 CI 中增加 TODO 检测规则

## 架构决策

- 事件：登录接口启动时依赖 `JWT_SECRET_KEY` 环境变量，缺失则拒绝启动
- 上下文：login.py 模块初始化阶段
- 决策：遵循安全规范（`.claude/rules/security.md` 凭证保护条款），API 密钥/私钥全部通过环境变量注入，不在代码中出现任何明文密钥；启动时使用 `if not JWT_SECRET: raise RuntimeError(...)` 实现快速失败
- 教训：环境变量缺失时在模块加载阶段立即报错（fail-fast），比运行时 500 更易排查；部署脚本需将 `JWT_SECRET_KEY` 纳入必检项
