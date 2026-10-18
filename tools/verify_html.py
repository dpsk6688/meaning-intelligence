#!/usr/bin/env python3
"""verify_html.py —— 校验构建出的单文件 HTML。

做三件事：
  1. 占位符残留检查：不能有未替换的 {{...}}
  2. 抽出内联 <script>，用 node --check 做真实语法检查
     （历史缺陷：模板把占位符又套了一层引号，注入后得到 ""planned""，
      触发 SyntaxError 使整段脚本失效 —— 页面能开，但滑块/画布/提示全死。
      只有做真正的 JS 语法检查才能拦住这类问题。）
  3. 关键注入项抽查

用法：
    python tools/verify_html.py msi/meaning_intelligence.html [--node <node 可执行文件>]
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html", type=Path)
    ap.add_argument("--node", default=None, help="node 可执行文件路径；默认从 PATH 查找")
    args = ap.parse_args()

    if not args.html.exists():
        print(f"FAIL 找不到文件：{args.html}")
        return 1
    html = args.html.read_text(encoding="utf-8")
    ok = True

    print(f"== 校验 {args.html} （{len(html):,} 字符）==")

    # 1. 占位符残留
    leftover = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", html)))
    if leftover:
        print(f"[1/3] 占位符残留 : FAIL -> {leftover}")
        ok = False
    else:
        print("[1/3] 占位符残留 : OK")

    # 2. 内联 JS 语法
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S)
    node = args.node or shutil.which("node")
    if not node:
        print("[2/3] 内联 JS 语法 : SKIP（未找到 node，跳过语法检查）")
    elif not blocks:
        print("[2/3] 内联 JS 语法 : SKIP（没有内联 script 块）")
    else:
        # 不用 tempfile：Windows 上 mkdtemp 会以 0o700 建目录，
        # 受限沙箱令牌可能无法写入其中。直接在 HTML 同级目录写固定文件，用完即删。
        written = []
        try:
            for i, b in enumerate(blocks):
                js = args.html.parent / f"_verify_block{i}.js"
                js.write_text(b, encoding="utf-8")
                written.append(js)
                r = subprocess.run([node, "--check", str(js)],
                                   capture_output=True, text=True,
                                   encoding="utf-8", errors="replace")
                if r.returncode == 0:
                    print(f"[2/3] 内联 JS 语法 : OK   block[{i}] {len(b):,} 字符")
                else:
                    print(f"[2/3] 内联 JS 语法 : FAIL block[{i}]")
                    for line in (r.stderr or "").splitlines()[:12]:
                        print("      ", line)
                    ok = False
        finally:
            for js in written:
                try:
                    js.unlink()
                except OSError:
                    pass

    # 3. 注入项抽查
    checks = {
        "TIMELINE 含 L6": bool(re.search(r"const TIMELINE\s*=\s*\{[^;]*\"L6\"", html, re.S)),
        "SOURCE 为合法 JS 字符串": bool(re.search(r'const\s+(?:SOURCE|TIMELINE_SOURCE)\s*=\s*"(measured|planned)"', html)),
        "六层键齐全": all(f'"{k}"' in html for k in
                          ("L1", "L2", "L3", "L4", "L5", "L6")),
        "证据色阶存在": all(f'"{k}"' in html for k in
                            ("E0", "E1", "E2", "E3", "E4", "E5", "E6")),
    }
    for name, passed in checks.items():
        print(f"[3/3] {name} : {'OK' if passed else 'FAIL'}")
        ok = ok and passed

    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
