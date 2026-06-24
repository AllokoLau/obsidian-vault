"""
Test script to check what subtitle types are available for a Bilibili video
"""
import asyncio
import json
import sys
from pathlib import Path

from bilibili_api import video, Credential

CRED_FILE = Path(__file__).resolve().parent.parent / "outputs" / "bilibili_credentials.json"

def load_credentials() -> Credential:
    with open(CRED_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Credential(
        sessdata=data.get("sessdata"),
        bili_jct=data.get("bili_jct"),
        buvid3=data.get("buvid3"),
        dedeuserid=data.get("dedeuserid"),
        ac_time_value=data.get("ac_time_value"),
    )

async def main(bv: str):
    cred = load_credentials()
    v = video.Video(bvid=bv, credential=cred)
    info = await v.get_info()

    # Check subtitle info
    subtitle_data = info.get("subtitle", {})
    print(f"\n=== Subtitle Info for {bv} ===")
    print(f"Subtitle key exists: {'subtitle' in info}")
    print(f"Full subtitle field: {json.dumps(subtitle_data, indent=2, ensure_ascii=False)[:2000]}")

    # Check if there are any subtitle lists
    sub_list = subtitle_data.get("list", [])
    print(f"\nSubtitle list count: {len(sub_list)}")
    for i, sub in enumerate(sub_list):
        print(f"  Subtitle {i}:")
        print(f"    lan: {sub.get('lan')}")
        print(f"    lan_doc: {sub.get('lan_doc')}")
        print(f"    subtitle_url: {sub.get('subtitle_url', 'N/A')[:100]}")

    # Try to get player info for subtitle tracks
    try:
        player_info = await v.get_player_info(cid=info.get("cid", 0))
        print(f"\nPlayer info keys: {list(player_info.keys())}")
        # Check for subtitle-related fields
        for key in ["subtitle", "subtitles", "subtitle_url", "sub"]:
            if key in player_info:
                print(f"Player info contains '{key}': {json.dumps(player_info[key], ensure_ascii=False)[:500]}")
    except Exception as e:
        print(f"\nPlayer info error: {e}")

    # Try get_cid to see all available cids/subtitles
    try:
        pages = await v.get_pages()
        print(f"\nPages: {len(pages)}")
        for pg in pages:
            cid = pg.get("cid", 0)
            print(f"  Page: cid={cid}, part={pg.get('part', 'N/A')}")
    except Exception as e:
        print(f"Pages error: {e}")

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "BV1cTEL6bECL"))
