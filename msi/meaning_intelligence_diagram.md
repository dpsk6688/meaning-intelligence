# 意义智能 (Meaning Intelligence) — zh

## 1. 六层应用栈

```mermaid
flowchart LR
    subgraph B0["界面带 · 信息进不来"]
        direction LR
        L1["L1 · 减负<br/>把认知负荷从信息量转移到结构<br/>E1(机制 E3)"]:::cyan
        L2["L2 · 可体验<br/>把「读到」变成「操作到」<br/>E1(机制 E3)"]:::cyan
    end
    subgraph B1["加工带 · 意义出不来"]
        direction LR
        L3["L3 · 意义生成<br/>组织成方向·价值·边界<br/>E0–E1"]:::purple
        L4["L4 · 价值评估<br/>为判断标注证据强度<br/>E2(工具)/ E1(模型)"]:::purple
    end
    subgraph B2["元带 · 方向守不住"]
        direction LR
        L5["L5 · 方向选择<br/>在五尺度上选定值得的方向<br/>E1"]:::amber
        L6["L6 · 反思与审视递归<br/>让系统审视自己的审视<br/>E2(案例)/ E1"]:::amber
    end
    L1 --> L2 --> L3 --> L4 --> L5 --> L6
    L6 -. "L1′" .-> L1
    classDef gray fill:#141820,stroke:#8b95a5,stroke-dasharray:4 3,color:#8b95a5
    classDef cyan fill:#0a1a20,stroke:#00e5ff,color:#00e5ff
    classDef purple fill:#150e26,stroke:#bb86fc,color:#bb86fc
    classDef amber fill:#241c08,stroke:#ffd166,color:#ffd166
    classDef white fill:#0a0c10,stroke:#ffffff,stroke-width:2px,color:#ffffff
```

## 2. 场景结构

```mermaid
flowchart TD
    N0["L1 · 信息洪流<br/>信息过载:45 条随机文本"]:::gray
    N1["L1 · 文本降维<br/>汇聚为一点 → 提炼三条核心语句"]:::cyan
    N2["L1 · 结构图<br/>转换为节点与箭头图"]:::cyan
    N3["L2 · 可操作界面<br/>浏览器窗口 + 滑块拖动"]:::cyan
    N4["L3 · 意义归位<br/>散点节点归位到方向·价值·边界三角"]:::purple
    N5["L4 · 证据着色<br/>每个节点套上证据色环(示意)"]:::purple
    N6["L5 · 路径选择<br/>三条候选路径,两条淡出,一条高亮"]:::amber
    N7["L6 · 递归螺旋<br/>螺旋回写至同角度的更高起点 L1′,监督之眼审视整圈"]:::amber
    N8["Meaning Intelligence<br/>渐变标题落幕"]:::white
    N0 --> N1 --> N2 --> N3 --> N4 --> N5 --> N6 --> N7 --> N8
    classDef gray fill:#141820,stroke:#8b95a5,stroke-dasharray:4 3,color:#8b95a5
    classDef cyan fill:#0a1a20,stroke:#00e5ff,color:#00e5ff
    classDef purple fill:#150e26,stroke:#bb86fc,color:#bb86fc
    classDef amber fill:#241c08,stroke:#ffd166,color:#ffd166
    classDef white fill:#0a0c10,stroke:#ffffff,stroke-width:2px,color:#ffffff
```

## 3. 视觉编码规范

```mermaid
flowchart LR
    P0["gray #8b95a5<br/>噪声 / 原始信息"]:::gray
    P1["cyan #00e5ff<br/>界面带 · L1–L2"]:::cyan
    P2["purple #bb86fc<br/>加工带 · L3–L4"]:::purple
    P3["amber #ffd166<br/>元带 · L5–L6"]:::amber
    P4["E0 → E6<br/>#5b6472 #ffd166"]:::white
    P0 --> P1 --> P2 --> P3 --> P4
    classDef gray fill:#141820,stroke:#8b95a5,stroke-dasharray:4 3,color:#8b95a5
    classDef cyan fill:#0a1a20,stroke:#00e5ff,color:#00e5ff
    classDef purple fill:#150e26,stroke:#bb86fc,color:#bb86fc
    classDef amber fill:#241c08,stroke:#ffd166,color:#ffd166
    classDef white fill:#0a0c10,stroke:#ffffff,stroke-width:2px,color:#ffffff
```

# Meaning Intelligence — en

## 1. Six-layer stack

```mermaid
flowchart LR
    subgraph B0["Interface band · Information can't get in"]
        direction LR
        L1["L1 · Cognitive Load Reduction<br/>Shift cognitive load from information volume to structure<br/>E1(机制 E3)"]:::cyan
        L2["L2 · Experiential Rendering<br/>Turn "read" into "operated"<br/>E1(机制 E3)"]:::cyan
    end
    subgraph B1["Processing band · Meaning can't come out"]
        direction LR
        L3["L3 · Meaning Generation<br/>Organise into direction · value · boundary<br/>E0–E1"]:::purple
        L4["L4 · Value Assessment<br/>Label every judgement with its strength of evidence<br/>E2(工具)/ E1(模型)"]:::purple
    end
    subgraph B2["Meta band · Direction can't hold"]
        direction LR
        L5["L5 · Direction Selection<br/>Choose the worthwhile direction across five scales<br/>E1"]:::amber
        L6["L6 · Recursive Reflection and Review<br/>Let the system review its own reviewing<br/>E2(案例)/ E1"]:::amber
    end
    L1 --> L2 --> L3 --> L4 --> L5 --> L6
    L6 -. "L1′" .-> L1
    classDef gray fill:#141820,stroke:#8b95a5,stroke-dasharray:4 3,color:#8b95a5
    classDef cyan fill:#0a1a20,stroke:#00e5ff,color:#00e5ff
    classDef purple fill:#150e26,stroke:#bb86fc,color:#bb86fc
    classDef amber fill:#241c08,stroke:#ffd166,color:#ffd166
    classDef white fill:#0a0c10,stroke:#ffffff,stroke-width:2px,color:#ffffff
```

## 2. Scene structure

```mermaid
flowchart TD
    N0["L1 · Information Overload<br/>Overload: 45 random text fragments"]:::gray
    N1["L1 · Text Reduction<br/>Collapse to a point → three core statements"]:::cyan
    N2["L1 · Structure Diagram<br/>Converted to a node-and-arrow graph"]:::cyan
    N3["L2 · Operable Interface<br/>Browser window + slider drag"]:::cyan
    N4["L3 · Meaning Placement<br/>Scattered nodes settle into the direction·value·boundary triangle"]:::purple
    N5["L4 · Evidence Rings<br/>Each node gets an evidence ring (illustrative)"]:::purple
    N6["L5 · Path Selection<br/>Three candidate paths: two fade, one is highlighted"]:::amber
    N7["L6 · Recursive Spiral<br/>Spiral returns to a higher start L1′ at the same angle; the eye reviews the whole loop"]:::amber
    N8["Meaning Intelligence<br/>Gradient title card"]:::white
    N0 --> N1 --> N2 --> N3 --> N4 --> N5 --> N6 --> N7 --> N8
    classDef gray fill:#141820,stroke:#8b95a5,stroke-dasharray:4 3,color:#8b95a5
    classDef cyan fill:#0a1a20,stroke:#00e5ff,color:#00e5ff
    classDef purple fill:#150e26,stroke:#bb86fc,color:#bb86fc
    classDef amber fill:#241c08,stroke:#ffd166,color:#ffd166
    classDef white fill:#0a0c10,stroke:#ffffff,stroke-width:2px,color:#ffffff
```

## 3. Visual encoding

```mermaid
flowchart LR
    P0["gray #8b95a5<br/>Noise / raw information"]:::gray
    P1["cyan #00e5ff<br/>Interface band · L1–L2"]:::cyan
    P2["purple #bb86fc<br/>Processing band · L3–L4"]:::purple
    P3["amber #ffd166<br/>Meta band · L5–L6"]:::amber
    P4["E0 → E6<br/>#5b6472 #ffd166"]:::white
    P0 --> P1 --> P2 --> P3 --> P4
    classDef gray fill:#141820,stroke:#8b95a5,stroke-dasharray:4 3,color:#8b95a5
    classDef cyan fill:#0a1a20,stroke:#00e5ff,color:#00e5ff
    classDef purple fill:#150e26,stroke:#bb86fc,color:#bb86fc
    classDef amber fill:#241c08,stroke:#ffd166,color:#ffd166
    classDef white fill:#0a0c10,stroke:#ffffff,stroke-width:2px,color:#ffffff
```
