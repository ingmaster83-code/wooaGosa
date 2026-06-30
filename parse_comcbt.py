#!/usr/bin/env python3
"""
comcbt.com / cbtestpro.kr 기출문제 PDF 통합 파서
- 문제지/ 폴더를 자동 스캔 (하드코딩 없음)
- 자격증 등급에 따라 max_q 자동 설정
- 교사용 우선 / 날짜별 중복 제거
- 그림·도면·파형 포함 문제 자동 제외
"""

import pdfplumber, json, re, sys, threading
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE    = Path(r"C:\개인\wooahouse\wooaGosa\문제지")
OUT_DIR = Path(r"C:\개인\wooahouse\wooaGosa\data")
OUT_DIR.mkdir(exist_ok=True)

# ── 상수 ──────────────────────────────────────────────────────
CIRCLE_MAP = {
    '①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5,  # 속빈 원 (U+2460)
    '❶': 1, '❷': 2, '❸': 3, '❹': 4, '❺': 5,  # 채워진 원 (U+2776)
}
CIRCLE_PAT = re.compile(r'[①②③④⑤❶❷❸❹❺]')

# 시각 자료가 필요한 문제 제외 (이미지 추출 불가)
IMAGE_PAT = re.compile(
    r'다음\s*그림|아래\s*그림|그림과\s*같|그림에서|그림을\s*보|그림.*참[고조]|'
    r'도면을\s*보|도면에서|도면과\s*같|도면.*참[고조]|'
    r'파형이.*같|파형을\s*보|파형에서|'
    r'회로도|회로\s*그림|'
    r'그래프에서|그래프와\s*같|그래프를\s*보'
)

# comcbt / cbtestpro 헤더·광고 필터
HEADER_PAT = re.compile(
    r'전자문제집\s*CBT|www\.comcbt\.com|comcbt\.com|'
    r'기출문제\s*및\s*해설집|CBT\s*홈페이지|CBT\s*앱|구글플레이|'
    r'PC\s*버전.*모바일|교사용.*학생용|오답.*수정|최신.*자료|'
    r'최강\s*자격증|모의고사.*오답.*노트|OMR\s*형식|종이\s*문제집|'
    r'실제.*시험.*사용|완벽\s*연동|관리기능|해설집\s*다운로드'
)

# ── 폴더 스킵 목록 (별도 파서 또는 비-CBT 자료) ──────────────
SKIP_FOLDERS = {
    # reparse_5choice.py 로 별도 처리
    '공인중개사 1차', '공인중개사 2차',
    '사회복지사1급 1교시', '사회복지사1급 2교시', '사회복지사1급 3교시',
    # 비-CBT (문제은행 형식)
    '운전면허',
    # 자체 파싱 형식
    '한국사 기본', '한국사 심화',
}

# ── 기존 자격증 폴더명 → JSON 키 매핑 (하위 호환 유지) ─────────
FOLDER_TO_KEY = {
    '네트워크관리사 1급':         'net_1',
    '네트워크관리사 2급':         'net_2',
    '리눅스마스터 1급':           'linux_1',
    '리눅스마스터 2급':           'linux_2',
    '워드프로세서':               'word',
    '전기기사':                  'elec_eng',
    '전기산업기사':               'elec_ind',
    '정보처리기사':               'info_proc',
    '정보처리산업기사':            'info_ind',
    '정보보안기사':               'info_sec',
    '위험물산업기사':              'hazmat_ind',
    '위험물기능사':               'hazmat_craft',
    '소방설비기사 기계분야':        'fire_mech',
    '소방설비기사 전기분야':        'fire_elec',
    '소방설비기사(기계분야)':       'fire_mech',
    '소방설비기사(전기분야)':       'fire_elec',
    '지게차운전기능사':            'forklift',
    '굴착기(굴삭기)운전기능사':     'excavator',
    '굴착기운전기능사':            'excavator',
    '산업안전산업기사':            'safety_ind',
    '산업안전기사':               'safety_eng',
    '전기기능사':                 'elec_craft',
    '제과기능사':                 'pastry',
    '제빵기능사':                 'bread',
    '한식조리기능사':              'korean_cook',
    '가스기능사':                 'gas_craft',
    '가스산업기사':               'gas_ind',
    '가스기사':                   'gas_eng',
    '건설안전산업기사':            'const_safety_ind',
    '건설안전기사':               'const_safety_eng',
    '공조냉동기계기능사':           'hvac_craft',
    '공조냉동기계기사':            'hvac_eng',
    '대기환경기사':               'air_eng',
    '수질환경기사':               'water_eng',
    '승강기기능사':               'elevator_craft',
    '승강기기사':                 'elevator_eng',
    '에너지관리기능사':            'energy_craft',
    '에너지관리기사':              'energy_eng',
}


# ── 자동 설정 헬퍼 ────────────────────────────────────────────

def get_key(folder_name: str) -> str:
    """폴더명 → JSON 키. 기존 매핑 우선, 없으면 한글 그대로 사용."""
    if folder_name in FOLDER_TO_KEY:
        return FOLDER_TO_KEY[folder_name]
    safe = re.sub(r'[\s/\\()·]', '_', folder_name)
    safe = re.sub(r'_+', '_', safe).strip('_')
    return safe


def get_max_q(folder_name: str) -> int:
    """자격증 등급별 문항 수 자동 설정."""
    if '기능사' in folder_name or '기능장' in folder_name:
        return 60
    if '산업기사' in folder_name:
        return 80
    if '기사' in folder_name:
        return 100
    # 관리사, 전문가, 이용사, 미용사 등 기타
    return 100


def build_exam_targets() -> list:
    """문제지/ 폴더를 스캔해서 처리 대상 목록 자동 생성."""
    targets = []
    for folder in sorted(BASE.iterdir()):
        if not folder.is_dir():
            continue
        name = folder.name
        if name in SKIP_FOLDERS:
            continue
        if not any(folder.glob('*.pdf')):
            continue
        key = get_key(name)
        targets.append({
            'key':    key,
            'folder': name,
            'out':    f'{key}.json',
            'max_q':  get_max_q(name),
        })
    return targets


# ── 정답 그리드 파싱 ──────────────────────────────────────────

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


def _extract_answer_grid(lines: list, max_q: int) -> dict:
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


def parse_answers(pdf, max_q: int) -> dict:
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


# ── 컬럼 추출 ─────────────────────────────────────────────────

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


# ── 과목명 동적 추출 ──────────────────────────────────────────

def collect_subject_names(pdfs: list) -> dict:
    subj_map = {}
    for pdf_path in pdfs[:3]:
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
        sm = re.match(r'^(\d+)과목\s*[:：]\s*', line)
        if sm:
            subject_state[0] = int(sm.group(1))
            continue
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
    if IMAGE_PAT.search(question):
        return None  # 그림/도면/파형 등 시각 자료 필요 문제 제외

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


# ── 날짜별 중복 제거 (교사용 우선) ───────────────────────────

def select_pdfs(pdfs: list) -> list:
    by_date = {}
    for pdf in pdfs:
        m = re.search(r'(\d{8})', pdf.name)
        if not m:
            continue
        date = m.group(1)
        is_teacher = '교사용' in pdf.name or re.search(r'\d{8}-0\.', pdf.name)
        is_student = '학생용' in pdf.name
        if date not in by_date:
            by_date[date] = pdf
        elif is_student:
            # 학생용 우선 (①②③④ 속빈 원 사용 → 파싱 오류 적음)
            by_date[date] = pdf
        elif is_teacher and '학생용' not in by_date[date].name:
            # 학생용 없을 때만 교사용으로 대체
            by_date[date] = pdf
    return sorted(by_date.values(), key=lambda p: p.name)


# ── 파일 파싱 ─────────────────────────────────────────────────

def parse_exam(pdf_path: Path, max_q: int) -> tuple:
    questions = {}
    with pdfplumber.open(str(pdf_path)) as pdf:
        answers = parse_answers(pdf, max_q)
        subject_state = [1]
        for page in pdf.pages:
            left, right = extract_columns(page)
            for col in (left, right):
                col = filter_lines(col)
                for block in lines_to_blocks(col, subject_state, max_q):
                    q = block_to_question(block)
                    if q and q['no'] not in questions:
                        questions[q['no']] = q
    return questions, answers


PDF_TIMEOUT = 60  # 초 — 이 시간 초과 시 해당 PDF 스킵


def parse_exam_timeout(pdf_path: Path, max_q: int):
    """타임아웃 적용 parse_exam (깨진 PDF 무한 대기 방지)."""
    result = [None]
    error  = [None]

    def _run():
        try:
            result[0] = parse_exam(pdf_path, max_q)
        except Exception as e:
            error[0] = e

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    t.join(PDF_TIMEOUT)

    if t.is_alive():
        raise TimeoutError(f"{PDF_TIMEOUT}초 초과 — 스킵")
    if error[0]:
        raise error[0]
    return result[0]


def process_file(pdf_path: Path, max_q: int, subj_map: dict, id_start: int) -> list:
    m = re.search(r'(\d{8})', pdf_path.name)
    date = m.group(1) if m else 'unknown'
    print(f"  파싱...", end=' ', flush=True)
    parsed = parse_exam_timeout(pdf_path, max_q)
    questions, answers = parsed
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

EXAM_TARGETS = build_exam_targets()
print(f"대상 자격증: {len(EXAM_TARGETS)}개\n")

errors = []

for cfg in EXAM_TARGETS:
    folder = BASE / cfg['folder']

    out_path = OUT_DIR / cfg['out']

    if out_path.exists():
        print(f"[{cfg['key']}] 완료 — 스킵")
        continue

    all_pdfs = sorted(folder.glob('*.pdf'))
    pdfs = select_pdfs(all_pdfs)

    print(f"\n{'='*60}")
    print(f"[{cfg['key']}] {cfg['folder']}  max_q={cfg['max_q']}")
    print(f"  전체 {len(all_pdfs)}개 → 날짜 중복 제거 후 {len(pdfs)}개 처리")

    subj_map = collect_subject_names(pdfs)
    if subj_map:
        print(f"  과목: {subj_map}")

    all_records, id_cnt = [], 1
    for pdf_path in pdfs:
        m = re.search(r'(\d{8})', pdf_path.name)
        date = m.group(1) if m else '?'
        print(f"\n  -- {date} ({pdf_path.name[:40]}) --")
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
        print(f"  [샘플] {s['date']} {s['question_no']}번: {s['question'][:60]}")

print(f"\n\n{'='*60}")
if errors:
    print(f"오류 {len(errors)}건:")
    for e in errors:
        print(f"  - {e}")
else:
    print("전체 완료 — 오류 없음")
