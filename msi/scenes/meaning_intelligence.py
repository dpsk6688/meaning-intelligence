"""Meaning Intelligence — Manim scene (six-layer stack, 8 acts).

Everything (copy, colours, fonts, timing) comes from config.json.

    manim -qh meaning_intelligence.py MeaningIntelligenceScene     # Chinese
    MI_LANG=en manim -qh meaning_intelligence.py MeaningIntelligenceScene

Acts -> layers:  overload/text/diagram = L1,  interactive = L2,
                 meaning = L3,  assess = L4,  select = L5,  reflect = L6.
A measured timeline.json is written next to this file after rendering;
`python build.py` then uses it for the HTML page's video seeking.
"""
import json
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))          # msi/scenes/
sys.path.insert(0, str(_HERE.parent))   # msi/  <- 这里是 mi_common.py 所在

import numpy as np
from manim import *

from mi_common import HERE, load_config

CFG = load_config()
LANG = os.environ.get("MI_LANG", CFG["default_lang"])
if LANG not in CFG["languages"]:
    raise ValueError(f"MI_LANG must be one of {CFG['languages']}, got {LANG!r}")

COL = CFG["colors"]
EVID = CFG["evidence_scale"]
ACT = {a["id"]: a for a in CFG["acts"]}
CONTENT = {k: v[LANG] for k, v in CFG["content"].items()}


def pick_font(candidates):
    """First installed font from the list, else '' (Manim/Pango default)."""
    try:
        import manimpango

        available = set(manimpango.list_fonts())
    except Exception:
        return ""
    return next((f for f in candidates if f in available), "")


UI_FONT = pick_font(CFG["fonts"]["cjk" if LANG == "zh" else "latin"])
MONO_FONT = pick_font(CFG["fonts"]["mono"])


def T(text, font=None, **kw):
    return Text(text, font=UI_FONT if font is None else font, **kw)


def P3(x, y):
    return np.array([x, y, 0.0])


class MeaningIntelligenceScene(Scene):
    # ---------------------------------------------------------------- helpers
    def mark(self, key):
        self.timeline[key] = round(float(self.renderer.time), 3)

    def begin(self, act_id):
        """Mark the act's start, and its layer's start if it is the layer's first act."""
        self.mark(act_id)
        layer = ACT[act_id]["layer"]
        if layer not in self.timeline:
            self.mark(layer)
        return ACT[act_id]

    def make_noise(self):
        rng = np.random.default_rng(CFG["overload"]["seed"])
        group = VGroup()
        for _ in range(CFG["overload"]["count"]):
            t = T("info. " * 3, font=MONO_FONT, font_size=11, color=COL["gray"])
            t.move_to([rng.uniform(-6.5, 6.5), rng.uniform(-3.5, 3.5), 0])
            t.set_opacity(rng.uniform(0.3, 0.8))
            group.add(t)
        return group

    def make_node(self, text, color):
        box = RoundedRectangle(corner_radius=0.15, height=0.9, width=3.0, color=color)
        box.set_fill(COL["fill_gray"], opacity=0.9)
        return VGroup(box, T(text, font_size=18, color=color).move_to(box))

    def make_eye(self, scale=1.0):
        c = COL["cyan"]
        outline = Ellipse(width=2.4 * scale, height=1.1 * scale, color=c)
        pupil = Circle(radius=0.32 * scale, color=c).set_fill(c, opacity=0.95)
        glow = Circle(radius=0.45 * scale, color=c).set_fill(c, opacity=0.25)
        return VGroup(outline, glow, pupil), pupil, glow

    # -------------------------------------------------------------- construct
    def construct(self):
        self.camera.background_color = COL["bg"]
        self.timeline = {}
        cyan, purple, amber, gray = COL["cyan"], COL["purple"], COL["amber"], COL["gray"]
        rng = np.random.default_rng(7)

        # ===== L1 · act 1: information overload ===========================
        s = self.begin("overload")
        noise = self.make_noise()
        self.play(FadeIn(noise), run_time=s["enter"])
        self.wait(s["hold"])

        # ===== L1 · act 2: gravitational collapse -> 3 core lines ============
        s = self.begin("text")
        E = s["enter"]
        core = Dot(color=cyan).scale(2.8)
        self.play(
            LaggedStart(*[t.animate.move_to(ORIGIN).scale(0.05).set_color(cyan) for t in noise],
                        lag_ratio=0.02),
            run_time=0.45 * E, rate_func=exponential_decay,
        )
        self.play(FadeOut(noise), FadeIn(core, scale=0.3), run_time=0.10 * E)
        ste = VGroup(*[T(l, font_size=30, color=cyan, weight=BOLD) for l in CONTENT["ste_lines"]]
                     ).arrange(DOWN, buff=0.45)
        self.play(FadeOut(core, scale=2),
                  LaggedStart(*[FadeIn(l, shift=UP * 0.2) for l in ste], lag_ratio=0.3),
                  run_time=0.45 * E)
        self.wait(s["hold"])

        # ===== L1 · act 3: structure diagram ================================
        s = self.begin("diagram")
        n1 = self.make_node(CONTENT["node1"], cyan)
        n2 = self.make_node(CONTENT["node2"], purple)
        n2.next_to(n1, RIGHT, buff=1.6)
        arrow = Arrow(n1.get_right(), n2.get_left(), buff=0.15, color=WHITE,
                      max_tip_length_to_length_ratio=0.2)
        diagram = VGroup(n1, arrow, n2).center()
        self.play(FadeOut(ste),
                  LaggedStart(FadeIn(n1), GrowArrow(arrow), FadeIn(n2), lag_ratio=0.4),
                  run_time=s["enter"])
        self.wait(s["hold"])

        # ===== L2 · operable interface ======================================
        s = self.begin("interactive")
        E = s["enter"]
        browser = RoundedRectangle(corner_radius=0.2, height=3.2, width=5.8, color=cyan)
        browser.set_fill(COL["fill_gray"], opacity=0.9)
        bar = Rectangle(height=0.35, width=5.8, color=cyan).set_fill(cyan, opacity=0.3)
        bar.align_to(browser, UP)
        track = Rectangle(height=0.08, width=3.8, color=gray).shift(DOWN * 0.3)
        knob = Circle(radius=0.16, color=cyan).set_fill(cyan, opacity=1).move_to(track.get_left())
        browser_group = VGroup(browser, bar, track, knob)
        self.play(FadeOut(diagram), FadeIn(browser_group), run_time=0.35 * E)
        self.play(knob.animate.shift(RIGHT * track.width), run_time=0.65 * E, rate_func=smooth)
        self.wait(s["hold"])

        # ===== L3 · meaning generation: nodes settle into direction·value·boundary
        s = self.begin("meaning")
        E = s["enter"]
        verts = [P3(0, 1.9), P3(-3.0, -1.5), P3(3.0, -1.5)]
        centroid = sum(verts) / 3
        starts = [P3(rng.uniform(-3, 3), rng.uniform(-1.6, 1.6)) for _ in range(9)]
        dots = VGroup(*[Dot(point=p, radius=0.11, color=cyan) for p in starts])
        targets = []
        for i in range(9):
            v = verts[i % 3]
            ang = (i // 3) * 2.1 + i
            targets.append(v + (centroid - v) * 0.24 + 0.34 * P3(np.cos(ang), np.sin(ang)))
        tri = Polygon(*verts, color=purple, stroke_width=3)
        tri.set_fill(COL["fill_purple"], opacity=0.5)
        axis_labels = VGroup(
            T(CONTENT["axes"][0], font_size=24, color=purple, weight=BOLD).next_to(verts[0], UP, buff=0.2),
            T(CONTENT["axes"][1], font_size=24, color=purple, weight=BOLD).next_to(verts[1], DOWN, buff=0.2),
            T(CONTENT["axes"][2], font_size=24, color=purple, weight=BOLD).next_to(verts[2], DOWN, buff=0.2),
        )
        self.play(FadeOut(browser_group), FadeIn(dots), run_time=0.25 * E)
        self.play(Create(tri), run_time=0.15 * E)
        self.play(*[d.animate.move_to(t) for d, t in zip(dots, targets)], run_time=0.40 * E,
                  rate_func=smooth)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in axis_labels], lag_ratio=0.3),
                  run_time=0.20 * E)
        self.wait(s["hold"])

        # ===== L4 · value assessment: evidence rings ==========================
        s = self.begin("assess")
        E = s["enter"]
        rings = VGroup(*[
            Circle(radius=0.22, color=EVID[lv], stroke_width=4).move_to(t)
            for lv, t in zip(CFG["demo"]["assess_levels"], targets)
        ])
        swatches = VGroup(*[Square(side_length=0.3, color=EVID[i]).set_fill(EVID[i], opacity=0.9)
                            for i in range(7)]).arrange(RIGHT, buff=0.08)
        e0 = T("E0", font_size=16, color=gray).next_to(swatches, LEFT, buff=0.2)
        e6 = T("E6", font_size=16, color=gray).next_to(swatches, RIGHT, buff=0.2)
        note = T(CONTENT["illustrative"], font_size=14, color=gray).next_to(swatches, DOWN, buff=0.15)
        legend = VGroup(swatches, e0, e6, note).move_to(P3(0, -3.0))
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.1), run_time=0.60 * E)
        self.play(FadeIn(legend, shift=UP * 0.2), run_time=0.40 * E)
        self.wait(s["hold"])

        # ===== L5 · direction selection: 3 candidates, 1 survives =============
        s = self.begin("select")
        E = s["enter"]
        old = VGroup(dots, rings, tri, axis_labels, legend)
        origin_pt = P3(-4.2, 0)
        ends = [P3(3.6, 1.7), P3(3.6, 0.0), P3(3.6, -1.7)]
        origin_dot = Dot(point=origin_pt, radius=0.16, color=WHITE)
        end_dots = VGroup(*[Dot(point=e, radius=0.14, color=amber) for e in ends])
        end_labels = VGroup(*[T(CONTENT["candidates"][i], font_size=22, color=amber).next_to(ends[i], RIGHT, buff=0.25)
                              for i in range(3)])
        paths = VGroup(*[
            CubicBezier(origin_pt, origin_pt + RIGHT * 3.2, e + LEFT * 3.2, e, color=amber, stroke_width=4)
            for e in ends
        ])
        k = CFG["demo"]["chosen_path"]
        self.play(FadeOut(old), FadeIn(origin_dot), FadeIn(end_dots), FadeIn(end_labels),
                  run_time=0.30 * E)
        self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.25), run_time=0.40 * E)
        fades = [paths[i].animate.set_stroke(opacity=0.15) for i in range(3) if i != k]
        fades += [end_dots[i].animate.set_opacity(0.2) for i in range(3) if i != k]
        fades += [end_labels[i].animate.set_opacity(0.2) for i in range(3) if i != k]
        self.play(*fades,
                  paths[k].animate.set_stroke(color=cyan, width=8),
                  end_dots[k].animate.scale(1.5).set_color(cyan),
                  run_time=0.30 * E)
        self.wait(s["hold"])

        # ===== L6 · recursive reflection: spiral back to L1' + overseeing eye ==
        s = self.begin("reflect")
        E = s["enter"]
        select_group = VGroup(origin_dot, end_dots, end_labels, paths)
        center = P3(0, -0.5)

        def spiral_pt(t):  # t in [0, 2*pi]; starts at the top, clockwise, radius grows
            r = 0.75 + 0.95 * t / TAU
            a = PI / 2 - t
            return center + r * P3(np.cos(a), np.sin(a))

        spiral = ParametricFunction(lambda t: spiral_pt(t), t_range=[0, TAU], color=amber, stroke_width=5)
        markers, labels = VGroup(), VGroup()
        names = [f"L{i + 1}" for i in range(6)] + ["L1′"]
        for i, nm in enumerate(names):
            p = spiral_pt(i * TAU / 6)
            out = (p - center) / np.linalg.norm(p - center)
            markers.add(Dot(point=p, radius=0.09, color=cyan if i < 6 else WHITE))
            labels.add(T(nm, font_size=18, color=cyan if i < 6 else WHITE).move_to(p + out * 0.38))
        link = DashedLine(spiral_pt(0), spiral_pt(TAU), color=WHITE, stroke_width=2)
        eye, pupil, glow = self.make_eye(0.8)
        eye.move_to(P3(0, 2.9))
        cap = T(CONTENT["supervisor"], font_size=18, color=cyan, weight=BOLD).move_to(P3(0, -3.35))

        self.play(FadeOut(select_group), run_time=0.15 * E)
        self.play(Create(spiral), run_time=0.45 * E, rate_func=linear)
        self.play(LaggedStart(*[FadeIn(VGroup(m, l)) for m, l in zip(markers, labels)], lag_ratio=0.15),
                  Create(link), run_time=0.20 * E)
        self.play(FadeIn(eye, shift=DOWN * 0.2), FadeIn(cap), run_time=0.10 * E)
        self.play(pupil.animate.scale(1.25), glow.animate.scale(1.5).set_opacity(0.4),
                  run_time=0.10 * E, rate_func=there_and_back)
        self.wait(s["hold"])

        # ===== finale ==========================================================
        f = CFG["final"]
        self.mark("final")
        title = T(f["label"][LANG], font_size=48, color=WHITE, weight=BOLD)
        title.set_color_by_gradient(cyan, purple, amber)
        self.play(FadeOut(*self.mobjects), run_time=0.4 * f["enter"])
        self.play(FadeIn(title, scale=0.88), run_time=0.6 * f["enter"])
        self.wait(f["hold"])
        self.mark("end")

        (HERE / "timeline.json").write_text(
            json.dumps({"lang": LANG, "timeline": self.timeline}, indent=2), encoding="utf-8")
