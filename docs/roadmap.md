# 路线图 / Roadmap

> 这份文档回答一个问题：**本项目在整个正典路线图中处于什么位置，当前版本交付了什么，下一步做什么？**
> This document answers one question: **where does this repository sit in the canon's roadmap, what does the current release deliver, and what comes next?**

---

## 一、本仓库的定位 / Where This Repository Sits

**本仓库定位在正典路线图的「第一阶段：认知普及与工具孵化」。**

白皮书与 MSI 演示系统都属于第一阶段的产品形态：一本专著与一批**个人版工具**。
本仓库不主张自己已经进入第二至第五阶段，也不把面向组织的、面向城市的、面向文明的部署
写成已经发生的事实。下面第三节的「近期待办」全部在第一阶段的范围内。

**This repository sits in the canon roadmap's first phase: cognitive popularization and tool
incubation.** The white paper and the MSI demonstration system are both first-phase product forms —
a monograph and a set of **individual-scale tools**. This repository does not claim to have entered
phases two through five, and it does not describe organizational, urban, or civilizational deployment
as though it had already happened. Every item in the near-term list below stays inside phase one.

---

## 二、五阶段路线图 / The Five Phases

| 阶段 Phase | 时间 Time | 主题 Theme | 主要产出 Main outputs | 六层的主要形态 Primary forms of the six layers |
|---|---|---|---|---|
| 第一阶段 / Phase 1 | 当下–2030<br>now–2030 | 认知普及与工具孵化<br>Cognitive popularization and tool incubation | 专著；个人版工具<br>Monograph; individual-scale tools | 个人阅读降维、可丢弃微应用（L1–L2）；意义自检、证据标注（L3–L4）；年度归零、螺旋追踪（L5–L6） |
| 第二阶段 / Phase 2 | 2030–2045 | 组织应用与制度嵌入<br>Organizational application and institutional embedding | 组织级评估与治理流程<br>Organizational assessment and governance processes | 汇报与文档受控化、仪表盘；使命合法性评估；使命压力测试、方向重置 |
| 第三阶段 / Phase 3 | 2045–2060 | 城市与区域意义治理<br>Urban and regional meaning governance | 城市尺度公共界面与集体记忆评估<br>Urban-scale public interfaces and collective-memory assessment | 公共信息可读化、参与式界面；地方感与集体记忆评估；城市归零工作坊 |
| 第四阶段 / Phase 4 | 2060–2080 | 国家与文明级 MI 架构<br>National and civilizational MI architecture | 跨尺度政策与制度一致性框架<br>Cross-scale policy and institutional consistency frameworks | 政策文本可读化；制度意义一致性评估；跨尺度方向校准（正典工具 A.9 跨尺度） |
| 第五阶段 / Phase 5 | 2080+ | 人类级意义智能与文明自觉<br>Humanity-scale meaning intelligence and civilizational self-awareness | 文明级方向治理与归零-螺旋机制<br>Civilization-scale direction governance and zeroing-spiral mechanisms | 文明叙事降维；物种责任与文明方向评估；文明级归零-螺旋治理 |

**读表须知：** 阶段二至阶段五的内容来自正典路线图与白皮书表 4（五尺度 × 六层的典型形态），
在此处的作用是**标明第一阶段不是终点**，而不是承诺时间表必然兑现。
六层在五个尺度上形态不同，是因为正典公理三指出：多尺度意义不可通约，协调不是加权求和。

**How to read the table:** phases two through five come from the canon roadmap and white paper Table 4
(typical forms of the six layers across five scales). Their role here is to show that **phase one is
not the endpoint**, not to promise that the schedule will be met. The layers take different forms at
different scales because Canon Axiom Three holds that multi-scale meanings are incommensurable and
that coordination is not weighted summation.

---

## 三、当前版本 0.2.0 / Current Release 0.2.0

**已完成 / Delivered:**

1. **六层应用栈首次公开**：L1 减负 / L2 可体验 / L3 意义生成 / L4 价值评估 / L5 方向选择 /
   L6 反思与审视递归，并给出三带划分（界面带 L1–L2、加工带 L3–L4、元带 L5–L6）。
   The six-layer stack published for the first time, together with the three-band partition.
2. **中英双语白皮书 v1.0**：正文、排版、插图均由脚本生成（[`whitepaper/build_whitepaper.py`](../whitepaper/build_whitepaper.py)、
   [`whitepaper/docx_style.py`](../whitepaper/docx_style.py)、[`whitepaper/make_figures.py`](../whitepaper/make_figures.py)），
   发布产物在 [`whitepaper/dist/`](../whitepaper/dist)。
   Bilingual white paper v1.0, generated end to end by scripts.
3. **MSI 六层演示系统**：Manim 六幕动画（[`msi/scenes/`](../msi/scenes)）＋ 单文件交互页
   [`msi/meaning_intelligence.html`](../msi/meaning_intelligence.html)，含时间轴联动、六层导航与实测/预算时间轴的分支处理（见
   [architecture.md](architecture.md)）。
   The MSI six-act demonstration system: Manim scenes plus a single-file interactive page with
   timeline linking, six-layer navigation, and explicit measured/planned timeline branching.
4. **E0–E6 证据等级与理论失败矩阵纳入仓库**：每层写明支持证据、部分支持、失败阈值与失败后操作
   （见 [failure-matrix.md](failure-matrix.md)），并配套
   [`falsification_report.yml`](../.github/ISSUE_TEMPLATE/falsification_report.yml) 证伪报告模板。
   Evidence levels and the failure matrix brought into the repository, with a falsification report
   template.
5. **本目录（`docs/`）**：架构、证据体系、失败矩阵、路线图、术语五份说明性文档。
   This documentation layer.

**明确未主张 / Explicitly not claimed:**

- 本版本**不主张任何模块达到 E4 及以上**；各模块当前等级见 [evidence.md](evidence.md)。
  No module is claimed at E4 or above.
- **六层栈本身是 E0（概念）**，未经独立检验。把它数据化、动画化、可操作化，
  **都不提高**它的证据等级。
  The stack itself is E0 and untested; implementing it does not raise its level.
- 18 张假设卡片 H1–H18 及其预注册证伪标准随正典发布；本仓库承载**引用与报告流程**，
  不复述全部标准，也不改写其中任何一条。
  The 18 hypothesis cards and their preregistered criteria ship with the canon; this repository
  carries references and the reporting workflow, not restatements or revisions.

---

## 四、近期待办 / Near-Term Work

分两类。这个分类不是进度管理，而是**承诺管理**：第一类工作**预先声明了自己被证伪时将被删除**。

Two categories. The split is not project management but **commitment management**: the first category
**declares in advance that it will be removed if falsified**.

| # | 工作 Work | 类别 Category | 完成判据 / 证伪条件 Criterion |
|---|---|---|---|
| 1 | L1 操作化的对照检验：降维前后的决策质量是否出现可察觉差异<br>Controlled test of L1: does decision quality differ detectably after reduction? | **已被证伪就删**<br>**Delete if falsified** | 若 d&lt;0.3，则重设压缩比或放弃字数硬限（阈值见 [failure-matrix.md](failure-matrix.md)）<br>If d&lt;0.3, reset the compression ratio or drop the hard word limit |
| 2 | L2 交互组与静态组的对照：结构回忆是否有显著差异<br>Interactive vs. static groups: is recall of structure significantly different? | **已被证伪就删**<br>**Delete if falsified** | 若无显著差异，L2 降为可选增强，不作必需层<br>If not significant, L2 becomes an optional enhancement |
| 3 | L3 三维度的独立可评分性：方向/价值/边界能否被独立评分<br>Can direction, value, and boundary be scored independently? | **已被证伪就删**<br>**Delete if falsified** | 若单一维度解释意义判断方差 &gt;90%，接受 H2 被证伪并重构结构模型<br>If one dimension explains &gt;90% of the variance, accept H2 falsified and rebuild the model |
| 4 | L4 测量工具的信效度验证（当前状态：验证中）<br>Reliability and validity of the L4 instruments (currently under validation) | **已被证伪就删**<br>**Delete if falsified** | 若证据标注与判断质量无相关，退回定性评估<br>If labelling does not correlate with judgment quality, revert to qualitative assessment |
| 5 | L6 的随机对照实验（当前状态：进行中）<br>The L6 randomized controlled trial (currently running) | **已被证伪就删**<br>**Delete if falsified** | 若 RCT 无显著差异（d&lt;0.3），放弃有效性主张，仅保留为操作规程<br>If the RCT shows no significant difference (d&lt;0.3), drop the efficacy claim and keep the procedure only |
| 6 | L5 跨尺度一致性与生存期的观测设计<br>Designing an observation for cross-scale consistency and survival | **待检验**<br>**To be tested** | 检验 H7／H8；若出现「长期背离却无危机」，标记 H8 被证伪并重估五尺度模型<br>Tests H7/H8; a case of long divergence without crisis marks H8 falsified |
| 7 | 六层切分本身的替代方案比较<br>Comparing alternative partitions of the stack | **待检验**<br>**To be tested** | 若出现更简洁且解释力更强的切分，**替换**六层栈，而不是为它辩护<br>If a simpler partition with greater explanatory power emerges, it replaces the stack |
| 8 | 各层操作化指标的边界条件与混淆清单<br>Boundary conditions and confound lists for each layer's indicators | **待检验**<br>**To be tested** | 按 [CONTRIBUTING.md](../CONTRIBUTING.md) 第 3 节提交：目标构念、测量程序、混淆、最小可判别效应、对可检验性的影响<br>Submitted per CONTRIBUTING.md §3 |
| 9 | 页面与白皮书之间的一致性自动检查<br>Automated consistency checking between page and white paper | **待检验**<br>**To be tested** | 层名、证据等级、失败阈值在 [`msi/config.json`](../msi/config.json)、白皮书脚本与 `docs/` 间一致<br>Layer names, evidence levels, and thresholds agree across the three sources |

**关于第 1–5 项的一点说明：** 它们的阈值已经写在 [failure-matrix.md](failure-matrix.md) 里，
因此这里的「待办」不是「打算做」，而是「已预先承诺结果如何处置」。
若检验结果不支持对应层，处理方式是标记或删除，不需要再讨论一次。
第 6–9 项没有预先声明的失败阈值，因为它们的产出是**设计**（观测方案、替代切分、混淆清单）而不是主张；
它们本身不构成可证伪命题，因此被归为「待检验」而非「已被证伪就删」。

**A note on items 1–5:** their thresholds are already written in the failure matrix, so "to do" here
means "the disposition of the result is already committed". If a test does not support its layer, that
layer is marked or removed; there is no second discussion. Items 6–9 carry no preregistered failure
threshold because their output is a **design** — an observation plan, an alternative partition, a
confound list — not a claim. They are therefore "to be tested" rather than "delete if falsified".

---

## 五、版本号的含义 / What the Version Number Means

`0.x` 表示六层栈与证据等级体系**仍在演进**，任何模块都可能因为未通过其预注册的证伪标准而被
标记或删除。这类变更会在 [`CHANGELOG.md`](../CHANGELOG.md) 中**显式说明**，而不是悄悄修改。

`0.x` means the six-layer stack and the evidence-level scheme are **still evolving**, and any module
may be marked or removed for failing its preregistered falsification criteria. Such changes are stated
**explicitly** in the changelog rather than edited silently.

---

后续阅读：[系统架构](architecture.md) · [证据体系](evidence.md) · [理论失败矩阵](failure-matrix.md)

Further reading: [System Architecture](architecture.md) · [Evidence System](evidence.md) ·
[Theory Failure Matrix](failure-matrix.md)
