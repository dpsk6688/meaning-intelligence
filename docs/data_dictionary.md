# 数据字典

## 主键
- `episode_id`：唯一决策 episode。

## 实验条件
- `baseline`：直接决策基线。
- `active_control`：单次结构化反思，资源匹配。
- `recursive`：递归审视，最多 5 轮。

## 主要终点
- `cumulative_net_utility`：CNU = 即时收益 − 干预成本 + 最终状态价值，任务内标准化。

## 排除规则
- `invalid_episode = 1` 时排除。
- 原因包括：模型未输出可解析行动、超预算、系统错误。
- 排除规则不得事后修改。

## 缺失数据
- 多重插补为主分析。
- 完整案例分析为敏感性分析。

## 复现字段
- `randomization_seed`、`api_date`、`temperature`、`system_prompt_hash`
- 用于审计模型版本与调用条件。