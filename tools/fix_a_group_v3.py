"""修正 L1/L6 证据等级 —— 用正则匹配,不依赖标点。"""
import re
from pathlib import Path

ROOT = Path(".")
readme = ROOT / "README.md"
t = readme.read_text(encoding="utf-8")
original = t

print("修复前,先看 L1/L6 行:")
for i, line in enumerate(t.splitlines(), 1):
    if "**L1**" in line and "减负" in line:
        print(f"  L{i}: {line}")
    if "**L6**" in line and "反思" in line:
        print(f"  L{i}: {line}")

# L1: 机制 E3 → E3–E4(注意可能是全角括号)
# 匹配行内容:"| **L1** | 减负 | ... | E1(机制 E3) |"
pat_l1 = re.compile(
    r"(^\|\s*\*\*L1\*\*\s*\|[^\n]*?\|\s*)E1[（(]机制 E3[）)](\s*\|)",
    re.MULTILINE
)
t2, n1 = pat_l1.subn(r"\1E1（机制 E3–E4）\2", t)
if n1:
    print(f"✅ L1 修复 {n1} 处")
    t = t2
else:
    print("⚠️ L1 未匹配到,需要人工处理")

# L6: E2(案例)/ E1 → E2(案例)
pat_l6 = re.compile(
    r"(^\|\s*\*\*L6\*\*\s*\|[^\n]*?\|\s*)E2[（(]案例[）)]\s*/\s*E1(\s*\|)",
    re.MULTILINE
)
t2, n2 = pat_l6.subn(r"\1E2（案例）\2", t)
if n2:
    print(f"✅ L6 修复 {n2} 处")
    t = t2
else:
    print("⚠️ L6 未匹配到,需要人工处理")

if t != original:
    readme.write_text(t, encoding="utf-8")
    print()
    print("修复后:")
    for i, line in enumerate(t.splitlines(), 1):
        if "**L1**" in line and "减负" in line:
            print(f"  L{i}: {line}")
        if "**L6**" in line and "反思" in line:
            print(f"  L{i}: {line}")