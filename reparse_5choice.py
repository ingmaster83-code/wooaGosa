"""
공인중개사·사회복지사1급 5지선다 재파싱 스크립트
CIRCLE_MAP에 ⑤ 추가, len(choices) 4 또는 5 허용
"""
import sys, json, re, pdfplumber
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE    = Path(r"C:\개인\wooahouse\wooaGosa\문제지")
OUT_DIR = Path(r"C:\개인\wooahouse\wooaGosa\data")

CIRCLE_MAP = {'①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5}
CIRCLE_PAT = re.compile(r'[①②③④⑤]')

IMAGE_PAT = re.compile(
    r'다음\s*그림|아래\s*그림|그림과\s*같|그림에서|그림을\s*보|그림.*참[고조]|'
    r'도면을\s*보|도면에서|도면과\s*같|도면.*참[고조]|'
    r'파형이.*같|파형을\s*보|파형에서|'
    r'회로도|회로\s*그림|'
    r'그래프에서|그래프와\s*같|그래프를\s*보'
)

HEADER_PAT = re.compile(
    r'전자문제집\s*CBT|www\.comcbt\.com|comcbt\.com|'
    r'기출문제\s*및\s*해설집|CBT\s*홈페이지|CBT\s*앱|구글플레이|'
    r'PC\s*버전.*모바일|교사용.*학생용|오답.*수정|최신.*자료|'
    r'최강\s*자격증|모의고사.*오답.*노트|OMR\s*형식|종이\s*문제집|'
    r'실제.*시험.*사용|완벽\s*연동|관리기능|해설집\s*다운로드'
)

TARGETS = [
    {'key': 'realtor_1', 'folder': '공인중개사 1차',     'out': 'realtor_1.json',  'max_q': 80},
    {'key': 'realtor_2', 'folder': '공인중개사 2차',     'out': 'realtor_2.json',  'max_q': 120},
    {'key': 'welfare_1', 'folder': '사회복지사1급 1교시', 'out': 'welfare_1.json',  'max_q': 50},
    {'key': 'welfare_2', 'folder': '사회복지사1급 2교시', 'out': 'welfare_2.json',  'max_q': 75},
    {'key': 'welfare_3', 'folder': '사회복지사1급 3교시', 'out': 'welfare_3.json',  'max_q': 75},
]


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


def filter_lines(lines):
    return [l for l in lines if l.strip() and not HEADER_PAT.search(l)]


def _extract_answer_grid(lines, max_q):
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


def parse_answers(pdf, max_q):
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


def extract_columns(page):
    words = page.extract_words(x_tolerance=3, y_tolerance=3)
    if not words:
        return [], []
    mid_x = page.width / 2
    left  = words_to_lines([w for w in words if w['x0'] <  mid_x])
    right = words_to_lines([w for w in words if w['x0'] >= mid_x])
    return left, right


def lines_to_blocks(lines, subject_state, max_q):
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
                        r'잘못|옳지|알맞은|적합|적절|올바르|해설|의미|정의|특징|방법|'
                        r'고르|모두|없는|있는|같은|다른|속하|순서|바른|바르|구성|유형|'
                        r'해당|조건|기준|단계|원칙|근거|이유|목적|효과|역할|기능',
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


def block_to_question(block):
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
        'no': block['no'],
        'subject': block['subject'],
        'question': question,
        'choices': choices,
    }


def select_pdfs(pdfs: list) -> list:
    """날짜별 중복 제거 — 교사용(-0) 우선"""
    by_date = {}
    for pdf in pdfs:
        m = re.search(r'(\d{8})', pdf.name)
        if not m:
            continue
        date = m.group(1)
        is_teacher = '교사용' in pdf.name or re.search(r'\d{8}-0\.', pdf.name)
        if date not in by_date or is_teacher:
            by_date[date] = pdf
    return sorted(by_date.values(), key=lambda p: p.name)


def parse_exam(pdf_path, max_q):
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


def collect_subject_names(pdfs):
    subj_map = {}
    for pdf_path in pdfs[:3]:
        try:
            with pdfplumber.open(str(pdf_path)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text() or ''
                    for m in re.finditer(r'(\d+)과목\s*[:：]\s*([^\n\r①②③④⑤\d]{2,25})', text):
                        no   = int(m.group(1))
                        name = m.group(2).strip().rstrip('◐').strip()
                        if no not in subj_map and name:
                            subj_map[no] = name
        except Exception:
            pass
    return subj_map


for cfg in TARGETS:
    folder = BASE / cfg['folder']
    if not folder.exists():
        print(f"[{cfg['key']}] 폴더 없음 — 스킵")
        continue

    all_pdfs = sorted(folder.glob('*.pdf'))
    if not all_pdfs:
        print(f"[{cfg['key']}] 파일 없음 — 스킵")
        continue
    pdfs = select_pdfs(all_pdfs)
    print(f"  전체 {len(all_pdfs)}개 중 {len(pdfs)}개 선택 (날짜 중복 제거)")

    print(f"\n[{cfg['key']}] {cfg['folder']} — {len(pdfs)}개 파일")
    subj_map = collect_subject_names(pdfs)
    if subj_map:
        print(f"  과목: {subj_map}")

    all_records, id_cnt = [], 1
    for pdf_path in pdfs:
        m = re.search(r'(\d{8})', pdf_path.name)
        date = m.group(1) if m else '?'
        try:
            questions, answers = parse_exam(pdf_path, cfg['max_q'])
            recs = []
            for no in sorted(questions):
                if no not in answers:
                    continue
                q = questions[no]
                recs.append({
                    "id":           id_cnt + len(recs),
                    "date":         date,
                    "subject":      q['subject'],
                    "subject_name": subj_map.get(q['subject'], f"{q['subject']}과목"),
                    "question_no":  no,
                    "question":     q['question'],
                    "choices":      q['choices'],
                    "answers":      [answers[no]],
                    "explanation":  "",
                })
            all_records.extend(recs)
            id_cnt += len(recs)
            print(f"  {date}: Q={len(questions)} A={len(answers)} -> {len(recs)}문항")
        except Exception as e:
            print(f"  {date}: ERROR {e}")

    out_path = OUT_DIR / cfg['out']
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)
    print(f"  => 총 {len(all_records)}문항 저장 → {out_path.name}")

print("\n완료")
