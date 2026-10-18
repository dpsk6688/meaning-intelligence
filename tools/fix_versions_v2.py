"""P0-02/03/04 收尾:修正 README badge / CITATION / CHANGELOG。"""
from pathlib import Path

ROOT = Path(".")


def replace_all(path, pairs):
    p = ROOT / path
    if not p.exists():
        print(f"  ⚠️ 未找到 {path}")
        return 0
    text = p.read_text(encoding="utf-8")
    n = 0
    for old, new in pairs:
        cnt = text.count(old)
        if cnt:
            text = text.replace(old, new)
            n += cnt
            print(f"  ✅ {path}: {cnt} 处  '{old[:50]}' → '{new[:50]}'")
    if n:
        p.write_text(text, encoding="utf-8")
    return n


def append_changelog_0_2_0():
    """在 CHANGELOG.md 的 [0.1.0] 段之前插入 [0.2.0] 段。"""
    p = ROOT / "CHANGELOG.md"
    if not p.exists():
        print("  ⚠️ 未找到 CHANGELOG.md")
        return 0
    text = p.read_text(encoding="utf-8")
    if "[0.2.0]" in text:
        print("  ✅ CHANGELOG.md 已含 [0.2.0] 段,跳过")
        return 0

    new_section = """## [0.2.0] - 2026-10-08

### Added
- **`VERSION.yaml`** — 单一版本源,所有版本号以此为唯一真相
- **`README.en.md`** — 英文版 README
- **`ROADMAP.md`** — 工程路线图 v0.2.0
- **`tools/audit_versions.py`** — 版本信号一致性扫描
- **`tools/fix_versions.py`** — 一致性缺陷批量修复
- **`tools/fix_versions_v2.py`** — badge / citation / changelog 收尾修复

### Changed
- 统一白皮书页数:`20` → `19`(与实际一致)
- 统一 Copyright:`2025` → `2026`
- `README.md` badge:`0.1.0` → `0.2.0`
- `CITATION.cff`:`0.1.0` → `0.2.0`

### Fixed
- 版本信号在 README / index.html / config.json / whitepaper 之间漂移的问题

---

"""
    # 在 "## [0.1.0]" 之前插入
    marker = "## [0.1.0]"
    if marker not in text:
        print("  ⚠️ CHANGELOG.md 未找到 '## [0.1.0]' 标记,无法插入")
        return 0
    text = text.replace(marker, new_section + marker, 1)
    p.write_text(text, encoding="utf-8")
    print("  ✅ CHANGELOG.md: 已插入 [0.2.0] 段")
    return 1


def main():
    print("═══ P0 收尾修复 ═══\n")

    total = 0

    # README.md badge
    print("[README] badge 0.1.0 → 0.2.0")
    total += replace_all("README.md", [
        ("version-0.1.0-6B4C9A", "version-0.2.0-6B4C9A"),
        ("version-0.1.0", "version-0.2.0"),
    ])
    print()

    # CITATION.cff
    print("[CITATION] version 0.1.0 → 0.2.0")
    total += replace_all("CITATION.cff", [
        ('version: "0.1.0"', 'version: "0.2.0"'),
        ("version: '0.1.0'", "version: '0.2.0'"),
    ])
    print()

    # CHANGELOG.md
    print("[CHANGELOG] 插入 [0.2.0] 段")
    total += append_changelog_0_2_0()
    print()

    # 复验
    print("═══ 复验 ═══\n")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    checks = [
        ("README badge 含 0.2.0", "version-0.2.0" in readme),
        ("README 不再含 badge 0.1.0", "version-0.1.0-" not in readme),
        ("CITATION version = 0.2.0", 'version: "0.2.0"' in citation),
        ("CHANGELOG 含 [0.2.0]", "[0.2.0]" in changelog),
        ("CHANGELOG 保留 [0.1.0]", "[0.1.0]" in changelog),
    ]
    all_ok = True
    for label, ok in checks:
        print(f"  {'✅' if ok else '❌'} {label}")
        if not ok:
            all_ok = False

    print()
    print(f"═══ 共 {total} 处修改,{'全部通过' if all_ok else '有未通过项'} ═══")


if __name__ == "__main__":
    main()