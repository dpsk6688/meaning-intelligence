# 贡献指南 / Contributing

感谢你愿意把注意力投入这个项目。在动手之前，请先读这一节——它决定了什么样的贡献在这里**能被合并**。

Thank you for spending attention on this project. Before you start, read this section: it decides what kinds of contributions **can be merged** here.

**本项目的核心承诺是"可失败性"。** 意义智能被当作一个**可检验的科学假说**，而不是哲学论断，也不是需要被捍卫的立场。因此：一个贡献的价值，取决于它是否让某条主张**更容易被检验、更容易被推翻**，而不是取决于它是否让主张听起来更可信。

**The core commitment of this project is falsifiability.** Meta-intelligence is treated as a **testable scientific hypothesis**, not a philosophical thesis and not a position to be defended. So the value of a contribution depends on whether it makes a claim **easier to test and easier to refute**, not on whether it makes the claim sound more credible.

---

## 目录 / Contents

1. [证伪报告：最重要的贡献方式 / Falsification reports](#1-证伪报告最重要的贡献方式--falsification-reports)
2. [假设卡片 H1–H18 的新增与修订 / Adding or revising hypothesis cards](#2-假设卡片-h1h18-的新增与修订--adding-or-revising-hypothesis-cards)
3. [六层栈的操作化改进 / Operationalization improvements for L1–L6](#3-六层栈的操作化改进--operationalization-improvements-for-l1l6)
4. [代码贡献 / Code contributions](#4-代码贡献--code-contributions)
5. [文档贡献 / Documentation contributions](#5-文档贡献--documentation-contributions)
6. [中英双语一致性 / Bilingual consistency](#6-中英双语一致性--bilingual-consistency)
7. [行为期待 / Behavioral expectations](#7-行为期待--behavioral-expectations)
8. [不予合并的情形 / What will not be merged](#8-不予合并的情形--what-will-not-be-merged)
9. [贡献的许可 / Licensing of contributions](#9-贡献的许可--licensing-of-contributions)

---

## 1. 证伪报告：最重要的贡献方式 / Falsification Reports

**中文**

如果你做了一项观测、实验或分析，其结果与正典中某条假设的预测不符，那么这份报告是本项目最有价值的贡献——比任何赞同都更有价值。请使用[证伪报告模板](.github/ISSUE_TEMPLATE/falsification_report.yml)提交，它要求的字段不是形式主义，而是让判断可以脱离报告人的身份独立完成。

提交时请做到：

- **指明对象**：哪一条假设（H1–H18）或哪一层（L1–L6）。
- **对准预注册标准**：正典为每条假设写了证伪标准。请引用该标准的具体条款，并说明你的结果**如何**满足它。如果结果只是"与预测方向相反"而没有达到标准中的阈值、样本量或统计要求，请如实说明——这类报告我们仍然会读，但它不构成证伪。
- **给出可复核的数字**：效应量（如 Cohen's d 或你实际使用的指标）、p 值、统计功效、样本量与抽样方式。没有这些，观测描述无法被复核为"证伪"。
- **交代数据可得性**：数据在哪、能否公开、受何限制。若不能公开，说明原因，并给出足以让别人重新设计一次检验的细节。
- **自评不确定性**：说明你最担心这个报告的哪一点（测量、混淆变量、样本、分析自由度）。诚实的自评比漂亮的结论更有用。

**后果是明确的：若证伪成立，对应模块将在后续版本中被标记或删除，而不是被辩护。** 这是我们对学术诚信的具体承诺，也适用于我们自己提出的任何模块。

**复制性报告同样欢迎。** 与正典预测一致的结果，只有在独立数据上重复出现（对应 E4 复制）才有证据价值。请同样说明样本、分析与偏差控制。

**English**

If an observation, experiment, or analysis of yours conflicts with a prediction in the canonical text, that report is the most valuable contribution to this project — more valuable than any agreement. Submit it with the [falsification report template](.github/ISSUE_TEMPLATE/falsification_report.yml). Its fields are not formalism; they let the judgment be made independently of who filed the report.

Please:

- **Name the target**: which hypothesis (H1–H18) or which layer (L1–L6).
- **Match the preregistered criterion**: the canonical text states a falsification criterion for each hypothesis. Quote the specific clause and explain **how** your result satisfies it. If your result merely runs opposite to the prediction without meeting the stated threshold, sample size, or statistical requirement, say so plainly — we still read such reports, but they are not a falsification.
- **Provide checkable numbers**: effect size (Cohen's d or whatever you actually used), p value, statistical power, sample size, and sampling procedure. Without these, an observation cannot be reviewed as a falsification.
- **State data availability**: where the data is, whether it can be public, and under what restrictions. If it cannot be public, explain why and give enough detail for someone else to redesign the test.
- **Self-assess uncertainty**: name what worries you most about your own report (measurement, confounds, sample, researcher degrees of freedom). An honest self-assessment is more useful than a tidy conclusion.

**The consequence is explicit: if the falsification holds, the module will be marked or removed in a later version, not defended.** That is our concrete commitment to research integrity, and it applies to modules we proposed ourselves.

**Replication reports are just as welcome.** Results consistent with a canonical prediction carry evidential weight only when they recur on independent data (evidence level E4, replicated). State sample, analysis, and bias controls there too.

---

## 2. 假设卡片 H1–H18 的新增与修订 / Adding or Revising Hypothesis Cards

**中文**

正典目前包含 18 张可检验假设卡片（H1–H18）。新增或修订一张卡片，请遵守下面的最小结构；缺少**预注册证伪标准**的卡片不予合并。

一张卡片至少需要：

1. **编号与名称**——新增用 H19 及以后，不要重排既有编号（编号是引用锚点）。
2. **主张陈述**——一句话，可判定真假，不包含"应当"类的规范语句。
3. **构念定义与操作化指标**——这个构念用什么被测量出来，单位与计分方式是什么。
4. **预测**——在什么条件下、预测观察到什么方向与量级的结果。
5. **预注册证伪标准**——阈值、样本量、统计判据、以及"若结果落在何处即判定为证伪"。此条为必需项。
6. **当前证据等级**——按 E0 概念 / E1 形式化 / E2 操作化 / E3 预测性 / E4 复制 / E5 证伪或存活 / E6 外部验证 标注，并说明依据。
7. **与六层栈的对应**——涉及 L1–L6 中的哪一层或哪几层。
8. **失败后操作**——若达到失败阈值，这条卡片应当被标记还是删除，理由是什么。

修订规则（**这一条比格式更重要**）：

- 证伪标准**只能**基于理论或方法学理由修订，且必须在 PR 中写明理由与影响；
- **不得在看到数据之后再放宽或改写证伪标准**（HARKing）。若某标准是在观测之后调整的，必须在卡片注释中标注该事实与时间顺序；
- 已发布卡片的编号、原有标准与失败阈值的历史应可追溯：修订请在卡片内保留变更说明，不要静默覆盖。

**English**

The canonical text currently contains 18 testable hypothesis cards (H1–H18). A new or revised card must have the minimal structure below. Cards without a **preregistered falsification criterion** will not be merged.

A card needs at least:

1. **Identifier and name** — new cards start at H19; never renumber existing ones (identifiers are citation anchors).
2. **Claim statement** — one sentence, truth-apt, with no normative "should".
3. **Construct definition and operationalization** — how the construct is measured, with units and scoring.
4. **Prediction** — under what conditions, what direction and magnitude of result is expected.
5. **Preregistered falsification criterion** — threshold, sample size, statistical rule, and where a result counts as falsifying. This one is mandatory.
6. **Current evidence level** — one of E0 conceptual, E1 formalized, E2 operationalized, E3 predictive, E4 replicated, E5 falsified or surviving, E6 externally validated, with the basis for the label.
7. **Mapping to the six-layer stack** — which of L1–L6 it touches.
8. **Post-failure action** — whether the card should be marked or removed on reaching its failure threshold, and why.

Revision rules (**more important than the format**):

- A falsification criterion may be revised **only** for theoretical or methodological reasons, and the PR must state the reason and its consequences;
- **Never relax or rewrite a criterion after seeing the data** (HARKing). If a criterion was adjusted after observation, the card must record that fact and the order of events;
- Identifiers, prior criteria, and failure thresholds must stay traceable: keep a revision note inside the card instead of overwriting silently.

---

## 3. 六层栈的操作化改进 / Operationalization Improvements for L1–L6

**中文**

六层应用栈是：L1 减负 / L2 可体验 / L3 意义生成 / L4 价值评估 / L5 方向选择 / L6 反思与审视递归；三带划分为界面带（L1–L2）、加工带（L3–L4）、元带（L5–L6）。

"某层不好用"不是可处理的贡献；"某层的某个指标可以这样测"才是。为某一层提交操作化改进时，请给出：

1. **目标构念**——这一层到底在调控什么（例如 L1 调控的是外在与内在认知负荷的哪一部分）。
2. **指标与测量程序**——具体任务、仪器或问卷、评分规则、观察单位。
3. **已知混淆与边界条件**——什么情况下这个指标会失效或误判。
4. **最小可判别效应**——多大的差异才值得当作差异，而不是噪声。
5. **对可检验性的影响**——这项操作化让哪条预测变得可检验？是否让某条原本可检验的预测变得不可检验？后一种情况必须说明。
6. **预期证据等级**——改进落地后，相关模块可望达到 E2 操作化 / E3 预测性 / E4 复制的哪一级，依据是什么。

跨层改进（例如 L3 与 L4 的指标互相污染）尤其欢迎，请明确写出层间依赖。

**English**

The six-layer application stack is L1 Cognitive Load Reduction, L2 Experiential Rendering, L3 Meaning Generation, L4 Value Assessment, L5 Direction Selection, and L6 Recursive Reflection and Review, grouped into the interface band (L1–L2), the processing band (L3–L4), and the meta band (L5–L6).

"This layer is not useful" is not an actionable contribution; "this indicator of this layer can be measured this way" is. For an operationalization proposal on any layer, provide:

1. **Target construct** — what the layer actually regulates (for example, which part of extraneous versus intrinsic cognitive load L1 targets).
2. **Indicator and measurement procedure** — task, instrument or questionnaire, scoring rule, unit of observation.
3. **Known confounds and boundary conditions** — when the indicator fails or misleads.
4. **Minimum detectable effect** — how large a difference must be to count as a difference rather than noise.
5. **Effect on testability** — which prediction does this operationalization make testable? Does it make any previously testable prediction untestable? The latter must be stated.
6. **Expected evidence level** — after the change, whether the module can be expected to reach E2 operationalized, E3 predictive, or E4 replicated, and on what basis.

Cross-layer proposals are especially welcome (for example, when L3 and L4 indicators contaminate each other); state the inter-layer dependency explicitly.

---

## 4. 代码贡献 / Code Contributions

**中文**

仓库包含两部分代码：`whitepaper/`（用 python-docx 生成中英双语 DOCX）与 `msi/`（Manim 场景 + 单文件交互页构建脚本）。

流程：

1. Fork 仓库，从 `main` 新建分支。分支名建议：`fix/…`、`feat/msi-…`、`docs/…`、`ci/…`、`hypothesis/h19-…`。
2. 本地运行受影响的部分（见下面"本地校验"）。
3. 提交 PR，并在描述里说明**这次改动改变了什么可观察行为**。若改动不改变任何可观察行为（纯重构），请直说。

提交信息风格（建议，不强制）：

- 一行主题，祈使句，≤ 72 字符，例如 `msi: 修复时间轴注入的空引号导致的 SyntaxError`；
- 可加作用域前缀：`msi:`、`whitepaper:`、`ci:`、`docs:`、`hypothesis:`；
- 正文说明**为什么**改，以及是否影响某条主张的证据等级；
- 不用夸张措辞描述改动规模。

本地校验（与 CI 一致）：

```bash
# YAML 可解析
python -c "import pathlib,yaml; [yaml.safe_load(p.read_text(encoding='utf-8')) for p in pathlib.Path('.github').rglob('*.yml')]"

# 重建白皮书
cd whitepaper && python make_figures.py && python build_whitepaper.py

# 构建 MSI 交互页
cd msi && python build.py

# 校验生成页面的内联 JavaScript 语法
node --check <抽出的内联脚本>
```

关于产物：`whitepaper/dist/` 是**有意入库**的发布产物，更新白皮书内容时请重新构建并一并提交；其余构建产物（Manim 的 `media/`、渲染出的 `*.mp4`）不入库，规则见 [`.gitignore`](.gitignore)。CI **不渲染 Manim**（太重），只跑 `planned` 时间轴分支。

**English**

The repository holds two code parts: `whitepaper/` (bilingual DOCX generated with python-docx) and `msi/` (Manim scenes plus the single-file interactive page builder).

Process:

1. Fork the repository and branch from `main`. Suggested branch names: `fix/…`, `feat/msi-…`, `docs/…`, `ci/…`, `hypothesis/h19-…`.
2. Run the affected part locally (see "Local checks").
3. Open a PR and state **what observable behavior changed**. If nothing observable changed (a pure refactor), say so.

Commit message style (a suggestion, not a rule):

- One imperative subject line, ≤ 72 characters, e.g. `msi: fix SyntaxError from empty quotes in timeline injection`;
- Optional scope prefix: `msi:`, `whitepaper:`, `ci:`, `docs:`, `hypothesis:`;
- The body explains **why**, and whether any claim's evidence level is affected;
- Do not describe the size of a change in grandiose terms.

Local checks (the same ones CI runs):

```bash
# YAML parses
python -c "import pathlib,yaml; [yaml.safe_load(p.read_text(encoding='utf-8')) for p in pathlib.Path('.github').rglob('*.yml')]"

# Rebuild the white paper
cd whitepaper && python make_figures.py && python build_whitepaper.py

# Build the MSI interactive page
cd msi && python build.py

# Check inline JavaScript syntax in the generated page
node --check <extracted inline script>
```

Artifacts: `whitepaper/dist/` is a release artifact and is **intentionally tracked** — rebuild and commit it when the white paper content changes. Other build outputs (Manim's `media/`, rendered `*.mp4`) are not tracked; see [`.gitignore`](.gitignore). CI **does not render Manim** (too heavy) and only exercises the `planned` timeline branch.

---

## 5. 文档贡献 / Documentation Contributions

**中文**

白皮书是**由脚本生成的**，不是手写文档：

- 正文与结构：`whitepaper/build_whitepaper.py`
- 排版与样式：`whitepaper/docx_style.py`
- 插图：`whitepaper/make_figures.py`

**请不要直接编辑 `whitepaper/dist/` 下的 DOCX 或 PDF。** 直接改二进制产物有两个后果：改动无法被评审（diff 不可读），并且会在下一次构建时被静默覆盖。请改生成脚本，然后重新构建。

DOCX 是二进制格式，评审者看不到逐行 diff。因此请在 PR 描述里贴出改动前后的**关键段落文本**（中文与英文各一段即可），让内容层面的变化可被评阅。

**English**

The white paper is **generated by scripts**, not hand-written:

- Content and structure: `whitepaper/build_whitepaper.py`
- Layout and styles: `whitepaper/docx_style.py`
- Figures: `whitepaper/make_figures.py`

**Do not edit the DOCX or PDF under `whitepaper/dist/` directly.** Editing binary artifacts has two consequences: the change cannot be reviewed (the diff is unreadable) and it is silently overwritten by the next build. Change the generator scripts and rebuild.

DOCX is binary, so reviewers see no line-by-line diff. In your PR description, quote the **key passages before and after** (one paragraph each in Chinese and English is enough) so the content change can be reviewed.

---

## 6. 中英双语一致性 / Bilingual Consistency

**中文**

面向读者的改动应当在同一个 PR 内同时更新中文与英文。两条具体要求：

1. **英文不得比中文更强。** 中文写"部分支持"，英文就不能写"confirms"；中文写"与预测一致"，英文不能写成"proves"。译文的证据强度不得超过原文。
2. **若你只能写一种语言**，请在 PR 中明确说明，并把另一种语言处标注 `TODO(bilingual)`，让缺口可见、可追踪。请不要用机器翻译填补并假装它已定稿。

**English**

Reader-facing changes should update Chinese and English in the same PR. Two requirements:

1. **English must not be stronger than Chinese.** If the Chinese says "部分支持" (partially supported), the English cannot say "confirms"; if it says "与预测一致" (consistent with the prediction), the English cannot say "proves". A translation may never exceed the evidential strength of the original.
2. **If you can write only one language**, say so in the PR and mark the other side `TODO(bilingual)` so the gap is visible and trackable. Do not fill it with machine translation and present it as final.

---

## 7. 行为期待 / Behavioral Expectations

**中文**

**可以攻击理论，不可以攻击人。**

- 针对主张的批评必须附带**可检验的理由**：说明在什么观测下你会改变看法，或者指出该主张在何种条件下无法被检验。
- 这条要求是对称的：为一条主张辩护时，同样要说明它在什么观测下会被放弃。只依赖"它说得通"的支持不是支持。
- 对方法、数据、推理的攻击是欢迎的；对报告人身份、动机、能力或人格的评论不是。
- 指出别人工作中的错误时，请给出定位（文件、行号、卡片编号），让问题可被独立复核。
- 若你发现自己先前的报告有误，请更正它。更正记录本身就是有价值的贡献。

完整的行为准则见 [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)。

**English**

**Attack the theory, not the person.**

- Criticism of a claim must come with **testable reasons**: state what observation would change your mind, or show under what conditions the claim cannot be tested at all.
- The requirement is symmetric: when defending a claim, likewise state what observation would make you abandon it. Support that rests only on "it makes sense" is not support.
- Attacks on methods, data, and reasoning are welcome; commentary on a reporter's identity, motives, competence, or character is not.
- When pointing out an error, locate it (file, line, card identifier) so it can be checked independently.
- If you find an error in your own earlier report, correct it. The correction is itself a valuable contribution.

The full code of conduct is in [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

---

## 8. 不予合并的情形 / What Will Not Be Merged

**中文**

- 缺少**预注册证伪标准**的假设卡片（第 2 节）；
- 事后放宽、删除或改写证伪标准，且未说明时间顺序与理由；
- 未标注来源的数据、引用或图表；编造的数据、DOI、机构或作者信息；
- 营销式措辞（"颠覆""革命性""世界首个""唯一正确"）与无法被检验的强主张；
- 把"符合直觉"或"内部一致"当作证据等级提升的理由；
- 中英双语中只更新一侧且未标注 `TODO(bilingual)`；
- 直接编辑 `whitepaper/dist/` 下的二进制产物；
- 针对个人的评论。

**English**

- Hypothesis cards without a **preregistered falsification criterion** (section 2);
- Relaxing, deleting, or rewriting a falsification criterion post hoc without stating the order of events and the reason;
- Data, citations, or figures without attribution; fabricated data, DOIs, institutions, or author identities;
- Marketing language ("disruptive", "revolutionary", "world's first", "the only correct") and strong claims that cannot be tested;
- Treating "it feels right" or "it is internally consistent" as grounds for raising an evidence level;
- Updating only one side of a bilingual change without a `TODO(bilingual)` marker;
- Direct edits to binary artifacts under `whitepaper/dist/`;
- Commentary aimed at persons.

---

## 9. 贡献的许可 / Licensing of Contributions

**中文**

本项目采用**入站即出站**（inbound = outbound）的许可方式，不要求签署额外协议：

- **代码贡献**适用 MIT（见 [`LICENSE`](LICENSE)）；
- **文档贡献**适用 CC BY 4.0（见 [`LICENSE-DOCS`](LICENSE-DOCS)）。

提交 PR 即表示你同意按上述许可发布你的贡献，并且你有权这样做。若你的贡献包含第三方内容，请注明其来源与许可，并确认该许可允许再分发。

**English**

This project uses **inbound = outbound** licensing with no additional agreement:

- **Code contributions** are under MIT (see [`LICENSE`](LICENSE));
- **Documentation contributions** are under CC BY 4.0 (see [`LICENSE-DOCS`](LICENSE-DOCS)).

By opening a pull request you agree to release your contribution under those terms, and you confirm you have the right to do so. If your contribution embeds third-party material, state its source and license and confirm that redistribution is permitted.

---

## 联系 / Contact

**中文**：请通过 [GitHub Issues](https://github.com/sara-protocol/meaning-intelligence/issues) 提交问题、证伪报告与建议。非议题类的联系请通过维护者主页 <https://github.com/sara-protocol>。本项目不公布邮箱地址；请不要在 issue 中提交未公开的个人信息或个人数据。

**English**: Use [GitHub Issues](https://github.com/sara-protocol/meaning-intelligence/issues) for questions, falsification reports, and proposals. For non-issue contact, reach the maintainer through <https://github.com/sara-protocol>. This project publishes no email address; please do not post private personal information or personal data in issues.
