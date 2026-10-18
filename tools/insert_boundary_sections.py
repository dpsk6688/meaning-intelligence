"""P0-08 + P0-09: 向 README 插入「不声称什么」与「与近邻概念的区别」两段。

锚点: 六层应用栈 / The six-layer application stack 之前的一个 ---
安全: 用唯一 marker 匹配,找不到就报错退出,不做任何修改。
"""
from pathlib import Path

ROOT = Path(".")

# ---------------------------------------------------------------------------
# P0-09: What This Theory Does NOT Claim (中文 + 英文)
# ---------------------------------------------------------------------------

NOT_CLAIM_ZH = """## 这个理论不声称什么

本理论最容易被误读为「AI 只会给答案,人类才能创造意义」一类的宣言。它**不是**。
为避免进入那个战场,这里明确列出它的边界。

### ❌ 本理论不声称

- 人类拥有意义的专属通道
- AI 不能参与意义过程
- 意义仅仅是主观偏好
- 所有智能系统都必须有人类监督
- 六层栈是唯一有效的分解方式
- 本理论已经过实证确认

### ✅ 本理论确实声称

- 智能需要方向性调控
- 意义判断可以被结构化分析
- 价值与边界是方向判断的组成部分
- 多尺度意义会产生协调问题
- 递归审视可能对长期稳定性是必要的
- 以上主张都是**可检验、可证伪**的

"""

NOT_CLAIM_EN = """## What This Theory Does NOT Claim

This theory is most easily misread as a manifesto of the form "AI gives answers, only humans
create meaning". It is **not**. To avoid that battlefield, here is an explicit list of its boundaries.

### ❌ This theory does NOT claim

- that humans possess exclusive access to meaning
- that AI cannot participate in meaning processes
- that meaning is subjective preference alone
- that all intelligent systems require human supervision
- that the six-layer stack is the only valid decomposition
- that the theory is empirically confirmed

### ✅ This theory DOES claim

- intelligence requires directional regulation
- meaning judgments can be structurally analyzed
- value and boundary are parts of directional judgment
- multi-scale meaning creates coordination problems
- recursive review may be necessary for long-horizon stability
- the claims above are **testable and falsifiable**

"""

# ---------------------------------------------------------------------------
# P0-08: Construct Boundaries (中文 + 英文)
# ---------------------------------------------------------------------------

BOUNDARY_ZH = """## 与近邻概念的区别

**本项目的「意义智能」是一个特定命名。** 截至 2026 年,`Meaning Intelligence` 在语义/语用分析、
决策支持、商业产品等多个方向已有使用。本项目的 **Meaning Intelligence Theory (MIT)**
指**对智能活动的方向性调控**,与下列方向不是同一构造。

| 近邻概念 | 关注什么 | 与本项目的关系 |
|---|---|---|
| **IQ / EQ / SQ** | 能不能算 / 能不能相处 / 能不能共处 | 平行能力;本理论**位于它们之上**做方向约束 |
| **Semantic / Pragmatic Intelligence** | 语言中的上下文、意图、反讽、隐含语义 | 处理**语言的意义**;本理论处理**行动的方向** |
| **Decision Intelligence** | 从信息 + 上下文 + 人类判断得到一致理解 | 应用层框架;本理论提供**元层结构** |
| **Metacognitive AI** | 自我监控、资源分配、难度估计 | 与 L6 邻接;L6 是**六层栈中的一环** |
| **AI Alignment** | 让 AI 行为符合人类价值 | 提供**方向性判断的结构**;不替代对齐研究 |
| **Wisdom / Judgment 传统** | 实践智慧、判断力 | 本理论试图把它**形式化**为可检验结构 |

> **命名冲突声明**:本项目不主张对 `Meaning Intelligence` 一词的独占。
> 但我们明确区分:本项目的 "Meaning Intelligence Theory" 指**方向性调控**,
> 与语义/语用/决策方向的同名使用是**不同的构造**。

"""

BOUNDARY_EN = """## Construct Boundaries

**This project's "Meaning Intelligence" is a specific naming.** As of 2026, `Meaning Intelligence`
is already in use across several directions — semantic/pragmatic analysis, decision support, and
commercial products among them. This project's **Meaning Intelligence Theory (MIT)** refers to
**the directional regulation of intelligent activities**. It is not identical to any of the
following adjacent constructs.

| Adjacent construct | Concerns | Relation to this project |
|---|---|---|
| **IQ / EQ / SQ** | Can it compute / get along / coexist | Parallel capabilities; this theory **sits above them** to constrain direction |
| **Semantic / Pragmatic Intelligence** | Context, intent, irony, coded subtext in language | Handles **meaning in language**; this theory handles **direction of action** |
| **Decision Intelligence** | Coherent understanding from information + context + human judgment | Application-layer framework; this theory provides the **meta-layer structure** |
| **Metacognitive AI** | Self-monitoring, resource allocation, difficulty estimation | Adjacent to L6; L6 is **one layer of the stack** |
| **AI Alignment** | Aligning AI behavior with human values | Provides **structure for directional judgment**; does not replace alignment research |
| **Wisdom / Judgment traditions** | Practical wisdom, judgment | This theory attempts to **formalize** them into testable structure |

> **Naming conflict statement**: This project does not claim exclusivity over the term
> `Meaning Intelligence`. We do explicitly distinguish: this project's "Meaning Intelligence Theory"
> refers to **directional regulation**, which is a **different construct** from same-named usage
> in semantic, pragmatic, or decision-oriented directions.

"""


def find_insertion_point(text, marker):
    """在 text 里找到 marker,返回 marker 前最近的 '---\\n' 之后的位置。
    找不到返回 None。"""
    idx = text.find(marker)
    if idx < 0:
        return None
    # 从 idx 往前找最近的 "---"
    before = text[:idx]
    sep_idx = before.rfind("---")
    if sep_idx < 0:
        return None
    # 找到该 "---" 行末尾的换行位置
    line_end = before.find("\n", sep_idx)
    if line_end < 0:
        return None
    return line_end + 1  # 插入点:分隔符行的下一行开头


def insert_sections(readme_path, marker, new_content):
    p = ROOT / readme_path
    if not p.exists():
        print(f"  ⚠️ 未找到 {readme_path}")
        return False

    text = p.read_text(encoding="utf-8")

    # 幂等检查
    first_line = new_content.strip().splitlines()[0]
    if first_line in text:
        print(f"  ⏭️ {readme_path} 已包含该段,跳过")
        return True

    pos = find_insertion_point(text, marker)
    if pos is None:
        print(f"  ❌ {readme_path}: 找不到锚点 '{marker[:40]}'")
        return False

    # 打印上下文用于确认
    context = text[max(0, pos - 80):pos + 40].replace("\n", "⏎")
    print(f"  📍 {readme_path} 插入点上下文: ...{context}...")

    # 插入: 新内容 + 分隔符
    new_text = text[:pos] + "\n" + new_content + "---\n\n" + text[pos:]
    p.write_text(new_text, encoding="utf-8")
    print(f"  ✅ {readme_path}: 已插入")
    return True


def main():
    print("═══ P0-08 + P0-09: 插入 README 边界段落 ═══\n")

    # --- README.md (中文) ---
    print("[README.md] 插入中文段")
    combined_zh = NOT_CLAIM_ZH + BOUNDARY_ZH
    ok1 = insert_sections("README.md", "六层应用栈 / The six-layer application stack", combined_zh)
    print()

    # --- README.en.md (英文) ---
    print("[README.en.md] 插入英文段")
    combined_en = NOT_CLAIM_EN + BOUNDARY_EN
    ok2 = insert_sections("README.en.md", "six-layer application stack", combined_en)
    print()

    # --- 复验 ---
    print("═══ 复验 ═══\n")
    checks = []

    if (ROOT / "README.md").exists():
        zh = (ROOT / "README.md").read_text(encoding="utf-8")
        checks += [
            ("README.md 含「不声称什么」", "## 这个理论不声称什么" in zh),
            ("README.md 含「与近邻概念的区别」", "## 与近邻概念的区别" in zh),
            ("README.md 含命名冲突声明", "命名冲突声明" in zh),
        ]

    if (ROOT / "README.en.md").exists():
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        checks += [
            ("README.en.md 含 'What This Theory Does NOT Claim'", "What This Theory Does NOT Claim" in en),
            ("README.en.md 含 'Construct Boundaries'", "## Construct Boundaries" in en),
            ("README.en.md 含 'Naming conflict statement'", "Naming conflict statement" in en),
        ]

    all_ok = True
    for label, ok in checks:
        print(f"  {'✅' if ok else '❌'} {label}")
        if not ok:
            all_ok = False

    print()
    if ok1 and ok2 and all_ok:
        print("🎉 全部通过。下一步: 推送")
    else:
        print("⚠️ 有未通过项,检查输出")


if __name__ == "__main__":
    main()