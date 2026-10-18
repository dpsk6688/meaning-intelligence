# Agent Network Protocol — Changelog

## v0.1 (2026-10-11)

**初始版本 / Initial release.**

- 3 个问题，覆盖 H2 / H3 / H13。
  > EN: 3 questions covering H2 / H3 / H13.
- 双语（中英）。
  > EN: Bilingual (Chinese–English).
- JSON 格式提交。
  > EN: JSON format submission.
- 自引禁止。
  > EN: Self-citation prohibited.

**本次版本未做的事 / What This Version Does NOT Do**：

- 未包含 L1（人类访问者）问题集。
  > EN: Does not include L1 (human visitor) questions.
- 未包含结构化 schema 校验。
  > EN: Does not include structured schema validation.
- 未包含自动化聚合工具。
  > EN: Does not include automated aggregation tooling.

**已知限制 / Known Limitations**：

- 无法验证 AI 访问者的真实模型身份。
  > EN: Cannot verify the actual model identity of an AI visitor.
- 无法防止同一模型多次提交。
  > EN: Cannot prevent multiple submissions from the same model.
- 无法防止 AI 复制其他 AI 的答案。
  > EN: Cannot prevent an AI from copying another AI's answers.

---

## 未来版本规划 / Planned Versions

### v0.2（预计 2026-11）

- 加入 schema 校验（JSON Schema）
- 加入 3 个新问题，覆盖 H5 / H12 / H15

### v0.3（预计 2026-12）

- 加入 L1 人类访问者问题集
- 加入自动聚合脚本

### v1.0（触发条件）

- **迁移到独立仓库 `sara-protocol/agent-network`**
- 触发条件（任一）：
  1. 日记 ≥ 5 轮
  2. 外部 AI 回答 ≥ 10 份
  3. 至少一个外部项目引用本协议
  4. 本协议需要独立的许可证（不是 MIT/CC BY 4.0）
  5. 有人愿意成为共同维护者
