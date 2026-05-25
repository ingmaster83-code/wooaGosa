"""
컴퓨터활용능력 1급·2급 필기 파서
- 파일명: 컴퓨터활용능력{1,2}급YYYYMMDD(학생용).pdf
- 마지막 페이지 정답 격자 파싱
- 2컬럼 문제 레이아웃 파싱
"""

import pdfplumber, json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = Path(r"C:\개인\wooahouse\wooaGosa\data")
OUTPUT_DIR.mkdir(exist_ok=True)

CIRCLE_MAP = {'①': 1, '②': 2, '③': 3, '④': 4}
CIRCLE_PAT = re.compile(r'[①②③④]')

# comcbt 헤더 필터 패턴
HEADER_PAT = re.compile(
    r'컴퓨터활용능력\s*\d급|전자문제집\s*CBT|www\.comcbt\.com|'
    r'기출문제\s*및\s*해설집|CBT\s*홈페이지|CBT\s*앱|구글플레이|'
    r'PC\s*버전|교사용.*학생용|오답.*수정|최신.*자료|최강\s*자격증'
)

# ── 유틸 ────────────────────────────────────────────────

def exam_date(name: str) -> str | None:
    """파일명에서 날짜 추출: YYYYMMDD"""
    m = re.search(r'(\d{8})', name)
    return m.group(1) if m else None

def exam_grade(name: str) -> int | None:
    m = re.search(r'([12])급', name)
    return int(m.group(1)) if m else None

# ── 정답 파싱 (마지막 페이지) ────────────────────────────

def _extract_answer_grid(lines: list[str]) -> dict[int, int]:
    """번호행 + 기호행 패턴에서 정답 추출 (기호행은 번호행 이후 3줄 이내 허용)"""
    answers = {}
    i = 0
    while i < len(lines):
        # 번호 행: "1 2 3 4 5 6 7 8 9 10" 처럼 숫자만 10개 내외
        tokens = lines[i].split()
        if len(tokens) >= 5 and all(re.fullmatch(r'\d+', t) for t in tokens):
            try:
                nums = list(map(int, tokens))
            except ValueError:
                i += 1
                continue
            # 이후 3줄 안에서 기호 행 찾기
            for j in range(i + 1, min(i + 4, len(lines))):
                syms = CIRCLE_PAT.findall(lines[j])
                if len(syms) == len(nums):
                    for n, s in zip(nums, syms):
                        if 1 <= n <= 60:
                            answers[n] = CIRCLE_MAP[s]
                    i = j + 1
                    break
            else:
                i += 1
        else:
            i += 1
    return answers

def parse_answers(pdf) -> dict[int, int]:
    """마지막 페이지의 정답 격자에서 번호→정답 추출 (2컬럼 대응)"""
    page = pdf.pages[-1]
    words = page.extract_words(x_tolerance=3, y_tolerance=3)

    def words_to_lines(wlist):
        if not wlist:
            return []
        wlist = sorted(wlist, key=lambda w: (round(w['top'] / 5), w['x0']))
        lines, cur_y, cur = [], None, []
        for w in wlist:
            y = round(w['top'] / 5)
            if cur_y is None or y != cur_y:
                if cur:
                    lines.append(' '.join(x['text'] for x in cur))
                cur_y, cur = y, [w]
            else:
                cur.append(w)
        if cur:
            lines.append(' '.join(x['text'] for x in cur))
        return lines

    mid_x = page.width / 2
    left_lines  = words_to_lines([w for w in words if w['x0'] <  mid_x])
    right_lines = words_to_lines([w for w in words if w['x0'] >= mid_x])
    all_lines   = words_to_lines(words)

    # 세 버전 모두 시도해서 가장 많이 파싱된 결과 사용
    best = {}
    for lines in (all_lines, right_lines, left_lines):
        ans = _extract_answer_grid(lines)
        if len(ans) > len(best):
            best = ans
    return best

# ── 컬럼 추출 ────────────────────────────────────────────

def extract_columns(page):
    words = page.extract_words(x_tolerance=3, y_tolerance=3)
    if not words:
        return [], []
    mid_x = page.width / 2

    def to_lines(wlist):
        if not wlist:
            return []
        wlist = sorted(wlist, key=lambda w: (round(w['top'] / 5), w['x0']))
        lines, cur_y, cur = [], None, []
        for w in wlist:
            y = round(w['top'] / 5)
            if cur_y is None or y != cur_y:
                if cur:
                    lines.append(' '.join(x['text'] for x in cur))
                cur_y, cur = y, [w]
            else:
                cur.append(w)
        if cur:
            lines.append(' '.join(x['text'] for x in cur))
        return lines

    left  = to_lines([w for w in words if w['x0'] < mid_x])
    right = to_lines([w for w in words if w['x0'] >= mid_x])
    return left, right

def filter_lines(lines: list[str]) -> list[str]:
    """comcbt 헤더·광고 줄 제거"""
    return [l for l in lines if l.strip() and not HEADER_PAT.search(l)]

# ── 과목 추적 & 블록 분리 ────────────────────────────────

SUBJECT_NAMES = {
    1: '컴퓨터 일반',
    2: '스프레드시트 일반',
    3: '데이터베이스 일반',
}

def lines_to_blocks(lines, subject_state: list):
    """
    lines → question blocks
    subject_state = [current_subject_no]  (mutable 리스트로 공유)
    """
    blocks, cur, last_no = [], None, 0

    for line in lines:
        # 과목 헤더 인식
        sm = re.match(r'^(\d+)과목\s*[:]\s*(.+)', line)
        if sm:
            subject_state[0] = int(sm.group(1))
            continue

        # 문제 번호 인식
        m = re.match(r'^(\d{1,2})\.\s*(.*)', line)
        if m:
            n = int(m.group(1))
            rest = m.group(2)
            is_q = (
                1 <= n <= 60
                and n > last_no
                and (
                    not rest
                    or re.search(r'[?\[]|것은|옳은|가장|고른|찾은|골라|보면|나타난|무엇|다음|어느|해당|설명|내용|관련|시기|아닌|대한|경우|위한', rest)
                )
            )
            if is_q:
                if cur:
                    blocks.append(cur)
                cur = {
                    'no': n,
                    'subject': subject_state[0],
                    'lines': [rest] if rest else [],
                }
                last_no = n
                continue

        if cur is not None:
            cur['lines'].append(line)

    if cur:
        blocks.append(cur)
    return blocks

def block_to_question(block):
    lines = block['lines']
    first_c = next((i for i, l in enumerate(lines) if CIRCLE_PAT.search(l)), None)
    if first_c is None:
        return None

    # 문제 텍스트 (선택지 이전)
    q_lines = [l.strip() for l in lines[:first_c] if l.strip()]
    question = ' '.join(q_lines).strip()
    if not question:
        return None

    # 선택지 파싱
    choice_text = ' '.join(lines[first_c:])
    parts = re.split(r'([①②③④])', choice_text)
    choices, cur_k, buf = {}, None, []
    for p in parts:
        if p in CIRCLE_MAP:
            if cur_k:
                choices[str(cur_k)] = ' '.join(buf).strip()
            cur_k, buf = CIRCLE_MAP[p], []
        elif cur_k:
            buf.append(p.strip())
    if cur_k and buf:
        choices[str(cur_k)] = ' '.join(buf).strip()

    if len(choices) != 4 or not question:
        return None

    return {
        'no': block['no'],
        'subject': block['subject'],
        'question': question,
        'choices': choices,
    }

# ── 전체 시험 파싱 ────────────────────────────────────────

def parse_exam(pdf_path: Path) -> tuple[dict[int, dict], dict[int, int]]:
    result = {}
    with pdfplumber.open(str(pdf_path)) as pdf:
        # 마지막 페이지 = 정답표 → 문제 페이지는 [:-1]
        answers = parse_answers(pdf)

        subject_state = [1]  # 현재 과목 번호 (mutable)
        for page in pdf.pages[:-1]:
            left, right = extract_columns(page)
            for col in (left, right):
                col = filter_lines(col)
                for block in lines_to_blocks(col, subject_state):
                    q = block_to_question(block)
                    if q:
                        result[q['no']] = q

    return result, answers

# ── 날짜 처리 ────────────────────────────────────────────

def process_file(pdf_path: Path, grade: int, id_start: int) -> list[dict]:
    date = exam_date(pdf_path.name) or 'unknown'
    print(f"  문제 파싱...", end=' ', flush=True)
    questions, answers = parse_exam(pdf_path)
    print(f"{len(questions)}문항  정답 {len(answers)}개")

    records = []
    for no in sorted(questions):
        if no not in answers:
            continue
        q = questions[no]
        records.append({
            "id":           id_start + len(records),
            "grade":        grade,
            "date":         date,
            "subject":      q['subject'],
            "subject_name": SUBJECT_NAMES.get(q['subject'], ''),
            "question_no":  no,
            "question":     q['question'],
            "choices":      q['choices'],
            "answers":      [answers[no]],
            "explanation":  "",
        })
    print(f"  -> {len(records)}문항 완성")
    return records

# ── 메인 ────────────────────────────────────────────────

TARGETS = [
    (Path(r"C:\개인\wooahouse\wooaGosa\문제지\컴퓨터활용능력 1급"), 1, "computer_1.json"),
    (Path(r"C:\개인\wooahouse\wooaGosa\문제지\컴퓨터활용능력 2급"), 2, "computer_2.json"),
]

for folder, grade, out_name in TARGETS:
    if not folder.exists():
        print(f"\n[컴활 {grade}급] 폴더 없음 — 스킵")
        continue

    pdfs = sorted(folder.glob('*학생용*.pdf'))
    if not pdfs:
        print(f"\n[컴활 {grade}급] 파일 없음 — 스킵")
        continue

    print(f"\n{'='*55}")
    print(f"[컴활 {grade}급] {len(pdfs)}개 파일")

    all_records, id_cnt = [], 1
    for pdf_path in pdfs:
        date = exam_date(pdf_path.name) or '?'
        print(f"\n-- {date} --")
        recs = process_file(pdf_path, grade, id_start=id_cnt)
        all_records.extend(recs)
        id_cnt += len(recs)

    out_path = OUTPUT_DIR / out_name
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)

    print(f"\n완료: 총 {len(all_records)}문항 -> {out_path}")

    # 샘플
    if all_records:
        s = all_records[0]
        print(f"\n[샘플] {s['date']} {s['question_no']}번 ({s['subject_name']})")
        print(f"  Q: {s['question'][:60]}...")
        for k, v in s['choices'].items():
            mark = " <=" if s['answers'][0] == int(k) else ""
            print(f"  {k}: {v[:40]}{mark}")
