"""
数据校验骨架。
用途：检查原始数据是否符合预注册数据字典。
注意：正式分析前需由统计师审核。
"""

import pandas as pd

RAW_PATH = "data/raw/episodes.csv"

REQUIRED_COLUMNS = [
    "episode_id",
    "model_id",
    "task_id",
    "condition",
    "cumulative_net_utility",
    "irreversible_error",
    "brier_score",
    "weakest_stakeholder_utility",
    "recursive_rounds",
    "invalid_episode",
]

ALLOWED_CONDITIONS = {"baseline", "active_control", "recursive"}


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def validate_columns(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"缺少必要列：{missing}")


def validate_conditions(df: pd.DataFrame) -> None:
    bad = set(df["condition"].dropna().unique()) - ALLOWED_CONDITIONS
    if bad:
        raise ValueError(f"非法 condition：{bad}")


def validate_ids(df: pd.DataFrame) -> None:
    if df["episode_id"].duplicated().any():
        raise ValueError("episode_id 存在重复。")


def validate_invalid(df: pd.DataFrame) -> None:
    if "invalid_episode" in df.columns:
        bad = set(df["invalid_episode"].dropna().unique()) - {0, 1}
        if bad:
            raise ValueError(f"invalid_episode 非法值：{bad}")


def main() -> None:
    df = load_data(RAW_PATH)
    validate_columns(df)
    validate_conditions(df)
    validate_ids(df)
    validate_invalid(df)
    print(f"校验通过：{len(df)} 行。")
    print(df["condition"].value_counts())


if __name__ == "__main__":
    main()