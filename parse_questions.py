import pdfplumber
import re
import json

# ------------------------------------------------------------------ #
# 유틸 - 전각/반각 콜론 정규화
# ------------------------------------------------------------------ #
# ①②③④⑤ = 일반 원문자, ➀➁➂➃ = 굵은 원문자 (일부 문제에서 사용)
CHOICE_SYMBOLS_A = "①②③④⑤"
CHOICE_SYMBOLS_B = "➀➁➂➃"
ALL_CHOICE_SYMBOLS = CHOICE_SYMBOLS_A + CHOICE_SYMBOLS_B

# 인덱스 매핑: 어느 타입이든 1-5로 변환
CHOICE_IDX = {c: i+1 for i, c in enumerate(CHOICE_SYMBOLS_A)}
CHOICE_IDX.update({c: i+1 for i, c in enumerate(CHOICE_SYMBOLS_B)})

CHOICE_PATTERN = re.compile(r"([①②③④⑤➀➁➂➃])")

def normalize(text):
    """전각 콜론(：)을 반각(:)으로 통일, 연속 공백 제거"""
    return text.replace("：", ":").strip()

# ------------------------------------------------------------------ #
# PDF 텍스트 전체 추출
# ------------------------------------------------------------------ #
def extract_text(pdf_path):
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for line in text.split("\n"):
                    line = line.strip()
                    if line:
                        lines.append(line)
    return lines

# ------------------------------------------------------------------ #
# 문제 블록 분리 (2-pass 방식)
#
# Pass 1: "■ 정답" 직전의 "N." 줄을 찾아 경계 후보를 수집
# Pass 2: 경계 후보 사이를 블록으로 분리, sequential 체크로 허위 양성 제거
# ------------------------------------------------------------------ #
def split_into_blocks(lines):
    q_start = re.compile(r"^(\d+)\.[^\d]")
    ans_pat = re.compile(r"^■\s*정답")

    # Pass 1: ■정답 앞에 나오는 가장 최근 "N." 줄을 찾기
    # 각 ■정답 줄에 대해 그 직전 "N." 줄의 인덱스를 기록
    candidate_starts = set()
    pending_q_idx = None  # 마지막으로 만난 "N." 줄의 인덱스

    for i, line in enumerate(lines):
        m = q_start.match(line)
        if m:
            pending_q_idx = i
        if ans_pat.match(line) and pending_q_idx is not None:
            candidate_starts.add(pending_q_idx)
            pending_q_idx = None

    # Pass 2: candidate_starts 기준으로 sequential 검증 후 블록 분리
    sorted_starts = sorted(candidate_starts)
    # sequential 체크: 번호가 증가하는 순서여야 함
    valid_starts = []
    last_num = 0
    for idx in sorted_starts:
        m = q_start.match(lines[idx])
        if m:
            num = int(m.group(1))
            if num > last_num:
                valid_starts.append(idx)
                last_num = num

    # 블록 분리
    blocks = []
    for k, start in enumerate(valid_starts):
        end = valid_starts[k + 1] if k + 1 < len(valid_starts) else len(lines)
        blocks.append(lines[start:end])

    return blocks

# ------------------------------------------------------------------ #
# 보기(선택지) 파싱
# 같은 줄에 여러 보기가 있을 수 있음: "① A ② B"
# ------------------------------------------------------------------ #
def parse_choices(choice_lines):
    """choice_lines: 보기가 들어있는 줄 목록 → {1:'텍스트', 2:'텍스트', ...}"""
    raw = " ".join(choice_lines)
    # 각 보기 기호 앞에 구분자 삽입
    raw = CHOICE_PATTERN.sub(r"\n\1", raw)
    choices = {}
    for part in raw.split("\n"):
        part = part.strip()
        if not part:
            continue
        if part[0] in ALL_CHOICE_SYMBOLS:
            idx = CHOICE_IDX[part[0]]
            choices[idx] = part[1:].strip()
    return choices

# ------------------------------------------------------------------ #
# 단일 블록 파싱
# ------------------------------------------------------------------ #
def parse_block(block):
    if not block:
        return None

    # 첫 줄에서 번호 추출
    first = block[0]
    m = re.match(r"^(\d+)\.\s*(.*)", first, re.DOTALL)
    if not m:
        return None

    q_num = int(m.group(1))
    q_text_parts = [m.group(2).strip()]

    choice_lines = []
    situation_lines = []
    answer_raw = ""
    explain_lines = []

    STATE = "QUESTION"  # QUESTION → CHOICES → SITUATION → ANSWER → EXPLAIN

    def has_choice(line):
        return bool(CHOICE_PATTERN.search(line))

    def is_answer(line):
        n = normalize(line)
        return n.startswith("■ 정답") or n.startswith("■정답")

    def is_explain(line):
        n = normalize(line)
        return n.startswith("■ 해설") or n.startswith("■해설")

    def is_situation(line):
        return line.startswith("■") and not is_answer(line) and not is_explain(line)

    for line in block[1:]:
        if is_explain(line):
            STATE = "EXPLAIN"
            # 해설 텍스트 (콜론 이후)
            n = normalize(line)
            after = re.sub(r"^■\s*해설\s*:\s*", "", n)
            explain_lines.append(after)
            continue

        if is_answer(line):
            STATE = "ANSWER"
            answer_raw = normalize(line)
            continue

        if STATE == "EXPLAIN":
            explain_lines.append(line)
            continue

        if STATE == "ANSWER":
            # 정답 다음 줄이 해설이 아니라면 상황 or 다음 문제 (예외 처리)
            explain_lines.append(line)
            continue

        if is_situation(line):
            STATE = "SITUATION"
            situation_lines.append(line[1:].strip())  # ■ 제거
            continue

        if has_choice(line):
            STATE = "CHOICES"
            choice_lines.append(line)
            continue

        if STATE == "QUESTION":
            q_text_parts.append(line)
        elif STATE == "CHOICES":
            # 보기 줄 이후 보기 기호 없는 줄 → 질문 연속일 수 있음 (긴 보기)
            choice_lines.append(line)
        elif STATE == "SITUATION":
            situation_lines.append(line)

    # 질문 텍스트 정리
    q_text = " ".join(q_text_parts).strip()

    # 선택지 파싱
    choices = parse_choices(choice_lines)

    # 정답 파싱: "■ 정답 : 1" 또는 "■ 정답 : 1, 4"
    answers = []
    if answer_raw:
        after = re.sub(r"^■\s*정답\s*:\s*", "", answer_raw)
        for tok in re.split(r"[,\s]+", after.strip()):
            tok = tok.strip()
            if tok.isdigit():
                answers.append(int(tok))

    # 해설 정리
    explanation = " ".join(explain_lines).strip()

    # 상황 정리
    situation = " ".join(situation_lines).strip() if situation_lines else ""

    # 비디오 문제 여부
    is_video = "(홈페이지 참조)" in q_text

    return {
        "id": q_num,
        "question": q_text,
        "choices": choices,
        "situation": situation,
        "answers": answers,
        "explanation": explanation,
        "is_video": is_video,
    }

# ------------------------------------------------------------------ #
# 메인 파싱 함수
# ------------------------------------------------------------------ #
def parse_pdf(pdf_path, out_path, label):
    print(f"[{label}] 텍스트 추출 중...")
    lines = extract_text(pdf_path)
    print(f"[{label}] 총 {len(lines)}줄 추출됨")

    print(f"[{label}] 문제 블록 분리 중...")
    blocks = split_into_blocks(lines)
    print(f"[{label}] {len(blocks)}개 문제 블록 발견")

    questions = []
    errors = []
    for block in blocks:
        try:
            q = parse_block(block)
            if q:
                questions.append(q)
        except Exception as e:
            errors.append((block[0] if block else "?", str(e)))


    if errors:
        print(f"[{label}] 파싱 오류 {len(errors)}건:")
        for title, err in errors[:5]:
            print(f"  - {title[:60]}: {err}")

    # JSON 저장
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print(f"[{label}] {len(questions)}개 문제 저장 완료: {out_path}")
    return questions

# ------------------------------------------------------------------ #
# 실행
# ------------------------------------------------------------------ #
BASE = r"C:\개인\wooahouse\wooaGosa"
PDFS = {
    "면허1,2종": (
        rf"{BASE}\문제지\(면허1,2종) 학과시험 문제은행[한국어]_(2026.3.9.시행).pdf",
        rf"{BASE}\data\license_1_2.json",
    ),
    "이륜자동차": (
        rf"{BASE}\문제지\(이륜자동차) 학과시험 문제은행[한국어]_(2026.3.9.시행).pdf",
        rf"{BASE}\data\motorcycle.json",
    ),
}

all_results = {}
for label, (pdf_path, out_path) in PDFS.items():
    qs = parse_pdf(pdf_path, out_path, label)
    all_results[label] = len(qs)

print("\n====== 파싱 결과 요약 ======")
for label, count in all_results.items():
    print(f"  {label}: {count}문제")
print("완료!")
