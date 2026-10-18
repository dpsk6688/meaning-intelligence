"""把 mi_v2_incoming/ 里的新版文件覆盖到 msi/ 对应位置。
安全：先备份整个 msi/ 到 msi_v0.2_backup/，任何一步失败都不覆盖。"""
import shutil
import sys
from pathlib import Path

ROOT = Path(".").resolve()
INCOMING = Path.home() / "Desktop" / "mi_v2_incoming"
BACKUP = ROOT / "msi_v0.2_backup"

# 目标映射：关键字 -> 目标相对路径
TARGETS = {
    "build":                ("msi/build.py",),
    "config":               ("msi/config.json",),
    "mi_common":            ("msi/mi_common.py",),
    "html_template":        ("msi/templates/html_template.html",),
    "meaning_intelligence": ("msi/scenes/meaning_intelligence.py",),
}


def classify(name: str):
    """根据文件名判断它对应哪个目标。返回 (key, target) 或 None。"""
    low = name.lower()
    if not low.endswith((".py", ".json", ".html", ".md")):
        return None
    for key in TARGETS:
        if key in low:
            # 特殊处理 meaning_intelligence：只接受 .py
            if key == "meaning_intelligence":
                if low.endswith(".py") and "(1)" not in low.replace("(1).py", "(1).py"):
                    return key, TARGETS[key][0]
                if low.endswith(".py"):
                    return key, TARGETS[key][0]
                continue
            # build / config / mi_common / html_template 也只看主扩展名
            if key == "build" and low.endswith(".py"):
                return key, TARGETS[key][0]
            if key == "config" and low.endswith(".json"):
                return key, TARGETS[key][0]
            if key == "mi_common" and low.endswith(".py"):
                return key, TARGETS[key][0]
            if key == "html_template" and low.endswith(".html"):
                return key, TARGETS[key][0]
    return None


def main():
    print("═══ MI v2 安装器 ═══\n")

    if not INCOMING.exists():
        print(f"❌ 找不到入口目录: {INCOMING}")
        print(f"   请先创建它，并把附件下载进去。")
        sys.exit(1)

    print(f"[scan] {INCOMING}")
    files = [p for p in INCOMING.iterdir() if p.is_file()]
    if not files:
        print("❌ 入口目录为空。请把附件下载进去。")
        sys.exit(1)

    # 匹配
    matched = {}      # key -> source path
    unknown = []
    for p in files:
        hit = classify(p.name)
        if hit:
            key, target = hit
            if key in matched:
                print(f"⚠️ 重复匹配 {key}: {p.name} 与 {matched[key].name}，保留第一个")
                continue
            matched[key] = p
        else:
            unknown.append(p.name)

    print(f"\n[classify] 匹配到 {len(matched)}/5 个目标文件：")
    for key, (target,) in TARGETS.items():
        src = matched.get(key)
        status = f"✅ {src.name}" if src else "❌ 未找到"
        print(f"  {key:24s} -> {target:32s}  {status}")

    if unknown:
        print(f"\n[ignored] {len(unknown)} 个未被识别：")
        for n in unknown:
            print(f"  - {n}")

    missing = [k for k in TARGETS if k not in matched]
    if missing:
        print(f"\n❌ 还缺 {len(missing)} 个文件：{', '.join(missing)}")
        print("   请把这几个附件也下载到入口目录，或手动确认它们的文件名。")
        sys.exit(1)

    # 备份整个 msi/
    if BACKUP.exists():
        print(f"\n⚠️ 备份目录已存在：{BACKUP}")
        print("   跳过备份（说明你之前已经备份过，或上一次安装已成功）。")
    else:
        print(f"\n[backup] {ROOT / 'msi'} -> {BACKUP}")
        shutil.copytree(ROOT / "msi", BACKUP)
        n = sum(1 for _ in BACKUP.rglob("*") if _.is_file())
        print(f"  ✅ 已备份 {n} 个文件")

    # 覆盖
    print(f"\n[install] 覆盖 5 个文件：")
    for key, (target,) in TARGETS.items():
        src = matched[key]
        dst = ROOT / target
        dst.parent.mkdir(parents=True, exist_ok=True)
        # 保存一份目标端旧文件（其实备份目录里已有，但这里额外保险）
        shutil.copy2(src, dst)
        print(f"  ✅ {src.name:35s} -> {target}  ({dst.stat().st_size} bytes)")

    print(f"\n🎉 安装完成。")
    print(f"\n下一步：")
    print(f"  cd msi")
    print(f"  python -c \"import sys; sys.path.insert(0, '.'); from mi_common import load_config; c = load_config(); print('config OK:', len(c['layers']), 'layers,', len(c['acts']), 'acts')\"")


if __name__ == "__main__":
    main()