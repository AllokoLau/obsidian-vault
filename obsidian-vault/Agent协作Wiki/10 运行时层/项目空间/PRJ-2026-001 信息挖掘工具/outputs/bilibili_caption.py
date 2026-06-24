"""
Bilibili Caption Fetcher
从 B站视频获取 AI 字幕，输出结构化 Markdown

用法:
  python bilibili_caption.py BV1ykA3zPEoD
  python bilibili_caption.py https://www.bilibili.com/video/BV1ykA3zPEoD

依赖: bilibili-api-python (pip install bilibili-api-python)
凭证: 需要同级目录的 bilibili_credentials.json (由 bilibili_qr_login.py 生成)
"""

import asyncio
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from bilibili_api import video, Credential


def resolve_bv(input_str: str) -> str:
    """从 URL 或纯 BV 号中提取 BV号."""
    # 已经是纯 BV 号
    if re.match(r'^BV[a-zA-Z0-9]{10,}$', input_str.strip()):
        return input_str.strip()
    # 从 URL 中提取
    m = re.search(r'(BV[a-zA-Z0-9]{10,})', input_str)
    if m:
        return m.group(1)
    raise ValueError(f"无法从输入中提取 BV 号: {input_str}")


def load_credentials() -> Credential:
    """加载之前保存的登录凭证."""
    cred_file = Path(__file__).parent / "bilibili_credentials.json"
    if not cred_file.exists():
        print("[ERROR] 未找到凭证文件。请先运行 bilibili_qr_login.py 登录。")
        print(f"  预期路径: {cred_file}")
        sys.exit(1)

    with open(cred_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Credential(
        sessdata=data.get("sessdata"),
        bili_jct=data.get("bili_jct"),
        buvid3=data.get("buvid3"),
        dedeuserid=data.get("dedeuserid"),
        ac_time_value=data.get("ac_time_value"),
    )


async def fetch_video_info(bv: str, credential: Credential) -> dict:
    """获取视频基本信息."""
    v = video.Video(bvid=bv, credential=credential)
    info = await v.get_info()
    return info


async def fetch_subtitles(bv: str, credential: Credential, preferred_lang: str = "zh-CN") -> list:
    """获取视频字幕列表，返回字幕内容列表."""
    v = video.Video(bvid=bv, credential=credential)
    info = await v.get_info()

    subtitle_list = info.get("subtitle", {}).get("list", [])
    if not subtitle_list:
        return []

    # 找首选语言的字幕
    selected = None
    for sub in subtitle_list:
        if sub.get("lan") == preferred_lang:
            selected = sub
            break
    # 没有首选语言就用第一个
    if not selected and subtitle_list:
        selected = subtitle_list[0]

    if not selected:
        return []

    import httpx
    sub_url = selected["subtitle_url"]
    if sub_url.startswith("//"):
        sub_url = "https:" + sub_url

    async with httpx.AsyncClient() as client:
        resp = await client.get(sub_url)
        data = resp.json()

    # 提取字幕文本和时间戳
    subtitles = []
    for item in data.get("body", []):
        subtitles.append({
            "from": item["from"],
            "to": item["to"],
            "content": item["content"],
        })
    return subtitles


def subtitles_to_text(subtitles: list) -> str:
    """将字幕列表转为结构化的 Markdown 文本."""
    if not subtitles:
        return "[该视频无可用字幕]"

    lines = []
    for s in subtitles:
        start_min = int(s["from"] // 60)
        start_sec = int(s["from"] % 60)
        timestamp = f"[{start_min:02d}:{start_sec:02d}]"
        lines.append(f"{timestamp} {s['content']}")

    return "\n".join(lines)


def format_output(bv: str, info: dict, subtitle_text: str) -> str:
    """生成最终 Markdown 输出."""
    title = info.get("title", "未知标题")
    desc = info.get("desc", "")
    owner = info.get("owner", {}).get("name", "未知UP主")
    pubdate = info.get("pubdate", 0)
    date_str = datetime.fromtimestamp(pubdate).strftime("%Y-%m-%d") if pubdate else "未知"
    view = info.get("stat", {}).get("view", 0)
    danmaku = info.get("stat", {}).get("danmaku", 0)

    lines = []
    lines.append("---")
    lines.append(f"type: knowledge")
    lines.append(f"入库日期: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"置信度: 0.00  # 待 Researcher 评估")
    lines.append(f"来源: [外部-Bilibili/{bv}]")
    lines.append(f"主题: {title}")
    lines.append(f"分类: 信息挖掘/B站")
    lines.append("tags: []")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"> **来源**: [外部-Bilibili/{bv}]")
    lines.append(f"> **UP主**: {owner}")
    lines.append(f"> **发布时间**: {date_str}")
    lines.append(f"> **播放量**: {view}  |  **弹幕**: {danmaku}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 视频简介")
    lines.append("")
    lines.append(desc if desc else "（无简介）")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 字幕全文")
    lines.append("")
    lines.append(subtitle_text)

    return "\n".join(lines)


async def main():
    if len(sys.argv) < 2:
        print("用法: python bilibili_caption.py <BV号 或 B站URL>")
        print("示例: python bilibili_caption.py BV1ykA3zPEoD")
        sys.exit(1)

    input_str = sys.argv[1]
    try:
        bv = resolve_bv(input_str)
    except ValueError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    credential = load_credentials()

    print(f"[INFO] 获取视频信息: {bv}")
    info = await fetch_video_info(bv, credential)
    print(f"[INFO] 标题: {info.get('title', '未知')}")

    print(f"[INFO] 获取字幕...")
    subtitles = await fetch_subtitles(bv, credential)

    if subtitles:
        print(f"[INFO] 获取到 {len(subtitles)} 条字幕 (语言: {subtitles[0].get('lan', 'unknown')})")
    else:
        print(f"[INFO] 该视频无可用字幕")

    subtitle_text = subtitles_to_text(subtitles)
    output = format_output(bv, info, subtitle_text)

    # 输出到 stdout，方便重定向
    print("\n" + "=" * 40 + "\n")
    print(output)


if __name__ == "__main__":
    asyncio.run(main())
