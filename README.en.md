# Meaning Intelligence



> **Meta-Intelligence Theory and Layered Applications**

> Aligned with the canon *Meaning Intelligence: The Cognitive Operating System of Meaning Civilization* V7.0



[![Live Page](https://img.shields.io/badge/live-page-00e5ff?style=flat-square)](https://sara-protocol.github.io/meaning-intelligence/)

[![Release](https://img.shields.io/github/v/release/sara-protocol/meaning-intelligence?style=flat-square&color=bb86fc)](https://github.com/sara-protocol/meaning-intelligence/releases/latest)

[![License](https://img.shields.io/badge/license-MIT-8b95a5?style=flat-square)](LICENSE)

[![Version](https://img.shields.io/badge/version-0.2.0-6B4C9A.svg)](VERSION.yaml)



---



**Meaning Intelligence is the *directional regulation* of other intelligent activities.** It is not a fourth kind of intelligence standing alongside logical, computational, and perceptual intelligence, but a *meta-layer* above them that constrains their direction. Its question is not *"can it be done"* but *"is it worth doing — worth it for whom, and at what scale?"*



[中文版](README.md)



---

## Research Status

| Dimension | Current status |
|---|---|
| Research phase | `public-research` — 0.x signals research formation, not yet empirically tested |
| Stack evidence level | **E0 (conceptual)** — not independently tested |
| White paper | v1.0 (19 pages, bilingual, DOCX + PDF) |
| Version source | [`VERSION.yaml`](VERSION.yaml) — single source of truth for all version numbers |
| Falsification path | [Failure matrix](docs/failure-matrix.md) · [Falsification report template](.github/ISSUE_TEMPLATE/falsification_report.yml) |
| Scholarly commitment | Any module reaching its failure threshold will be **marked or removed**, not defended |

> **On version numbering**: This project uses `0.x` to signal research formation.
> Only after construct validation, a first predictive study, and independent replication
> does it reach `1.0`. This is a deliberate, conservative convention.

---




## What This Theory Does NOT Claim



This theory is most easily misread as a manifesto of the form "AI gives answers, only humans create meaning". It is **not**. To avoid that battlefield, here is an explicit list of its boundaries.



### ❌ This theory does NOT claim



- that humans possess exclusive access to meaning

- that AI cannot participate in meaning processes

- that meaning is subjective preference alone

- that all intelligent systems require human supervision

- that the six-layer stack is the only valid decomposition

- that the theory is empirically confirmed



### ✅ This theory DOES claim



- intelligence requires directional regulation

- meaning judgments can be structurally analyzed

- value and boundary are parts of directional judgment

- multi-scale meaning creates coordination problems

- recursive review may be necessary for long-horizon stability

- the claims above are **testable and falsifiable**



---



## Construct Boundaries



**This project's "Meaning Intelligence" is a specific naming.** As of 2026, `Meaning Intelligence` is already in use across several directions — semantic/pragmatic analysis, decision support, and commercial products among them. This project's **Meaning Intelligence Theory (MI Theory)** refers to **the directional regulation of intelligent activities**. It is not identical to any of the following adjacent constructs.



| Adjacent construct | Concerns | Relation to this project |

|---|---|---|

| **IQ / EQ / SQ** | Can it compute / get along / coexist | Parallel capabilities; this theory **sits above them** to constrain direction |

| **Semantic / Pragmatic Intelligence** | Context, intent, irony, coded subtext in language | Handles **meaning in language**; this theory handles **direction of action** |

| **Decision Intelligence** | Coherent understanding from information + context + human judgment | Application-layer framework; this theory provides the **meta-layer structure** |

| **Metacognitive AI** | Self-monitoring, resource allocation, difficulty estimation | Adjacent to L6; L6 is **one layer of the stack** |

| **AI Alignment** | Aligning AI behavior with human values | Provides **structure for directional judgment**; does not replace alignment research |

| **Wisdom / Judgment traditions** | Practical wisdom, judgment | This theory attempts to **formalize** them into testable structure |



> **Naming conflict statement**: This project does not claim exclusivity over the term `Meaning Intelligence`. We do explicitly distinguish: this project's "Meaning Intelligence Theory" refers to **directional regulation**, which is a **different construct** from same-named usage in semantic, pragmatic, or decision-oriented directions.



---



### Construct Boundary Map

![Construct Boundary Map](whitepaper/figures/fig3_construct_boundary.png)

The figure places MIT in a conceptual space: the **inner ring** is MIT itself (a meta-layer for
the directional regulation of intelligent activities); the **middle ring** is IQ / EQ / SQ
(parallel capabilities, constrained by the meta-layer); the **outer ring** is the adjacent
fields (Semantic/Pragmatic, Decision Intelligence, Metacognitive AI, AI Alignment, Wisdom
traditions).

Naming collision is unavoidable — `Meaning Intelligence` is already in use across multiple
directions. This project's **Meaning Intelligence Theory (MI Theory)** refers to **directional
regulation**, which is a **different construct** from same-named usage in semantic, pragmatic,
or decision-oriented directions.


## The Six-Layer Stack



The six layers fall into **three bands** by cognitive distance:



| Band | Layer | Name | Solves |

|---|---|---|---|

| **Interface** | L1 | Cognitive Load Reduction | *Information cannot get in* |

| **Interface** | L2 | Experiential Rendering | *Information cannot get in* |

| **Processing** | L3 | Meaning Generation | *Meaning cannot get out* |

| **Processing** | L4 | Value Assessment | *Meaning cannot get out* |

| **Meta** | L5 | Direction Selection | *Direction cannot be held* |

| **Meta** | L6 | Recursive Reflection and Review | *Direction cannot be held* |



**Only the meta band can rewrite the premises of the layers below it** — this is the formal signature of "meta".



L6's output is written back as L1's input. The six layers form a **closed spiral**, not a one-way pipeline.



> ### ⚠️ A note on the stack itself

>

> The six-layer stack is an **integrative structure** at evidence level **E0 (conceptual)**. It has not been independently tested. Treat it as a **testable organizing tool**, not a confirmed finding. If a simpler partition with greater explanatory power emerges, it should **replace** this one.



## What's in this Repository



| Directory | Contents |

|---|---|

| `whitepaper/` | Bilingual public-release white paper v1.0 (19 pages, 7 tables, 2 figures), DOCX + PDF, generation scripts |

| `msi/` | Meaning Intelligence Demonstration System — six-act Manim animation, single-file interactive page, per-layer screenshots |

| `toolkit/` | 11 fillable checklists derived from Canon Appendix A (A.1–A.10) |

| `docs/` | Architecture, evidence levels, failure matrix, glossary, roadmap, automation governance |

| `tools/` | Zero-dependency publisher, PDF/HTML verifiers, issue-form validator |



## Quick Start



```bash

# 1. Clone

git clone https://github.com/sara-protocol/meaning-intelligence.git

cd meaning-intelligence



# 2. Read the white paper

#    → whitepaper/dist/意义智能_元智能理论与分层应用_公开发布白皮书_v1.0_中英双语.pdf



# 3. Watch the six-act animation

#    → msi/MeaningIntelligenceScene.mp4



# 4. Open the interactive dashboard

#    → msi/meaning_intelligence.html  (double-click; no server required)



# 5. Rebuild the white paper (optional)

python whitepaper/build_whitepaper.py



# 6. Re-render the animation (optional, requires manim)

cd msi && python run.ps1     # Windows

cd msi && bash run.sh        # macOS / Linux



