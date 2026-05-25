import pdfplumber

# 중간/끝 부분 확인 - 카테고리 구분이 있는지 확인
pdf_path = r"C:\개인\wooahouse\wooaGosa\문제지\(면허1,2종) 학과시험 문제은행[한국어]_(2026.3.9.시행).pdf"
out_path = r"C:\개인\wooahouse\wooaGosa\inspect_out2.txt"

with pdfplumber.open(pdf_path) as pdf:
    total = len(pdf.pages)
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(f"총 페이지 수: {total}\n\n")
        # 80, 160, 240, 320 페이지 근처 확인 (섹션 구분 찾기)
        for i in [79, 80, 81, 159, 160, 161, 239, 240, 241, 329, 330]:
            if i < total:
                out.write(f"\n===== 페이지 {i+1} =====\n")
                text = pdf.pages[i].extract_text()
                if text:
                    out.write(text[:2000] + "\n")

        # 이미지가 있는 페이지 찾기 (처음 50페이지 중 이미지 포함된 페이지)
        out.write("\n\n===== 이미지 포함 페이지 목록 (처음 50페이지) =====\n")
        for i in range(min(50, total)):
            imgs = pdf.pages[i].images
            if imgs:
                out.write(f"페이지 {i+1}: {len(imgs)}개 이미지\n")

print("완료")
