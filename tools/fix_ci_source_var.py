"""修复 CI 与 verify_html.py，让它们兼容新版模板的 TIMELINE_SOURCE 变量名。
旧版模板用 const SOURCE = ...，新版用 const TIMELINE_SOURCE = ...。"""
from pathlib import Path

fixes = [
    # ---- ci.yml: grep 检查 ----
    (
        Path(".github/workflows/ci.yml"),
        [
            # 1. grep 检查（bash）
            (
                """if ! grep -Eq 'const +SOURCE *= *"planned"' "$PLANNED_DIR/meaning_intelligence.html"; then""",
                """if ! grep -Eq 'const +(SOURCE|TIMELINE_SOURCE) *= *"planned"' "$PLANNED_DIR/meaning_intelligence.html"; then""",
            ),
            # 2. Python 内联检查（用于打印时间轴来源）
            (
                """match = re.search(r'const\\s+SOURCE\\s*=\\s*"(planned|measured)"', text)""",
                """match = re.search(r'const\\s+(?:SOURCE|TIMELINE_SOURCE)\\s*=\\s*"(planned|measured)"', text)""",
            ),
        ],
    ),
    # ---- verify_html.py: 关键字检查 ----
    (
        Path("tools/verify_html.py"),
        [
            (
                '''"SOURCE 为合法 JS 字符串": bool(re.search(r'const SOURCE\\s*=\\s*"(measured|planned)"', html)),''',
                '''"SOURCE 为合法 JS 字符串": bool(re.search(r'const\\s+(?:SOURCE|TIMELINE_SOURCE)\\s*=\\s*"(measured|planned)"', html)),''',
            ),
        ],
    ),
]

total = 0
for path, pairs in fixes:
    if not path.exists():
        print(f"⚠️ 跳过不存在的 {path}")
        continue
    text = path.read_text(encoding="utf-8")
    n = 0
    for old, new in pairs:
        if new in text:
            print(f"  ⏭️ {path.name} 已是新版（跳过一处置换）")
            continue
        if old in text:
            text = text.replace(old, new, 1)
            n += 1
            print(f"  ✅ {path.name}: 替换 1 处")
        else:
            print(f"  ❌ {path.name}: 找不到预期字符串：{old[:60]}...")
    if n:
        path.write_text(text, encoding="utf-8")
        total += n
    print()

print(f"总计 {total} 处修改")

# 复验
print("\n═══ 复验 ═══")
checks = []

ci = Path(".github/workflows/ci.yml")
if ci.exists():
    t = ci.read_text(encoding="utf-8")
    checks.append(("ci.yml grep 兼容 TIMELINE_SOURCE", "SOURCE|TIMELINE_SOURCE" in t))

vh = Path("tools/verify_html.py")
if vh.exists():
    t = vh.read_text(encoding="utf-8")
    checks.append(("verify_html.py 兼容 TIMELINE_SOURCE", "SOURCE|TIMELINE_SOURCE" in t))

for label, ok in checks:
    print(f"  {'✅' if ok else '❌'} {label}")