"""修复 build.py 里的两个路径：
  html_template.html     ->  templates/html_template.html
  meaning_intelligence.py -> scenes/meaning_intelligence.py
"""
from pathlib import Path

p = Path("msi/build.py")
text = p.read_text(encoding="utf-8")

# 修复 1：html_template 路径
OLD1 = 'html = (HERE / "html_template.html").read_text(encoding="utf-8")'
NEW1 = 'html = (HERE / "templates" / "html_template.html").read_text(encoding="utf-8")'

# 修复 2：meaning_intelligence.py 路径
OLD2 = '"__SRC_PY__": js((HERE / "meaning_intelligence.py").read_text(encoding="utf-8")),'
NEW2 = '"__SRC_PY__": js((HERE / "scenes" / "meaning_intelligence.py").read_text(encoding="utf-8")),'

n = 0
if NEW1 in text:
    print("⏭️ html_template 路径已是新版")
elif OLD1 in text:
    text = text.replace(OLD1, NEW1, 1)
    n += 1
    print("✅ html_template.html → templates/")
else:
    print("⚠️ 找不到 html_template 那行，尝试宽松匹配…")
    # 宽松匹配
    import re
    text2 = re.sub(
        r'HERE / "html_template\.html"',
        'HERE / "templates" / "html_template.html"',
        text, count=1
    )
    if text2 != text:
        text = text2
        n += 1
        print("✅ html_template.html → templates/（宽松匹配）")
    else:
        print("❌ 无法修复 html_template 路径")

if NEW2 in text:
    print("⏭️ meaning_intelligence 路径已是新版")
elif OLD2 in text:
    text = text.replace(OLD2, NEW2, 1)
    n += 1
    print("✅ meaning_intelligence.py → scenes/")
else:
    import re
    text2 = re.sub(
        r'HERE / "meaning_intelligence\.py"',
        'HERE / "scenes" / "meaning_intelligence.py"',
        text, count=1
    )
    if text2 != text:
        text = text2
        n += 1
        print("✅ meaning_intelligence.py → scenes/（宽松匹配）")
    else:
        print("❌ 无法修复 meaning_intelligence.py 路径")

p.write_text(text, encoding="utf-8")
print(f"\n共 {n} 处修改")

# 复验
print("\n═══ 复验 ═══")
t2 = p.read_text(encoding="utf-8")
checks = [
    ("指向 templates/html_template.html", 'HERE / "templates" / "html_template.html"' in t2),
    ("指向 scenes/meaning_intelligence.py", 'HERE / "scenes" / "meaning_intelligence.py"' in t2),
]
for label, ok in checks:
    print(f"  {'✅' if ok else '❌'} {label}")