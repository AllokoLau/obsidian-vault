"""
Extract subtitle JSON files and save as structured Markdown
"""
import json
import os
import re
from datetime import datetime

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_RAW = SCRIPT_DIR  # same directory

def format_timestamp(seconds):
    """Convert seconds to [MM:SS] format."""
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"[{m:02d}:{s:02d}]"

def extract_content_from_subtitle_file(filepath):
    """Extract subtitle entries from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    body = data.get('body', [])
    entries = []
    for item in body:
        entries.append({
            'from': item['from'],
            'to': item['to'],
            'content': item['content']
        })
    return entries

def build_markdown(bv, title, pubdate_ts, duration, desc, entries,
                   upload_date=None):
    """Build structured markdown content."""
    if upload_date is None:
        upload_date = datetime.now().strftime('%Y-%m-%d')

    pubdate_str = datetime.fromtimestamp(pubdate_ts).strftime('%Y-%m-%d')

    lines = []
    lines.append("---")
    lines.append("type: knowledge")
    lines.append(f"入库日期: {upload_date}")
    lines.append("置信度: 0.70  # B站 AI 字幕，待评估")
    lines.append(f"来源: [外部-Bilibili/{bv}]")
    lines.append(f"主题: {title}")
    lines.append("分类: 信息挖掘/B站/晚点LatePost")
    lines.append("tags: [晚点LatePost, B站, 商业报道]")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"> **来源**: [外部-Bilibili/{bv}]")
    lines.append("> **UP主**: 晚点LatePost")
    lines.append(f"> **发布时间**: {pubdate_str}")
    lines.append(f"> **时长**: {duration//60}分{duration%60}秒  |  **字幕条数**: {len(entries)}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 视频简介")
    lines.append("")
    # Clean desc
    desc_clean = desc.replace('\\n', '\n').replace('\\"', '"') if desc else '（无简介）'
    lines.append(desc_clean)
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 字幕全文")
    lines.append("")

    for e in entries:
        lines.append(f"{format_timestamp(e['from'])} {e['content']}")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 关键要点")
    lines.append("")
    lines.append("<!-- TODO: 由 Writer 精炼后填写 -->")
    lines.append("")
    lines.append("## 关联")
    lines.append("")
    lines.append("- [[晚点LatePost]]")
    lines.append("- [[B站]]")
    lines.append("")
    lines.append("## 备注")
    lines.append("")
    lines.append("> 置信度 0.70：B站 AI 字幕，可能有识别错误。需 Writer 精炼后提升置信度。")

    return '\n'.join(lines)

def get_meta(meta_file):
    """Read metadata from meta JSON file."""
    with open(meta_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# Video data
videos = [
    {
        'bv': 'BV1Zb6EB2EF8',
        'json_file': r'D:\Alloko\obsidian-vault\raw\晚点LatePost\..\..\..\..\tmp\latepost_subtitles\BV1Zb6EB2EF8.json',
        'pubdate': 1769850000,
        'duration': 255,
        'desc': '从街边零食店起家，一群小镇青年，第一次创业，就做成了中国最大的休闲食品饮料零售公司。刚在港股上市的鸣鸣很忙，如何用十年时间成为下沉零售之王？'
    },
    {
        'bv': 'BV1km4AzwE1G',
        'json_file': r'D:\Alloko\obsidian-vault\raw\晚点LatePost\..\..\..\..\tmp\latepost_subtitles\BV1km4AzwE1G.json',
        'pubdate': 1760184464,
        'duration': 343,
        'desc': '今年上半年，A股最年轻董事长出现在一家2000亿传统车企。90后董事长上任，公司市值单周暴涨60%。不靠接班继承，他们如何掌舵千亿市值公司？'
    },
    {
        'bv': 'BV1rLeXzQEXi',
        'json_file': r'D:\Alloko\obsidian-vault\raw\晚点LatePost\..\..\..\..\tmp\latepost_subtitles\BV1rLeXzQEXi.json',
        'pubdate': 1756372200,
        'duration': 321,
        'desc': '深圳两家世界第一的公司，最近打起来了。影石Insta360和大疆，一个是全景相机全球第一，一个是无人机全球第一。后来者影石，如何避免被巨头抄家？'
    },
    {
        'bv': 'BV12unizyEwA',
        'json_file': r'D:\Alloko\obsidian-vault\raw\晚点LatePost\..\..\..\..\tmp\latepost_subtitles\BV12unizyEwA.json',
        'pubdate': 1759377600,
        'duration': 3499,
        'desc': '张益唐，70岁数学家，北京大学1978级校友。他最新出版的科普书《素数之恋》的中文版前言中写道：2022年，我完成了一项多年未完成的数学工作，那一年正好是7月3号——而2012年7月3号，正是他上一次重大突破的日子。'
    }
]

for v in videos:
    json_path = v['json_file']
    if not os.path.exists(json_path):
        print(f"[SKIP] {v['bv']} - JSON not found: {json_path}")
        continue

    entries = extract_content_from_subtitle_file(json_path)
    if not entries:
        print(f"[SKIP] {v['bv']} - No entries found")
        continue

    # Clean title
    title_base = videos[videos.index(v)]['bv']  # just use BV as placeholder
    title = f"{v['bv']} - {v['desc'][:30]}..."

    # Build filename
    pubdate_str = datetime.fromtimestamp(v['pubdate']).strftime('%Y-%m-%d')
    title_short = v['desc'].split('，')[0][:20] if v['desc'] else v['bv']
    filename = f"{pubdate_str}_{title_short}.md"

    markdown = build_markdown(
        bv=v['bv'],
        title=title,
        pubdate_ts=v['pubdate'],
        duration=v['duration'],
        desc=v['desc'],
        entries=entries,
        upload_date='2026-06-24'
    )

    filepath = os.path.join(VAULT_RAW, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"[OK] {v['bv']}: {len(entries)} entries -> {filename}")
