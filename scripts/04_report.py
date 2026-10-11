"""
生成分析报告骨架。
"""

import pandas as pd

REPORT_PATH = "docs/analysis_report.md"


def main() -> None:
    desc = pd.read_csv("data/processed/descriptives_by_condition.csv")
    primary = pd.read_csv("data/processed/primary_results.csv")

    lines = [
        "# 分析报告草案",
        "",
        "> 本报告按预注册分析计划生成。不得事后修改主要终点或排除规则。",
        "",
        "## 描述统计",
        "",
        desc.to_markdown(index=False),
        "",
        "## 主要结果",
        "",
        primary.to_markdown(index=False),
        "",
        "## 失败与解释规则",
        "",
        "- 若递归 vs 主动控制无显著净收益，应修改或撤回相关主张。",
        "- 不把失败解释为参与者未正确理解理论。",
        "",
    ]

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"已生成：{REPORT_PATH}")


if __name__ == "__main__":
    main()