"""
次要分析骨架：重大错误率、校准、成本、停止规则。
"""

import pandas as pd
import statsmodels.formula.api as smf

DATA_PATH = "data/processed/analysis_dataset.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    df = df[df["invalid_episode"] == 0].copy()

    # 重大不可逆错误率
    logit = smf.logit(
        "irreversible_error ~ C(condition)",
        data=df,
    ).fit(disp=False)
    print("=== 重大不可逆错误率 ===")
    print(logit.summary())

    # 预测校准
    if "brier_score" in df.columns:
        brier = smf.ols(
            "brier_score ~ C(condition)",
            data=df,
        ).fit()
        print("\n=== Brier 分数 ===")
        print(brier.summary())

    # 成本
    print("\n=== 干预成本 ===")
    print(df.groupby("condition")["intervention_cost"].describe())

    # 停止规则
    if "stop_triggered" in df.columns:
        print("\n=== 停止规则触发率 ===")
        print(df.groupby("condition")["stop_triggered"].mean())


if __name__ == "__main__":
    main()