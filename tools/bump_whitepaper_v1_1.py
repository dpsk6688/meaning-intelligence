"""把白皮书升级到 v1.1:加入 fig3 + Claim Registry 摘要 + 版本号递增。"""
from pathlib import Path

p = Path("whitepaper/build_whitepaper.py")
text = p.read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# 幂等检查
# ---------------------------------------------------------------------------
if "fig3_construct_boundary" in text or "MI-C001" in text:
    print("⚠️ 已包含 fig3 或 Claim Registry,跳过")
    raise SystemExit(0)

# ---------------------------------------------------------------------------
# 1. 版本号 1.0 → 1.1
# ---------------------------------------------------------------------------
OLD_V1 = 'set_font(p.add_run("公开发布白皮书 v1.0"), 14, NAVY, True, HEI, LATIN_H)'
OLD_V2 = 'set_font(p.add_run("\\u3000Public Release White Paper v1.0"), 10, GRAY, False, HEI, LATIN_H)'

NEW_V1 = 'set_font(p.add_run("公开发布白皮书 v1.1"), 14, NAVY, True, HEI, LATIN_H)'
NEW_V2 = 'set_font(p.add_run("\\u3000Public Release White Paper v1.1"), 10, GRAY, False, HEI, LATIN_H)'

n = 0
if OLD_V1 in text:
    text = text.replace(OLD_V1, NEW_V1)
    n += 1
    print("  ✅ 封面中文版本号 → v1.1")
if OLD_V2 in text:
    text = text.replace(OLD_V2, NEW_V2)
    n += 1
    print("  ✅ 封面英文版本号 → v1.1")

# ---------------------------------------------------------------------------
# 2. 插入「构造边界」节 (含 fig3)
# ---------------------------------------------------------------------------
ANCHOR_HEX = "# ================================================================ 六层详解"

FIG3_SECTION = '''# ================================================================ 构造边界
h(doc, "构造边界", "Construct Boundaries", size=17)
note(doc,
     "MIT 是一个特定命名。截至 2026 年，`Meaning Intelligence` 一词在语义/语用分析、决策支持、"
     "商业产品等多个方向已有使用。本项目的 Meaning Intelligence Theory (MIT) 指方向性调控，"
     "与下列方向不是同一构造。",
     "MIT is a specific naming. As of 2026, `Meaning Intelligence` is already in use across several "
     "directions — semantic/pragmatic analysis, decision support, and commercial products among them. "
     "This project's Meaning Intelligence Theory (MIT) refers to directional regulation, which is a "
     "different construct from same-named usage in those directions.")

figure(doc, FIG / "fig3_construct_boundary.png", 14.6,
       "图 3　构造边界：MIT 与邻接场域", "Figure 3  Construct Boundary Map")

note(doc,
     "内环是 MIT 本身（元层，对智能活动的方向性调控）；中环是 IQ / EQ / SQ（平行能力，被元层约束）；"
     "外环是邻接场域（Semantic / Pragmatic、Decision Intelligence、Metacognitive AI、AI Alignment、"
     "Wisdom 传统）。只有 MIT 位于其他智能活动之上，对它们进行方向约束——这是「元」的形式特征。",
     "The inner ring is MIT itself (a meta-layer for the directional regulation of intelligent activities); "
     "the middle ring is IQ / EQ / SQ (parallel capabilities, constrained by the meta-layer); "
     "the outer ring is the adjacent fields (Semantic/Pragmatic, Decision Intelligence, Metacognitive AI, "
     "AI Alignment, Wisdom traditions). Only MIT sits above the others and constrains their direction — "
     "the formal signature of the word meta.")

'''

if ANCHOR_HEX in text:
    text = text.replace(ANCHOR_HEX, FIG3_SECTION + ANCHOR_HEX, 1)
    n += 1
    print("  ✅ 已插入「构造边界」节（含 fig3）")
else:
    print(f"  ❌ 找不到锚点：{ANCHOR_HEX[:60]}")
    raise SystemExit(1)

# ---------------------------------------------------------------------------
# 3. 插入「Claim Registry 摘要」节
# ---------------------------------------------------------------------------
ANCHOR_TERM = "# ================================================================ 术语"

CLAIMS_SECTION = '''# ================================================================ Claim Registry 摘要
h(doc, "Claim Registry 摘要", "Claim Registry — Summary", size=17)
note(doc,
     "每个理论主张在此有一个唯一 ID。论文、网站、实验、工具都应引用 claim ID（如 MI-C003），"
     "而非笼统引用「L6」或「六层栈」。完整版（含测试方式与失败条件）见仓库 docs/claims.md。",
     "Every theoretical claim has a unique ID here. Papers, websites, experiments, and tools should "
     "reference the claim ID (e.g., MI-C003), not loosely reference L6 or the six-layer stack. "
     "The full version with test methods and falsification criteria lives at docs/claims.md in the repository.")

table(doc,
      ["ID", "陈述（摘要）", "证据", "状态"],
      [["MI-C001", "意义智能是对其他智能活动的方向性调控", "E1", "Formalized"],
       ["MI-C002", "意义智能是元层，不与 IQ/EQ/SQ 并列", "E1", "Formalized"],
       ["MI-C003", "意义判断可分解为方向·价值·边界", "E0–E1", "Formalized"],
       ["MI-C004", "意义沿一条连续光谱带分布，而非离散层次", "E0", "Draft"],
       ["MI-C005", "多尺度意义不可通约，协调不是加权求和", "E1", "Formalized"],
       ["MI-C006", "递归审视改善长期决策质量", "E2", "Under Test"],
       ["MI-C007", "六层栈是一种有效的操作性表示", "E0", "Draft"],
       ["MI-C008", "减负改善决策质量（相对纯信息呈现）", "E1", "Under Test"],
       ["MI-C009", "可体验（交互）提升结构回忆", "E1", "Under Test"],
       ["MI-C010", "跨尺度一致性预测系统生存", "E1", "Under Test"],
       ["MI-C011", "主动归零缓解长期僵化", "E2", "Under Test"],
       ["MI-C012", "无归零导致僵化", "E1", "Formalized"]],
      widths=[1.8, 7.5, 1.5, 2.2],
      caption="表 8　Claim Registry 摘要", caption_en="Table 8  Claim Registry — Summary")

note(doc,
     "六层栈本身是 E0 结构——由本项目提出的整合框架，未经独立检验。若出现更简洁且解释力更强的切分，"
     "应当替换它，而不是为它辩护。",
     "The six-layer stack itself is an E0 structure — an integrative framework proposed by this project, "
     "not independently tested. If a simpler partition with greater explanatory power emerges, it should "
     "replace this one rather than be defended.")

'''

if ANCHOR_TERM in text:
    text = text.replace(ANCHOR_TERM, CLAIMS_SECTION + ANCHOR_TERM, 1)
    n += 1
    print("  ✅ 已插入「Claim Registry 摘要」节（含表 8）")
else:
    print(f"  ❌ 找不到锚点：{ANCHOR_TERM[:60]}")
    raise SystemExit(1)

# ---------------------------------------------------------------------------
# 写回
# ---------------------------------------------------------------------------
p.write_text(text, encoding="utf-8")
print(f"\n✅ 共 {n} 处修改。下一步：cd whitepaper && python build_whitepaper.py")

# ---------------------------------------------------------------------------
# 复验
# ---------------------------------------------------------------------------
print("\n═══ 复验 ═══")
text2 = p.read_text(encoding="utf-8")
checks = [
    ("含 fig3 引用", "fig3_construct_boundary" in text2),
    ("含 Claim Registry 摘要", "Claim Registry 摘要" in text2),
    ("含表 8", "表 8" in text2),
    ("版本号为 v1.1", "公开发布白皮书 v1.1" in text2),
    ("不再含旧版本 v1.0（封面）", '"公开发布白皮书 v1.0"' not in text2),
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