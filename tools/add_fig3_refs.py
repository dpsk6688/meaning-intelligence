"""在 README.md / README.en.md / docs/architecture.md 三处引用 fig3。"""
from pathlib import Path

ROOT = Path(".")


def insert_before(path, anchor, content):
    """在 anchor 之前插入 content。幂等。"""
    p = ROOT / path
    if not p.exists():
        print(f"  ⚠️ 未找到 {path}")
        return False

    text = p.read_text(encoding="utf-8")

    # 幂等检查
    if "fig3_construct_boundary.png" in text:
        print(f"  ⏭️ {path} 已引用 fig3,跳过")
        return True

    idx = text.find(anchor)
    if idx < 0:
        print(f"  ❌ {path}: 找不到锚点 '{anchor[:50]}'")
        return False

    new_text = text[:idx] + content + "\n\n" + text[idx:]
    p.write_text(new_text, encoding="utf-8")
    print(f"  ✅ {path}: 已插入")
    return True


def append_section(path, content):
    """向文件末尾追加新段落。幂等。"""
    p = ROOT / path
    if not p.exists():
        print(f"  ⚠️ 未找到 {path}")
        return False

    text = p.read_text(encoding="utf-8")

    if "fig3_construct_boundary.png" in text:
        print(f"  ⏭️ {path} 已引用 fig3,跳过")
        return True

    new_text = text.rstrip() + "\n\n" + content + "\n"
    p.write_text(new_text, encoding="utf-8")
    print(f"  ✅ {path}: 已追加")
    return True


# ==========================================================================
# 中文 README:插在「## 六层应用栈」之前
# ==========================================================================

REF_ZH = """### 构造边界

![构造边界图](whitepaper/figures/fig3_construct_boundary.png)

上图把 MIT 放在一个概念空间里:**内环**是 MIT 本身(元层,对智能活动的方向性调控);
**中环**是 IQ / EQ / SQ(平行能力,被元层约束);**外环**是邻接场域
(Semantic / Pragmatic、Decision Intelligence、Metacognitive AI、AI Alignment、Wisdom 传统)。

命名冲突不可避免——`Meaning Intelligence` 一词在多个方向已被使用。本项目的
**Meaning Intelligence Theory (MIT)** 指**方向性调控**,与语义/语用/决策方向的同名使用
是**不同的构造**。
"""

# ==========================================================================
# 英文 README:插在「## The Six-Layer Stack」之前
# ==========================================================================

REF_EN = """### Construct Boundary Map

![Construct Boundary Map](whitepaper/figures/fig3_construct_boundary.png)

The figure places MIT in a conceptual space: the **inner ring** is MIT itself (a meta-layer for
the directional regulation of intelligent activities); the **middle ring** is IQ / EQ / SQ
(parallel capabilities, constrained by the meta-layer); the **outer ring** is the adjacent
fields (Semantic/Pragmatic, Decision Intelligence, Metacognitive AI, AI Alignment, Wisdom
traditions).

Naming collision is unavoidable — `Meaning Intelligence` is already in use across multiple
directions. This project's **Meaning Intelligence Theory (MIT)** refers to **directional
regulation**, which is a **different construct** from same-named usage in semantic, pragmatic,
or decision-oriented directions.
"""

# ==========================================================================
# docs/architecture.md:追加一节
# ==========================================================================

ARCH_SECTION = """## 构造边界 / Construct Boundary

![构造边界图](../whitepaper/figures/fig3_construct_boundary.png)

MIT 在概念空间中的位置:

| 环 | 内容 | 与 MIT 的关系 |
|---|---|---|
| **内环** | MIT | 元层:对智能活动的方向性调控 |
| **中环** | IQ · EQ · SQ | 平行能力;被 MIT 约束,而非与之并列 |
| **外环** | Semantic / Pragmatic · Decision Intelligence · Metacognitive AI · AI Alignment · Wisdom | 邻接场域;与 MIT 相邻但不同构造 |

**"元"的形式特征**:只有 MIT 位于其他智能活动之上,对它们进行方向约束。IQ 关心「能不能算」,
EQ 关心「能不能相处」,SQ 关心「能不能共处」——三者都在回答「如何做到」。唯有 MIT 追问
「为何要做」以及「值不值得」。

**命名提示**:本项目的 "Meaning Intelligence Theory" 使用 `MIT` 缩写时,指**方向性调控**,
与语义/语用/决策方向的同名 `Meaning Intelligence` 是不同构造。详见
[`docs/glossary.md`](glossary.md) 的命名冲突声明。
"""


def main():
    print("═══ 在 3 处引用 fig3 ═══\n")

    print("[1/3] README.md")
    ok1 = insert_before(
        "README.md",
        "## 六层应用栈",
        REF_ZH,
    )
    print()

    print("[2/3] README.en.md")
    ok2 = insert_before(
        "README.en.md",
        "## The Six-Layer Stack",
        REF_EN,
    )
    print()

    print("[3/3] docs/architecture.md")
    ok3 = append_section(
        "docs/architecture.md",
        ARCH_SECTION,
    )
    print()

    # --- 复验 ---
    print("═══ 复验 ═══\n")
    checks = []
    for path, label in [
        ("README.md", "README.md"),
        ("README.en.md", "README.en.md"),
        ("docs/architecture.md", "docs/architecture.md"),
    ]:
        p = ROOT / path
        if p.exists():
            t = p.read_text(encoding="utf-8")
            checks.append((f"{label} 引用 fig3", "fig3_construct_boundary.png" in t))

    all_ok = all(ok for _, ok in checks)
    for label, ok in checks:
        print(f"  {'✅' if ok else '❌'} {label}")

    print()
    if ok1 and ok2 and ok3 and all_ok:
        print("🎉 全部通过。下一步: 推送")
    else:
        print("⚠️ 有未通过项")


if __name__ == "__main__":
    main()