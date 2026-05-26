"""
comcbt.com 학생용/교사용 PDF 통합 파서
- 네트워크관리사 1급/2급
- 리눅스마스터 1급/2급
- 워드프로세서
- 전기기사 / 전기산업기사
- 정보처리기사 / 정보처리산업기사
- 정보보안기사
"""

import pdfplumber, json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE     = Path(r"C:\개인\wooahouse\wooaGosa\문제지")
OUT_DIR  = Path(r"C:\개인\wooahouse\wooaGosa\data")
OUT_DIR.mkdir(exist_ok=True)

CIRCLE_MAP = {'①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5}
CIRCLE_PAT = re.compile(r'[①②③④⑤]')

# comcbt 헤더 / 광고 필터
HEADER_PAT = re.compile(
    r'전자문제집\s*CBT|www\.comcbt\.com|comcbt\.com|'
    r'기출문제\s*및\s*해설집|CBT\s*홈페이지|CBT\s*앱|구글플레이|'
    r'PC\s*버전.*모바일|교사용.*학생용|오답.*수정|최신.*자료|'
    r'최강\s*자격증|모의고사.*오답.*노트|OMR\s*형식|종이\s*문제집|'
    r'실제.*시험.*사용|완벽\s*연동|관리기능|해설집\s*다운로드'
)

# 시험별 설정
EXAM_TARGETS = [
    {
        'key': 'net_1',
        'folder': '네트워크관리사 1급',
        'out': 'net_1.json',
        'max_q': 60,
    },
    {
        'key': 'net_2',
        'folder': '네트워크관리사 2급',
        'out': 'net_2.json',
        'max_q': 50,
    },
    {
        'key': 'linux_1',
        'folder': '리눅스마스터 1급',
        'out': 'linux_1.json',
        'max_q': 100,
    },
    {
        'key': 'linux_2',
        'folder': '리눅스마스터 2급',
        'out': 'linux_2.json',
        'max_q': 80,
    },
    {
        'key': 'word',
        'folder': '워드프로세서',
        'out': 'word.json',
        'max_q': 60,
    },
    {
        'key': 'elec_eng',
        'folder': '전기기사',
        'out': 'elec_eng.json',
        'max_q': 100,
    },
    {
        'key': 'elec_ind',
        'folder': '전기산업기사',
        'out': 'elec_ind.json',
        'max_q': 100,
    },
    {
        'key': 'info_proc',
        'folder': '정보처리기사',
        'out': 'info_proc.json',
        'max_q': 100,
    },
    {
        'key': 'info_ind',
        'folder': '정보처리산업기사',
        'out': 'info_ind.json',
        'max_q': 100,
    },
    {
        'key': 'info_sec',
        'folder': '정보보안기사',
        'out': 'info_sec.json',
        'max_q': 100,
    },
    # ── 2차 추가 ──────────────────────────────────────────────
    {
        'key': 'hazmat_ind',
        'folder': '위험물산업기사',
        'out': 'hazmat_ind.json',
        'max_q': 60,
    },
    {
        'key': 'hazmat_craft',
        'folder': '위험물기능사',
        'out': 'hazmat_craft.json',
        'max_q': 60,
    },
    {
        'key': 'fire_mech',
        'folder': '소방설비기사 기계분야',
        'out': 'fire_mech.json',
        'max_q': 80,
    },
    {
        'key': 'fire_elec',
        'folder': '소방설비기사 전기분야',
        'out': 'fire_elec.json',
        'max_q': 80,
    },
    {
        'key': 'forklift',
        'folder': '지게차운전기능사',
        'out': 'forklift.json',
        'max_q': 60,
    },
    {
        'key': 'excavator',
        'folder': '굴착기(굴삭기)운전기능사',
        'out': 'excavator.json',
        'max_q': 60,
    },
    {
        'key': 'realtor_1',
        'folder': '공인중개사 1차',
        'out': 'realtor_1.json',
        'max_q': 80,
    },
    {
        'key': 'realtor_2',
        'folder': '공인중개사 2차',
        'out': 'realtor_2.json',
        'max_q': 120,
    },
    {
        'key': 'welfare_1',
        'folder': '사회복지사1급 1교시',
        'out': 'welfare_1.json',
        'max_q': 50,
    },
    {
        'key': 'welfare_2',
        'folder': '사회복지사1급 2교시',
        'out': 'welfare_2.json',
        'max_q': 75,
    },
    {
        'key': 'welfare_3',
        'folder': '사회복지사1급 3교시',
        'out': 'welfare_3.json',
        'max_q': 75,
    },
    {
        'key': 'safety_ind',
        'folder': '산업안전산업기사',
        'out': 'safety_ind.json',
        'max_q': 100,
    },
    {
        'key': 'safety_eng',
        'folder': '산업안전기사',
        'out': 'safety_eng.json',
        'max_q': 120,
    },
    # ── 3차 추가 ──────────────────────────────────────────────
    {
        'key': 'elec_craft',
        'folder': '전기기능사',
        'out': 'elec_craft.json',
        'max_q': 60,
    },
    {
        'key': 'pastry',
        'folder': '제과기능사',
        'out': 'pastry.json',
        'max_q': 60,
    },
    {
        'key': 'bread',
        'folder': '제빵기능사',
        'out': 'bread.json',
        'max_q': 60,
    },
    {
        'key': 'korean_cook',
        'folder': '한식조리기능사',
        'out': 'korean_cook.json',
        'max_q': 60,
    },
    # ── 4차 추가 ──────────────────────────────────────────────
    {
        'key': 'gas_craft',
        'folder': '가스기능사',
        'out': 'gas_craft.json',
        'max_q': 60,
    },
    {
        'key': 'gas_ind',
        'folder': '가스산업기사',
        'out': 'gas_ind.json',
        'max_q': 60,
    },
    {
        'key': 'gas_eng',
        'folder': '가스기사',
        'out': 'gas_eng.json',
        'max_q': 100,
    },
    {
        'key': 'const_safety_ind',
        'folder': '건설안전산업기사',
        'out': 'const_safety_ind.json',
        'max_q': 100,
    },
    {
        'key': 'const_safety_eng',
        'folder': '건설안전기사',
        'out': 'const_safety_eng.json',
        'max_q': 120,
    },
    {
        'key': 'hvac_craft',
        'folder': '공조냉동기계기능사',
        'out': 'hvac_craft.json',
        'max_q': 60,
    },
    {
        'key': 'hvac_eng',
        'folder': '공조냉동기계기사',
        'out': 'hvac_eng.json',
        'max_q': 100,
    },
    {
        'key': 'air_eng',
        'folder': '대기환경기사',
        'out': 'air_eng.json',
        'max_q': 100,
    },
    {
        'key': 'water_eng',
        'folder': '수질환경기사',
        'out': 'water_eng.json',
        'max_q': 100,
    },
    {
        'key': 'elevator_craft',
        'folder': '승강기기능사',
        'out': 'elevator_craft.json',
        'max_q': 60,
    },
    {
        'key': 'elevator_eng',
        'folder': '승강기기사',
        'out': 'elevator_eng.json',
        'max_q': 80,
    },
    {
        'key': 'energy_craft',
        'folder': '에너지관리기능사',
        'out': 'energy_craft.json',
        'max_q': 60,
    },
    {
        'key': 'energy_eng',
        'folder': '에너지관리기사',
        'out': 'energy_eng.json',
        'max_q': 100,
    },
]


# ── 정답 그리드 파싱 ─────────────────────────────────────────

def _extract_answer_grid(lines: list, max_q: int) -> dict:
    """번호행(숫자만) + 기호행(①②③④)을 매핑, 최대 max_q까지"""
    answers = {}
    i = 0
    while i < len(lines):
        tokens = lines[i].split()
        if len(tokens) >= 5 and all(re.fullmatch(r'\d+', t) for t in tokens):
            try:
                nums = list(map(int, tokens))
            except ValueError:
                i += 1
                continue
            # 번호행 다음 4줄 이내에서 기호행 탐색
            for j in range(i + 1, min(i + 5, len(lines))):
                syms = CIRCLE_PAT.findall(lines[j])
                if len(syms) == len(nums):
                    for n, s in zip(nums, syms):
                        if 1 <= n <= max_q:
                            answers[n] = CIRCLE_MAP[s]
                    i = j + 1
                    break
            else:
                i += 1
        else:
            i += 1
    return answers


def words_to_lines(wlist: list) -> list:
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


def parse_answers(pdf, max_q: int) -> dict:
    """마지막 페이지에서 정답 추출 (2컬럼 포함 대응)"""
    page = pdf.pages[-1]
    words = page.extract_words(x_tolerance=3, y_tolerance=3)
    mid_x = page.width / 2
    all_lines   = words_to_lines(words)
    left_lines  = words_to_lines([w for w in words if w['x0'] <  mid_x])
    right_lines = words_to_lines([w for w in words if w['x0'] >= mid_x])

    best = {}
    for lines in (all_lines, right_lines, left_lines):
        ans = _extract_answer_grid(lines, max_q)
        if len(ans) > len(best):
            best = ans
    return best


# ── 컬럼 추출 ────────────────────────────────────────────────

def extract_columns(page):
    words = page.extract_words(x_tolerance=3, y_tolerance=3)
    if not words:
        return [], []
    mid_x = page.width / 2
    left  = words_to_lines([w for w in words if w['x0'] <  mid_x])
    right = words_to_lines([w for w in words if w['x0'] >= mid_x])
    return left, right


def filter_lines(lines: list) -> list:
    return [l for l in lines if l.strip() and not HEADER_PAT.search(l)]


# ── 과목 이름 동적 추출 ───────────────────────────────────────

def collect_subject_names(pdfs: list) -> dict:
    """PDF 전체를 스캔해서 과목번호→이름 맵 생성"""
    subj_map = {}
    for pdf_path in pdfs[:3]:  # 최대 3개 파일만 확인
        try:
            with pdfplumber.open(str(pdf_path)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text() or ''
                    for m in re.finditer(r'(\d+)과목\s*[:：]\s*([^\n\r①②③④\d]{2,25})', text):
                        no   = int(m.group(1))
                        name = m.group(2).strip().rstrip('◐').strip()
                        if no not in subj_map and name:
                            subj_map[no] = name
        except Exception:
            pass
    return subj_map


# ── 문제 블록 분리 ────────────────────────────────────────────

def lines_to_blocks(lines: list, subject_state: list, max_q: int) -> list:
    blocks, cur, last_no = [], None, 0

    for line in lines:
        # 과목 헤더
        sm = re.match(r'^(\d+)과목\s*[:：]\s*', line)
        if sm:
            subject_state[0] = int(sm.group(1))
            continue

        # 문제 번호 (1~max_q, 순서 증가)
        m = re.match(r'^(\d{1,3})\.\s*(.*)', line)
        if m:
            n = int(m.group(1))
            rest = m.group(2)
            is_q = (
                1 <= n <= max_q
                and n > last_no
                and (
                    not rest
                    or re.search(
                        r'[?\[]|것은|옳은|가장|고른|찾은|골라|보면|나타난|무엇|다음|어느|'
                        r'해당|설명|내용|관련|시기|아닌|대한|경우|위한|틀린|맞는|올바른|'
                        r'잘못|옳지|알맞은|적합|적절|올바르|해설|의미|정의|특징|방법',
                        rest
                    )
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


def block_to_question(block: dict):
    lines = block['lines']
    first_c = next((i for i, l in enumerate(lines) if CIRCLE_PAT.search(l)), None)
    if first_c is None:
        return None

    q_lines = [l.strip() for l in lines[:first_c] if l.strip()]
    question = ' '.join(q_lines).strip()
    if not question:
        return None

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

    return {
        'no':      block['no'],
        'subject': block['subject'],
        'question': question,
        'choices':  choices,
    }


# ── 파일 파싱 ─────────────────────────────────────────────────

def parse_exam(pdf_path: Path, max_q: int) -> tuple:
    questions = {}
    with pdfplumber.open(str(pdf_path)) as pdf:
        answers = parse_answers(pdf, max_q)
        subject_state = [1]
        # 정답 페이지(마지막)와 정답 혼합 페이지 모두 처리하되,
        # 마지막 페이지에도 문제가 있을 수 있으므로 전체 파싱
        for page in pdf.pages:
            left, right = extract_columns(page)
            for col in (left, right):
                col = filter_lines(col)
                for block in lines_to_blocks(col, subject_state, max_q):
                    q = block_to_question(block)
                    if q and q['no'] not in questions:
                        questions[q['no']] = q
    return questions, answers


def process_file(pdf_path: Path, max_q: int, subj_map: dict, id_start: int) -> list:
    m = re.search(r'(\d{8})', pdf_path.name)
    date = m.group(1) if m else 'unknown'
    print(f"  파싱...", end=' ', flush=True)
    questions, answers = parse_exam(pdf_path, max_q)
    print(f"{len(questions)}문항  정답 {len(answers)}개", end='  ')

    records = []
    for no in sorted(questions):
        if no not in answers:
            continue
        q = questions[no]
        records.append({
            "id":           id_start + len(records),
            "date":         date,
            "subject":      q['subject'],
            "subject_name": subj_map.get(q['subject'], f"{q['subject']}과목"),
            "question_no":  no,
            "question":     q['question'],
            "choices":      q['choices'],
            "answers":      [answers[no]],
            "explanation":  "",
        })
    print(f"-> {len(records)}문항")
    return records


# ── 메인 ──────────────────────────────────────────────────────

errors = []

for cfg in EXAM_TARGETS:
    folder = BASE / cfg['folder']
    if not folder.exists():
        print(f"\n[{cfg['key']}] 폴더 없음 — 스킵")
        continue

    # 학생용/교사용 모두 수집
    pdfs = sorted(folder.glob('*.pdf'))
    if not pdfs:
        print(f"\n[{cfg['key']}] 파일 없음 — 스킵")
        continue

    print(f"\n{'='*60}")
    print(f"[{cfg['key']}] {cfg['folder']} — {len(pdfs)}개 파일")

    # 과목명 동적 추출
    subj_map = collect_subject_names(pdfs)
    if subj_map:
        print(f"  과목: {subj_map}")

    all_records, id_cnt = [], 1
    for pdf_path in pdfs:
        m = re.search(r'(\d{8})', pdf_path.name)
        date = m.group(1) if m else '?'
        print(f"\n  -- {date} ({pdf_path.name[:30]}) --")
        try:
            recs = process_file(pdf_path, cfg['max_q'], subj_map, id_start=id_cnt)
            all_records.extend(recs)
            id_cnt += len(recs)
        except Exception as e:
            msg = f"{cfg['key']} {date}: {e}"
            print(f"  [ERROR] {msg}")
            errors.append(msg)

    out_path = OUT_DIR / cfg['out']
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)
    print(f"\n  완료: 총 {len(all_records)}문항 → {out_path.name}")

    if all_records:
        s = all_records[0]
        print(f"  [샘플] {s['date']} {s['question_no']}번 ({s.get('subject_name','')})")
        print(f"    Q: {s['question'][:70]}")

print(f"\n\n{'='*60}")
if errors:
    print(f"오류 {len(errors)}건:")
    for e in errors:
        print(f"  - {e}")
else:
    print("전체 완료 — 오류 없음")
