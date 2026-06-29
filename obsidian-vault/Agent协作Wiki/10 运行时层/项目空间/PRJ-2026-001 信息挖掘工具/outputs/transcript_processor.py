"""
Transcript Processor  —  播客逐字稿文案处理工具

功能：
  1. 读取含 [MM:SS] 时间戳的原始逐字稿
  2. 时间间隔分析 → 自动识别话题分段边界
  3. 统计信息输出（时长、字幕数、语速等）
  4. 生成精炼后的 wiki 条目框架

用法：
  python transcript_processor.py <输入.md> [选项]

选项：
  --analyze     仅分析结构，输出统计信息
  --refine      生成精炼后的 wiki 条目格式（含分段，待填充核心结论/要点）
  --prompt      生成供 Claude 处理用的完整提示
  --output PATH 输出到指定文件（默认 stdout）

示例：
  python transcript_processor.py 厚雪长波_xxx.md --analyze
  python transcript_processor.py 厚雪长波_xxx.md --refine --output 精炼版.md
"""

import re
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta


def parse_transcript(text: str) -> list[dict]:
    """
    解析含 [MM:SS] 时间戳的逐字稿文本。

    返回: [{"time_sec": int, "timestamp": "MM:SS", "text": str}, ...]
    """
    entries = []
    # 匹配 [MM:SS] 或 [MM:SS.xx] 格式的时间戳
    pattern = re.compile(r'\[(\d{1,2}):(\d{2})(?:\.\d+)?\]\s*(.*?)(?=\n\[|\Z)', re.DOTALL)

    for m in pattern.finditer(text):
        minutes = int(m.group(1))
        seconds = int(m.group(2))
        content = m.group(3).strip()
        total_seconds = minutes * 60 + seconds
        entries.append({
            "time_sec": total_seconds,
            "timestamp": f"{minutes:02d}:{seconds:02d}",
            "text": content,
        })

    return entries


def analyze_gaps(entries: list[dict], gap_threshold: float = 15.0) -> list[dict]:
    """
    分析时间间隔，识别话题边界。

    gap_threshold: 间隔超过此秒数视为分段点
    返回带分段标记的条目列表
    """
    if not entries:
        return []

    segments = []
    current_segment = {"start": entries[0], "entries": [entries[0]]}

    for i in range(1, len(entries)):
        gap = entries[i]["time_sec"] - entries[i-1]["time_sec"]
        if gap > gap_threshold:
            # 新段落
            current_segment["end"] = entries[i-1]
            segments.append(current_segment)
            current_segment = {"start": entries[i], "entries": [entries[i]]}
        else:
            current_segment["entries"].append(entries[i])

    # 最后一段
    if current_segment["entries"]:
        current_segment["end"] = entries[-1]
        segments.append(current_segment)

    return segments


def format_timestamp(seconds: int) -> str:
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def seconds_to_hms(seconds: int) -> str:
    h, r = divmod(seconds, 3600)
    m, s = divmod(r, 60)
    if h > 0:
        return f"{h}时{m}分{s}秒"
    else:
        return f"{m}分{s}秒"


def analyze(entries: list[dict]) -> dict:
    """分析逐字稿统计信息。"""
    if not entries:
        return {"error": "无有效字幕"}

    total_duration = entries[-1]["time_sec"] - entries[0]["time_sec"]
    total_count = len(entries)

    # 计算语速（字/分钟）
    total_chars = sum(len(e["text"]) for e in entries)
    duration_min = total_duration / 60 if total_duration > 0 else 1
    speed = total_chars / duration_min if duration_min > 0 else 0

    # 最长单句
    longest = max(entries, key=lambda e: len(e["text"]))

    # 分段
    segments = analyze_gaps(entries, gap_threshold=15.0)

    return {
        "total_duration_sec": total_duration,
        "total_duration_display": seconds_to_hms(total_duration),
        "subtitle_count": total_count,
        "total_chars": total_chars,
        "avg_speed_cpm": round(speed, 1),  # chars per minute
        "longest_subtitle": {"time": longest["timestamp"], "text": longest["text"], "chars": len(longest["text"])},
        "segment_count": len(segments),
        "segments": [
            {
                "start": s["start"]["timestamp"],
                "end": s["end"]["timestamp"],
                "duration_sec": s["end"]["time_sec"] - s["start"]["time_sec"] if s["end"]["time_sec"] > s["start"]["time_sec"] else 0,
                "subtitle_count": len(s["entries"]),
                "chars": sum(len(e["text"]) for e in s["entries"]),
                "first_text": s["entries"][0]["text"][:60] if s["entries"] else "",
            }
            for s in segments
        ],
    }


def generate_prompt(entries: list[dict], title: str, source: str, stats: dict) -> str:
    """生成供 Claude 处理用的完整提示。"""
    segments = analyze_gaps(entries, gap_threshold=15.0)

    text = f"""# 逐字稿处理任务

## 基本信息
- 标题: {title}
- 来源: {source}
- 总时长: {stats['total_duration_display']}
- 字幕数: {stats['subtitle_count']}
- 分段数: {stats['segment_count']}

## 任务要求

请对以下播客逐字稿进行文案处理：

1. **核心结论**：用 3-5 句话概括本期播客的核心内容
2. **章节速览**：按话题分段，列出每个段落的时间范围和话题
3. **关键要点**：提取本期最重要的 5-10 个观点/知识点，每个用 2-3 句说明
4. **精彩引述**：标注 3-5 处嘉宾最精彩的直接引语，注明时间戳
5. 整体使用中文 Markdown，时间戳保持 [MM:SS] 格式

## 逐字稿分段内容

"""

    for i, seg in enumerate(segments):
        start_ts = seg["start"]["timestamp"]
        end_ts = seg["end"]["timestamp"]
        first_text = seg["entries"][0]["text"][:80]
        text += f"\n### 分段 {i+1} ({start_ts}-{end_ts})\n"
        text += f"> 起始句: {first_text}\n\n"
        for e in seg["entries"]:
            text += f"[{e['timestamp']}] {e['text']}\n"

    return text


def generate_refined_output(entries: list[dict], title: str, source: str,
                             stats: dict, source_tag: str, tags: list[str],
                             category: str = "信息挖掘/小宇宙") -> str:
    """生成精炼后的 wiki 条目框架。"""
    segments = analyze_gaps(entries, gap_threshold=30.0)

    lines = []
    lines.append("---")
    lines.append(f"type: knowledge")
    lines.append(f"入库日期: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"置信度: 0.80")
    lines.append(f"主题: {title}")
    lines.append(f"分类: {category}")
    lines.append(f"来源: [{source_tag}]")
    lines.append(f"tags: [{', '.join(tags)}]")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append("## 核心结论")
    lines.append("")
    lines.append(f"<!-- TODO: 由 Claude 阅读全文后填写 — 3-5 句话概括本期核心内容 -->")
    lines.append("")
    lines.append(f"---")
    lines.append("")
    lines.append("## 详细内容")
    lines.append("")
    lines.append("### 背景")
    lines.append("")
    lines.append(f"- **来源**: {source}")
    lines.append(f"- **时长**: {stats['total_duration_display']}")
    lines.append(f"- **字幕数**: {stats['subtitle_count']} 条")
    lines.append(f"- **语速**: {stats['avg_speed_cpm']} 字/分钟")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("### 章节速览")
    lines.append("")
    lines.append("| 时间段 | 话题 | 要点 |")
    lines.append("|--------|------|------|")
    for i, seg in enumerate(segments):
        start_ts = seg["start"]["timestamp"]
        end_ts = seg["end"]["timestamp"]
        lines.append(f"| {start_ts}-{end_ts} | <!-- 话题{i+1} --> | <!-- 要点 --> |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("### 关键要点")
    lines.append("")
    lines.append("<!-- TODO: Claude 阅读后提炼 5-10 个核心观点 -->")
    lines.append("")
    lines.append("1. **要点1** — 说明...")
    lines.append("2. **要点2** — 说明...")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("### 精彩引述")
    lines.append("")
    lines.append("<!-- TODO: Claude 阅读后标注 3-5 处精彩引语 -->")
    lines.append("")
    lines.append("> [MM:SS] \"引述内容\"")
    lines.append("> → 解读")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("### 逐字稿全文（原文备查）")
    lines.append("")
    for e in entries:
        lines.append(f"[{e['timestamp']}] {e['text']}")

    lines.append("")
    lines.append("## 关联")
    lines.append("")
    lines.append(f"- [[{tags[0]}]]" if tags else "")
    lines.append(f"- [[小宇宙]]")
    lines.append("")
    lines.append("## 备注")
    lines.append("")
    lines.append(f"> 置信度 0.80：完整 AI 逐字稿含时间戳。需人工审核核心结论和要点。")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"[ERROR] 文件不存在: {input_path}")
        sys.exit(1)

    # 判断模式
    mode = "refine"  # default
    output_path = None

    remaining = sys.argv[2:]
    i = 0
    while i < len(remaining):
        if remaining[i] == "--analyze":
            mode = "analyze"
        elif remaining[i] == "--refine":
            mode = "refine"
        elif remaining[i] == "--prompt":
            mode = "prompt"
        elif remaining[i] == "--output" and i + 1 < len(remaining):
            output_path = Path(remaining[i + 1])
            i += 1
        i += 1

    # 读取文件
    content = input_path.read_text(encoding="utf-8")

    # 提取元数据
    title = "未知标题"
    source = "未知来源"
    source_tag = "外部-播客"
    tags = ["播客"]
    category = "信息挖掘/小宇宙"

    yaml_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if yaml_match:
        yaml_text = yaml_match.group(1)
        title_m = re.search(r'主题:\s*(.*)', yaml_text)
        if title_m:
            title = title_m.group(1).strip()
        source_m = re.search(r'来源:\s*\[?(.*?)\]?', yaml_text)
        if source_m:
            source_tag = source_m.group(1).strip().strip("[]")
        tags_m = re.search(r'tags:\s*\[(.*?)\]', yaml_text)
        if tags_m:
            tags = [t.strip() for t in tags_m.group(1).split(",") if t.strip()]
        cat_m = re.search(r'分类:\s*(.*)', yaml_text)
        if cat_m:
            category = cat_m.group(1).strip()

    # 解析逐字稿
    entries = parse_transcript(content)

    if not entries:
        print(f"[ERROR] 未找到时间戳格式的逐字稿")
        sys.exit(1)

    # 分析（播客用60秒间隔，更符合话题分段）
    stats = analyze(entries)
    # 重新用更合理的阈值分段
    segments = analyze_gaps(entries, gap_threshold=60.0)
    stats['segment_count'] = len(segments)
    stats['segments'] = [
        {
            "start": s["start"]["timestamp"],
            "end": s["end"]["timestamp"],
            "duration_sec": s["end"]["time_sec"] - s["start"]["time_sec"] if s["end"]["time_sec"] > s["start"]["time_sec"] else 0,
            "subtitle_count": len(s["entries"]),
            "chars": sum(len(e["text"]) for e in s["entries"]),
            "first_text": s["entries"][0]["text"][:60] if s["entries"] else "",
        }
        for s in segments
    ]

    if mode == "analyze":
        print(f"\n[ANALYSIS] 逐字稿分析报告")
        print(f"{'='*50}")
        print(f"  标题:        {title}")
        print(f"  来源:        {source_tag}")
        print(f"  总时长:      {stats['total_duration_display']}")
        print(f"  字幕总条数:  {stats['subtitle_count']}")
        print(f"  总字符数:    {stats['total_chars']}")
        print(f"  平均语速:    {stats['avg_speed_cpm']} 字/分钟")
        print(f"  自动分段数:  {stats['segment_count']}")
        print(f"  最长单句:    [{stats['longest_subtitle']['time']}] \"{stats['longest_subtitle']['text'][:40]}...\" ({stats['longest_subtitle']['chars']}字)")
        print(f"{'='*50}")
        print(f"\n话题分段明细:")
        print(f"{'='*50}")
        for i, seg in enumerate(stats['segments']):
            dur = seconds_to_hms(seg['duration_sec'])
            print(f"  [{seg['start']}-{seg['end']}] ({dur}) {seg['subtitle_count']}条字幕, {seg['chars']}字")
            print(f"    开头: \"{seg['first_text'][:50]}\"")
        print(f"{'='*50}")

    elif mode == "prompt":
        prompt = generate_prompt(entries, title, source_tag, stats)
        if output_path:
            output_path.write_text(prompt, encoding="utf-8")
            print(f"[OK]  提示已写入: {output_path}")
        else:
            print(prompt)

    elif mode == "refine":
        output = generate_refined_output(entries, title, source_tag, stats, source_tag, tags, category)
        if output_path:
            output_path.write_text(output, encoding="utf-8")
            print(f"[OK]  精炼版已写入: {output_path}")
            print(f"      统计: {stats['total_duration_display']}, {stats['subtitle_count']}条字幕, {stats['segment_count']}个分段")
        else:
            print(output)

    else:
        print(f"[ERROR] 未知模式: {mode}")


if __name__ == "__main__":
    main()
