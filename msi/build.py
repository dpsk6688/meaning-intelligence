"""Generate every derived deliverable from config.json.

    python build.py            -> meaning_intelligence.html + meaning_intelligence_diagram.md

If timeline.json (written by the Manim render) exists it is used for the
slider's video seeking; otherwise the timeline is planned from config.
"""
import json
from pathlib import Path

from mi_common import HERE, all_mermaid, load_config, plan_timeline


def js(obj):
    # safe to embed inside <script>
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def main():
    cfg = load_config()
    planned = plan_timeline(cfg)

    tl_file = HERE / "timeline.json"
    timeline, source = planned, "planned"
    if tl_file.exists():
        measured = json.loads(tl_file.read_text(encoding="utf-8"))["timeline"]
        missing = [k for k in planned if k not in measured]
        if missing:
            print(f"! timeline.json lacks {missing}; falling back to planned timeline")
        else:
            timeline, source = measured, "measured"
            drift = max(abs(measured[k] - planned[k]) for k in planned)
            print(f"timeline: measured (max drift vs plan {drift:.2f}s)")
    if source == "planned":
        print("timeline: planned from config (render with manim to get measured values)")

    mm = all_mermaid(cfg)
    html = (HERE / "templates" / "html_template.html").read_text(encoding="utf-8")
    _src_py_path = HERE / "scenes" / "meaning_intelligence.py"
    _src_py_text = _src_py_path.read_text(encoding="utf-8") if _src_py_path.exists() else "// (scenes/ not present in this build)\\n"

    repl = {
        "__CONFIG_JSON__": js(cfg),
        "__TIMELINE_JSON__": js(timeline),
        "__TIMELINE_SOURCE__": js(source),
        "__MERMAID_JSON__": js(mm),
        "__SRC_PY__": js(_src_py_text),
        "__SRC_CFG__": js((HERE / "config.json").read_text(encoding="utf-8")),
    }
    for k, v in repl.items():
        assert k in html, f"placeholder {k} missing from template"
        html = html.replace(k, v)
    (HERE / "meaning_intelligence.html").write_text(html, encoding="utf-8")

    titles = {lg: cfg["ui"][lg]["diagrams"] for lg in cfg["languages"]}
    parts = []
    for lg in cfg["languages"]:
        parts.append(f"# {cfg['ui'][lg]['title']} — {lg}\n")
        for i, k in enumerate(["pipeline", "scenes", "palette"]):
            parts.append(f"## {i + 1}. {titles[lg][i]}\n\n```mermaid\n{mm[lg][k]}\n```\n")
    (HERE / "meaning_intelligence_diagram.md").write_text("\n".join(parts), encoding="utf-8")
    print("wrote meaning_intelligence.html, meaning_intelligence_diagram.md")


if __name__ == "__main__":
    main()
