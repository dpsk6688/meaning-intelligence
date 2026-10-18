"""逐页分析 PDF，定位 '1 1 1 1...' 污染的来源与位置。"""
import sys
from pathlib import Path
import pymupdf  # 新版 API，替代 fitz

PDF = Path("whitepaper/dist/意义智能_元智能理论与分层应用_公开发布白皮书_v1.0_中英双语.pdf")


def main():
    if not PDF.exists():
        raise SystemExit(f"未找到: {PDF}")

    doc = pymupdf.open(PDF)
    print(f"总页数: {len(doc)}\n")

    # 先全量扫描每一页,找出异常页
    suspicious = []
    for i, page in enumerate(doc):
        text = page.get_text()
        ones = text.count("1")
        # 正常页字符数应该 <3000; 若某页 '1' 计数占比 >30% 则嫌疑
        if ones > 100 or (len(text) > 50 and ones / max(len(text), 1) > 0.3):
            suspicious.append((i + 1, len(text), ones))

    if not suspicious:
        print("没有扫描到明显异常页。")
        print("若你仍看到视觉污染,请用屏幕截图发我。")
        return

    print(f"发现 {len(suspicious)} 个嫌疑页:\n")
    for pageno, total, ones in suspicious:
        print(f"  第 {pageno} 页  字符数={total}  '1'计数={ones}")
    print()

    # 对每个嫌疑页做详细分析
    for pageno, _, _ in suspicious:
        page = doc[pageno - 1]
        print(f"═══ 第 {pageno} 页 详细分析 ═══")
        print(f"  页面尺寸: {page.rect}")

        # 提取所有文本块及其位置
        blocks = page.get_text("blocks")
        print(f"  文本块数量: {len(blocks)}")
        for bi, b in enumerate(blocks[:20]):  # 只看前 20 个
            x0, y0, x1, y1, text, block_no, block_type = b
            snippet = text[:60].replace("\n", " ")
            print(f"    block[{bi}] 位置=({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f}) "
                  f"类型={block_type} 文本={snippet!r}")

        # 提取所有图片(可能是被渲染成图的污染)
        images = page.get_images()
        if images:
            print(f"  图片数量: {len(images)}")
            for im in images[:10]:
                print(f"    xref={im[0]} 尺寸={im[2]}x{im[3]}")

        print()


if __name__ == "__main__":
    main()