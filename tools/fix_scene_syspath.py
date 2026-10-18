"""让 msi/scenes/meaning_intelligence.py 能找到 msi/mi_common.py。
把 sys.path 从 'msi/scenes/' 扩展到同时包含 'msi/'。"""
from pathlib import Path

p = Path("msi/scenes/meaning_intelligence.py")
text = p.read_text(encoding="utf-8")

OLD = 'sys.path.insert(0, str(Path(__file__).resolve().parent))'
NEW = '''_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))          # msi/scenes/
sys.path.insert(0, str(_HERE.parent))   # msi/  <- 这里是 mi_common.py 所在'''

if NEW in text:
    print("⏭️ 已修复,跳过")
elif OLD in text:
    text = text.replace(OLD, NEW, 1)
    p.write_text(text, encoding="utf-8")
    print("✅ 已把 msi/ 加入 sys.path")
else:
    print("❌ 找不到预期的那行 sys.path.insert,请人工检查")
    raise SystemExit(1)

# 复验
t2 = p.read_text(encoding="utf-8")
checks = [
    ("含 _HERE.parent", "str(_HERE.parent)" in t2),
    ("不再用裸的 .parent", "sys.path.insert(0, str(Path(__file__).resolve().parent))" not in t2),
]
for label, ok in checks:
    print(f"  {'✅' if ok else '❌'} {label}")