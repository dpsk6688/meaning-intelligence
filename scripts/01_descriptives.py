"""
描述统计与操纵检查。
"""

import pandas as pd

DATA_PATH = "data/processed/analysis_dataset.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    print("=== 样本量 ===")
    print(df.groupby("condition")["episode_id"].nunique())

    print("\n=== CNU 描述统计 ===")
    print(df.groupby("condition")["cumulative_net_utility"].describe())

    print("\n=== 递归轮数操纵检查 ===")
    print(df.groupby("condition")["recursive_rounds"].describe())

    print("\n=== 无效 episode ===")
    if "invalid_episode" in df.columns:
        print(df.groupby("condition")["invalid_episode"].mean())

    out = df.groupby("condition").agg(
        n=("episode_id", "nunique"),
        cnu_mean=("cumulative_net_utility", "mean"),
        cnu_sd=("cumulative_net_utility", "std"),
        recursive_rounds_mean=("recursive_rounds", "mean"),
    )
    out.to_csv("data/processed/descriptives_by_condition.csv")
    print("\n已保存：data/processed/descriptives_by_condition.csv")


if __name__ == "__main__":
    main()