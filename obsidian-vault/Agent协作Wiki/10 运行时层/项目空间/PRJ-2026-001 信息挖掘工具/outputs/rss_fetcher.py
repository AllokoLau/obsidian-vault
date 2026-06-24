"""
RSS Fetcher for 小宇宙播客
通过 RSSHub 拉取播客 shownotes，输出结构化 Markdown

用法:
  python rss_fetcher.py <播客ID>

支持的播客:
  张小珺商业访谈录:  626b46ea9cbbf0451cf5a962
  晚点聊 LateTalk:   61933ace1b4320461e91fd55
  厚雪长波:          646d6bfa53a5e5ea14e69c7c
  十字路口 Crossing: 60502e253c92d4f62c2a9577

依赖: feedparser (pip install feedparser)
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

import httpx


PODCASTS = {
    "张小珺": "626b46ea9cbbf0451cf5a962",
    "晚点聊": "61933ace1b4320461e91fd55",
    "厚雪长波": "646d6bfa53a5e5ea14e69c7c",
    "十字路口": "60502e253c92d4f62c2a9577",
}

RSSHUB_BASE = "https://rsshub.app"

# 各播客的上次获取时间记录
STATE_FILE = Path(__file__).parent / "rss_state.json"


def load_state() -> dict:
    """加载各播客上次拉取的最新时间."""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state: dict):
    """保存各播客上次拉取的最新时间."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def parse_rss(xml_text: str) -> list:
    """解析 RSS XML，返回新节目列表."""
    items = []
    root = ElementTree.fromstring(xml_text)
    # RSS 2.0 namespace
    ns = {"": "", "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}

    for item_el in root.iter("item"):
        title = item_el.findtext("title", "")
        link = item_el.findtext("link", "")
        pubdate_str = item_el.findtext("pubDate", "")
        description = item_el.findtext("description", "")
        guid = item_el.findtext("guid", "")

        # 解析发布日期
        pubdate = None
        if pubdate_str:
            try:
                # RSS pubDate 格式: "Tue, 24 Jun 2026 08:00:00 GMT"
                from email.utils import parsedate_to_datetime
                pubdate = parsedate_to_datetime(pubdate_str)
            except Exception:
                pubdate = None

        items.append({
            "title": title.strip(),
            "link": link.strip(),
            "pubdate": pubdate.isoformat() if pubdate else "",
            "description": (description or "").strip(),
            "guid": guid.strip(),
        })

    return items


def format_markdown(podcast_name: str, episode: dict) -> str:
    """将单集 RSS 条目格式化为 Markdown."""
    title = episode["title"]
    desc = episode["description"]
    pubdate = episode["pubdate"][:10] if episode["pubdate"] else "未知日期"
    link = episode["link"]

    # 清理 HTML 标签（粗略）
    import re
    desc_clean = re.sub(r'<[^>]+>', '', desc)
    desc_clean = re.sub(r'&amp;', '&', desc_clean)
    desc_clean = re.sub(r'&lt;', '<', desc_clean)
    desc_clean = re.sub(r'&gt;', '>', desc_clean)
    desc_clean = re.sub(r'&nbsp;', ' ', desc_clean)
    desc_clean = re.sub(r'&[a-zA-Z]+;', '', desc_clean)

    # 截取前 300 字作为摘要
    summary = desc_clean[:300] + "..." if len(desc_clean) > 300 else desc_clean

    lines = []
    lines.append("---")
    lines.append("type: knowledge")
    lines.append(f"入库日期: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("置信度: 0.00  # 待 Researcher 评估")
    lines.append(f"来源: [外部-小宇宙/{podcast_name}/{title}]")
    lines.append(f"主题: {title}")
    lines.append("分类: 信息挖掘/播客")
    lines.append(f"tags: [{podcast_name}]")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"> **来源**: [外部-小宇宙/{podcast_name}/{title}]")
    lines.append(f"> **播客**: {podcast_name}")
    lines.append(f"> **日期**: {pubdate}")
    lines.append(f"> **链接**: {link}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 节目简介")
    lines.append("")
    lines.append(desc_clean if desc_clean else "（无简介）")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("> **注意**: 本条目仅基于 RSS shownotes，置信度上限 0.69")
    lines.append("> 如需逐字稿，请使用 BibiGPT 或手动转录后重新评估")
    lines.append("")

    return "\n".join(lines)


async def fetch_podcast(podcast_name: str, podcast_id: str, max_items: int = 5) -> list:
    """拉取单个播客的 RSS，返回新节目列表."""
    rss_url = f"{RSSHUB_BASE}/xiaoyuzhou/podcast/{podcast_id}"

    state = load_state()
    last_fetch = state.get(podcast_name, "")

    print(f"[INFO] 拉取: {podcast_name}")
    print(f"[INFO] 上次获取: {last_fetch or '从未'}")

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(rss_url)

    if resp.status_code != 200:
        print(f"[WARN] RSSHub 返回 {resp.status_code}，跳过")
        return []

    items = parse_rss(resp.text)

    # 只保留新节目（通过 pubdate 比较）
    new_items = []
    for item in items:
        pubdate = item["pubdate"]
        if pubdate > last_fetch:
            new_items.append(item)

    # 如果没有新节目，但从未获取过，返回最近 max_items 条
    if not new_items and not last_fetch:
        new_items = items[:max_items]

    if new_items:
        print(f"[INFO] 新节目: {len(new_items)} 条")
        # 更新最新时间
        latest = max(item["pubdate"] for item in new_items if item["pubdate"])
        state[podcast_name] = latest
        save_state(state)
    else:
        print(f"[INFO] 无新节目")

    return new_items


async def main():
    if len(sys.argv) < 2:
        print("用法: python rss_fetcher.py <播客名 或 all>")
        print("支持:")
        for name in PODCASTS:
            print(f"  - {name}")
        print("  - all (全部)")
        sys.exit(1)

    target = sys.argv[1]

    if target == "all":
        targets = PODCASTS.items()
    elif target in PODCASTS:
        targets = [(target, PODCASTS[target])]
    else:
        print(f"[ERROR] 未知播客: {target}")
        print(f"支持: {', '.join(PODCASTS.keys())}, all")
        sys.exit(1)

    all_new = []
    for name, pid in targets:
        items = await fetch_podcast(name, pid)
        all_new.extend([(name, item) for item in items])

    if not all_new:
        print("\n[INFO] 没有新节目")
        return

    print(f"\n[INFO] 共 {len(all_new)} 条新节目，生成 Markdown...")
    for podcast_name, episode in all_new:
        md = format_markdown(podcast_name, episode)
        print("\n" + "=" * 40 + "\n")
        print(f"# {podcast_name}: {episode['title']}")
        print(md)


if __name__ == "__main__":
    asyncio.run(main())
