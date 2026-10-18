"""把 docx_style.py 里的 OUT 文件名从 v1.0 改为 v1.1,
并删除旧的 v1.0 产物,避免 Release 里有两份。"""
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. 改 docx_style.py
# ---------------------------------------------------------------------------
p = Path("whitepaper/docx_style.py")
text = p.read_text(encoding="utf-8")

OLD = 'OUT = DIST / "意义智能_元智能理论与分层应用_公开发布白皮书_v1.0_中英双语.docx"'
NEW = 'OUT = DIST / "意义智能_元智能理论与分层应用_公开发布白皮书_v1.1_中英双语.docx"'

if NEW in text:
    print("⏭️ docx_style.py 已指向 v1.1,跳过")
elif OLD in text:
    text = text.replace(OLD, NEW)
    p.write_text(text, encoding="utf-8")
    print("✅ docx_style.py: OUT → v1.1")
else:
    print("❌ 找不到预期的 OUT 行,请人工检查")
    raise SystemExit(1)

# ---------------------------------------------------------------------------
# 2. 删除旧的 v1.0 产物
# ---------------------------------------------------------------------------
DIST = Path("whitepaper/dist")
old_files = [
    DIST / "意义智能_元智能理论与分层应用_公开发布白皮书_v1.0_中英双语.docx",
    DIST / "意义智能_元智能理论与分层应用_公开发布白皮书_v1.0_中英双语.pdf",
]
removed = 0
for f in old_files:
    if f.exists():
        f.unlink()
        print(f"🗑️  已删除 {f.name}")
        removed += 1

if removed == 0:
    print("⏭️ 没有找到旧的 v1.0 产物")

# ---------------------------------------------------------------------------
# 3. 更新 VERSION.yaml
# ---------------------------------------------------------------------------
v = Path("VERSION.yaml")
vt = v.read_text(encoding="utf-8")
if 'whitepaper:' in vt and 'version: "1.0"' in vt:
    # 只替换 whitepaper 段下的 version
    lines = vt.splitlines()
    out = []
    in_wp = False
    for line in lines:
        if line.startswith("whitepaper:"):
            in_wp = True
            out.append(line)
            continue
        if in_wp and line and not line.startswith(" "):
            in_wp = False
        if in_wp and line.strip() == 'version: "1.0"':
            out.append(line.replace('"1.0"', '"1.1"'))
            print("✅ VERSION.yaml: whitepaper.version → 1.1")
            continue
        out.append(line)
    v.write_text("\n".join(out) + "\n", encoding="utf-8")
else:
    print("⏭️ VERSION.yaml 无需修改")

print("\n下一步：")
print("  cd whitepaper")
print("  python build_whitepaper.py")
print("  cd ..")