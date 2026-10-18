"""让 publish.py 的 ascii_asset_name 从 VERSION.yaml 动态读取版本号。"""
from pathlib import Path

p = Path("tools/publish.py")
text = p.read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# 1. 在文件顶部附近插入 VERSION.yaml 读取辅助函数
# ---------------------------------------------------------------------------
HELPER = '''

def _read_whitepaper_version() -> str:
    """从 VERSION.yaml 读取 whitepaper.version（如 '1.1' → 返回 'v1.1'）。
    找不到文件时返回 'v0.0' 而非崩溃,便于在非标准位置调用。"""
    try:
        import re
        v = Path(__file__).resolve().parent.parent / "VERSION.yaml"
        if not v.exists():
            v = Path("VERSION.yaml")
        if not v.exists():
            return "v0.0"
        txt = v.read_text(encoding="utf-8")
        # 只在 whitepaper 段内匹配 version:
        m = re.search(r"^whitepaper:.*?^\\s+version:\\s*\"([^\"]+)\"",
                      txt, re.MULTILINE | re.DOTALL)
        if m:
            return "v" + m.group(1)
    except Exception:
        pass
    return "v0.0"

'''

# 插到 ascii_asset_name 定义之前
ANCHOR = "def ascii_asset_name(path: Path, version: str = \"v1.0\") -> str:"
if ANCHOR not in text:
    print("❌ 找不到 ascii_asset_name 定义,请人工检查")
    raise SystemExit(1)

NEW_SIG = "def ascii_asset_name(path: Path, version: str = None) -> str:"
text = text.replace(ANCHOR, HELPER + NEW_SIG)
print("  ✅ 已插入 _read_whitepaper_version()")
print("  ✅ ascii_asset_name 默认参数改为 None（将动态读取）")

# ---------------------------------------------------------------------------
# 2. 在函数体开头加动态读取逻辑
# ---------------------------------------------------------------------------
OLD_BODY_START = '''    所以附件名一律走 ASCII。
    """
    name = path.name'''

NEW_BODY_START = '''    所以附件名一律走 ASCII。
    """
    if version is None:
        version = _read_whitepaper_version()
    name = path.name'''

if OLD_BODY_START not in text:
    print("❌ 找不到函数体开头,请人工检查")
    raise SystemExit(1)

text = text.replace(OLD_BODY_START, NEW_BODY_START)
print("  ✅ 函数体开头已加动态读取逻辑")

# ---------------------------------------------------------------------------
# 3. 写回
# ---------------------------------------------------------------------------
p.write_text(text, encoding="utf-8")
print("\n✅ publish.py 已修复")

# ---------------------------------------------------------------------------
# 4. 复验
# ---------------------------------------------------------------------------
print("\n═══ 复验 ═══")
t2 = p.read_text(encoding="utf-8")
checks = [
    ("含 _read_whitepaper_version 定义", "def _read_whitepaper_version" in t2),
    ("含 whitepaper 段正则", "whitepaper:.*?version" in t2),
    ("ascii_asset_name 默认参数为 None", 'version: str = None' in t2),
    ("函数体含动态读取逻辑", "if version is None:" in t2),
    ("不再硬编码 v1.0 默认", 'version: str = "v1.0"' not in t2),
]
all_ok = True
for label, ok in checks:
    print(f"  {'✅' if ok else '❌'} {label}")
    if not ok:
        all_ok = False

if all_ok:
    print("\n🎉 全部通过")
else:
    print("\n⚠️ 有未通过项")