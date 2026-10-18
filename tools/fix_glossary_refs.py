"""同步 docx 术语表里 MCA/SA/AZ 的章节引用到 7B.2/7B.3/7B.4。
安全：先备份，再修正，最后复验。"""
import re
import shutil
from pathlib import Path
from docx import Document

DOCX = Path("whitepaper/dist/意义智能_元智能理论与分层应用_公开发布白皮书_v1.0_中英双语.docx")
BACKUP = DOCX.with_suffix(".docx.bak")

# 只针对术语表里 MCA/SA/AZ 的章节引用
FIXES = [
    (re.compile(r"(元认知觉察[^第\n]{0,30})第\s*12\s*章"),     r"\g<1>正典 7B.2"),
    (re.compile(r"(螺旋上升[^第\n]{0,30})第\s*13\s*章"),       r"\g<1>正典 7B.3"),
    (re.compile(r"(主动归零[^第\n]{0,30})第\s*13\s*章"),       r"\g<1>正典 7B.4"),
    (re.compile(r"(Metacognitive Awareness[^第\n]{0,40})第\s*12\s*章"), r"\g<1>正典 7B.2"),
    (re.compile(r"(Spiral Ascent[^第\n]{0,40})第\s*13\s*章"),           r"\g<1>正典 7B.3"),
    (re.compile(r"(Active Zeroing[^第\n]{0,40})第\s*13\s*章"),          r"\g<1>正典 7B.4"),
]


def fix_cell(cell):
    n = 0
    for p in cell.paragraphs:
        for run in p.runs:
            for pattern, repl in FIXES:
                new_text, count = pattern.subn(repl, run.text)
                if count:
                    run.text = new_text
                    n += count
    return n


def main():
    if not DOCX.exists():
        raise SystemExit(f"未找到: {DOCX}")

    if not BACKUP.exists():
        shutil.copy2(DOCX, BACKUP)
        print(f"已备份 → {BACKUP}")
    else:
        print(f"备份已存在，跳过: {BACKUP}")

    doc = Document(DOCX)
    total = 0

    # 扫描所有表格的单元格
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                total += fix_cell(cell)

    # 也扫描正文段落
    for p in doc.paragraphs:
        for run in p.runs:
            for pattern, repl in FIXES:
                new_text, count = pattern.subn(repl, run.text)
                if count:
                    run.text = new_text
                    total += count

    doc.save(DOCX)
    print(f"完成 {total} 处修正\n")

    # 复验
    doc2 = Document(DOCX)
    residual = []
    for tbl in doc2.tables:
        for row in tbl.rows:
            for cell in row.cells:
                t = cell.text
                if "元认知觉察" in t and "第 12 章" in t:
                    residual.append(("MCA", t[:80]))
                if "螺旋上升" in t and "第 13 章" in t:
                    residual.append(("SA", t[:80]))
                if "主动归零" in t and "第 13 章" in t:
                    residual.append(("AZ", t[:80]))

    if residual:
        print(f"⚠️ 仍有 {len(residual)} 处未修正：")
        for kw, snippet in residual:
            print(f"   [{kw}] {snippet}")
    else:
        print("✅ 复验通过：术语表章节引用已全部同步")


if __name__ == "__main__":
    main()