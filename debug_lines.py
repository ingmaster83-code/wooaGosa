import pdfplumber
import re

pdf_path = r"C:\개인\wooahouse\wooaGosa\문제지\(면허1,2종) 학과시험 문제은행[한국어]_(2026.3.9.시행).pdf"
out_path = r"C:\개인\wooahouse\wooaGosa\debug_lines.txt"

q_start = re.compile(r"^(\d+)\.\s")

lines_sample = []
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages[:5]:
        text = page.extract_text()
        if text:
            for line in text.split("\n"):
                line = line.strip()
                if line:
                    lines_sample.append(line)

# 처음 100줄 + 숫자로 시작하는 줄만 별도 표시
with open(out_path, "w", encoding="utf-8") as f:
    f.write("=== 처음 100줄 ===\n")
    for i, line in enumerate(lines_sample[:100]):
        m = q_start.match(line)
        marker = f"[Q{m.group(1)}]" if m else "     "
        f.write(f"{i:3d} {marker} | {line}\n")

    f.write("\n\n=== 숫자 패턴 매칭 줄 (처음 5페이지) ===\n")
    for i, line in enumerate(lines_sample):
        m = q_start.match(line)
        if m:
            f.write(f"줄{i:3d} 번호={m.group(1)} | {line[:80]}\n")

print("완료: debug_lines.txt")
