"""A 组修正版:处理审计发现的具体文本。"""
from pathlib import Path
import re

ROOT = Path(".")


def read(p):
    return (ROOT / p).read_text(encoding="utf-8") if (ROOT / p).exists() else None


def write(p, t):
    (ROOT / p).write_text(t, encoding="utf-8")


def fix(path, pairs):
    """pairs: [(old, new, expected_count)]。返回改动数。"""
    t = read(path)
    if t is None:
        print(f"  ⏭️ {path} 不存在,跳过")
        return 0
    n = 0
    for old, new, expected in pairs:
        cnt = t.count(old)
        if cnt == 0:
            print(f"  ⚠️ {path}: 找不到 '{old[:50]}'")
            continue
        if cnt != expected:
            print(f"  ⚠️ {path}: '{old[:40]}' 出现 {cnt} 次 (期望 {expected})")
        t = t.replace(old, new)
        n += cnt
        print(f"  ✅ {path}: '{old[:50]}' → '{new[:50]}'  ({cnt} 处)")
    if n:
        write(path, t)
    return n


print("=" * 70)
print("  A 组修正 (A2 + A5)")
print("=" * 70)

# ---- A2: docs/roadmap.md ----
print("\n[A2] docs/roadmap.md 当前版本")
fix("docs/roadmap.md", [
    ("## 三、当前版本 0.1.0 / Current Release 0.1.0",
     "## 三、当前版本 0.2.0 / Current Release 0.2.0",
     1),
])

# ---- A2b: docs/README.md ----
print("\n[A2b] docs/README.md roadmap 描述")
fix("docs/README.md", [
    ("0.1.0 已完成什么、下一步做什么",
     "0.2.0 已完成什么、下一步做什么",
     1),
])

# ---- A5: README + README.en.md ----
print("\n[A5] MIT 理论缩写去混淆")

# 中文 README
fix("README.md", [
    # 定义处:"**Meaning Intelligence Theory (MIT)**" → "(MI Theory)"
    ("**Meaning Intelligence Theory (MIT)**",
     "**Meaning Intelligence Theory (MI Theory)**",
     2),  # L100 和 L128 各一次
    # 图片描述:"把 MIT 放在一个概念空间里" → "把 MI Theory 放在..."
    ("上图把 MIT 放在一个概念空间里",
     "上图把 MI Theory 放在一个概念空间里",
     1),
    # "内环是 MIT 本身" → "内环是 MI Theory 本身"
    ("**内环**是 MIT 本身",
     "**内环**是 MI Theory 本身",
     1),
])

# 英文 README
fix("README.en.md", [
    ("**Meaning Intelligence Theory (MIT)**",
     "**Meaning Intelligence Theory (MI Theory)**",
     2),
])

# ---- A4: README 承诺矛盾 ----
print("\n[A4] README 承诺矛盾")
fix("README.md", [
    ("| 研究阶段 | `public-research` —— 0.x 表示 research formation,尚未进入实证检验阶段 |",
     "| 研究阶段 | `public-research` —— 0.x 表示 research formation;L4 量表信效度验证与 L6 RCT 正在进行中,六层栈整体仍是 E0(概念) |",
     1),
])

# ---- A3: L1 + L6 证据等级对齐 ----
print("\n[A3] 六层证据等级对齐 (以 evidence.md 为准)")

# L1: "E1(机制 E3)" → "E1(机制 E3–E4)"  只改第 136 行
fix("README.md", [
    ("| **L1** | 减负 | Cognitive Load Reduction | 把认知负荷从信息量转移到结构 | 第1章 1.1;工具 A.1 | E1(机制 E3) |",
     "| **L1** | 减负 | Cognitive Load Reduction | 把认知负荷从信息量转移到结构 | 第1章 1.1;工具 A.1 | E1(机制 E3–E4) |",
     1),
])

# L6: "E2(案例)/ E1" → "E2(案例)"  只改第 141 行
fix("README.md", [
    ("| **L6** | 反思与审视递归 | Recursive Reflection and Review | 让系统审视自己的审视 | 第7章 7B.2/7B.3/7B.4 三特性;失败矩阵 | E2(案例)/ E1 |",
     "| **L6** | 反思与审视递归 | Recursive Reflection and Review | 让系统审视自己的审视 | 第7章 7B.2/7B.3/7B.4 三特性;失败矩阵 | E2(案例) |",
     1),
])

# 顺便把 L1-L6 表格里的全角括号统一(可选,如果你有这问题)
# 不做,保留现状

print()
print("=" * 70)
print("  完成")
print("=" * 70)