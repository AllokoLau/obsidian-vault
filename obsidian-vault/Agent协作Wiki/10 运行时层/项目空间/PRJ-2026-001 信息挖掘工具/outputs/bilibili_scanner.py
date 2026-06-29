"""
Bilibili UP主批量扫描器
扫描指定UP主的视频列表，检查AI字幕，批量抓取新视频字幕并入库

用法:
  python bilibili_scanner.py 280780745                  # 张小珺Jùn
  python bilibili_scanner.py 280780745 --force          # 强制重新抓取所有
  python bilibili_scanner.py 280780745 --limit 5        # 只处理最近5个
  python bilibili_scanner.py 280780745 --dry-run        # 预览，不实际抓取

支持的UP主:
  张小珺Jùn｜商业访谈录: 280780745
  晚点LatePost:          478559884
  opus精译:             163682133

输出目录: raw/B站/{UP主名}/
状态追踪: outputs/bilibili_scanner_state.json
"""

import asyncio
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from bilibili_api import user, video, Credential

# 路径
SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parents[4]  # obsidian-vault/
RAW_DIR = VAULT_ROOT / "raw" / "B站"
STATE_FILE = SCRIPT_DIR / "bilibili_scanner_state.json"

# 已知UP主
KNOWN_UPERS = {
    "280780745": "张小珺Jùn｜商业访谈录",
    "478559884": "晚点LatePost",
    "3493292599675775": "厚雪长波",
    "505301413": "十字路口Crossing_Koji杨远骋",
    "163682133": "opus精译",
}


def load_credentials() -> Credential:
    """加载B站登录凭证."""
    cred_file = SCRIPT_DIR / "bilibili_credentials.json"
    if not cred_file.exists():
        print("[ERROR] 未找到凭证文件。请先运行 bilibili_qr_login.py 登录。")
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


def load_state() -> dict:
    """加载已处理视频的记录."""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state: dict):
    """保存已处理视频的记录."""
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def sanitize_filename(text: str) -> str:
    """清理文件名中的非法字符."""
    text = re.sub(r'[\\/:*?"<>|]', '', text)
    text = text.strip()
    return text[:60]  # 限制长度


def format_bilibili_md(bv: str, info: dict, subtitle_text: str) -> str:
    """格式化为B站入库Markdown."""
    title = info.get("title", "未知标题")
    desc = info.get("desc", "")
    owner = info.get("owner", {}).get("name", "未知UP主")
    pubdate = info.get("pubdate", 0)
    date_str = datetime.fromtimestamp(pubdate).strftime("%Y-%m-%d") if pubdate else "未知"
    stat = info.get("stat", {})
    view = stat.get("view", 0)
    danmaku = stat.get("danmaku", 0)
    like = stat.get("like", 0)

    lines = []
    lines.append("---")
    lines.append("type: knowledge")
    lines.append(f"入库日期: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("置信度: 0.70  # B站AI字幕，来源可信")
    lines.append(f"来源: [外部-Bilibili/{bv}]")
    lines.append(f"主题: {title}")
    lines.append("分类: 信息挖掘/B站")
    lines.append(f"tags: [{owner}]")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"> **来源**: [外部-Bilibili/{bv}]")
    lines.append(f"> **UP主**: {owner}")
    lines.append(f"> **发布时间**: {date_str}")
    lines.append(f"> **播放量**: {view}  |  **弹幕**: {danmaku}  |  **点赞**: {like}")
    lines.append(f"> **BV号**: {bv}")
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
    lines.append(subtitle_text if subtitle_text else "（该视频无可用字幕）")

    return "\n".join(lines)


async def fetch_subtitles(bv: str, credential: Credential) -> list:
    """获取视频字幕列表，优先通过 player_info 获取完整字幕URL."""
    v = video.Video(bvid=bv, credential=credential)
    try:
        info = await v.get_info()
        cid = info.get("cid", 0)
    except Exception as e:
        print(f"    [ERROR] 获取视频信息失败: {e}")
        return []

    # 方法1: 通过 get_player_info 获取字幕（更可靠）
    try:
        player_info = await v.get_player_info(cid=cid)
        subtitle_container = player_info.get("subtitle", {})
        # 注意: player_info 中 subtitle.subtitles 是数组（多个字幕轨道）
        sub_list = subtitle_container.get("subtitles", [])
        if sub_list:
            selected = None
            for sub in sub_list:
                if sub.get("lan") in ("zh-CN", "ai-zh", "zh-Hans"):
                    selected = sub
                    break
            if not selected:
                selected = sub_list[0]

            sub_url = selected.get("subtitle_url", "")
            if sub_url.startswith("//"):
                sub_url = "https:" + sub_url

            if sub_url:
                import httpx
                try:
                    async with httpx.AsyncClient() as client:
                        resp = await client.get(sub_url)
                        data = resp.json()
                except Exception as e:
                    print(f"    [ERROR] 下载字幕失败: {e}")
                    return []

                subtitles = []
                for item in data.get("body", []):
                    subtitles.append({
                        "from": item["from"],
                        "to": item["to"],
                        "content": item["content"],
                    })
                if subtitles:
                    return subtitles
    except Exception as e:
        print(f"    [WARN] player_info 获取字幕失败: {e}")

    # 方法2: 回退到 get_info 的 subtitle.list（某些视频可能在此）
    try:
        sub_list = info.get("subtitle", {}).get("list", [])
        if sub_list:
            selected = None
            for sub in sub_list:
                if sub.get("lan") in ("zh-CN", "ai-zh"):
                    selected = sub
                    break
            if not selected:
                selected = sub_list[0]

            sub_url = selected.get("subtitle_url", "")
            if sub_url.startswith("//"):
                sub_url = "https:" + sub_url

            if sub_url:
                import httpx
                async with httpx.AsyncClient() as client:
                    resp = await client.get(sub_url)
                    data = resp.json()

                subtitles = []
                for item in data.get("body", []):
                    subtitles.append({
                        "from": item["from"],
                        "to": item["to"],
                        "content": item["content"],
                    })
                if subtitles:
                    return subtitles
    except Exception as e:
        pass

    return []


def subtitles_to_text(subtitles: list) -> str:
    """将字幕列表转为带时间戳的Markdown文本."""
    if not subtitles:
        return ""

    lines = []
    for s in subtitles:
        start_min = int(s["from"] // 60)
        start_sec = int(s["from"] % 60)
        timestamp = f"[{start_min:02d}:{start_sec:02d}]"
        lines.append(f"{timestamp} {s['content']}")

    return "\n".join(lines)


async def process_upor(uid: str, force: bool = False, limit: int = 0, dry_run: bool = False):
    """处理一个UP主的所有新视频."""
    upor_name = KNOWN_UPERS.get(uid, f"UID_{uid}")
    print(f"\n{'='*50}")
    print(f"[INFO] 扫描UP主: {upor_name} (UID: {uid})")
    print(f"{'='*50}")

    cred = load_credentials()
    state = load_state()
    upor_state = state.get(uid, {"processed": []})
    processed_bvs = set(upor_state.get("processed", []))

    # 拉取视频列表
    u = user.User(int(uid), cred)
    try:
        page = 1
        all_videos = []
        while True:
            result = await u.get_videos(ps=50, pn=page)
            vlist = result.get("list", {}).get("vlist", [])
            if not vlist:
                break
            all_videos.extend(vlist)
            if len(vlist) < 50:
                break
            page += 1
    except Exception as e:
        print(f"[ERROR] 获取视频列表失败: {e}")
        return

    print(f"[INFO] 共 {len(all_videos)} 个视频")

    if limit > 0:
        all_videos = all_videos[:limit]

    # 处理每个视频
    new_count = 0
    subtitle_count = 0
    processed_this_run = []

    for idx, vobj in enumerate(all_videos):
        bvid = vobj["bvid"]
        title = vobj.get("title", "?")
        play = vobj.get("play", 0)

        # 检查是否已处理
        if bvid in processed_bvs and not force:
            print(f"  [{idx+1}/{len(all_videos)}] [SKIP] {bvid} 已处理，跳过")
            continue

        print(f"  [{idx+1}/{len(all_videos)}] [PROC] {bvid} | {title[:40]}...", end="")

        # 获取字幕
        subtitles = await fetch_subtitles(bvid, cred)
        if not subtitles:
            # 即使无字幕也记录为已处理，避免重复检查
            processed_this_run.append(bvid)
            print(f" [WARN] 无字幕，跳过")
            if not dry_run:
                processed_bvs.add(bvid)
            continue

        subtitle_count += 1
        subtitle_text = subtitles_to_text(subtitles)
        print(f" [OK] {len(subtitles)} 条字幕 ({len(subtitle_text)}字)")

        if dry_run:
            processed_this_run.append(bvid)
            continue

        # 获取视频详情
        try:
            v = video.Video(bvid=bvid, credential=cred)
            info = await v.get_info()
        except Exception as e:
            print(f"    [ERROR] 获取详情失败: {e}")
            processed_this_run.append(bvid)
            continue

        # 保存到文件
        output_md = format_bilibili_md(bvid, info, subtitle_text)

        # 文件名: 日期_UP主_标题.md
        today = datetime.now().strftime("%Y%m%d")
        safe_title = sanitize_filename(title)[:40]
        out_name = f"{today}_{sanitize_filename(upor_name)}_{safe_title}.md"
        out_path = RAW_DIR / sanitize_filename(upor_name) / out_name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_md, encoding="utf-8")
        print(f"    [SAVE] 保存至: {out_path.relative_to(VAULT_ROOT)}")

        new_count += 1
        processed_this_run.append(bvid)
        processed_bvs.add(bvid)

    # 保存状态
    if not dry_run:
        upor_state["processed"] = list(processed_bvs)
        upor_state["last_scan"] = datetime.now().isoformat()
        state[uid] = upor_state
        save_state(state)

    print(f"\n[SUMMARY] {upor_name}:")
    print(f"  新处理: {new_count} 个")
    print(f"  有字幕: {subtitle_count} 个")
    print(f"  累计:   {len(processed_bvs)} 个")

    return new_count


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="B站UP主批量扫描器")
    parser.add_argument("uid", nargs="?", help="UP主UID")
    parser.add_argument("--force", action="store_true", help="强制重新处理所有视频")
    parser.add_argument("--limit", type=int, default=0, help="最多处理N个视频")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际抓取")
    parser.add_argument("--all", action="store_true", help="处理所有已知UP主")

    args = parser.parse_args()

    if not args.uid and not args.all:
        print("用法: python bilibili_scanner.py <UID> [选项]")
        print("或: python bilibili_scanner.py --all")
        print("\n已知UP主:")
        for uid, name in KNOWN_UPERS.items():
            print(f"  {uid}: {name}")
        sys.exit(1)

    if args.all:
        uids = list(KNOWN_UPERS.keys())
    else:
        uids = [args.uid]

    total = 0
    for uid in uids:
        count = await process_upor(
            uid=uid,
            force=args.force,
            limit=args.limit,
            dry_run=args.dry_run,
        )
        total += count or 0

    print(f"\n{'='*50}")
    print(f"[DONE] 共处理 {total} 个新视频")
    print(f"{'='*50}")


if __name__ == "__main__":
    asyncio.run(main())
