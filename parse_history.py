"""
한국사능력검정시험 파서 (기본 + 심화)
- 텍스트 기반 PDF만 처리 (스캔본 자동 스킵)
- 기출문제 + 정답표/답지 자동 매칭
"""

import pdfplumber, json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = Path(r"C:\개인\wooahouse\wooaGosa\data")
OUTPUT_DIR.mkdir(exist_ok=True)

CIRCLE_MAP = {'①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5}
CIRCLE_PAT = re.compile(r'[①②③④⑤]')

# ── 유틸 ────────────────────────────────────────────────

def is_text_pdf(path: Path) -> bool:
    try:
        with pdfplumber.open(str(path)) as pdf:
            words = sum(len(p.extract_words()) for p in pdf.pages[:2])
        return words > 50
    except:
        return False

def round_no(name: str) -> int | None:
    m = re.search(r'(\d{2,3})회', name)
    return int(m.group(1)) if m else None

def pair_files(folder: Path):
    """폴더에서 (회차, 문제지, 정답파일) 쌍 반환 — 텍스트 PDF만"""
    q_files = [f for f in folder.glob('*.pdf')
               if '문제지' in f.name or ('문제' in f.name and '정답' not in f.name)]
    a_files = [f for f in folder.glob('*.pdf')
               if any(k in f.name for k in ('정답표', '답지', '정답지')) and '문제' not in f.name]

    q_map = {}
    for f in q_files:
        r = round_no(f.name)
        if r and is_text_pdf(f):
            q_map[r] = f

    a_map = {}
    for f in a_files:
        r = round_no(f.name)
        if r:
            a_map[r] = f

    pairs = []
    for r in sorted(q_map):
        if r in a_map:
            pairs.append((r, q_map[r], a_map[r]))
        else:
            print(f"  ⚠️  {r}회 정답 파일 없음 — 스킵")
    return pairs

# ── 정답표 파서 ──────────────────────────────────────────

def parse_answers(path: Path) -> dict[int, int]:
    answers = {}
    try:
        with pdfplumber.open(str(path)) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ''
                for m in re.finditer(r'(\d{1,2})\s+([①②③④⑤])\s+\d', text):
                    n = int(m.group(1))
                    if 1 <= n <= 50:
                        answers[n] = CIRCLE_MAP[m.group(2)]
    except Exception as e:
        print(f"    정답 파싱 오류: {e}")
    return answers

# ── 기출문제 파서 ────────────────────────────────────────

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

    return (to_lines([w for w in words if w['x0'] < mid_x]),
            to_lines([w for w in words if w['x0'] >= mid_x]))

def lines_to_blocks(lines):
    blocks, cur, last_no = [], None, 0
    for line in lines:
        m = re.match(r'^(\d{1,2})\.\s*(.*)', line)
        if m:
            n = int(m.group(1))
            rest = m.group(2)
            # 실제 문제 시작 조건:
            #  1) 번호가 last_no 보다 커야 함 (역방향 번호는 본문 속 소제목)
            #  2) 나머지 텍스트가 비어있거나, 시험 문제 특유의 키워드/기호 포함
            is_question_start = (
                1 <= n <= 50
                and n > last_no
                and (
                    not rest                                         # "2." 처럼 번호만 있는 행
                    or re.search(r'[?\[]', rest)                    # ? 또는 [ (배점 마커)
                    or re.search(r'것은|옳은|가장|고른|찾은|골라|보면|나타난|무엇|다음|어느|해당|설명|내용|관련|시기', rest)
                )
            )
            if is_question_start:
                if cur:
                    blocks.append(cur)
                cur = {'no': n, 'lines': [rest] if rest else []}
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

    # 문제 텍스트
    q_lines = [l.strip() for l in lines[:first_c] if l.strip()]
    q_lines = [l for l in q_lines if not re.match(r'^제\d+회', l)]
    q_lines = [re.sub(r'\s*\[\d점\]', '', l).strip() for l in q_lines]
    q_lines = [l for l in q_lines if l]
    question = ' '.join(q_lines).strip()

    # 선택지
    choice_text = ' '.join(lines[first_c:])
    parts = re.split(r'([①②③④⑤])', choice_text)
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

    if len(choices) not in (4, 5) or not question:
        return None
    return {'no': block['no'], 'question': question, 'choices': choices}

def parse_exam(pdf_path: Path) -> dict[int, dict]:
    result = {}
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page in pdf.pages:
                for col in extract_columns(page):
                    for block in lines_to_blocks(col):
                        q = block_to_question(block)
                        if q:
                            result[q['no']] = q
    except Exception as e:
        print(f"    문제 파싱 오류: {e}")
    return result

# ── 회차 처리 ────────────────────────────────────────────

def process_round(r, q_pdf, a_pdf, id_start=1):
    print(f"  문제 파싱...", end=' ', flush=True)
    questions = parse_exam(q_pdf)
    print(f"{len(questions)}문항", end='  ', flush=True)

    print(f"정답 파싱...", end=' ', flush=True)
    answers = parse_answers(a_pdf)
    print(f"{len(answers)}개")

    records = []
    for no in sorted(questions):
        if no not in answers:
            continue
        q = questions[no]
        records.append({
            "id":          id_start + len(records),
            "round":       r,
            "question_no": no,
            "question":    q['question'],
            "choices":     q['choices'],
            "answers":     [answers[no]],
            "explanation": ""
        })
    print(f"  -> {len(records)}문항 완성")
    return records

# ── 메인 ────────────────────────────────────────────────

TARGETS = [
    (Path(r"C:\개인\wooahouse\wooaGosa\문제지\한국사 기본"),  "history_basic.json",    "기본"),
    (Path(r"C:\개인\wooahouse\wooaGosa\문제지\한국사 심화"),  "history_advanced.json", "심화"),
]

for folder, out_name, label in TARGETS:
    if not folder.exists():
        print(f"\n[{label}] 폴더 없음 — 스킵")
        continue

    print(f"\n{'='*55}")
    print(f"[{label}] {folder}")
    pairs = pair_files(folder)
    print(f"처리 회차: {[r for r,_,_ in pairs]}")

    all_records, id_cnt = [], 1
    for r, q_pdf, a_pdf in pairs:
        print(f"\n-- {r}회 --")
        recs = process_round(r, q_pdf, a_pdf, id_start=id_cnt)
        all_records.extend(recs)
        id_cnt += len(recs)

    out_path = OUTPUT_DIR / out_name
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)

    print(f"\n완료: 총 {len(all_records)}문항 -> {out_path}")

    # 샘플
    if all_records:
        s = all_records[0]
        print(f"\n[샘플] {s['round']}회 {s['question_no']}번")
        print(f"  Q: {s['question'][:60]}...")
        for k,v in s['choices'].items():
            mark = " <=" if s['answers'][0] == int(k) else ""
            print(f"  {k}: {v}{mark}")
