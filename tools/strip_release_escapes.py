from pathlib import Path

p = Path("release_v0.2.0.md")
text = p.read_text(encoding="utf-8")

REPLACEMENTS = [
    (r"\*\*", "**"),
    (r"\*", "*"),
    (r"\#", "#"),
    (r"\[", "["),
    (r"\]", "]"),
    (r"\&", "&"),
    (r"\_", "_"),
    (r"\-", "-"),
    (r"\|", "|"),
    (r"\(", "("),
    (r"\)", ")"),
    (r"\!", "!"),
]

n = 0
for old, new in REPLACEMENTS:
    c = text.count(old)
    if c:
        text = text.replace(old, new)
        n += c
        print(f"  {old!r} → {new!r}  {c} 处")

p.write_text(text, encoding="utf-8")
print(f"\n共 {n} 处修改")
print("前 10 字节:", p.read_bytes()[:10])