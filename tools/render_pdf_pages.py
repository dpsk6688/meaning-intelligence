"""把 PDF 逐页渲染为 PNG，便于肉眼检查视觉污染。"""
from pathlib import Path
import pymupdf

PDF = Path("whitepaper/dist/意义智能_元智能理论与分层应用_公开发布白皮书_v1.0_中英双语.pdf")
OUT = Path("tools/pdf_render")


def main():
    if not PDF.exists():
        raise SystemExit(f"未找到: {PDF}")
    OUT.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(PDF)
    print(f"总页数: {len(doc)}")
    print(f"输出目录: {OUT.resolve()}\n")

    for i, page in enumerate(doc):
        # 2x 缩放,约 150 DPI,足够肉眼看污染
        pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))
        out = OUT / f"page_{i + 1:02d}.png"
        pix.save(out)
        print(f"  ✅ 第 {i + 1:2d} 页 → {out.name}  ({pix.width}x{pix.height})")

    print(f"\n完成。请用 Windows 相册打开 {OUT.resolve()} 目录，重点看 page_13.png")


if __name__ == "__main__":
    main()