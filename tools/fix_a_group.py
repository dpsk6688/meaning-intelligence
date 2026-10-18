"""A 组自动修复:
- A1: 根 ROADMAP.md 若内容 <500 字节且含 'notepad'/'文件 2' → 重写为短指针
- A5: README / README.en.md 里作为"理论缩写"出现的 MIT 改为 MI Theory
- A2(部分): docs/roadmap.md 里的 '当前版本 0.1.0' → 0.2.0
"""
from pathlib import Path
import re

ROOT = Path(".")
report = []


def read(p):
    return (ROOT / p).read_text(encoding="utf-8") if (ROOT / p).exists() else None


def write(p, t):
    (ROOT / p).write_text(t, encoding="utf-8")


def step(name, action):
    """执行 action,返回 (success, description)。"""
    try:
        result = action()
        report.append((name, "OK", result or ""))
        print(f"✅ {name}: {result}")
    except Exception as e:
        report.append((name, "FAIL", str(e)))
        print(f"❌ {name}: {e}")


# ---------------------------------------------------------------- A1
def fix_root_roadmap():
    p = ROOT / "ROADMAP.md"
    if not p.exists():
        return "根 ROADMAP.md 不存在,跳过"

    t = p.read_text(encoding="utf-8")
    # 探测是否是误提交的操作提示
    is_garbage = (
        len(t) < 500
        or "notepad" in t.lower()
        or "文件 2" in t
        or "在 cmd 里运行" in t
    )

    if not is_garbage:
        return f"根 ROADMAP.md 内容看起来正常 ({len(t)} 字符),未修改"

    new_content = """# Roadmap

**工程路线图在 [`docs/roadmap.md`](docs/roadmap.md)。**

本文件仅作为 GitHub 根目录的可发现入口。所有版本号以 [`VERSION.yaml`](VERSION.yaml) 为准。
"""
    p.write_text(new_content, encoding="utf-8")
    return f"重写为指针 (旧 {len(t)} 字符 → 新 {len(new_content)} 字符)"


# ---------------------------------------------------------------- A5
def fix_mit_ambiguity():
    """只改 'MIT 缩写' / 'MIT 理论' / 'MIT 是' 这类作为理论出现的 MIT。
    保留 'MIT License' / 'MIT license'。"""
    total = 0
    for fname in ["README.md", "README.en.md"]:
        t = read(fname)
        if t is None:
            continue
        original = t

        # 修复模式:
        # 1) "MIT 缩写" → "MI Theory 缩写"
        # 2) "MIT 是" / "MIT 的" / "MIT 理论" / "MIT 在" → "MI Theory 是/的/理论/在"
        # 3) "使用 MIT" / "以 MIT 为" → "使用 MI Theory" / "以 MI Theory 为"
        replacements = [
            (r"MIT 缩写", "MI Theory 缩写"),
            (r"MIT 理论", "MI Theory 理论"),
            (r"MIT 是", "MI Theory 是"),
            (r"MIT 的", "MI Theory 的"),
            (r"MIT 在", "MI Theory 在"),
            (r"MIT 为", "MI Theory 为"),
            (r"使用 MIT(?![a-zA-Z ]*[Ll]icense)", "使用 MI Theory"),
            (r"以 MIT(?![a-zA-Z ]*[Ll]icense)", "以 MI Theory"),
            (r"MIT (?:项目|研究)", "MI Theory 研究"),
            (r"\bMIT(?:\(|（)", "MI Theory("),
        ]

        for old, new in replacements:
            t2, cnt = re.subn(old, new, t)
            if cnt:
                t = t2
                total += cnt

        if t != original:
            write(fname, t)
    return f"{total} 处 MIT → MI Theory" if total else "无修改"


# ---------------------------------------------------------------- A2 (部分)
def fix_roadmap_version():
    p = ROOT / "docs" / "roadmap.md"
    if not p.exists():
        return "docs/roadmap.md 不存在,跳过"

    t = p.read_text(encoding="utf-8")
    original = t

    # 只改"当前版本 0.1.0"相关的表述
    # 保留历史记录里的 0.1.0
    patterns = [
        (r"当前版本[:：]\s*0\.1\.0", "当前版本:0.2.0"),
        (r"current version[:：]\s*0\.1\.0", "current version: 0.2.0"),
        (r"\*\*Current Release:\*\*\s*0\.1\.0", "**Current Release:** 0.2.0"),
        (r"\*\*当前版本[:：]\*\*\s*0\.1\.0", "**当前版本:** 0.2.0"),
    ]
    n = 0
    for old, new in patterns:
        t2, cnt = re.subn(old, new, t, flags=re.IGNORECASE)
        if cnt:
            t = t2
            n += cnt

    if t != original:
        p.write_text(t, encoding="utf-8")
        return f"docs/roadmap.md {n} 处 0.1.0 → 0.2.0"
    return "docs/roadmap.md 无 '当前版本 0.1.0' 表述,未修改"


print("=" * 70)
print("  A 组自动修复")
print("=" * 70)
step("A1 根 ROADMAP.md 重写", fix_root_roadmap)
step("A5 MIT 去混淆", fix_mit_ambiguity)
step("A2 docs/roadmap.md 版本号", fix_roadmap_version)
print()
print("=" * 70)
print("  完成")
print("=" * 70)