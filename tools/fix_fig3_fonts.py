"""修复 fig3:所有中文改用中文字体,不再误用 Georgia 拉丁字体。"""
from pathlib import Path

p = Path("whitepaper/make_figures.py")
text = p.read_text(encoding="utf-8")

# 定位 fig_boundary 函数体
START = "# ---------------------------------------------------------------- 图 3"
END = 'if __name__ == "__main__":'

start_idx = text.find(START)
end_idx = text.find(END)
if start_idx < 0 or end_idx < 0:
    print("❌ 找不到 fig_boundary 的起止标记")
    raise SystemExit(1)

# 提取需要替换的区间
head = text[:start_idx]
tail = text[end_idx:]

NEW_FUNC = '''# ---------------------------------------------------------------- 图 3
def fig_boundary():
    """构造边界图:MIT 是元层,与邻接场域不是同一构造。

    三同心环:
      内环 (蓝)   MIT — 对智能活动的方向性调控
      中环 (紫)   IQ / EQ / SQ — 平行能力,被元层约束
      外环 (金)   Semantic / Decision / Metacognitive / Alignment / Wisdom
    """
    W, H = 1740, 1110
    img = Image.new("RGB", (W, H), PARCHMENT)
    d = ImageDraw.Draw(img)

    # 中文 / 英文分别声明字体,避免 Georgia 渲染中文变方块
    # 中文专用
    f_centerzh = F(YAHEI, 30)      # 圆心副标题
    f_zh_sm = F(YAHEI, 20)         # 图例中文小字
    f_zh_md = F(HEI, 26)           # 图例中文标题
    f_zh_hdr = F(HEI, 30)          # 段落主标题
    f_notezh = F(YAHEI, 22)        # 底部图注中文
    # 英文专用
    f_center = F(HEI, 92)          # MIT
    f_ringen = F(GEO, 20)          # 环带英文标签
    f_ringen_title = F(HEI, 28)    # 环带英文主标题
    f_legen = F(GEO, 18)           # 图例英文
    f_hdren = F(GEO, 22)           # 段落英文副标题
    f_noteen = F(GEO, 18)          # 底部图注英文

    # 同心圆圆心 (偏左,右侧留空间放图例)
    cx, cy = 560, 540
    r_mit = 165
    r_par = 320
    r_adj = 465

    # 从外到内绘制三个环
    d.ellipse((cx - r_adj, cy - r_adj, cx + r_adj, cy + r_adj),
              fill=tint(SPECTRAL_GOLD, 0.09),
              outline=tint(SPECTRAL_GOLD, 0.55), width=3)
    d.ellipse((cx - r_par, cy - r_par, cx + r_par, cy + r_par),
              fill=tint(SPECTRAL_PURPLE, 0.11),
              outline=tint(SPECTRAL_PURPLE, 0.55), width=3)
    d.ellipse((cx - r_mit, cy - r_mit, cx + r_mit, cy + r_mit),
              fill=tint(SPECTRAL_BLUE, 0.16),
              outline=tint(SPECTRAL_BLUE, 0.72), width=4)

    # 圆心文字 (MIT 用英文大号,副标题用中文)
    d.text((cx, cy - 34), "MIT", font=f_center, fill=NAVY, anchor="mm")
    d.text((cx, cy + 44), "方向性调控", font=f_centerzh, fill=NAVY, anchor="mm")

    # 中环环带标签(顶部) —— 英文
    mid_par = (r_mit + r_par) // 2
    d.text((cx, cy - mid_par - 18), "IQ · EQ · SQ", font=f_ringen_title,
           fill=NAVY, anchor="mm")
    d.text((cx, cy - mid_par + 22), "Parallel capabilities",
           font=f_ringen, fill=GRAY, anchor="mm")

    # 外环环带标签(顶部) —— 英文主 + 中文副(用中文字体!)
    mid_adj = (r_par + r_adj) // 2
    d.text((cx, cy - mid_adj - 18), "Adjacent Fields",
           font=f_ringen_title, fill=NAVY, anchor="mm")
    d.text((cx, cy - mid_adj + 22), "邻接场域",
           font=f_zh_sm, fill=GRAY, anchor="mm")

    # =================================================== 右侧图例
    lx = 1120
    ly = 120

    # 标题区 (主标题用中文字体,副标题用英文字体)
    d.text((lx, ly), "邻接场域 · Adjacent Fields",
           font=f_zh_hdr, fill=NAVY)
    d.text((lx, ly + 38), "与 MIT 相邻,但不是同一构造",
           font=f_zh_sm, fill=GRAY)
    d.text((lx, ly + 68), "Adjacent to MIT, but distinct constructs",
           font=f_hdren, fill=GRAY)
    d.line([(lx, ly + 106), (lx + 560, ly + 106)], fill=GRAY, width=2)

    ly += 140
    ADJ = [
        ("Semantic / Pragmatic", "语言中的上下文、意图、反讽",
         "Handles meaning in language; MIT handles direction."),
        ("Decision Intelligence", "从信息到决策的应用框架",
         "Application layer; MIT provides the meta-structure."),
        ("Metacognitive AI", "自我监控、资源分配、难度估计",
         "Adjacent to L6; L6 is one layer of the stack."),
        ("AI Alignment", "让 AI 行为符合人类价值",
         "MIT provides structure; does not replace alignment."),
        ("Wisdom / Judgment", "实践智慧、判断力传统",
         "MIT attempts to formalize them into testable structure."),
    ]
    for name, zh, en in ADJ:
        d.ellipse((lx, ly + 6, lx + 20, ly + 26), fill=SPECTRAL_GOLD)
        d.text((lx + 34, ly - 2), name, font=f_zh_md, fill=NAVY)     # 拉丁名,HEI 可显示
        d.text((lx + 34, ly + 34), zh, font=f_zh_sm, fill=SECOND)    # 中文,用中文字体
        d.text((lx + 34, ly + 60), en, font=f_legen, fill=GRAY)      # 英文,用拉丁字体
        ly += 116

    # =================================================== 环层图例
    ly += 20
    d.text((lx, ly), "环层图例 · Ring legend", font=f_zh_hdr, fill=NAVY)
    d.line([(lx, ly + 46), (lx + 560, ly + 46)], fill=GRAY, width=2)
    ly += 74

    RINGS = [
        (SPECTRAL_BLUE, "MIT — 元层", "Directional regulation"),
        (SPECTRAL_PURPLE, "IQ · EQ · SQ", "Parallel capabilities, constrained by MIT"),
        (SPECTRAL_GOLD, "邻接场域", "Adjacent but distinct constructs"),
    ]
    for col, zh, en in RINGS:
        d.ellipse((lx, ly + 4, lx + 22, ly + 26), fill=col)
        d.text((lx + 40, ly - 4), zh, font=f_zh_md, fill=NAVY)      # 中文,中文字体
        d.text((lx + 40, ly + 32), en, font=f_legen, fill=GRAY)     # 英文,拉丁字体
        ly += 88

    # =================================================== 底部图注
    d.text((60, H - 62),
           "MIT 是元层:对 IQ/EQ/SQ 约束方向,与邻接场域并列但不同构造。",
           font=f_notezh, fill=SECOND)
    d.text((60, H - 32),
           "MIT sits above parallel capabilities and is distinct from adjacent fields — a meta-layer, not a substitute.",
           font=f_noteen, fill=GRAY)

    img.save(OUT / "fig3_construct_boundary.png", dpi=(300, 300))
    print("saved", OUT / "fig3_construct_boundary.png", img.size)


'''

new_text = head + NEW_FUNC + tail
p.write_text(new_text, encoding="utf-8")
print("✅ fig_boundary() 已重写,所有中文改用中文字体")