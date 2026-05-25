import pdfplumber
import sys

pdf_path = r"C:\개인\wooahouse\wooaGosa\문제지\(면허1,2종) 학과시험 문제은행[한국어]_(2026.3.9.시행).pdf"
out_path = r"C:\개인\wooahouse\wooaGosa\inspect_out.txt"

with pdfplumber.open(pdf_path) as pdf, open(out_path, "w", encoding="utf-8") as out:
    out.write(f"총 페이지 수: {len(pdf.pages)}\n")
    out.write("=" * 80 + "\n")
    for i in range(min(8, len(pdf.pages))):
        out.write(f"\n--- 페이지 {i+1} ---\n")
        text = pdf.pages[i].extract_text()
        if text:
            out.write(text[:4000] + "\n")

print("완료: inspect_out.txt 생성됨")
