"""审计仓库一致性:版本号、证据等级、ROADMAP 文件。
只读,不改文件。"""
from pathlib import Path
import re

ROOT = Path(".")


def h(title):
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)


def grep_lines(path, pattern):
    """返回 (行号, 行文本) 列表。"""
    p = ROOT / path
    if not p.exists():
        return []
    out = []
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if re.search(pattern, line):
            out.append((i, line.strip()[:130]))
    return out


def main():
    h("1. VERSION.yaml 是否存在")
    v = ROOT / "VERSION.yaml"
    if v.exists():
        txt = v.read_text(encoding="utf-8")
        for line in txt.splitlines():
            if "version:" in line or line.startswith(("research_system:", "whitepaper:", "toolkit:", "msi_demo:")):
                print(f"  {line.strip()}")
    else:
        print("  ❌ VERSION.yaml 不存在")

    h("2. 出现 '0.1.0' 的所有文件")
    for path in ROOT.rglob("*.md"):
        if ".git" in str(path):
            continue
        hits = grep_lines(path.relative_to(ROOT), r"0\.1\.0")
        if hits:
            print(f"\n  --- {path.relative_to(ROOT)} ---")
            for i, line in hits:
                print(f"    L{i}: {line}")

    h("3. 出现 '0.2.0' 的所有文件")
    for path in ROOT.rglob("*.md"):
        if ".git" in str(path):
            continue
        hits = grep_lines(path.relative_to(ROOT), r"0\.2\.0")
        if hits:
            print(f"\n  --- {path.relative_to(ROOT)} ---")
            for i, line in hits[:3]:
                print(f"    L{i}: {line}")
            if len(hits) > 3:
                print(f"    ... 共 {len(hits)} 处")

    h("4. 根 ROADMAP.md 内容 (前 500 字符)")
    root_rm = ROOT / "ROADMAP.md"
    if root_rm.exists():
        t = root_rm.read_text(encoding="utf-8")
        print(f"  大小: {len(t)} 字符")
        print(f"  前 500 字符:\n{t[:500]}")
    else:
        print("  根 ROADMAP.md 不存在")

    h("5. docs/roadmap.md 里的 '当前版本'")
    for i, line in grep_lines("docs/roadmap.md", r"0\.1\.0|0\.2\.0|当前版本|current"):
        print(f"  L{i}: {line}")

    h("6. README 里的六层证据等级 (L1-L6)")
    for i, line in grep_lines("README.md", r"L[1-6].*E[0-6]"):
        print(f"  L{i}: {line}")

    h("7. docs/evidence.md 里的六层证据等级")
    for i, line in grep_lines("docs/evidence.md", r"L[1-6]"):
        print(f"  L{i}: {line}")

    h("8. README 里 '尚未进入实证检验阶段' 相关表述")
    for i, line in grep_lines("README.md", r"尚未|未进入|not yet|not been"):
        print(f"  L{i}: {line}")

    h("9. README 里 'MIT' 出现情况")
    for i, line in grep_lines("README.md", r"MIT"):
        print(f"  L{i}: {line}")

    print()
    print("=" * 70)
    print("  审计完成")
    print("=" * 70)


if __name__ == "__main__":
    main()