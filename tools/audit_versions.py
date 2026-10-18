"""扫描所有文件里的版本数字,找出不一致处。"""
import re
from pathlib import Path

ROOT = Path(".")

SCAN = ["README.md", "README.en.md", "index.html", "CHANGELOG.md", "CITATION.cff"]
PATTERNS = [
    (r"20\s*页", "白皮书页数(中文)"),
    (r"20\s*pages?", "白皮书页数(英文)"),
    (r"19\s*页", "白皮书页数(中文)"),
    (r"19\s*pages?", "白皮书页数(英文)"),
    (r"10\s*tools?", "toolkit数量"),
    (r"11\s*tools?", "toolkit数量"),
    (r"10\s*份工具", "toolkit数量(中文)"),
    (r"11\s*份工具", "toolkit数量(中文)"),
    (r"10\s*fillable", "toolkit数量(英文)"),
    (r"11\s*fillable", "toolkit数量(英文)"),
    (r"©\s*20\d\d", "copyright"),
    (r"v?0?\.?1\.0", "版本号 1.0"),
    (r"v?0?\.?2\.0", "版本号 2.0"),
    (r"V7\.0", "正典版本"),
]


def main():
    print("═══ 版本信号扫描 ═══\n")
    for fname in SCAN:
        p = ROOT / fname
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        lines = text.splitlines()
        print(f"--- {fname} ---")
        found = False
        for lineno, line in enumerate(lines, 1):
            for pattern, label in PATTERNS:
                if re.search(pattern, line):
                    snippet = line.strip()[:100]
                    print(f"  L{lineno:4d} [{label:20s}] {snippet}")
                    found = True
        if not found:
            print("  (无匹配)")
        print()


if __name__ == "__main__":
    main()