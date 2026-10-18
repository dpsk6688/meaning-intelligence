"""修复 publish.py 里被破坏的 _read_whitepaper_version 函数。
用 raw triple-quoted 字符串,保证写回的内容里 \s 和 " 都原样保留。"""
from pathlib import Path

p = Path("tools/publish.py")
text = p.read_text(encoding="utf-8")

START = "def _read_whitepaper_version() -> str:"
NEXT = "def ascii_asset_name"

start_idx = text.find(START)
if start_idx < 0:
    raise SystemExit("找不到 _read_whitepaper_version 起点")

next_idx = text.find(NEXT, start_idx)
if next_idx < 0:
    raise SystemExit("找不到 ascii_asset_name 起点")

NEW_FUNC = r'''def _read_whitepaper_version() -> str:
    """从 VERSION.yaml 读取 whitepaper.version（如 '1.1' 返回 'v1.1'）。
    找不到文件时返回 'v0.0' 而非崩溃。"""
    try:
        import re
        v = Path(__file__).resolve().parent.parent / "VERSION.yaml"
        if not v.exists():
            v = Path("VERSION.yaml")
        if not v.exists():
            return "v0.0"
        txt = v.read_text(encoding="utf-8")
        pattern = r'^whitepaper:.*?^\s+version:\s*"([^"]+)"'
        m = re.search(pattern, txt, re.MULTILINE | re.DOTALL)
        if m:
            return "v" + m.group(1)
    except Exception:
        pass
    return "v0.0"


'''

new_text = text[:start_idx] + NEW_FUNC + text[next_idx:]
p.write_text(new_text, encoding="utf-8")
print("✅ 已重写 _read_whitepaper_version")
print(f"  替换: {next_idx - start_idx} -> {len(NEW_FUNC)} 字节")