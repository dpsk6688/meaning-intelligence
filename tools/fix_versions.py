"""P0-02/03/04/05: 一次性修正版本一致性缺陷。
用 UTF-8 读写，不受 GBK 控制台影响。"""
from pathlib import Path

ROOT = Path(".")


def replace_all(path, pairs):
    """对文件做字符串替换,返回改动次数。"""
    p = ROOT / path
    if not p.exists():
        print(f"  ⚠️ 未找到 {path}")
        return 0
    text = p.read_text(encoding="utf-8")
    original = text
    n = 0
    for old, new in pairs:
        cnt = text.count(old)
        if cnt:
            text = text.replace(old, new)
            n += cnt
            print(f"  ✅ {path}: {cnt} 处  '{old[:40]}' → '{new[:40]}'")
    if n:
        p.write_text(text, encoding="utf-8")
    return n


def main():
    print("═══ P0 一致性修复 ═══\n")

    total = 0

    # --- P0-02: 白皮书页数 20 → 19 -------------------------------------------
    print("[P0-02] 白皮书页数 20 → 19")
    total += replace_all("index.html", [
        ("20 pages / 7 tables / 2 figures", "19 pages / 7 tables / 2 figures"),
        ("20 页 / 7 表 / 2 图", "19 页 / 7 表 / 2 图"),
    ])
    total += replace_all("README.md", [
        ("20 pages / 7 tables / 2 figures", "19 pages / 7 tables / 2 figures"),
        ("20 页 / 7 表 / 2 图", "19 页 / 7 表 / 2 图"),
    ])
    total += replace_all("README.en.md", [
        ("20 pages, 7 tables, 2 figures", "19 pages, 7 tables, 2 figures"),
    ])
    print()

    # --- P0-03: toolkit 数量 10 → 11 ------------------------------------------
    print("[P0-03] toolkit 数量 10 → 11")
    total += replace_all("README.md", [
        ("10 tools", "11 tools"),
        ("10 份工具", "11 份工具"),
        ("11 fillable checklists", "11 fillable checklists"),  # 已正确,占位
    ])
    total += replace_all("README.en.md", [
        ("11 fillable checklists", "11 fillable checklists"),  # 已正确
        ("10 tools", "11 tools"),
    ])
    print()

    # --- P0-04: 2025 → 2026 ---------------------------------------------------
    print("[P0-04] Copyright 2025 → 2026")
    total += replace_all("index.html", [
        ("© 2025", "© 2026"),
        ("©2025", "©2026"),
        ("2025 Meaning Intelligence", "2026 Meaning Intelligence"),
    ])
    total += replace_all("README.md", [
        ("© 2025", "© 2026"),
        ("2025 Meaning Intelligence", "2026 Meaning Intelligence"),
    ])
    total += replace_all("README.en.md", [
        ("© 2025", "© 2026"),
        ("2025 Meaning Intelligence", "2026 Meaning Intelligence"),
    ])
    print()

    # --- P0-05: 明确 stack = E0 (仅检查,不改内容) ------------------------------
    print("[P0-05] 检查 six-layer stack = E0 声明")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "E0" in readme and ("untested" in readme.lower() or "未经" in readme):
        print("  ✅ README 已含 E0 / untested 声明,无需修改")
    else:
        print("  ⚠️ README 未明确 stack = E0,需要手动加一段")
        print("     建议在六层表格前插入:")
        print("     > **证据状态：E0（概念）。** 六层栈是本项目提出的操作性表示,不是理论本体。")
    print()

    print(f"═══ 完成,共 {total} 处修改 ═══")
    print("\n下一步: cd .. 然后跑 publish.py 推送")


if __name__ == "__main__":
    main()