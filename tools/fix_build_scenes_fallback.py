"""让 msi/build.py 容忍 scenes/meaning_intelligence.py 缺失。
CI 的 planned 回退分支测试只拷 build.py / mi_common.py / config.json / templates，
不拷 scenes/，所以需要 fallback。"""
from pathlib import Path

p = Path("msi/build.py")
text = p.read_text(encoding="utf-8")

# 找到注入 __SRC_PY__ 的那一行
OLD = '"__SRC_PY__": js((HERE / "scenes" / "meaning_intelligence.py").read_text(encoding="utf-8")),'

if 'scenes/meaning_intelligence.py 缺失时' in text:
    print("⏭️ 已修复,跳过")
    raise SystemExit(0)

if OLD not in text:
    print("❌ 找不到预期的那行 __SRC_PY__ 注入,请人工检查")
    print("   期望找到:", OLD)
    raise SystemExit(1)

# 在注入前，先做一次容错读取
# 找一个合适的插入点：在 `repl = {` 之前
ANCHOR = "    repl = {"
if ANCHOR not in text:
    raise SystemExit("❌ 找不到 'repl = {' 锚点")

HELPER = '''    # scenes/meaning_intelligence.py 缺失时（例如 CI 的 planned 回退测试临时目录）
    # 用一个占位注释代替，而不是让整个构建失败。
    _src_py_path = HERE / "scenes" / "meaning_intelligence.py"
    if _src_py_path.exists():
        _src_py_text = _src_py_path.read_text(encoding="utf-8")
    else:
        _src_py_text = "// (scenes/meaning_intelligence.py not present in this build)\n"

'''

# 插入 helper
text = text.replace(ANCHOR, HELPER + ANCHOR, 1)

# 替换 OLD 那行
NEW = '"__SRC_PY__": js(_src_py_text),'
text = text.replace(OLD, NEW, 1)

p.write_text(text, encoding="utf-8")
print("✅ 已加 scenes fallback")
print("✅ __SRC_PY__ 改为引用 _src_py_text")

# 复验
t2 = p.read_text(encoding="utf-8")
checks = [
    ("含 fallback 注释", "scenes/meaning_intelligence.py 缺失时" in t2),
    ("含 _src_py_text 定义", "_src_py_text = " in t2),
    ("__SRC_PY__ 指向 _src_py_text", '"__SRC_PY__": js(_src_py_text)' in t2),
    ("不再无条件读取 scenes", '_src_py_path.read_text(encoding="utf-8")\n' in t2),
]
for label, ok in checks:
    print(f"  {'✅' if ok else '❌'} {label}")