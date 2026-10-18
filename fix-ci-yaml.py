"""修复 ci.yml 里被搞乱的 '安装依赖' 和 '仓库一致性检查' 两步。"""
from pathlib import Path

p = Path(".github/workflows/ci.yml")
t = p.read_text(encoding="utf-8")

# 被搞乱的错误段落
BROKEN = """      - name: 安装依赖 / Install dependencies
      - name: 仓库一致性检查 / Repository consistency check
        run: |
          set -euo pipefail
          python tools/verify_consistency.py
        run: |
          set -euo pipefail
          python -m pip install --upgrade pip
          python -m pip install python-docx pillow pyyaml"""

# 正确的段落(两个独立的 step)
FIXED = """      - name: 安装依赖 / Install dependencies
        run: |
          set -euo pipefail
          python -m pip install --upgrade pip
          python -m pip install python-docx pillow pyyaml

      - name: 仓库一致性检查 / Repository consistency check
        run: |
          set -euo pipefail
          python tools/verify_consistency.py"""

if FIXED in t:
    print("already fixed")
    raise SystemExit(0)

if BROKEN not in t:
    print("❌ 找不到被搞乱的段落,请人工检查")
    print()
    print("搜索定位:")
    for i, line in enumerate(t.splitlines(), 1):
        if "安装依赖" in line or "仓库一致性检查" in line:
            print(f"  L{i}: {line}")
    raise SystemExit(1)

t = t.replace(BROKEN, FIXED, 1)
p.write_text(t, encoding="utf-8")
print("✅ 已修复 ci.yml")
print()
print("修复后的段落:")
lines = t.splitlines()
for i, line in enumerate(lines, 1):
    if "安装依赖" in line or "仓库一致性检查" in line or "python -m pip install" in line or "verify_consistency" in line:
        print(f"  L{i}: {line}")