"""CI 一致性检查:版本号 / 根 ROADMAP.md / MIT 缩写 / 证据等级 / hypotheses.yaml。
任何一项失败 → 非零退出码。"""
import re
import sys
from pathlib import Path

ROOT = Path(".")
failures = []


def fail(msg):
    failures.append(msg)
    print(f"::error::{msg}")


def ok(msg):
    print(f"OK   {msg}")


# ---------------------------------------------------------------- 1. VERSION.yaml
v = ROOT / "VERSION.yaml"
if not v.exists():
    fail("VERSION.yaml 不存在")
    print(f"\n共 {len(failures)} 项失败")
    sys.exit(1)

vt = v.read_text(encoding="utf-8")
ok("VERSION.yaml 存在")

m = re.search(r"research_system:.*?^\s+version:\s*\"([^\"]+)\"", vt, re.M | re.S)
version = m.group(1) if m else None
if version:
    ok(f"research_system.version = {version}")
else:
    fail("VERSION.yaml 找不到 research_system.version")

# ---------------------------------------------------------------- 2. README badge
if version:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    badge = re.search(r"badge/version-(\d+\.\d+\.\d+)", readme)
    if not badge:
        fail("README.md 找不到 version badge")
    elif badge.group(1) != version:
        fail(f"README badge ({badge.group(1)}) != VERSION.yaml ({version})")
    else:
        ok(f"README badge 版本一致 = {version}")

# ---------------------------------------------------------------- 3. docs/roadmap.md 当前版本
if version:
    rm = ROOT / "docs" / "roadmap.md"
    if rm.exists():
        rt = rm.read_text(encoding="utf-8")
        m2 = re.search(r"(?:当前版本|Current Release)\s+(\d+\.\d+\.\d+)", rt, re.IGNORECASE)
        if m2 and m2.group(1) != version:
            fail(f"docs/roadmap.md 当前版本 ({m2.group(1)}) != VERSION.yaml ({version})")
        elif m2:
            ok(f"docs/roadmap.md 当前版本一致 = {version}")
        else:
            print("INFO docs/roadmap.md 无'当前版本'标记,跳过")

# ---------------------------------------------------------------- 4. 根 ROADMAP.md 有效
root_rm = ROOT / "ROADMAP.md"
if root_rm.exists():
    t = root_rm.read_text(encoding="utf-8")
    if len(t) < 100 or "notepad" in t.lower() or "文件 2" in t:
        fail(f"根 ROADMAP.md 内容异常 (长度 {len(t)})")
    else:
        ok(f"根 ROADMAP.md 有效 ({len(t)} 字符)")

# ---------------------------------------------------------------- 5. MIT 缩写不冲突
readme = (ROOT / "README.md").read_text(encoding="utf-8")
if re.search(r"\bMIT\b(?!\s*[Ll]icense)", readme) and re.search(r"MIT [Ll]icense", readme):
    stray_mit = re.findall(r"\bMIT\b(?!\s*[Ll]icense)(?!\s*Theory)", readme)
    if stray_mit:
        fail(f"README 里 {len(stray_mit)} 处裸露的 MIT (既不是 License 也不是 Theory)")
    else:
        ok("MIT 缩写无冲突")
else:
    ok("MIT 缩写无冲突")

# ---------------------------------------------------------------- 6. 六层证据等级跨文件一致性
readme = (ROOT / "README.md").read_text(encoding="utf-8")
ev = ROOT / "docs" / "evidence.md"
if ev.exists():
    evt = ev.read_text(encoding="utf-8")
    if "机制 E3–E4" in evt and "机制 E3)" in readme:
        fail("L1 证据等级不一致:evidence.md 说 E3–E4,README 说 E3")
    else:
        ok("L1 证据等级跨文件一致")

# ---------------------------------------------------------------- 7. hypotheses.yaml 完整性
hy = ROOT / "hypotheses.yaml"
if hy.exists():
    try:
        import yaml
        data = yaml.safe_load(hy.read_text(encoding="utf-8"))
        raw_hyps = data.get("hypotheses", {})
        
        if isinstance(raw_hyps, dict):
            ids = list(raw_hyps.keys())
        elif isinstance(raw_hyps, list):
            ids = [h.get("id") for h in raw_hyps if isinstance(h, dict)]
        else:
            ids = []
            
        missing_ids = [i for i in ids if not i]
        if missing_ids or len(ids) == 0:
            fail("hypotheses.yaml 存在缺少 id 的假说或为空")
        else:
            ok(f"hypotheses.yaml 完整 ({len(ids)} 条, 支持列表/字典结构)")
    except ImportError:
        print("INFO 未装 pyyaml,跳过 hypotheses.yaml 检查")
    except Exception as e:
        fail(f"hypotheses.yaml 解析失败: {e}")
else:
    print("INFO hypotheses.yaml 不存在,跳过")

# ---------------------------------------------------------------- 结果
print()
if failures:
    print(f"共 {len(failures)} 项失败")
    sys.exit(1)
print("所有一致性检查通过")
sys.exit(0)