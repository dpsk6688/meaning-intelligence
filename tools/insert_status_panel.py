"""P0-10: 向两个 README 插入「研究状态面板」。
锚点: 已有的边界段落之前。
安全: 幂等,找不到锚点则报错退出,不做任何修改。
"""
from pathlib import Path

ROOT = Path(".")

# ---------------------------------------------------------------------------
# 中文面板
# ---------------------------------------------------------------------------

PANEL_ZH = """## 研究状态

| 维度 | 当前状态 |
|---|---|
| 研究阶段 | `public-research` —— 0.x 表示 research formation,尚未进入实证检验阶段 |
| 六层栈证据等级 | **E0(概念)** —— 未经独立检验 |
| 白皮书版本 | v1.0(19 页,中英双语,DOCX + PDF) |
| 版本源 | [`VERSION.yaml`](VERSION.yaml) —— 所有版本号以此为唯一真相 |
| 证伪路径 | [失败矩阵](docs/failure-matrix.md) · [证伪报告模板](.github/ISSUE_TEMPLATE/falsification_report.yml) |
| 学术承诺 | 任何模块达到失败阈值,将被**标记或删除**,而不是被辩护 |

> **关于版本编号**:本项目使用 `0.x` 表示 research formation 阶段。
> 只有在完成 construct validation、首次预测性研究、以及独立复现之后,
> 才会进入 `1.0`。这是一个刻意保守的约定。

"""

# ---------------------------------------------------------------------------
# 英文面板
# ---------------------------------------------------------------------------

PANEL_EN = """## Research Status

| Dimension | Current status |
|---|---|
| Research phase | `public-research` — 0.x signals research formation, not yet empirically tested |
| Stack evidence level | **E0 (conceptual)** — not independently tested |
| White paper | v1.0 (19 pages, bilingual, DOCX + PDF) |
| Version source | [`VERSION.yaml`](VERSION.yaml) — single source of truth for all version numbers |
| Falsification path | [Failure matrix](docs/failure-matrix.md) · [Falsification report template](.github/ISSUE_TEMPLATE/falsification_report.yml) |
| Scholarly commitment | Any module reaching its failure threshold will be **marked or removed**, not defended |

> **On version numbering**: This project uses `0.x` to signal research formation.
> Only after construct validation, a first predictive study, and independent replication
> does it reach `1.0`. This is a deliberate, conservative convention.

"""


def insert_before_anchor(path, anchor, content):
    p = ROOT / path
    if not p.exists():
        print(f"  ⚠️ 未找到 {path}")
        return False

    text = p.read_text(encoding="utf-8")

    # 幂等检查
    first_line = content.strip().splitlines()[0]
    if first_line in text:
        print(f"  ⏭️ {path} 已包含该段,跳过")
        return True

    idx = text.find(anchor)
    if idx < 0:
        print(f"  ❌ {path}: 找不到锚点 '{anchor[:40]}'")
        return False

    # 往前找到最近的 "---" 行,插在它之后 (让分隔符对称)
    before = text[:idx]
    sep_idx = before.rfind("\n---\n")
    if sep_idx >= 0:
        pos = sep_idx + len("\n---\n")
    else:
        pos = idx

    context = text[max(0, pos - 60):pos + 30].replace("\n", "⏎")
    print(f"  📍 {path} 插入点上下文: ...{context}...")

    new_text = text[:pos] + "\n" + content + "---\n\n" + text[pos:]
    p.write_text(new_text, encoding="utf-8")
    print(f"  ✅ {path}: 已插入")
    return True


def main():
    print("═══ P0-10: 插入研究状态面板 ═══\n")

    print("[README.md] 中文面板")
    ok1 = insert_before_anchor(
        "README.md",
        "## 这个理论不声称什么",
        PANEL_ZH,
    )
    print()

    print("[README.en.md] 英文面板")
    ok2 = insert_before_anchor(
        "README.en.md",
        "## What This Theory Does NOT Claim",
        PANEL_EN,
    )
    print()

    # --- 复验 ---
    print("═══ 复验 ═══\n")
    checks = []

    if (ROOT / "README.md").exists():
        zh = (ROOT / "README.md").read_text(encoding="utf-8")
        checks += [
            ("README.md 含「研究状态」标题", "## 研究状态" in zh),
            ("README.md 含 public-research", "public-research" in zh),
            ("README.md 含 VERSION.yaml 链接", "VERSION.yaml" in zh),
            ("README.md 含失败矩阵链接", "failure-matrix.md" in zh),
            ("README.md 面板在「不声称什么」之前",
             zh.find("## 研究状态") < zh.find("## 这个理论不声称什么")),
        ]

    if (ROOT / "README.en.md").exists():
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        checks += [
            ("README.en.md 含 'Research Status'", "## Research Status" in en),
            ("README.en.md 含 public-research", "public-research" in en),
            ("README.en.md 含 VERSION.yaml link", "VERSION.yaml" in en),
            ("README.en.md 含 failure-matrix link", "failure-matrix.md" in en),
            ("README.en.md 面板在 'NOT Claim' 之前",
             en.find("## Research Status") < en.find("## What This Theory Does NOT Claim")),
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