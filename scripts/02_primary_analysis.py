"""
主要分析骨架：CNU ~ condition + 随机效应。
正式分析前必须按 OSF 预注册冻结。

说明：statsmodels 对交叉随机效应支持有限。
正式分析建议用 R lme4 / brms 或 Python pymer4 复核。
"""

import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

DATA_PATH = "data/processed/analysis_dataset.csv"
OUT_PATH = "data/processed/primary_results.csv"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df = df[df["invalid_episode"] == 0].copy()
    df["condition"] = pd.Categorical(
        df["condition"],
        categories=["baseline", "active_control", "recursive"],
        ordered=False,
    )
    return df


def fit_primary_model(df: pd.DataFrame):
    # 简化演示：groups=model，task 作为方差成分。
    # 正式分析建议使用交叉随机效应 (1|model) + (1|task) + (1|model:task)。
    model = smf.mixedlm(
        "cumulative_net_utility ~ C(condition)",
        data=df,
        groups=df["model_id"],
        vc_formula={"task": "0 + C(task_id)"},
    )
    return model.fit(reml=False)


def extract_contrasts(result):
    params = result.params
    b_active = params.get("C(condition)[T.active_control]", 0.0)
    b_recursive = params.get("C(condition)[T.recursive]", 0.0)

    contrasts = {
        "recursive_vs_active_control": b_recursive - b_active,
        "recursive_vs_baseline": b_recursive,
        "active_control_vs_baseline": b_active,
    }
    return contrasts


def main() -> None:
    df = load_data()
    result = fit_primary_model(df)
    print(result.summary())

    contrasts = extract_contrasts(result)
    pvals = [0.05, 0.05, 0.05]  # 占位：正式分析从模型协方差矩阵计算
    reject, p_adj, _, _ = multipletests(pvals, method="holm")

    out = pd.DataFrame({
        "contrast": list(contrasts.keys()),
        "estimate": list(contrasts.values()),
        "p_adj_placeholder": p_adj,
        "reject_placeholder": reject,
    })
    out.to_csv(OUT_PATH, index=False)
    print(f"已保存：{OUT_PATH}")


if __name__ == "__main__":
    main()