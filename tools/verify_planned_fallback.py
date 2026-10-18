"""本地模拟 CI 的 planned 回退分支测试。
1. 把 build.py / mi_common.py / config.json / templates/ 拷到临时目录
2. 在那个目录里跑 build.py
3. 检查生成的 HTML 里有 planned 时间轴
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FILES = ["msi/build.py", "msi/mi_common.py", "msi/config.json"]
TEMPLATE_DIR = "msi/templates"


def main():
    d = Path(tempfile.mkdtemp())
    print("临时目录:", d)

    # 拷贝文件
    for rel in FILES:
        src = ROOT / rel
        if not src.exists():
            print(f"❌ 找不到 {src}")
            return 1
        shutil.copy2(src, d / Path(rel).name)

    # 拷贝 templates/
    tpl_src = ROOT / TEMPLATE_DIR
    if not tpl_src.exists():
        print(f"❌ 找不到 {tpl_src}")
        return 1
    shutil.copytree(tpl_src, d / "templates")

    print("已拷贝:", [f.name for f in d.iterdir()])

    # 跑 build.py
    r = subprocess.run(
        [sys.executable, "build.py"],
        cwd=d,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    print()
    print("--- build.py exit:", r.returncode)
    print("--- stdout ---")
    print(r.stdout or "(空)")
    if r.stderr:
        print("--- stderr ---")
        print(r.stderr[:1500])

    if r.returncode != 0:
        print("\n❌ build.py 失败")
        return 1

    # 检查 HTML
    html_path = d / "meaning_intelligence.html"
    if not html_path.exists():
        print(f"\n❌ 未生成 {html_path}")
        return 1

    html = html_path.read_text(encoding="utf-8")

    # 检查 SOURCE/TIMELINE_SOURCE
    m = re.search(r'const\s+(?:SOURCE|TIMELINE_SOURCE)\s*=\s*"(planned|measured)"', html)
    found = m.group(1) if m else "NOT FOUND"

    print()
    print("═══════════════════════════════════")
    print(f"grep 结果: {found}")
    print(f"CI 检查会: {'PASS ✅' if found == 'planned' else 'FAIL ❌'}")
    print("═══════════════════════════════════")

    return 0 if found == "planned" else 1


if __name__ == "__main__":
    sys.exit(main())