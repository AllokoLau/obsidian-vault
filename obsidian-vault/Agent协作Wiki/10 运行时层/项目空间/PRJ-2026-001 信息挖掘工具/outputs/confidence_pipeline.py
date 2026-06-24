"""
Confidence Pipeline
将 raw/ 中新内容按置信度路由到 process/ 或 wiki/

流程:
  1. 扫描 raw/ 中所有 .md 文件（排除入库模板/目录）
  2. 读取 YAML 头部的 置信度 字段
  3. 根据阈值路由:
     < 0.4  → 丢弃（记日志）
     0.4-0.7 → process/（等待人为判断）
     > 0.7  → wiki/（直接入库）

用法:
  python confidence_pipeline.py                           # 处理所有待处理条目
  python confidence_pipeline.py --dry-run                 # 预览模式，不改动文件
  python confidence_pipeline.py --file <路径>             # 处理单个文件

依赖: 无（仅 Python 标准库）
"""

import re
import sys
import shutil
from datetime import datetime
from pathlib import Path


# 路径
VAULT_ROOT = Path(__file__).resolve().parents[5]  # obsidian-vault/
RAW_DIR = VAULT_ROOT / "raw"
PROCESS_DIR = VAULT_ROOT / "process"
WIKI_DIR = VAULT_ROOT / "wiki"
DISCARD_LOG = Path(__file__).parent / "discard_log.md"

# 阈值
THRESHOLD_LOW = 0.4    # < 0.4 丢弃
THRESHOLD_HIGH = 0.7   # > 0.7 直接入库 wiki/


def extract_confidence(filepath: Path) -> float | None:
    """从文件的 YAML 头中提取置信度值."""
    content = filepath.read_text(encoding="utf-8")

    # 匹配 YAML frontmatter 中的置信度字段
    m = re.search(r'置信度:\s*([0-9]+\.?[0-9]*)', content)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None

    # 也支持带注释的格式: 置信度: 0.85  # 注释
    m = re.search(r'置信度:\s*([0-9]+\.?[0-9]*)', content)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None

    return None


def get_dest_path(src: Path, dest_dir: Path) -> Path:
    """生成目标路径，避免文件名冲突."""
    dest = dest_dir / src.name
    if not dest.exists():
        return dest
    # 加时间戳后缀
    stem = src.stem
    ts = datetime.now().strftime("%H%M%S")
    return dest_dir / f"{stem}_{ts}{src.suffix}"


def log_discard(filepath: Path, confidence: float, reason: str = ""):
    """记录丢弃的条目到日志."""
    DISCARD_LOG.parent.mkdir(parents=True, exist_ok=True)

    entry = (
        f"| {datetime.now().strftime('%Y-%m-%d %H:%M')} "
        f"| {filepath.name} "
        f"| {confidence:.2f} "
        f"| {reason} |\n"
    )

    if DISCARD_LOG.exists():
        with open(DISCARD_LOG, "a", encoding="utf-8") as f:
            f.write(entry)
    else:
        with open(DISCARD_LOG, "w", encoding="utf-8") as f:
            f.write("# 丢弃记录\n\n")
            f.write("| 时间 | 文件 | 置信度 | 原因 |\n")
            f.write("|------|------|--------|------|\n")
            f.write(entry)


def find_pending_files() -> list[Path]:
    """扫描 raw/ 中待处理的 .md 文件（排除模板和 README）。"""
    if not RAW_DIR.exists():
        return []

    files = []
    skip_dirs = {"入库模板", "_已处理", "_失败"}

    for f in RAW_DIR.rglob("*.md"):
        # 跳过模板目录和特殊目录
        if any(d in f.parts for d in skip_dirs):
            continue
        # 跳过 README
        if f.name.upper() == "README.md":
            continue
        files.append(f)

    return files


def add_process_marker(content: str, confidence: float, reason: str) -> str:
    """为 process/ 条目添加待判断标记."""
    marker = (
        "\n\n---\n"
        f"> **状态**: 待人为判断\n"
        f"> **置信度**: {confidence:.2f}\n"
        f"> **原因**: {reason}\n"
        f"> **入库时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    )
    return content + marker


def main():
    dry_run = "--dry-run" in sys.argv

    # 单文件模式
    if "--file" in sys.argv:
        idx = sys.argv.index("--file")
        if idx + 1 < len(sys.argv):
            files = [Path(sys.argv[idx + 1])]
        else:
            print("[ERROR] --file 需要指定文件路径")
            sys.exit(1)
    else:
        files = find_pending_files()

    if not files:
        print("[INFO] raw/ 中没有待处理条目")
        return

    print(f"[INFO] 发现 {len(files)} 个待处理条目")
    if dry_run:
        print("[INFO] 预览模式（不会改动文件）")

    stats = {"wiki": 0, "process": 0, "discard": 0, "unknown": 0}

    for f in sorted(files):
        confidence = extract_confidence(f)
        if confidence is None:
            print(f"  [?] {f.name} — 未找到置信度字段，跳过")
            stats["unknown"] += 1
            continue

        print(f"  [{confidence:.2f}] {f.name}")

        if dry_run:
            if confidence >= THRESHOLD_HIGH:
                print(f"       → wiki/（置信度 {confidence:.2f} >= {THRESHOLD_HIGH}）")
                stats["wiki"] += 1
            elif confidence < THRESHOLD_LOW:
                print(f"       → 丢弃（置信度 {confidence:.2f} < {THRESHOLD_LOW}）")
                stats["discard"] += 1
            else:
                print(f"       → process/（{THRESHOLD_LOW} <= {confidence:.2f} < {THRESHOLD_HIGH}）")
                stats["process"] += 1
            continue

        # 执行路由
        if confidence >= THRESHOLD_HIGH:
            dest = get_dest_path(f, WIKI_DIR)
            shutil.copy2(f, dest)
            f.unlink()
            print(f"       ✅ → wiki/{dest.name}")
            stats["wiki"] += 1

        elif confidence < THRESHOLD_LOW:
            log_discard(f, confidence, f"置信度 {confidence:.2f} < {THRESHOLD_LOW}")
            f.unlink()  # 从 raw/ 删除
            print(f"       🗑 → 丢弃（已记录日志）")
            stats["discard"] += 1

        else:
            content = f.read_text(encoding="utf-8")
            reason = f"置信度 {confidence:.2f} 在待判断区间 [{THRESHOLD_LOW}, {THRESHOLD_HIGH})"
            content = add_process_marker(content, confidence, reason)

            dest = get_dest_path(f, PROCESS_DIR)
            dest.write_text(content, encoding="utf-8")
            f.unlink()
            print(f"       ⏳ → process/{dest.name}")
            stats["process"] += 1

    # 汇总
    print(f"\n{'='*40}")
    print(f"汇总 (raw/ → 路由)：")
    print(f"  wiki/:    {stats['wiki']}")
    print(f"  process/: {stats['process']}")
    print(f"  丢弃:     {stats['discard']}")
    print(f"  跳过:     {stats['unknown']}")
    print(f"  合计:     {sum(stats.values())}")


if __name__ == "__main__":
    main()
