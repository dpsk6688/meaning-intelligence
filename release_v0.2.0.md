# Meaning Intelligence v0.2.0



## 意义智能 v0.2.0 —— 研究系统统一与 Claim 治理



**Meaning Intelligence v0.2.0 — Version Unification and Claim Governance**



这是《意义智能：意义文明的认知操作系统》V7.0 应用层的第二次公开发布。

本版本不新增理论主张,只做一件事:**把理论从叙述收敛为可引用的研究系统**。



This is the second public release of the application layer of \*Meaning Intelligence:

The Cognitive Operating System of Meaning Civilization\*, V7.0. This release introduces no new

theoretical claims. It does exactly one thing: \*\*converge the theory from narrative into a

citable research system\*\*.



\---



## 本版核心:从「叙述」到「可引用的 claims」



### 1\. Claim Registry(`docs/claims.md`)



**12 个理论主张首次获得唯一 ID。** 论文、网站、实验、工具都应引用 claim ID(如 `MI-C003`),

而不是笼统引用「L6」或「六层栈」。



每个 claim 有:



* 唯一 ID(`MI-C001` \~ `MI-C012`,新 claim 从 `MI-C100` 起)
* 精确定义
* 锚定正典章节
* Evidence Status(E0–E6)
* Claim Status(`Draft` / `Formalized` / `Under Test` / `Survived` / `Falsified` / `Withdrawn`)
* 测试方式
* **失败条件**(什么观察会让它作废)



12 claims 的三层分布:



| 层 | Claim ID | 内容 |

|---|---|---|

| Core | MI-C001, MI-C002 | 定义与元层关系 |

| Model | MI-C003 \~ MI-C005 | 三维度 / 光谱带 / 多尺度 |

| Stack | MI-C006 \~ MI-C012 | 六层各层效应 |



### 2\. Construct Boundary Map(Figure 3)



**MIT 在概念空间中的位置首次被画成图。** 三同心环:



* 内环(蓝):MIT —— 对智能活动的方向性调控
* 中环(紫):IQ / EQ / SQ —— 平行能力,被元层约束
* 外环(金):Semantic/Pragmatic · Decision Intelligence · Metacognitive AI · AI Alignment · Wisdom



清晰区分「MIT 是什么」与「MIT 不是什么」。



### 3\. Single Version Source(`VERSION.yaml`)



**所有版本号唯一真相源。** 此前 README badge / `config.json` / 白皮书 / 首页之间存在版本漂移;

本版起,任何版本号改动只需改 `VERSION.yaml`,其他文件从它派生。



### 4\. What This Theory Does NOT Claim(README)



在 README 显著位置新增一节,明确边界:



> ❌ 不声称:人类有意义的专属通道 / AI 不能参与意义过程 / 意义仅仅是主观偏好 /

> 所有智能系统都必须有人类监督 / 六层栈是唯一有效分解 / 本理论已经过实证确认



> ✅ 确实声称:智能需要方向性调控 / 意义判断可被结构化分析 / 价值与边界是方向判断的

> 组成部分 / 多尺度意义产生协调问题 / 递归审视可能对长期稳定性是必要的 /

> 以上主张都是\\\\\\\\\\\\\\\*\\\\\\\\\\\\\\\*可检验、可证伪\\\\\\\\\\\\\\\*\\\\\\\\\\\\\\\*的



### 5\. Research Status Panel(README)



README 顶部新增研究状态面板:



| 维度 | 状态 |

|---|---|

| 研究阶段 | `public-research` |

| 六层栈证据等级 | **E0(概念)** |

| 白皮书 | v1.1(21 页) |

| 版本源 | `VERSION.yaml` |

| 学术承诺 | 失败阈值触发 → **标记或删除,不辩护** |



\---



## 白皮书更新至 v1.1



《意义智能 · 元智能理论与分层应用》公开发布白皮书更新:



* **新增 Chapter:构造边界**(含 Figure 3)
* **新增 Chapter:Claim Registry 摘要**(含 Table 8,12 claims)
* 页数:19 → **21**
* 版本号:1.0 → **1.1**



白皮书的 claim ID 与 `docs/claims.md` 一一对应,但**详细测试方式与失败条件以仓库为准**——

白皮书只作摘要与引用,避免双重维护漂移。



\---



## 版本治理规范



本版起明确**四层版本身份**:



| 层 | 版本 | 含义 |

|---|---|---|

| **正典 Canon** | V7.0 | 理论原典,不由本仓库版本化 |

| **研究系统 Research System** | v0.2.0 | 当前公开研究实现,`0.x` = research formation |

| **操作栈 Operational Stack** | v2.0 | 当前实验性结构,证据等级 E0 |

| **白皮书 White Paper** | v1.1 | 当前公开摘要 |



**`0.x` 是刻意保守的约定**:只有在完成 construct validation、首次预测性研究、

以及独立复现之后,才进入 `1.0`。



\---



## 与前版对比



| 项 | v0.1.0 | v0.2.0 |

|---|---|---|

| Claim ID 治理 | 无 | 12 个 claim 有唯一 ID |

| 版本单一源 | 无 | `VERSION.yaml` |

| 构造边界图 | 无 | `fig3\\\\\\\\\\\\\\\_construct\\\\\\\\\\\\\\\_boundary.png` |

| 研究状态面板 | 无 | README 顶部 |

| What It Does NOT Claim | 无 | README 显著位置 |

| 白皮书版本 | v1.0(19 页) | v1.1(21 页) |

| 白皮书 Claim 摘要 | 无 | Table 8 |



\---



## 文件清单(本版新增或修改)



**新增**:

* `VERSION.yaml` —— 单一版本源
* `docs/claims.md` —— Claim Registry
* `README.en.md` —— 英文版 README
* `ROADMAP.md` —— 工程路线图
* `whitepaper/figures/fig3\\\\\\\\\\\\\\\_construct\\\\\\\\\\\\\\\_boundary.png` —— 构造边界图
* `tools/` 下若干维护脚本



**修改**:

* `README.md` / `README.en.md` —— 加入研究状态面板、不声称声明、构造边界
* `docs/architecture.md` —— 加入构造边界章节
* `CITATION.cff` —— version 0.2.0
* `CHANGELOG.md` —— 加入 \[0.2.0] 段
* `whitepaper/build\\\\\\\\\\\\\\\_whitepaper.py` —— fig3 + Claim Registry 摘要
* `whitepaper/docx\\\\\\\\\\\\\\\_style.py` —— 输出文件名 v1.1
* `whitepaper/dist/` —— 白皮书 v1.1(DOCX + PDF)



\---



## 可失败性承诺不变



本版**不引入新理论主张**,因此不改变失败矩阵。既有承诺继续有效:



> 任何模块达到失败阈值,将被\\\\\\\\\\\\\\\*\\\\\\\\\\\\\\\*标记或删除\\\\\\\\\\\\\\\*\\\\\\\\\\\\\\\*,而不是被辩护。



六层栈本身仍是 **E0(概念)**——未经独立检验。若出现更简洁且解释力更强的切分,

应当**替换**它,而不是为它辩护。



\---



## 如何参与



* 📄 白皮书:见本页附件(v1.1,21 页,中英双语,DOCX + PDF)
* 🗂 Claim Registry:[`docs/claims.md`](../blob/main/docs/claims.md)
* 🗺 路线图:[`ROADMAP.md`](../blob/main/ROADMAP.md)
* 🧪 证伪报告:[Issue 模板](../issues/new?template=falsification_report.yml)
* 💬 讨论:[Discussions](../discussions)



\---



**理论引用请以正典为准**:《意义智能:意义文明的认知操作系统》V7.0。

