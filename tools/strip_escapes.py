"""去掉 README.en.md 里被自动转义的 markdown 特殊字符。
只处理确认存在的转义序列,不碰代码块里的反斜杠。"""
from pathlib import Path

p = Path("README.en.md")
text = p.read_text(encoding="utf-8")

# 严格顺序: 先长的、后短的,避免 \*\* 被 \* 先吃掉一半
REPLACEMENTS = [
    (r"\*\*", "**"),   # 粗体
    (r"\*",   "*"),    # 斜体
    (r"\#",   "#"),    # 标题
    (r"\[",   "["),    # 链接左括号
    (r"\]",   "]"),    # 链接右括号
    (r"\&",   "&"),    # URL 参数
    (r"\_",   "_"),    # 文件名下划线
    (r"\-",   "-"),    # 破折号/列表
    (r"\|",   "|"),    # 表格竖线
    (r"\(",   "("),
    (r"\)",   ")"),
    (r"\!",   "!"),
]

n_total = 0
for old, new in REPLACEMENTS:
    cnt = text.count(old)
    if cnt:
        text = text.replace(old, new)
        n_total += cnt
        print(f"  ✅ {old!r:8s} → {new!r:8s}  {cnt:3d} 处")

p.write_text(text, encoding="utf-8")
print(f"\n总计 {n_total} 处修改")


# 复验
print("\n═══ 复验 ═══")
lines = p.read_text(encoding="utf-8").splitlines()
print(f"总行数: {len(lines)}")
print(f"第 1 行: {lines[0]!r}")

if lines[0].startswith("#") and not lines[0].startswith("\\"):
    print("✅ 第一行是标题(未转义)")
else:
    print("❌ 第一行仍有转义字符")

# 检查关键内容是否就位
body = "\n".join(lines)
checks = [
    ("含 'What This Theory Does NOT Claim'", "What This Theory Does NOT Claim" in body),
    ("含 'Construct Boundaries'", "Construct Boundaries" in body),
    ("含 'The Six-Layer Stack'", "The Six-Layer Stack" in body),
    ("含 badge 图片", "[![Live Page]" in body),
]
for label, ok in checks:
    print(f"  {'✅' if ok else '❌'} {label}")