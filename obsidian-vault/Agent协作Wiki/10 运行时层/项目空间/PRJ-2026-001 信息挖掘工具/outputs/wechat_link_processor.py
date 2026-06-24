"""
WeChat Article Link Processor
监控微信公众号目录，处理新链接文件，导出全文。

用法:
  python wechat_link_processor.py                    # 处理所有待处理的链接文件
  python wechat_link_processor.py --watch            # 单次运行模式

目录结构:
  raw/微信公众号/          ← 用户放链接文件
  raw/入库模板/            ← 处理后存入此目录

链接文件格式:
  ```markdown
  来源: 海外独角兽
  链接: https://mp.weixin.qq.com/s/xxx
  备注: 可选
  ```

注意:
  微信公众号文章有反爬机制，本脚本会尝试多种方式获取。
  如果全部失败，会记录链接到日志供手动处理。
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

import httpx


# 路径
VAULT_ROOT = Path(__file__).resolve().parents[5]  # obsidian-vault/
WECHAT_DIR = VAULT_ROOT / "raw" / "微信公众号"
RAW_DIR = VAULT_ROOT / "raw"
PROCESSED_DIR = WECHAT_DIR / "_已处理"
FAILED_DIR = WECHAT_DIR / "_失败"

SUPPORTED_SOURCES = ["海外独角兽", "晚点LatePost", "晚点LatePost"]


def ensure_dirs():
    """确保所需目录存在."""
    for d in [PROCESSED_DIR, FAILED_DIR]:
        d.mkdir(exist_ok=True)


def parse_link_file(filepath: Path) -> dict:
    """解析链接文件，返回 {source, url, note}."""
    content = filepath.read_text(encoding="utf-8")

    source = ""
    url = ""
    note = ""

    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("来源:"):
            source = line.replace("来源:", "").strip()
        elif line.startswith("链接:"):
            url = line.replace("链接:", "").strip()
        elif line.startswith("备注:"):
            note = line.replace("备注:", "").strip()

    return {"source": source, "url": url, "note": note, "file": filepath}


def find_new_links() -> list:
    """扫描微信公众号目录，找到所有未处理的链接文件."""
    if not WECHAT_DIR.exists():
        print(f"[INFO] 目录不存在: {WECHAT_DIR}")
        return []

    new_files = []
    for f in sorted(WECHAT_DIR.glob("*.md")):
        # 跳过 README 和子目录
        if f.name == "README.md":
            continue
        new_files.append(f)

    return new_files


async def try_fetch_article(url: str) -> str | None:
    """尝试获取微信公众号文章内容."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(url, headers=headers)

        if resp.status_code != 200:
            print(f"  [WARN] HTTP {resp.status_code}")
            return None

        html = resp.text
        if not html or len(html) < 100:
            return None

        return html

    except Exception as e:
        print(f"  [ERROR] 请求失败: {e}")
        return None


def extract_article_text(html: str) -> str:
    """从微信公众号 HTML 中提取正文."""
    # 尝试提取页面标题
    title = "未知标题"
    m = re.search(r'<h1[^>]*class="rich_media_title"[^>]*>(.*?)</h1>', html, re.DOTALL)
    if m:
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()

    # 尝试提取正文
    content = ""
    m = re.search(r'<div[^>]*class="rich_media_content[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
    if m:
        content = m.group(1)
    else:
        # 备选：提取所有文本
        content = re.sub(r'<[^>]+>', '\n', html)

    # 清理 HTML 标签
    text = re.sub(r'<[^>]+>', '', content)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&#39;', "'", text)
    text = re.sub(r'<br\s*/?>', '\n', text)

    # 清理多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    return title, text


def format_article(source: str, url: str, title: str, text: str) -> str:
    """格式化为入库模板格式."""
    lines = []
    lines.append("---")
    lines.append("type: knowledge")
    lines.append(f"入库日期: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("置信度: 0.00  # 待 Researcher 评估")
    lines.append(f"来源: [外部-微信公众号/{title}]")
    lines.append(f"主题: {title}")
    lines.append("分类: 信息挖掘/微信公众号")
    lines.append(f"tags: [{source}]")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"> **来源**: [外部-微信公众号/{title}]")
    lines.append(f"> **公众号**: {source}")
    lines.append(f"> **原文链接**: {url}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 正文")
    lines.append("")
    lines.append(text if text else "（未能提取正文）")
    lines.append("")

    return "\n".join(lines)


async def process_link(link_info: dict) -> bool:
    """处理一个链接文件，返回成功与否."""
    source = link_info["source"]
    url = link_info["url"]
    filepath = link_info["file"]

    print(f"\n[INFO] 处理: {source}")
    print(f"[INFO] 链接: {url}")

    # 尝试获取
    html = await try_fetch_article(url)
    if not html:
        print(f"  [FAIL] 无法获取文章内容")
        # 移入失败目录
        fail_path = FAILED_DIR / filepath.name
        filepath.rename(fail_path)
        print(f"  [INFO] 已移入: {fail_path}")
        return False

    title, text = extract_article_text(html)
    print(f"  [OK] 标题: {title}")
    print(f"  [OK] 正文长度: {len(text)} 字")

    # 写入 raw/
    today = datetime.now().strftime("%Y%m%d")
    out_name = f"{today}_{source}_{title[:30]}.md"
    out_path = RAW_DIR / out_name
    out_path.write_text(format_article(source, url, title, text), encoding="utf-8")
    print(f"  [OK] 已保存至: {out_path}")

    # 移走已处理的链接文件
    processed_path = PROCESSED_DIR / filepath.name
    filepath.rename(processed_path)
    print(f"  [OK] 链接文件已归档")

    return True


async def main():
    ensure_dirs()

    files = find_new_links()
    if not files:
        print("[INFO] 没有待处理的微信公众号链接文件")
        print(f"[INFO] 目录: {WECHAT_DIR}")
        print("[INFO] 在此目录放 .md 文件，内容格式: 来源 / 链接")
        return

    print(f"[INFO] 发现 {len(files)} 个待处理链接")
    success = 0
    for f in files:
        link_info = parse_link_file(f)
        ok = await process_link(link_info)
        if ok:
            success += 1

    print(f"\n{'='*40}")
    print(f"处理完成: {success}/{len(files)} 成功")


if __name__ == "__main__":
    asyncio.run(main())
