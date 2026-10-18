# -*- coding: utf-8 -*-
"""生成白皮书插图：六层元智能栈 + 递归螺旋闭合。
配色沿用《意义智能》V7.0 视觉语言：
  书卷白 #F7F4EE / 阅读灰 #1F2937 / 标题深蓝 #1B3A5C / 辅助灰 #7A8CA3 / 次级 #4A5A70
  光谱蓝 #2A5C8E(认知) / 光谱紫 #6B4C9A(价值) / 光谱金 #C49B3B(存在)
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(exist_ok=True)

PARCHMENT = (247, 244, 238)
READING = (31, 41, 55)
NAVY = (27, 58, 92)
GRAY = (122, 140, 163)
SECOND = (74, 90, 112)
WHITE = (255, 255, 255)
RED = (239, 68, 68)

SPECTRAL_BLUE = (42, 92, 142)
SPECTRAL_PURPLE = (107, 76, 154)
SPECTRAL_GOLD = (196, 155, 59)

# 跨平台字体解析。
# 早期版本把字体路径硬编码成 C:/Windows/Fonts/...，导致 Linux/macOS 上必然失败
# （在 Linux 上那只是个相对路径，会直接抛 OSError）。CI 曾经靠"装字体 + 建同名软链"
# 绕过，那是治标；这里按平台逐个候选探测，找不到就给出可操作的报错。
_FONT_CANDIDATES = {
    # 黑体 / 无衬线标题（需含 CJK 字形）
    "hei": [
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/msyhbd.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/arphic/uming.ttc",
    ],
    # 正文（需含 CJK 字形）
    "body": [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simsun.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    ],
    # 拉丁文 / 数字。DejaVu 在多数 Linux 发行版上随基础镜像存在。
    "latin": [
        "C:/Windows/Fonts/georgia.ttf",
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    ],
}


def _resolve_fonts():
    resolved = {}
    missing = []
    for role, candidates in _FONT_CANDIDATES.items():
        for c in candidates:
            if Path(c).is_file():
                resolved[role] = c
                break
        else:
            missing.append((role, candidates))
    if missing:
        lines = ["找不到可用的字体文件，无法绘制插图。", ""]
        for role, cands in missing:
            lines.append(f"  缺少字体角色 {role!r}，已尝试：")
            lines.extend(f"    - {c}" for c in cands)
        lines += [
            "",
            "解决办法（任一）：",
            "  Debian/Ubuntu : sudo apt-get install -y fonts-wqy-zenhei fonts-dejavu-core",
            "  Fedora        : sudo dnf install -y wqy-zenhei-fonts dejavu-serif-fonts",
            "  macOS         : 系统自带 PingFang / Georgia，通常无需安装",
            "  或在 _FONT_CANDIDATES 中补上你本机字体的绝对路径。",
        ]
        print("\n".join(lines), file=sys.stderr)
        raise SystemExit(2)
    return resolved


_FONTS = _resolve_fonts()
HEI = _FONTS["hei"]
YAHEI = _FONTS["body"]
GEO = _FONTS["latin"]


def F(path, size):
    return ImageFont.truetype(path, size)


def tint(rgb, a):
    return tuple(round(PARCHMENT[i] + (rgb[i] - PARCHMENT[i]) * a) for i in range(3))


def rounded(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


LAYERS = [
    ("L1", "减负", "Cognitive Load Reduction",
     "把认知负荷从信息量转移到结构", "Shift load from volume to structure"),
    ("L2", "可体验", "Experiential Rendering",
     "把「读到」变成「操作到」", "Turn reading into operating"),
    ("L3", "意义生成", "Meaning Generation",
     "组织成方向·价值·边界", "Organize into direction / value / boundary"),
    ("L4", "价值评估", "Value Assessment",
     "为判断标注证据强度", "Label judgments with evidence strength"),
    ("L5", "方向选择", "Direction Selection",
     "在五尺度上选定值得的方向", "Choose the worth-going direction"),
    ("L6", "反思与审视递归", "Recursive Reflection",
     "让系统审视自己的审视", "Let the system review its own review"),
]
COLORS = [SPECTRAL_BLUE, SPECTRAL_BLUE, SPECTRAL_PURPLE,
          SPECTRAL_PURPLE, SPECTRAL_GOLD, SPECTRAL_GOLD]


# ---------------------------------------------------------------- 图 1
def fig_stack():
    # 图内不再画标题：标题与图注统一由 DOCX 生成，避免同一句话出现两次
    W, H = 1740, 1110
    img = Image.new("RGB", (W, H), PARCHMENT)
    d = ImageDraw.Draw(img)

    f_bandzh = F(HEI, 27)
    f_banden = F(GEO, 20)
    f_badge = F(HEI, 34)
    f_axiszh = F(HEI, 23)
    f_axisen = F(GEO, 16)
    f_defzh = F(YAHEI, 22)
    f_defen = F(GEO, 18)

    x0, x1 = 250, 1690
    top, bh, gap = 44, 142, 14
    bands = [("界面层", "Interface", 0, 1), ("加工层", "Processing", 2, 3),
             ("元层", "Meta", 4, 5)]

    for gzh, gen, a, b in bands:
        y_top = top + a * (bh + gap)
        y_bot = top + b * (bh + gap) + bh
        d.line([(196, y_top + 6), (196, y_bot - 6)], fill=GRAY, width=3)
        d.line([(196, y_top + 6), (206, y_top + 6)], fill=GRAY, width=3)
        d.line([(196, y_bot - 6), (206, y_bot - 6)], fill=GRAY, width=3)
        cy = (y_top + y_bot) // 2
        d.text((60, cy - 30), gzh, font=f_axiszh, fill=NAVY)
        d.text((60, cy + 2), gen, font=f_axisen, fill=GRAY)

    for i, (tag, zh, en, dzh, den) in enumerate(LAYERS):
        col = COLORS[i]
        y = top + i * (bh + gap)
        rounded(d, (x0, y, x1, y + bh), 14, fill=tint(col, 0.10),
                outline=tint(col, 0.42), width=2)
        rounded(d, (x0, y, x0 + 128, y + bh), 14, fill=col)
        d.rectangle((x0 + 100, y, x0 + 128, y + bh), fill=col)
        tb = d.textbbox((0, 0), tag, font=f_badge)
        d.text((x0 + 64 - (tb[2] - tb[0]) / 2,
                y + bh / 2 - (tb[3] - tb[1]) / 2 - tb[1]), tag, font=f_badge, fill=WHITE)
        d.text((x0 + 152, y + 28), zh, font=f_bandzh, fill=NAVY)
        d.text((x0 + 152, y + 72), en, font=f_banden, fill=GRAY)
        d.line([(x0 + 470, y + 24), (x0 + 470, y + bh - 24)],
               fill=tint(col, 0.45), width=2)
        d.text((x0 + 500, y + 32), dzh, font=f_defzh, fill=READING)
        d.text((x0 + 500, y + 76), den, font=f_defen, fill=SECOND)

    d.text((60, H - 62),
           "递归：L6 的输出回写为 L1 的输入，六层构成闭合螺旋，而非单向流水线。",
           font=f_defzh, fill=SECOND)
    d.text((60, H - 32),
           "Recursion: L6 output is rewritten as L1 input — the six layers form a closed spiral, not a linear pipeline.",
           font=f_defen, fill=GRAY)

    img.save(OUT / "fig1_six_layer_stack.png", dpi=(300, 300))
    print("saved", OUT / "fig1_six_layer_stack.png", img.size)


# ---------------------------------------------------------------- 图 2
def fig_spiral():
    # 同上：不画图内标题
    W, H = 1740, 1070
    img = Image.new("RGB", (W, H), PARCHMENT)
    d = ImageDraw.Draw(img)

    f_node = F(HEI, 30)
    f_legzh = F(HEI, 26)
    f_legen = F(GEO, 17)
    f_ann = F(YAHEI, 22)
    f_annen = F(GEO, 18)
    f_next = F(HEI, 25)

    cx, cy = 1150, 520
    turns = 1.72
    r0, r1 = 80, 330

    def spiral_point(t):
        ang = -math.pi / 2 + t * turns * 2 * math.pi
        r = r0 + (r1 - r0) * t
        return cx + r * math.cos(ang), cy + r * math.sin(ang), ang, r

    ts = [0.06, 0.22, 0.38, 0.54, 0.70, 0.86]
    # 螺旋从 L1 节点起画，避免内圈多出一截无意义的尾巴
    pts = [spiral_point(ts[0] + (1.0 - ts[0]) * k / 900)[:2] for k in range(901)]
    d.line(pts, fill=tint(SPECTRAL_BLUE, 0.78), width=5, joint="curve")

    coords = []
    for i, t in enumerate(ts):
        x, y, ang, r = spiral_point(t)
        coords.append((x, y, ang, r))
        rounded(d, (x - 33, y - 33, x + 33, y + 33), 33, fill=COLORS[i])
        tb = d.textbbox((0, 0), LAYERS[i][0], font=f_node)
        d.text((x - (tb[2] - tb[0]) / 2, y - (tb[3] - tb[1]) / 2 - tb[1]),
               LAYERS[i][0], font=f_node, fill=WHITE)

    # 递归回写：从 L6 绕到「同角度的更高一层起点 L1'」
    a6, r6 = coords[5][2], coords[5][3]
    a1 = coords[0][2]
    end_ang = a1 + 2 * math.pi
    R_END = 404
    M = 240
    arc = []
    for k in range(M + 1):
        t = k / M
        ang = a6 + (end_ang - a6) * t
        # 前段沿螺旋继续，后段抬升到更高一层
        rr = r6 + (R_END - r6) * (t ** 0.72)
        arc.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))

    # 从 L6 节点外侧起笔，避免红线压住节点与编号
    x6c, y6c = coords[5][0], coords[5][1]
    start_idx = 0
    for k, (ax, ay) in enumerate(arc):
        if math.hypot(ax - x6c, ay - y6c) > 40:
            start_idx = k
            break
    arc = arc[start_idx:]
    d.line(arc, fill=RED, width=5, joint="curve")

    (px, py), (qx, qy) = arc[-2], arc[-1]
    dxa, dya = qx - px, qy - py
    L = math.hypot(dxa, dya) or 1
    ux, uy = dxa / L, dya / L
    s = 24
    d.polygon([(qx, qy),
               (qx - ux * s - uy * s * 0.62, qy - uy * s + ux * s * 0.62),
               (qx - ux * s + uy * s * 0.62, qy - uy * s - ux * s * 0.62)], fill=RED)

    d.ellipse((qx - 33, qy - 33, qx + 33, qy + 33), outline=RED, width=5, fill=PARCHMENT)
    tb = d.textbbox((0, 0), "L1'", font=f_next)
    d.text((qx - (tb[2] - tb[0]) / 2, qy - (tb[3] - tb[1]) / 2 - tb[1]),
           "L1'", font=f_next, fill=RED)
    d.text((qx + 50, qy - 32), "下一轮起点", font=f_ann, fill=RED)
    d.text((qx + 50, qy + 2), "Next-cycle entry", font=f_annen, fill=RED)

    mid = arc[int(M * 0.50)]
    d.text((mid[0] + 6, mid[1] - 44), "递归回写", font=f_ann, fill=RED, anchor="lm")
    d.text((mid[0] + 6, mid[1] - 14), "Recursive rewrite", font=f_annen,
           fill=RED, anchor="lm")

    d.text((cx, cy - 34), "螺旋上升", font=f_ann, fill=NAVY, anchor="mm")
    d.text((cx, cy - 4), "Spiral ascent", font=f_annen, fill=GRAY, anchor="mm")

    # 左侧图例
    ly = 100
    for i, (tag, zh, en, _, _) in enumerate(LAYERS):
        rounded(d, (62, ly - 8, 106, ly + 36), 24, fill=COLORS[i])
        tb = d.textbbox((0, 0), tag, font=f_legzh)
        d.text((84 - (tb[2] - tb[0]) / 2, ly + 14 - (tb[3] - tb[1]) / 2 - tb[1]),
               tag, font=f_legzh, fill=WHITE)
        d.text((124, ly - 2), zh, font=f_legzh, fill=NAVY)
        d.text((124, ly + 32), en, font=f_legen, fill=GRAY)
        ly += 88

    d.text((62, 22), "本轮六层", font=f_ann, fill=NAVY)
    d.text((196, 26), "One cycle of six layers", font=f_annen, fill=GRAY)
    d.line([(62, 60), (500, 60)], fill=GRAY, width=2)

    d.text((60, H - 62),
           "归零不是回到原点，而是回到同角度的更高一层起点——这是「元」的落点。",
           font=f_ann, fill=SECOND)
    d.text((60, H - 32),
           "Zeroing does not return to the origin, but to a higher entry point at the same angle — this is where \"meta\" lands.",
           font=f_annen, fill=GRAY)

    img.save(OUT / "fig2_recursive_spiral.png", dpi=(300, 300))
    print("saved", OUT / "fig2_recursive_spiral.png", img.size)




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


if __name__ == "__main__":
    fig_stack()
    fig_spiral()
    fig_boundary()
