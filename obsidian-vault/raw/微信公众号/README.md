---
role: Coordinator
type: 说明
doc_name: 使用说明
version: 1.0
project_id: PRJ-2026-001
---

# 微信公众号链接投递说明

在此目录下放置需要处理的微信公众号文章链接。

## 使用方式

创建一个 `.md` 文件，内容格式如下：

```markdown
来源: 海外独角兽
链接: https://mp.weixin.qq.com/s/xxx
备注: 可选，补充说明
```

## 文件命名

建议：`YYYY-MM-DD_来源名_关键词.md`

示例：`2026-06-24_海外独角兽_AI投资趋势.md`

## 说明

- 我定时扫描此目录处理新文件
- 处理完成后文件会自动移入 `raw/`（已处理）
- 支持的信源：海外独角兽、晚点LatePost
