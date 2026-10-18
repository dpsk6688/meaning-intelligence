"""向 whitepaper/make_figures.py 追加 fig_boundary() 函数。
不重写现有代码,只在 main 块之前插入新函数,并更新 main 调用。"""
from pathlib import Path

p = Path("whitepaper/make_figures.py")
text = p.read_text(encoding="utf-8")

# 幂等检查
if "def fig_boundary" in text:
    print("⚠️ fig_boundary 已存在,跳过")
    raise SystemExit(0)

NEW_FUNC = '''

# ---------------------------------------------------------------- 图 3
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

    f_center = F(HEI, 92)
    f_centerzh = F(YAHEI, 30)
    f_ring = F(HEI, 28)
    f_ringen = F(GEO, 20)
    f_legzh = F(HEI, 26)
    f_legen = F(GEO, 18)
    f_note = F(YAHEI, 22)
    f_noteen = F(GEO, 18)
    f_hdr = F(HEI, 30)
    f_hdren = F(GEO, 22)

    # 同心圆圆心 (偏左,右侧留空间放图例)
    cx, cy = 560, 540

    r_mit = 165
    r_par = 320
    r_adj = 465

    # 从外到内绘制三个环
    # 外环:邻接场域
    d.ellipse((cx - r_adj, cy - r_adj, cx + r_adj, cy + r_adj),
              fill=tint(SPECTRAL_GOLD, 0.09),
              outline=tint(SPECTRAL_GOLD, 0.55), width=3)
    # 中环:平行能力
    d.ellipse((cx - r_par, cy - r_par, cx + r_par, cy + r_par),
              fill=tint(SPECTRAL_PURPLE, 0.11),
              outline=tint(SPECTRAL_PURPLE, 0.55), width=3)
    # 内环:MIT
    d.ellipse((cx - r_mit, cy - r_mit, cx + r_mit, cy + r_mit),
              fill=tint(SPECTRAL_BLUE, 0.16),
              outline=tint(SPECTRAL_BLUE, 0.72), width=4)

    # 圆心文字
    d.text((cx, cy - 34), "MIT", font=f_center, fill=NAVY, anchor="mm")
    d.text((cx, cy + 44), "方向性调控", font=f_centerzh, fill=NAVY, anchor="mm")

    # 内环与中环之间的环带标签(顶部)
    mid_par = (r_mit + r_par) // 2
    d.text((cx, cy - mid_par - 18), "IQ · EQ · SQ", font=f_ring, fill=NAVY, anchor="mm")
    d.text((cx, cy - mid_par + 22), "Parallel capabilities", font=f_ringen, fill=GRAY, anchor="mm")

    # 中环与外环之间的环带标签(顶部)
    mid_adj = (r_par + r_adj) // 2
    d.text((cx, cy - mid_adj - 18), "Adjacent Fields", font=f_ring, fill=NAVY, anchor="mm")
    d.text((cx, cy - mid_adj + 22), "邻接场域", font=f_ringen, fill=GRAY, anchor="mm")

    # =================================================== 右侧图例
    lx = 1120
    ly = 120

    d.text((lx, ly), "邻接场域 · Adjacent Fields", font=f_hdr, fill=NAVY)
    d.text((lx, ly + 38), "与 MIT 相邻,但不是同一构造", font=f_hdren, fill=GRAY)
    d.line([(lx, ly + 76), (lx + 560, ly + 76)], fill=GRAY, width=2)

    ly += 110
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
        d.text((lx + 34, ly - 2), name, font=f_legzh, fill=NAVY)
        d.text((lx + 34, ly + 34), zh, font=f_legen, fill=SECOND)
        d.text((lx + 34, ly + 60), en, font=f_legen, fill=GRAY)
        ly += 116

    # =================================================== 环层图例
    ly += 8
    d.text((lx, ly), "环层图例 · Ring legend", font=f_hdr, fill=NAVY)
    d.line([(lx, ly + 40), (lx + 560, ly + 40)], fill=GRAY, width=2)
    ly += 64

    RINGS = [
        (SPECTRAL_BLUE, "MIT — 元层", "Directional regulation"),
        (SPECTRAL_PURPLE, "IQ · EQ · SQ", "Parallel capabilities, constrained by MIT"),
        (SPECTRAL_GOLD, "Adjacent fields", "Adjacent but distinct constructs"),
    ]
    for col, zh, en in RINGS:
        d.ellipse((lx, ly + 4, lx + 22, ly + 26), fill=col)
        d.text((lx + 40, ly - 4), zh, font=f_legzh, fill=NAVY)
        d.text((lx + 40, ly + 32), en, font=f_legen, fill=GRAY)
        ly += 88

    # =================================================== 底部图注
    d.text((60, H - 62),
           "MIT 是元层:对 IQ/EQ/SQ 约束方向,与邻接场域并列但不同构造。",
           font=f_note, fill=SECOND)
    d.text((60, H - 32),
           "MIT sits above parallel capabilities and is distinct from adjacent fields — a meta-layer, not a substitute.",
           font=f_noteen, fill=GRAY)

    img.save(OUT / "fig3_construct_boundary.png", dpi=(300, 300))
    print("saved", OUT / "fig3_construct_boundary.png", img.size)
'''

OLD_MAIN = '''if __name__ == "__main__":
    fig_stack()
    fig_spiral()'''

NEW_MAIN = '''if __name__ == "__main__":
    fig_stack()
    fig_spiral()
    fig_boundary()'''

if OLD_MAIN not in text:
    print("❌ 找不到预期的 main 块,请人工检查 make_figures.py")
    raise SystemExit(1)

text = text.replace(OLD_MAIN, NEW_FUNC + "\n\n" + NEW_MAIN)
p.write_text(text, encoding="utf-8")
print("✅ 已追加 fig_boundary(),main 块已更新")