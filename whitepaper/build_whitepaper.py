# -*- coding: utf-8 -*-
"""《意义智能 · 元智能理论与分层应用》中英双语公开发布白皮书 v1.0"""
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

from docx_style import (BASE, FIG, OUT, NAVY, BODY, GRAY, SECOND, HEI, SONG,
                        LATIN_H, LATIN_B, title, h, label, body, bullet, note,
                        table, figure, para, set_font, CONTENT_W)

doc = Document()

# 页面：对齐正典 A4 + 页边距
for s in doc.sections:
    s.page_width, s.page_height = Cm(21.0), Cm(29.7)
    s.top_margin = s.bottom_margin = Cm(2.54)
    s.left_margin = s.right_margin = Cm(3.17)

st = doc.styles["Normal"]
st.font.name = LATIN_B
st.font.size = Pt(12)
st.element.rPr.rFonts.set(
    __import__("docx").oxml.ns.qn("w:eastAsia"), SONG)

# ================================================================ 封面区
title(doc, "意义智能 · 元智能理论与分层应用",
      "Meaning Intelligence: Meta-Intelligence Theory and Layered Applications",
      size=22, after=6)
p = para(doc, spacing=1.3, after=2, align=WD_ALIGN_PARAGRAPH.LEFT)
set_font(p.add_run("公开发布白皮书 v1.1"), 14, NAVY, True, HEI, LATIN_H)
set_font(p.add_run("\u3000Public Release White Paper v1.1"), 10, GRAY, False, HEI, LATIN_H)
p = para(doc, spacing=1.3, after=18)
set_font(p.add_run("对齐正典：《意义智能：意义文明的认知操作系统》V7.0"),
         10.5, SECOND, False, SONG, LATIN_B)
set_font(p.add_run("\u3000Aligned with the canonical text: Meaning Intelligence: "
                   "The Cognitive Operating System of Meaning Civilization, V7.0"),
         9, GRAY, False, SONG, LATIN_B)

# ================================================================ 发布声明
h(doc, "发布声明", "Release Statement", size=17, before=6)
body(doc,
     "本白皮书是《意义智能》V7.0 的应用层配套文档。它不新增本体论主张：所有理论命题、"
     "构念定义与证据等级一律以 V7.0 正典为准。本白皮书只承担一件事——把正典中的元智能理论，"
     "转译为可分层操作、可逐层检验的应用栈。",
     "This white paper is a companion document at the application layer of Meaning "
     "Intelligence V7.0. It introduces no new ontological claims: all theoretical "
     "propositions, construct definitions, and evidence levels follow the V7.0 canon. "
     "It does exactly one thing — translate the meta-intelligence theory of the canon "
     "into an application stack that can be operated layer by layer and tested layer by layer.")

label(doc, "三条自我约束", "[Three Self-Imposed Constraints]")
bullet(doc, "理论从属：凡本白皮书与正典冲突之处，以正典为准。",
       "Theoretical subordination: wherever this white paper conflicts with the canon, the canon prevails.")
bullet(doc, "证据诚实：每一层均标注证据等级并给出证伪条件；不确定处标注「待检验」，不写成「已成立」。",
       "Evidence honesty: every layer carries an evidence level and a falsification condition; "
       "what is uncertain is marked \"to be tested\", never written as \"established\".")
bullet(doc, "结构标明：六层栈本身是本白皮书提出的整合结构，当前证据等级为 E0（概念），"
            "尚未经过独立检验。请把它当作一个待检验的组织工具，而非一个已证实的发现。",
       "Structural disclosure: the six-layer stack itself is an integrative structure proposed by "
       "this white paper. Its current evidence level is E0 (conceptual); it has not been "
       "independently tested. Treat it as a testable organizing tool, not a confirmed finding.")

note(doc,
     "说明：正典《意义智能》V7.0 的中英双语版本仅在标题与图表题层面双语。本白皮书作为独立发布物，"
     "正文亦提供英文，以便英文读者完整阅读——这是刻意的体例升级，不改变正典体例。",
     "Note: the bilingual edition of the canon provides English only at headings and captions. "
     "As a standalone release document, this white paper also provides English for body text so "
     "that English readers can read it in full — a deliberate upgrade in convention that does not "
     "alter the canon's own convention.")

# ================================================================ 一页总览
h(doc, "一页总览", "One-Page Overview", size=17)

label(doc, "元智能的定义（引自正典 1.3）", "[Definition of Meta-Intelligence, from Canon §1.3]")
body(doc,
     "意义智能是对其他智能活动的方向性调控。它不是与逻辑智能、计算智能、感知智能并列的"
     "第四类智能，而是位于它们之上、对它们进行方向约束的元层。它的追问不是「能不能做到」，"
     "而是「值不值得做？对谁值得？在什么尺度上值得？」",
     "Meaning intelligence is the directional regulation of other intelligent activities. It is not "
     "a fourth kind of intelligence standing alongside logical, computational, and perceptual "
     "intelligence, but a meta-layer above them that constrains their direction. Its question is "
     "not \"can it be done\" but \"is it worth doing — worth it for whom, and at what scale?\"")

label(doc, "六层不是六个功能，而是一个递归栈", "[Six Layers as a Recursive Stack, Not Six Features]")
body(doc,
     "六层按认知距离分为三带：界面带（L1–L2）解决「信息进不来」，把外部信息压到可处理的带宽内；"
     "加工带（L3–L4）解决「意义出不来」，把材料转成有结构、有强度标注的判断；"
     "元带（L5–L6）解决「方向守不住」，选定方向并让系统审视自己的审视。"
     "三带之中，只有元带具备改写下层前提的能力——这正是「元」的形式特征。",
     "The six layers fall into three bands by cognitive distance. The interface band (L1–L2) solves "
     "\"information cannot get in\" by compressing external input to a workable bandwidth. The "
     "processing band (L3–L4) solves \"meaning cannot get out\" by turning material into structured "
     "judgments carrying strength labels. The meta band (L5–L6) solves \"direction cannot be held\" "
     "by selecting a direction and letting the system review its own review. Of the three bands, "
     "only the meta band can rewrite the premises of the layers below — this is the formal "
     "signature of \"meta\".")

figure(doc, FIG / "fig1_six_layer_stack.png", 14.6,
       "图 1　元智能六层栈", "Figure 1  The Six-Layer Meta-Intelligence Stack")

table(doc,
      ["层", "名称", "一句话定义", "理论锚点（正典）", "证据等级"],
      [["L1", "减负", "把认知负荷从信息量转移到结构", "第1章 1.1；工具 A.1", "机制 E3 / 本框架 E1"],
       ["L2", "可体验", "把「读到」变成「操作到」", "第3章；第9章 M1", "机制 E3 / 本框架 E1"],
       ["L3", "意义生成", "组织成方向·价值·边界", "第3章 3.1 / 3.2；第8章 8.1", "E0–E1"],
       ["L4", "价值评估", "为判断标注证据强度", "第6章 E0–E6；3.3 PE 方程", "E2（工具）/ E1（模型）"],
       ["L5", "方向选择", "在五尺度上选定值得的方向", "第4章；DC 指标；三级修正", "E1"],
       ["L6", "反思与审视递归", "让系统审视自己的审视", "三特性；理论失败矩阵", "E2（案例）/ E1"]],
      widths=[1.2, 2.6, 4.0, 4.0, 2.8],
      caption="表 1　六层总表", caption_en="Table 1  Overview of the Six Layers")

# ================================================================ 为什么是元
h(doc, "元智能为什么是「元」", "Why Meta-Intelligence Is \"Meta\"", size=17)

h(doc, "一、不是并列，而是嵌套与约束", "1. Not Parallel, But Nested and Constraining", size=13)
body(doc,
     "正典 1.3 明确：意义智能与 IQ、EQ、SQ 的关系不是并列，而是嵌套与约束。IQ 关心「能不能算」，"
     "EQ 关心「能不能相处」，SQ 关心「能不能共处」；三者都在回答「如何做到」。"
     "唯有意义智能追问「为何要做」以及「值不值得」。这不是能力更强，而是**层级更高**。",
     "Canon §1.3 states that meaning intelligence relates to IQ, EQ, and SQ not by parallelism but by "
     "nesting and constraint. IQ asks whether something can be computed, EQ whether people can get "
     "along, SQ whether they can coexist. All three answer \"how\". Only meaning intelligence asks "
     "\"why\" and \"whether it is worth it\". This is not greater capability but a higher level.")

h(doc, "二、递归是「元」的形式特征", "2. Recursion Is the Formal Signature of \"Meta\"", size=13)
body(doc,
     "一个普通的能力栈是单向流水线：输入经各级加工后输出，加工规则本身不受输出影响。"
     "元智能栈不是这样——第六层的产出会改写第一层的输入标准。"
     "换句话说，第二轮进入 L1 的材料，已经按第一轮 L6 的判断重新定义过「什么才算值得处理的材料」。",
     "An ordinary capability stack is a one-way pipeline: input passes through stages and emerges as "
     "output, while the processing rules themselves are unaffected by the output. A "
     "meta-intelligence stack is different — the output of layer six rewrites the input criteria of "
     "layer one. In other words, the material entering L1 in the second cycle has already had "
     "\"what counts as worth processing\" redefined by the L6 judgment of the first cycle.")

figure(doc, FIG / "fig2_recursive_spiral.png", 14.6,
       "图 2　递归闭合：六层螺旋", "Figure 2  Recursive Closure: The Six-Layer Spiral")

note(doc,
     "图 2 的关键几何：归零后的落点 L1′ 与原点 L1 处于同一角度，但半径更大。"
     "归零不是回到原点，而是回到更高一层的起点。若第二轮与第一轮完全重合，说明这一轮没有产生意义增量。",
     "The key geometry of Figure 2: the post-zeroing entry point L1′ sits at the same angle as the "
     "original L1 but at a larger radius. Zeroing does not return to the origin but to a higher entry "
     "point. If the second cycle coincides exactly with the first, no meaning increment was produced.")

h(doc, "三、与正典运行机制的映射", "3. Mapping onto the Canon's Operating Mechanisms", size=13)
table(doc,
      ["六层", "正典三模块（第9章）", "正典四流程（第10章）", "主要产出"],
      [["L1 减负", "M1 感知（输入侧）", "F1 意义识别", "结构化材料"],
       ["L2 可体验", "M1 感知（呈现侧）", "F1 意义识别", "可交互产物"],
       ["L3 意义生成", "M2 判断", "F2 意义评估", "候选意义结构"],
       ["L4 价值评估", "M2 判断", "F2 意义评估", "证据强度标注"],
       ["L5 方向选择", "M3 行动", "F3 意义决策", "方向声明＋偏离阈值"],
       ["L6 反思与审视递归", "M1→M2→M3 回环", "F4 意义反馈", "前提改写＋螺旋回环"]],
      widths=[2.6, 3.6, 3.2, 5.2],
      caption="表 2　六层与正典运行机制的对应", caption_en="Table 2  Mapping the Six Layers onto Canon Mechanisms")

# ================================================================ 构造边界
h(doc, "构造边界", "Construct Boundaries", size=17)
note(doc,
     "MIT 是一个特定命名。截至 2026 年，`Meaning Intelligence` 一词在语义/语用分析、决策支持、"
     "商业产品等多个方向已有使用。本项目的 Meaning Intelligence Theory (MIT) 指方向性调控，"
     "与下列方向不是同一构造。",
     "MIT is a specific naming. As of 2026, `Meaning Intelligence` is already in use across several "
     "directions — semantic/pragmatic analysis, decision support, and commercial products among them. "
     "This project's Meaning Intelligence Theory (MIT) refers to directional regulation, which is a "
     "different construct from same-named usage in those directions.")

figure(doc, FIG / "fig3_construct_boundary.png", 14.6,
       "图 3　构造边界：MIT 与邻接场域", "Figure 3  Construct Boundary Map")

note(doc,
     "内环是 MIT 本身（元层，对智能活动的方向性调控）；中环是 IQ / EQ / SQ（平行能力，被元层约束）；"
     "外环是邻接场域（Semantic / Pragmatic、Decision Intelligence、Metacognitive AI、AI Alignment、"
     "Wisdom 传统）。只有 MIT 位于其他智能活动之上，对它们进行方向约束——这是「元」的形式特征。",
     "The inner ring is MIT itself (a meta-layer for the directional regulation of intelligent activities); "
     "the middle ring is IQ / EQ / SQ (parallel capabilities, constrained by the meta-layer); "
     "the outer ring is the adjacent fields (Semantic/Pragmatic, Decision Intelligence, Metacognitive AI, "
     "AI Alignment, Wisdom traditions). Only MIT sits above the others and constrains their direction — "
     "the formal signature of the word meta.")

# ================================================================ 六层详解
h(doc, "六层详解", "The Six Layers in Detail", size=17)
note(doc, "每层按统一体例展开：本层追问 / 定义 / 理论锚点 / 操作 / 证据等级 / 常见误区 / 与相邻层的关系。",
     "Each layer follows a uniform template: Core Question / Definition / Theoretical Anchor / "
     "Practice / Evidence Level / Common Misconception / Relation to Adjacent Layers.")

# ---- L1
h(doc, "第一层　减负", "Layer 1  Cognitive Load Reduction", size=15)
label(doc, "【本层追问】", "[Core Question]")
body(doc, "当信息供给远超认知带宽时，第一步该做什么？",
     "When information supply far exceeds cognitive bandwidth, what is the first thing to do?")
label(doc, "【定义】", "[Definition]")
body(doc,
     "在不丢失决策所需关键结构的前提下，降低单位时间内的认知负荷总量。"
     "减负不是删减信息，而是把负荷从「处理原始信息」转移到「理解已结构化的关系」。",
     "To reduce the total cognitive load per unit of time without losing the key structure needed "
     "for decision. Load reduction is not deleting information; it shifts load from \"processing raw "
     "information\" to \"understanding already-structured relations\".")
label(doc, "【理论锚点】", "[Theoretical Anchor]")
body(doc, "正典第1章 1.1 智能的「方向性盲区」；附录 A 工具 A.1 意义自检卡。",
     "Canon §1.1, the \"directional blind spot\" of intelligence; Appendix A, Tool A.1, the Meaning Self-Check Card.")
label(doc, "【操作】", "[Practice]")
bullet(doc, "设定字数硬上限（建议 300 字），超限即触发重述。",
       "Set a hard word limit (300 characters/words suggested); exceeding it triggers a rewrite.")
bullet(doc, "用受控语言重述：主动语态、一句话一个指令、约 900 个核心词；取 ASD-STE100 的 80% 严格度，兼顾可读性。",
       "Restate in controlled language: active voice, one instruction per sentence, roughly 900 core "
       "words; apply ASD-STE100 at about 80% strictness to keep it readable.")
bullet(doc, "强制分离两份清单：「核心事实」与「待决问题」。前者可归档，后者必须带入下一层。",
       "Force a separation into two lists: \"core facts\" and \"open questions\". The former can be "
       "archived; the latter must be carried into the next layer.")
bullet(doc, "原始长文归档而非删除——减负不等于销毁证据。",
       "Archive the original long text rather than delete it — load reduction is not the destruction of evidence.")
label(doc, "【证据等级】", "[Evidence Level]")
body(doc, "底层机制 E3–E4（认知负荷与受控语言有长期实证积累）；本框架下的操作化 E1。",
     "Underlying mechanisms E3–E4 (cognitive load and controlled language have a long empirical "
     "record); operationalization within this framework E1.")
label(doc, "【常见误区】", "[Common Misconception]")
bullet(doc, "把减负等同于「摘要」。摘要仍是被动阅读；减负的目标是让读者从「读」转为「判断」。",
       "Equating load reduction with summarization. A summary is still passive reading; the goal is "
       "to move the reader from reading to judging.")
bullet(doc, "过度压缩导致边界信息丢失。正典公理四指出意义判断永远具有不完备性，压缩会放大这种不完备性。",
       "Over-compression loses boundary information. Canon Axiom Four holds that meaning judgment is "
       "always incomplete; compression amplifies that incompleteness.")
label(doc, "【与相邻层的关系】", "[Relation to Adjacent Layers]")
body(doc, "L1 的产物是 L2 的输入。没有 L1，L2 只是把混乱做得更好看。",
     "The output of L1 is the input of L2. Without L1, L2 merely makes confusion look better.")

# ---- L2
h(doc, "第二层　可体验", "Layer 2  Experiential Rendering", size=15)
label(doc, "【本层追问】", "[Core Question]")
body(doc, "理解一个结构，最短的路径是什么？",
     "What is the shortest path to understanding a structure?")
label(doc, "【定义】", "[Definition]")
body(doc,
     "把抽象关系转译为可操作、可回放的感知对象，使主体通过「动手」而非「阅读」获得结构直觉。",
     "To translate abstract relations into operable, replayable perceptual objects, so that the "
     "subject acquires structural intuition by doing rather than by reading.")
label(doc, "【理论锚点】", "[Theoretical Anchor]")
body(doc, "正典第3章 意义的结构与层次；第9章 M1 感知模块。本项目 MSI（意义智能演示系统）为本层的一个参考实现。",
     "Canon Chapter 3, the structure and levels of meaning; Chapter 9, module M1 (perception). The "
     "MSI (Meaning Intelligence demonstration system) in this project is one reference implementation of this layer.")
label(doc, "【操作】", "[Practice]")
bullet(doc, "为每个待理解的概念至少生成一种可交互形式。",
       "Produce at least one interactive form for every concept to be understood.")
bullet(doc, "交互必须暴露一个可改变的参数，并让结果可预测——这是「可体验」与「好看」的分界。",
       "The interaction must expose one changeable parameter whose effect is predictable — this is the "
       "dividing line between experiential and merely attractive.")
bullet(doc, "保留「可丢弃产物」思维：用完即弃，不占用记忆负担。",
       "Keep the disposable-artifact mindset: use it and discard it, so it occupies no memory burden.")
bullet(doc, "交互产物应附带时间轴标注，使「看到」与「读到」可对齐。",
       "Interactive artifacts should carry timeline annotations so that seeing and reading can be aligned.")
label(doc, "【证据等级】", "[Evidence Level]")
body(doc, "机制 E3（多媒体学习与双通道效应有实证支持）；本框架下的操作化 E1。",
     "Mechanisms E3 (multimedia learning and dual-channel effects have empirical support); "
     "operationalization within this framework E1.")
label(doc, "【常见误区】", "[Common Misconception]")
bullet(doc, "把「好看」当「可体验」。判据是用户能否改变参数并预测结果，而非页面是否精致。",
       "Mistaking good-looking for experiential. The criterion is whether the user can change a "
       "parameter and predict the result, not whether the page is polished.")
bullet(doc, "用交互掩饰逻辑空洞——交互会同时放大结构与错误。",
       "Using interactivity to mask an empty logic — interactivity amplifies errors as much as structures.")
label(doc, "【与相邻层的关系】", "[Relation to Adjacent Layers]")
body(doc, "L2 暴露结构，但不判断结构是否值得追求；后者属 L3 至 L5。",
     "L2 exposes structure but does not judge whether the structure is worth pursuing; that belongs to L3 through L5.")

# ---- L3
h(doc, "第三层　意义生成", "Layer 3  Meaning Generation", size=15)
label(doc, "【本层追问】", "[Core Question]")
body(doc, "一堆已经看懂的材料，如何变成「对我／我们意味着什么」？",
     "How does a pile of already-understood material become \"what it means for me / for us\"?")
label(doc, "【定义】", "[Definition]")
body(doc,
     "把材料组织为方向、价值、边界三个维度，并沿意义光谱带定位其抽象程度与时间尺度。",
     "To organize material along three dimensions — direction, value, boundary — and to locate its "
     "level of abstraction and time scale along the meaning spectrum.")
label(doc, "【理论锚点】", "[Theoretical Anchor]")
body(doc, "正典第3章 3.1（三层次）与 3.2（三维度）；**第8章 8.1 光谱带模型**。",
     "Canon §3.1 (three levels) and §3.2 (three dimensions); **Chapter 8 §8.1, the spectral band model**.")
note(doc,
     "V7 的重要更动：第3章 3.1 给出的是**离散三层次**，而第8章 8.1「光谱带模型取代固定层次」把它们"
     "重释为**一条连续光谱带**——原元意义层在高端（高抽象、长时距、低频率），原情境意义层在低端"
     "（高具体、短时距、高频率），「中间不存在断层，而是连续过渡」。"
     "因此 L3 的操作不是把材料塞进三个抽屉，而是判断它落在光谱带的哪一段。",
     "An important V7 change: §3.1 gives **discrete** levels, while §8.1 (\"the spectral band model "
     "replaces fixed levels\") reinterprets them as **one continuous band** — the former meta-meaning "
     "level at the abstract end, the former situational level at the concrete end, with \"no fault line "
     "in between, only continuous transition.\" L3's job is therefore not to sort material into three "
     "drawers but to judge which segment of the band it occupies.")
note(doc,
     "另注意不要与「四维度」混淆：**三维度 = 方向·价值·边界**（3.2）是一次意义判断要回答的三个问题；"
     "**四维度 = 认知 C·价值 V·存在 E·行动 A**（8.2）是光谱带上的四个耦合维度，用于系缚强度 BS 分析。",
     "Do not confuse this with the **four dimensions**: direction / value / boundary (§3.2) are the three "
     "questions one meaning judgment answers, whereas cognitive C / value V / existential E / action A "
     "(§8.2) are the four coupled dimensions of the spectral band used for binding-strength (BS) analysis.")
label(doc, "【操作】", "[Practice]")
bullet(doc, "方向之问：这件事把我们带向哪里？它的反方向是什么？",
       "Question of direction: where does this take us? What is its opposite direction?")
bullet(doc, "价值之问：它满足的是效用价值、内在价值还是关系价值？",
       "Question of value: does it satisfy utility value, intrinsic value, or relational value?")
bullet(doc, "边界之问：时间边界、空间边界、关系边界各在哪里？",
       "Question of boundary: where lie the temporal, spatial, and relational boundaries?")
bullet(doc, "光谱定位：它落在光谱带的哪一段？越靠上端越抽象、时距越长、频率越低；越靠下端越具体、时距越短、频率越高。",
       "Spectral placement: which segment of the band does it occupy? The higher the end, the more "
       "abstract, longer in time scale, and lower in frequency; the lower the end, the more concrete, "
       "shorter in time scale, and higher in frequency.")
label(doc, "【证据等级】", "[Evidence Level]")
body(doc, "E0（构念已定义）至 E1（已形式化）。",
     "E0 (construct defined) to E1 (formalized).")
label(doc, "【常见误区】", "[Common Misconception]")
bullet(doc, "层次混淆——把情境层的即时判断当作元意义层的终极方向。正典 3.4 指出：意义的丧失往往不是「没有意义」，"
            "而是意义结构出了问题。",
       "Level confusion — treating an immediate situational judgment as an ultimate meta-meaning "
       "direction. Canon §3.4 notes that loss of meaning is often not the absence of meaning but a "
       "structural failure of meaning.")
label(doc, "【与相邻层的关系】", "[Relation to Adjacent Layers]")
body(doc, "L3 产出候选意义结构，尚未评估其强度；强度评估属 L4。",
     "L3 produces candidate meaning structures without assessing their strength; strength assessment belongs to L4.")

# ---- L4
h(doc, "第四层　价值评估", "Layer 4  Value Assessment", size=15)
label(doc, "【本层追问】", "[Core Question]")
body(doc, "这个意义判断有多可靠？凭什么？",
     "How reliable is this meaning judgment, and on what grounds?")
label(doc, "【定义】", "[Definition]")
body(doc,
     "用统一标尺为意义判断标注证据强度与不确定性，并估计意义势能的变化方向。",
     "To label meaning judgments with evidence strength and uncertainty on a common scale, and to "
     "estimate the direction of change of meaning potential.")
label(doc, "【理论锚点】", "[Theoretical Anchor]")
body(doc, "正典第6章 E0–E6 证据等级；第3章 3.3 意义势能（PE）动态方程。",
     "Canon Chapter 6, the E0–E6 evidence levels; §3.3, the dynamic equation of meaning potential (PE).")
p = para(doc, spacing=1.4, before=4, after=4, align=WD_ALIGN_PARAGRAPH.CENTER)
set_font(p.add_run("PE_t = α_t A_t − β_t C_t − γ_t G_t − δ_t M_t"), 12, NAVY, True, SONG, LATIN_B)
note(doc,
     "A＝技术／行动能力，C＝认知复杂度，G＝治理能力，M＝意义协调度；α、β、γ、δ 为时变权重，"
     "由数据估计而非作者指定。权重更新规则见正典 3.3。",
     "A = technical/action capability, C = cognitive complexity, G = governance capability, "
     "M = meaning coordination; α, β, γ, δ are time-varying weights estimated from data rather than "
     "assigned by the author. See Canon §3.3 for the weight update rule.")
label(doc, "【操作】", "[Practice]")
bullet(doc, "为每个判断标注证据等级 E0–E6。",
       "Label every judgment with an evidence level from E0 to E6.")
bullet(doc, "写出它的证伪条件：什么观察会让它作废？写不出证伪条件的判断，应退回 L3 重新结构化。",
       "Write down its falsification condition: what observation would void it? A judgment with no "
       "falsification condition should be returned to L3 for re-structuring.")
bullet(doc, "估计 A／C／G／M 四个变量的变化方向，判断 PE 是升还是降。",
       "Estimate the direction of change of A / C / G / M to determine whether PE rises or falls.")
bullet(doc, "明确适用尺度——个人尺度的评估不能直接套用到组织尺度（正典公理三：多尺度意义不可通约）。",
       "State the applicable scale — an assessment at the individual scale cannot be directly applied "
       "at the organizational scale (Canon Axiom Three: multi-scale meanings are incommensurable).")
label(doc, "【证据等级】", "[Evidence Level]")
body(doc, "测量工具 E2（量表信效度验证中）；PE 动态模型 E1（H4 势能驱动行动假说）。",
     "Measurement instruments E2 (scale reliability and validity under validation); the dynamic PE "
     "model E1 (hypothesis H4, potential drives action).")
label(doc, "【常见误区】", "[Common Misconception]")
bullet(doc, "把「我相信」当作证据等级。",
       "Treating \"I believe it\" as an evidence level.")
bullet(doc, "违反公理三，把多尺度意义简单加权求和——正典明确：协调不是加权求和。",
       "Violating Axiom Three by simply weighting and summing meanings across scales — the canon "
       "states explicitly that coordination is not weighted summation.")
label(doc, "【与相邻层的关系】", "[Relation to Adjacent Layers]")
body(doc, "L4 给出强度，但强度高不等于方向对；方向由 L5 决定。",
     "L4 yields strength, but high strength does not mean the direction is right; direction is settled at L5.")

# ---- L5
h(doc, "第五层　方向选择", "Layer 5  Direction Selection", size=15)
label(doc, "【本层追问】", "[Core Question]")
body(doc, "在多个都「有价值」的方向中，选哪一个？",
     "Among several directions that all have value, which one to choose?")
label(doc, "【定义】", "[Definition]")
body(doc,
     "在五尺度框架下选定一个方向并显式承担其代价，同时输出该选择的修正触发条件。",
     "To select one direction within the five-scale framework while explicitly bearing its cost, and "
     "to output the correction triggers for that choice.")
label(doc, "【理论锚点】", "[Theoretical Anchor]")
body(doc, "正典第4章五尺度导航（个人／组织／城市／国家／人类）；DC 方向一致性指标；三级修正机制。",
     "Canon Chapter 4, five-scale navigation (individual / organizational / urban / national / "
     "humanity); the DC direction-consistency indicator; the three-level correction mechanism.")
label(doc, "【操作】", "[Practice]")
bullet(doc, "五尺度检查：该方向在个人、组织、城市、国家、人类五个尺度上，哪些一致、哪些冲突？",
       "Five-scale check: at which of the individual, organizational, urban, national, and human "
       "scales is this direction consistent, and at which does it conflict?")
bullet(doc, "冲突不可加权求和，须回到元意义层递归校准（正典 4.3）。",
       "Conflicts cannot be resolved by weighted summation; they must return to the meta-meaning "
       "level for recursive calibration (Canon §4.3).")
bullet(doc, "输出「方向声明＋预先声明的偏离阈值」：一级修正 <10%，二级修正 10–30%，三级修正 >30%。",
       "Output a direction statement plus pre-declared deviation thresholds: level-one correction "
       "<10%, level-two 10–30%, level-three >30%.")
bullet(doc, "设定自动失效日期，防止方向因惯性而长期未经检验。",
       "Set an automatic expiry date so that a direction is not left untested for long out of inertia.")
label(doc, "【证据等级】", "[Evidence Level]")
body(doc, "E1（H7 跨尺度一致性-生存假说；H8 尺度背离-危机假说）。",
     "E1 (hypothesis H7, cross-scale consistency and survival; hypothesis H8, scale divergence and crisis).")
label(doc, "【常见误区】", "[Common Misconception]")
bullet(doc, "把「共识」当「方向」。共识是分布，方向是承诺。",
       "Mistaking consensus for direction. Consensus is a distribution; direction is a commitment.")
bullet(doc, "把方向选择当成一次性决定——它是持续校准的过程。",
       "Treating direction selection as a one-off decision — it is an ongoing calibration.")
label(doc, "【与相邻层的关系】", "[Relation to Adjacent Layers]")
body(doc, "L5 的输出必然产生新的不确定性，交给 L6 审视。",
     "The output of L5 necessarily produces new uncertainty, which is handed to L6 for review.")

# ---- L6
h(doc, "第六层　反思与审视递归", "Layer 6  Recursive Reflection and Review", size=15)
label(doc, "【本层追问】", "[Core Question]")
body(doc, "谁来审视审视者？",
     "Who reviews the reviewer?")
label(doc, "【定义】", "[Definition]")
body(doc,
     "系统对自身的意义判断过程进行再判断，包括对判断框架本身的审查、周期性归零与重构。"
     "这是六层栈的闭合环节，也是「元」字的落点。",
     "The system re-judges its own meaning-judgment process, including review of the judging framework "
     "itself, and periodic zeroing and reconstruction. This is the closing link of the six-layer stack "
     "and where the word \"meta\" lands.")
label(doc, "【理论锚点】", "[Theoretical Anchor]")
body(doc,
     "正典三特性：MCA 元认知觉察、SA 螺旋上升、AZ 主动归零；F1–F4 四流程的元认知部署；"
     "理论失败矩阵；H12 归零防僵化、H13 元认知-判断质量、H14 无归零-僵化。",
     "Canon three properties: MCA (metacognitive awareness), SA (spiral ascent), AZ (active zeroing); "
     "the metacognitive deployment of processes F1–F4; the Theory Failure Matrix; H12 (zeroing prevents "
     "ossification), H13 (metacognition improves judgment quality), H14 (no zeroing leads to ossification).")
label(doc, "【操作】", "[Practice]")
bullet(doc, "元认知觉察：在 M1／M2／M3 与 F1–F4 的每个环节加入「我为何这样判断」的显式陈述。",
       "Metacognitive awareness: add an explicit statement of \"why I judge this way\" at every step of "
       "M1 / M2 / M3 and F1–F4.")
bullet(doc, "螺旋回环：比较本轮与上轮的意义深度增量 SD，而不是比较绝对水平。",
       "Spiral looping: compare the meaning-depth increment SD against the previous cycle rather than "
       "comparing absolute levels.")
bullet(doc, "主动归零：设置周期性重置（个人年度、组织按需）；归零前先过「归零安全检查清单」（正典工具 A.10）。",
       "Active zeroing: set a periodic reset (annually for individuals, on demand for organizations); "
       "before zeroing, pass the Zeroing Safety Checklist (Canon Tool A.10).")
bullet(doc, "失败矩阵自查：本层所依赖的假设若被证伪，应触发哪一级修正？",
       "Failure-matrix self-check: if an assumption this layer depends on is falsified, which level of "
       "correction should it trigger?")
bullet(doc, "递归闭合：把 L6 的产出（更新后的元意义理解）回写为 L1 的输入标准。",
       "Recursive closure: write the output of L6 — the updated meta-meaning understanding — back as "
       "the input criteria of L1.")
label(doc, "【证据等级】", "[Evidence Level]")
body(doc, "E2（案例支持：主动归零防僵化、元认知训练提升判断质量；随机对照实验进行中）。",
     "E2 (case-supported: zeroing prevents ossification, metacognitive training improves judgment "
     "quality; randomized controlled trials in progress).")
label(doc, "【常见误区】", "[Common Misconception]")
bullet(doc, "过度元认知导致决策瘫痪——这是正典明确列出的边界之一。",
       "Excessive metacognition causing decision paralysis — one of the boundaries explicitly listed in the canon.")
bullet(doc, "把归零当成「推倒重来」。归零是有控制的重置，不是放弃；正典以 H12／H14 区分「主动归零」与「无归零僵化」。",
       "Treating zeroing as starting over from scratch. Zeroing is a controlled reset, not abandonment; "
       "the canon distinguishes active zeroing from zeroing-free ossification via H12 / H14.")
label(doc, "【与相邻层的关系】", "[Relation to Adjacent Layers]")
body(doc, "L6 是唯一会改写前五层前提的一层。",
     "L6 is the only layer that rewrites the premises of the five layers below it.")

# ================================================================ 协同
h(doc, "六层如何协同：三条闭环", "How the Six Layers Work Together: Three Loops", size=17)
body(doc,
     "六层不是六道串行工序，而是三条闭环叠加。闭环的意义在于：任何一环失败，都应回到闭环内的上游，"
     "而不是把问题推给下一层。",
     "The six layers are not six serial steps but the superposition of three loops. The point of a loop "
     "is that if any link fails, work returns to an upstream point inside the same loop rather than "
     "pushing the problem downstream.")
table(doc,
      ["闭环", "路径", "触发条件", "回到哪一层"],
      [["认知闭环", "L1 → L2 → L1", "减负后的材料无法被交互化呈现", "L1（判断是否降维过度）"],
       ["意义闭环", "L3 → L4 → L5 → L3", "生成的意义结构无法通过证据评估", "L3（重组，而非硬推）"],
       ["元闭环", "L6 → L1", "完成一轮螺旋，元意义理解已更新", "L1（重置输入标准）"]],
      widths=[2.2, 3.6, 5.4, 3.4],
      caption="表 3　三条闭环", caption_en="Table 3  The Three Loops")

# ================================================================ 五尺度
h(doc, "五尺度部署", "Deployment Across the Five Scales", size=17)
body(doc,
     "正典第4章指出，每个尺度有不可还原的意义逻辑：个人的意义不是组织的意义的缩小版，反之亦然。"
     "因此六层在五个尺度上的主要形态并不相同。下表给出典型形态与正典工具对应。",
     "Canon Chapter 4 holds that each scale has an irreducible logic of meaning: individual meaning is "
     "not a scaled-down version of organizational meaning, and vice versa. The six layers therefore "
     "take different primary forms across the five scales. The table below gives typical forms and the "
     "corresponding canon tools.")
table(doc,
      ["尺度", "L1–L2 主要形态", "L3–L4 主要形态", "L5–L6 主要形态", "对应工具（正典附录A）"],
      [["个人", "个人阅读降维、可丢弃微应用", "意义自检、证据标注", "年度归零、螺旋追踪", "A.1 / A.2 / A.3"],
       ["组织", "汇报与文档受控化、仪表盘", "使命合法性评估", "使命压力测试、方向重置", "A.4 / A.5 / A.6"],
       ["城市", "公共信息可读化、参与式界面", "地方感与集体记忆评估", "城市归零工作坊", "A.7 / A.8"],
       ["国家", "政策文本可读化", "制度意义一致性评估", "跨尺度方向校准", "（A.9 跨尺度）"],
       ["人类", "文明叙事降维", "物种责任与文明方向评估", "文明级归零-螺旋治理", "（A.9 跨尺度）"]],
      widths=[1.5, 4.0, 3.4, 3.4, 3.1],
      caption="表 4　五尺度 × 六层的典型形态", caption_en="Table 4  Typical Forms of the Six Layers Across Five Scales")
note(doc,
     "正典路线图的第一阶段（当下至 2030 年）为「认知普及与工具孵化」，主要产出为专著与个人版工具。"
     "本白皮书与 MSI 实现均定位在该阶段。",
     "The first phase of the canon roadmap (now to 2030) is \"cognitive popularization and tool "
     "incubation\", whose main outputs are the monograph and individual-scale tools. This white paper "
     "and the MSI implementation both sit in that phase.")

# ================================================================ 证据与边界
h(doc, "证据、失败与边界", "Evidence, Failure, and Boundaries", size=17)
label(doc, "一、六层证据等级一览", "[Evidence Levels at a Glance]")
table(doc,
      ["层", "本框架证据等级", "底层机制证据", "当前状态"],
      [["L1 减负", "E1", "E3–E4", "机制成熟，框架内操作化待测"],
       ["L2 可体验", "E1", "E3", "机制成熟，框架内操作化待测"],
       ["L3 意义生成", "E0–E1", "E0", "构念已定义并形式化"],
       ["L4 价值评估", "E2（工具）/ E1（模型）", "E1–E2", "量表信效度验证中"],
       ["L5 方向选择", "E1", "E1", "假设 H7／H8 待检验"],
       ["L6 反思与审视递归", "E2", "E2", "案例支持，RCT 进行中"],
       ["六层栈本身", "E0", "—", "本白皮书提出的整合结构，未经独立检验"]],
      widths=[3.0, 3.6, 2.8, 6.0],
      caption="表 5　证据等级一览", caption_en="Table 5  Evidence Levels at a Glance")

label(doc, "二、失败矩阵：六层版的证伪条件", "[Failure Matrix: Falsification Conditions per Layer]")
body(doc,
     "沿用正典「理论失败矩阵」的体例：每一层给出支持证据、部分支持、失败阈值与失败后操作。"
     "任何一层触及失败阈值，该层将在后续版本中被标记或删除。",
     "Following the canon's Theory Failure Matrix: each layer states supporting evidence, partial "
     "support, the failure threshold, and the operation after failure. If any layer reaches its "
     "failure threshold, that layer will be marked or removed in a later version.")
table(doc,
      ["层", "支持证据", "部分支持", "失败阈值", "失败后操作"],
      [["L1 减负", "受控语言降低误读率", "特定文本类型有效", "降维后决策质量无提升（d<0.3）", "重设压缩比或放弃字数硬限"],
       ["L2 可体验", "交互提升结构回忆", "特定概念类型有效", "交互组与静态组无显著差异", "降为可选增强，不作必需层"],
       ["L3 意义生成", "三维度可被独立评分", "特定文化背景下成立", "意义判断方差被单一维度解释>90%", "接受 H2 被证伪，重构结构模型"],
       ["L4 价值评估", "证据标注提升判断一致性", "领域专家群体内有效", "标注与判断质量无相关", "退回定性评估"],
       ["L5 方向选择", "跨尺度一致者生存更久", "特定尺度组合成立", "长期背离却无危机（H8 反例）", "标记 H8 被证伪，重估五尺度模型"],
       ["L6 反思与审视递归", "归零缓解僵化", "案例层面成立", "RCT 无显著差异（d<0.3）", "放弃有效性主张，仅保留为操作规程"]],
      widths=[2.4, 3.2, 2.9, 4.0, 3.0],
      caption="表 6　六层失败矩阵", caption_en="Table 6  Six-Layer Failure Matrix")

label(doc, "三、边界", "[Boundaries]")
bullet(doc, "不适用于无主体系统。纯物理系统不适用。",
       "Not applicable to subject-less systems. Purely physical systems are out of scope.")
bullet(doc, "不能替代领域专业知识。本框架提供方向性判断，不替代医学、工程等专业判断。",
       "It cannot replace domain expertise. The framework offers directional judgment and does not "
       "replace medical, engineering, or other professional judgment.")
bullet(doc, "不承诺「正确答案」。它提供「更值得的方向」，而不是唯一答案。",
       "It promises no \"correct answer\". It offers a more worth-going direction, not a unique answer.")
bullet(doc, "文化敏感性。具体操作需适配文化背景。",
       "Cultural sensitivity. Concrete practices must be adapted to cultural context.")
bullet(doc, "元认知的限度。过度元认知可导致决策瘫痪。",
       "Limits of metacognition. Excessive metacognition can cause decision paralysis.")
bullet(doc, "本白皮书新增的边界：六层栈本身是 E0 结构，其分层方式可能被证明不是最优切分。"
            "若出现更简洁且解释力更强的切分，应替换而非辩护。",
       "A boundary added by this white paper: the six-layer stack itself is an E0 structure, and its "
       "partition may prove not to be the optimal cut. If a simpler partition with greater explanatory "
       "power emerges, it should replace this one rather than be defended.")

# ================================================================ 如何开始
h(doc, "如何开始", "Getting Started", size=17)
label(doc, "个人版：今天就能做的四步", "[Individual: Four Steps You Can Take Today]")
bullet(doc, "选一个你最近没搞懂的概念，先只做 L1：压到 300 字以内，并写出「待决问题」清单。",
       "Pick a concept you have recently failed to understand and do only L1: compress it under 300 "
       "characters/words and write the \"open questions\" list.")
bullet(doc, "为它做一个可交互的最小产物，暴露一个可改变的参数（L2）。",
       "Build a minimal interactive artifact for it that exposes one changeable parameter (L2).")
bullet(doc, "按方向／价值／边界三问写出候选意义，并给每条标注证据等级与证伪条件（L3–L4）。",
       "Write candidate meanings using the direction / value / boundary questions, and label each with "
       "an evidence level and a falsification condition (L3–L4).")
bullet(doc, "设定一个归零日期，写下「到期时我凭什么判断这个方向仍然成立」（L5–L6）。",
       "Set a zeroing date and write down \"on that date, on what grounds would I judge this direction "
       "still holds\" (L5–L6).")
label(doc, "组织版：本季度", "[Organizational: This Quarter]")
bullet(doc, "选一个正在推进的方向，做一次完整五尺度检查，并显式写出各级偏离阈值。",
       "Take one direction currently being pursued, run a full five-scale check, and write out the "
       "deviation thresholds at each level.")
bullet(doc, "把「使命压力测试」与「组织归零协议」（A.4／A.5）纳入季度节奏。",
       "Bring the Mission Stress Test and the Organizational Zeroing Protocol (A.4 / A.5) into the "
       "quarterly rhythm.")
bullet(doc, "建立一张失败矩阵看板：把本组织依赖的关键假设及其证伪条件写在墙上。",
       "Build a failure-matrix board: write the key assumptions the organization relies on, together "
       "with their falsification conditions, on the wall.")

# ================================================================ Claim Registry 摘要
h(doc, "Claim Registry 摘要", "Claim Registry — Summary", size=17)
note(doc,
     "每个理论主张在此有一个唯一 ID。论文、网站、实验、工具都应引用 claim ID（如 MI-C003），"
     "而非笼统引用「L6」或「六层栈」。完整版（含测试方式与失败条件）见仓库 docs/claims.md。",
     "Every theoretical claim has a unique ID here. Papers, websites, experiments, and tools should "
     "reference the claim ID (e.g., MI-C003), not loosely reference L6 or the six-layer stack. "
     "The full version with test methods and falsification criteria lives at docs/claims.md in the repository.")

table(doc,
      ["ID", "陈述（摘要）", "证据", "状态"],
      [["MI-C001", "意义智能是对其他智能活动的方向性调控", "E1", "Formalized"],
       ["MI-C002", "意义智能是元层，不与 IQ/EQ/SQ 并列", "E1", "Formalized"],
       ["MI-C003", "意义判断可分解为方向·价值·边界", "E0–E1", "Formalized"],
       ["MI-C004", "意义沿一条连续光谱带分布，而非离散层次", "E0", "Draft"],
       ["MI-C005", "多尺度意义不可通约，协调不是加权求和", "E1", "Formalized"],
       ["MI-C006", "递归审视改善长期决策质量", "E2", "Under Test"],
       ["MI-C007", "六层栈是一种有效的操作性表示", "E0", "Draft"],
       ["MI-C008", "减负改善决策质量（相对纯信息呈现）", "E1", "Under Test"],
       ["MI-C009", "可体验（交互）提升结构回忆", "E1", "Under Test"],
       ["MI-C010", "跨尺度一致性预测系统生存", "E1", "Under Test"],
       ["MI-C011", "主动归零缓解长期僵化", "E2", "Under Test"],
       ["MI-C012", "无归零导致僵化", "E1", "Formalized"]],
      widths=[1.8, 7.5, 1.5, 2.2],
      caption="表 8　Claim Registry 摘要", caption_en="Table 8  Claim Registry — Summary")

note(doc,
     "六层栈本身是 E0 结构——由本项目提出的整合框架，未经独立检验。若出现更简洁且解释力更强的切分，"
     "应当替换它，而不是为它辩护。",
     "The six-layer stack itself is an E0 structure — an integrative framework proposed by this project, "
     "not independently tested. If a simpler partition with greater explanatory power emerges, it should "
     "replace this one rather than be defended.")

# ================================================================ 术语
h(doc, "术语对照", "Glossary", size=17)
table(doc,
      ["中文", "English", "出处"],
      [["意义智能", "Meaning Intelligence (MI)", "正典 1.3"],
       ["元智能", "Meta-Intelligence", "正典 1.3"],
       ["意义势能", "Meaning Potential (PE)", "正典 3.3"],
       ["方向一致性", "Direction Consistency (DC)", "正典附录B"],
       ["系缚强度", "Binding Strength (BS)", "正典附录B"],
       ["螺旋深度", "Spiral Depth (SD)", "正典附录B"],
       ["归零准备度", "Zeroing Readiness (RZ)", "正典附录B"],
       ["意义清晰度", "Meaning Clarity (MC)", "正典附录B"],
       ["元认知觉察", "Metacognitive Awareness (MCA)", "正典 7B.2"],
       ["螺旋上升", "Spiral Ascent (SA)", "正典 7B.3"],
       ["主动归零", "Active Zeroing (AZ)", "正典 7B.4"],
       ["理论失败矩阵", "Theory Failure Matrix", "正典附录D"],
       ["证据等级", "Evidence Level (E0–E6)", "正典绪论 / 第6章"]],
      widths=[4.0, 6.0, 4.0],
      caption="表 7　术语对照表", caption_en="Table 7  Glossary")

p = para(doc, spacing=1.35, before=18, after=4)
set_font(p.add_run("本白皮书为公开发布文档，可自由传播。理论引用请以正典 "
                   "《意义智能：意义文明的认知操作系统》V7.0 为准。"),
         9.5, SECOND, False, SONG, LATIN_B)
p = para(doc, spacing=1.3, after=4)
set_font(p.add_run("This white paper is a public release document and may be freely distributed. "
                   "For theoretical citation, please refer to the canonical text, Meaning "
                   "Intelligence: The Cognitive Operating System of Meaning Civilization, V7.0."),
         9, GRAY, False, SONG, LATIN_B)

doc.save(OUT)
print("已生成：", OUT)
print("段落数：", len(doc.paragraphs), " 表格数：", len(doc.tables))
