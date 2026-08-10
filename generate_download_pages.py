# -*- coding: utf-8 -*-
"""
문제은행 다운로드 페이지 자동 생성기
data/*.json (302개 시험) -> download-{key}.html
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
PDF_DIR = ROOT / "문제지"

# data 키 -> 문제지 폴더명이 NAME_MAP과 다른 예외 케이스
PDF_FOLDER_OVERRIDE = {
    'excavator': '굴착기(굴삭기)운전기능사',
    'history_advanced': '한국사 심화',
    'history_basic': '한국사 기본',
    'license_1_2': '운전면허',
    'motorcycle': '운전면허',
    'motorbike': '운전면허',
    '미용사_네일': '미용사(네일)',
    '미용사_일반': '미용사(일반)',
    '미용사_피부': '미용사(피부)',
    '생물분류기사_동물': '생물분류기사(동물)',
    '생물분류기사_식물': '생물분류기사(식물)',
    '신재생에너지발전설비기능사_태양광': '신재생에너지발전설비기능사(태양광)',
    '신재생에너지발전설비기사_태양광': '신재생에너지발전설비기사(태양광)',
    '컴퓨터활용능력_1급': '컴퓨터활용능력 1급',
    '컴퓨터활용능력_2급': '컴퓨터활용능력 2급',
}

# 운전면허 폴더 안에서 license_1_2/motorcycle을 구분하는 키워드
PDF_KIND_HINT = {
    'license_1_2': '면허1-2종',
    'motorcycle': '이륜자동차',
}

# 영문 키 -> 한글 표시명 (js/exam.js TYPE_LABELS 재사용)
NAME_MAP = {
    '1jong-daebyeong': '1종 대형', '1jong-botong': '1종 보통', '2jong-botong': '2종 보통',
    'motorcycle': '2종 소형(이륜)', 'motorbike': '원동기장치자전거', 'license_1_2': '1·2종 면허',
    'history_basic': '한국사능력검정시험 기본', 'history_advanced': '한국사능력검정시험 심화',
    'computer_1': '컴퓨터활용능력 1급', 'computer_2': '컴퓨터활용능력 2급',
    'net_1': '네트워크관리사 1급', 'net_2': '네트워크관리사 2급',
    'linux_1': '리눅스마스터 1급', 'linux_2': '리눅스마스터 2급',
    'word': '워드프로세서', 'elec_eng': '전기기사', 'elec_ind': '전기산업기사',
    'info_proc': '정보처리기사', 'info_ind': '정보처리산업기사', 'info_sec': '정보보안기사',
    'hazmat_ind': '위험물산업기사', 'hazmat_craft': '위험물기능사',
    'fire_mech': '소방설비기사 기계분야', 'fire_elec': '소방설비기사 전기분야',
    'forklift': '지게차운전기능사', 'excavator': '굴착기운전기능사',
    'realtor_1': '공인중개사 1차', 'realtor_2': '공인중개사 2차',
    'welfare_1': '사회복지사1급 1교시', 'welfare_2': '사회복지사1급 2교시', 'welfare_3': '사회복지사1급 3교시',
    'safety_ind': '산업안전산업기사', 'safety_eng': '산업안전기사',
    'elec_craft': '전기기능사', 'pastry': '제과기능사', 'bread': '제빵기능사',
    'korean_cook': '한식조리기능사', 'gas_craft': '가스기능사', 'gas_ind': '가스산업기사', 'gas_eng': '가스기사',
    'const_safety_ind': '건설안전산업기사', 'const_safety_eng': '건설안전기사',
    'hvac_craft': '공조냉동기계기능사', 'hvac_eng': '공조냉동기계기사',
    'air_eng': '대기환경기사', 'water_eng': '수질환경기사',
    'elevator_craft': '승강기기능사', 'elevator_eng': '승강기기사',
    'energy_craft': '에너지관리기능사', 'energy_eng': '에너지관리기사',
}

PAGE_TMPL = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9ZGENFSXWC"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-9ZGENFSXWC');
  </script>
  <meta name="naver-site-verification" content="e97ec06f3d64c3b7795ba7724e1f0be02a26fb41" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="img/icon.svg" type="image/svg+xml">
  <title>{name} 기출문제 PDF 다운로드 - 문제은행 | 우아고사</title>
  <meta name="description" content="{name} 기출문제 {qcount}문항({rcount}개 회차) 무료 다운로드. 원본 PDF 그대로, 회차별로 골라서 다운로드하세요.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://wooagosa.wooahouse.com/download-{key}.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{name} 기출문제 PDF 다운로드 - 문제은행 | 우아고사">
  <meta property="og:description" content="{name} 기출문제 {qcount}문항({rcount}개 회차) 무료 다운로드. 원본 PDF 그대로, 회차별로 골라서 다운로드하세요.">
  <meta property="og:url" content="https://wooagosa.wooahouse.com/download-{key}.html">
  <meta property="og:locale" content="ko_KR">
  <meta property="og:site_name" content="WooaGosa">
  <link rel="manifest" href="manifest.json">
  <meta name="theme-color" content="#1a3a5c">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css?v=4">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6464921081676309" crossorigin="anonymous"></script>
</head>
<body>

<header class="site-header">
  <div class="header-inner">
    <a href="index.html" class="logo">
      <span class="logo-icon">🚛</span>
      Wooa<span>Gosa</span>
    </a>
    <nav class="header-nav">
      <a href="index.html">홈</a>
      <a href="wrong-notes.html">오답노트</a>
    </nav>
  </div>
</header>

<script src="js/wooa-sites-bar.js"></script>

<section class="hero" style="padding:2rem 1.25rem 1.5rem;">
  <h1>{name} 문제은행 다운로드</h1>
  <div class="hero-badges">
    <span class="badge">📚 총 {qcount}문항</span>
    <span class="badge">🗓 {rcount}개 회차</span>
    <span class="badge">✅ 정답 포함</span>
    <span class="badge">🆓 무료</span>
  </div>
</section>

<main>

  <div class="mobile-top-ad">
    <ins class="adsbygoogle"
         style="display:block;width:100%;height:80px"
         data-ad-client="ca-pub-6464921081676309"
         data-ad-slot="7080296704"
         data-ad-format="auto"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
  </div>

<nav class="breadcrumb" aria-label="breadcrumb">
  <a href="index.html">홈</a> &rsaquo; <span>{name} 문제은행 다운로드</span>
</nav>

  <div class="page-with-sidebar">
    <div class="gosa-main">

      <!-- 광고 -->
      <div class="ad-slot" style="margin-bottom:1.5rem;">
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-6464921081676309"
             data-ad-slot="1419180025"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>

      <div class="dl-static-preview">
        <h2 class="section-title">🛕 최신 회차 미리보기</h2>
        <p style="font-size:.85rem;color:var(--text-mid);margin-bottom:.75rem;">{latest_date_label} 시행 문제 중 일부입니다.</p>
        {static_preview_html}
      </div>

      <div class="exam-schedule-box">
        <span class="sch-label">✏️ 실전처럼 풀어보고 싶다면</span>
        <div class="exam-link-btns">
          <a href="{mock_exam_link}" class="exam-link-btn">모의고사 바로 풀기 ↗</a>
        </div>
      </div>

      <!-- 광고 -->
      <div class="ad-slot" style="margin-bottom:1.5rem;">
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-6464921081676309"
             data-ad-slot="6255378195"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>

      <div class="round-select-box">
        <div class="round-select-head">
          <h2 class="section-title" style="margin:0;">📥 회차 선택해서 다운로드</h2>
        </div>
        <p style="font-size:.82rem;color:var(--text-mid);margin:-.3rem 0 .75rem;">회차 하나를 선택하고 버튼을 누르면 새 탭에서 원본 PDF를 미리보고 다운로드할 수 있습니다.</p>
        <div class="round-list" id="roundList"></div>
        <div class="sel-count-bar">
          <span id="selCount" style="font-size:.85rem;color:var(--text-mid);">선택: 0개 회차 · PDF 0개</span>
          <button class="btn btn-primary btn-lg" id="dlBtn" disabled>📥 선택 회차 PDF 미리보기</button>
        </div>
      </div>

      <div class="dl-static-preview">
        <h2 class="section-title">자주 묻는 질문</h2>
        <details style="margin-bottom:.6rem;">
          <summary style="cursor:pointer;font-weight:600;">이 문제은행은 어디서 가져온 데이터인가요?</summary>
          <p style="margin-top:.4rem;color:var(--text-mid);font-size:.88rem;">공개된 기출문제 자료를 우아고사가 직접 수집한 원본 PDF입니다. 가공 없이 원본 그대로 제공되며, 실제 시행처 문제·정답과 다를 수 있으니 참고용으로 활용하세요.</p>
        </details>
        <details style="margin-bottom:.6rem;">
          <summary style="cursor:pointer;font-weight:600;">다운로드하면 어떤 형식으로 받아지나요?</summary>
          <p style="margin-top:.4rem;color:var(--text-mid);font-size:.88rem;">회차를 선택하고 버튼을 누르면 새 탭에서 원본 PDF를 먼저 미리볼 수 있고, 그 화면의 다운로드 버튼을 누르면 별도의 가공·변환 없이 실제 시험지·정답표 파일이 그대로 다운로드됩니다.</p>
        </details>
        <details>
          <summary style="cursor:pointer;font-weight:600;">모바일에서도 다운로드되나요?</summary>
          <p style="margin-top:.4rem;color:var(--text-mid);font-size:.88rem;">네, 모바일 브라우저에서도 동일하게 새 탭에서 미리보기 후 PDF 파일이 다운로드되며, 기기의 다운로드 폴더나 파일 앱에서 확인할 수 있습니다.</p>
        </details>
      </div>

    </div>
    <aside class="tool-sidebar">
      <div class="ad-card">
        <ins class="adsbygoogle"
             style="display:block;width:100%;min-height:250px"
             data-ad-client="ca-pub-6464921081676309"
             data-ad-slot="7080296704"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>
    </aside>
  </div>

</main>

<footer class="site-footer">
  <div class="footer-inner">
    <p>&copy; 2026 WooaGosa. 본 문제은행은 참고용이며 실제 시험과 다를 수 있습니다.</p>
  </div>
</footer>

<script>
window.EXAM_DL_META = {{ name: {name_json}, key: {key_json} }};
window.EXAM_DL_QUESTIONS = {questions_json};
window.EXAM_DL_PDFS = {pdfs_json};
</script>
<script src="js/download-bank.js"></script>
<script src="js/ad-dev-placeholder.js"></script>

</body>
</html>
"""


def strip_html(text):
    return (text or "").replace("\n", " ").strip()


def render_static_question(q, idx):
    choices = q.get("choices", {}) or {}
    answers = q.get("answers", []) or []
    choices_html = "".join(
        f'<div class="choice-item{" correct-choice" if int(num) in answers else ""}">{num}. {text}</div>'
        for num, text in choices.items()
    )
    return f'''<div class="preview-q">
      <div class="q-meta">{q.get("question_no", idx)}번</div>
      <div class="q-text">{q.get("question", "")}</div>
      <div class="q-choices">{choices_html}</div>
      <div class="q-answer">✅ 정답: {", ".join(str(a) for a in answers)}번</div>
    </div>'''


import re as _re

_STD_PATTERN = _re.compile(r"^wooagosa-(\d{8})-(.+)-(교사용|학생용)\.pdf$")
_HISTORY_PATTERN = _re.compile(r"^wooagosa-(\d+)회-한국사(기본|심화)-(문제지|정답표)\.pdf$")
_LICENSE_PATTERN = _re.compile(r"^wooagosa-(\d{8})-운전면허-(.+)\.pdf$")


def build_pdf_index(key):
    """{date_key: [{kind, path}, ...]} 를 반환. date_key='' 는 회차 구분 없는 단일 자료 묶음."""
    folder_name = PDF_FOLDER_OVERRIDE.get(key, NAME_MAP.get(key, key))
    folder = PDF_DIR / folder_name
    if not folder.is_dir():
        return {}

    index = {}
    kind_hint = PDF_KIND_HINT.get(key)

    for pdf in sorted(folder.glob("wooagosa-*.pdf")):
        rel_path = f"문제지/{folder_name}/{pdf.name}"

        m = _STD_PATTERN.match(pdf.name)
        if m and folder_name not in ("운전면허",):
            date, _exam, kind = m.groups()
            index.setdefault(date, []).append({"kind": kind, "path": rel_path})
            continue

        m = _HISTORY_PATTERN.match(pdf.name)
        if m:
            round_no, _level, doc_type = m.groups()
            index.setdefault("", []).append({"kind": f"{round_no}회 {doc_type}", "path": rel_path})
            continue

        m = _LICENSE_PATTERN.match(pdf.name)
        if m and folder_name == "운전면허":
            _date, kind_part = m.groups()
            if kind_hint and kind_hint not in kind_part:
                continue
            index.setdefault("", []).append({"kind": kind_part, "path": rel_path})
            continue

    return index


def build_page(key, questions):
    name = NAME_MAP.get(key, key)
    dates = sorted(set(q.get("date", "") for q in questions if q.get("date")), reverse=True)
    qcount = len(questions)

    pdf_index = build_pdf_index(key)
    pdf_rounds = [d for d, files in pdf_index.items() if files]
    rcount = len(pdf_rounds) if pdf_rounds else (len(dates) if dates else 1)

    if dates:
        latest_date = dates[0]
        latest_questions = [q for q in questions if q.get("date") == latest_date][:5]
        y, m, d = latest_date[:4], latest_date[4:6], latest_date[6:8]
        latest_date_label = f"{y}년 {int(m)}월 {int(d)}일"
    else:
        latest_questions = questions[:5]
        latest_date_label = "최신"

    static_preview_html = "".join(render_static_question(q, i) for i, q in enumerate(latest_questions, 1))
    if len(questions) > 5:
        static_preview_html += f'<p class="preview-more">…외 {qcount - len(latest_questions)}문항은 아래에서 회차를 선택해 확인하세요.</p>'

    mock_exam_link = f"exam-{key}.html" if (ROOT / f"exam-{key}.html").exists() else "index.html"

    html = PAGE_TMPL.format(
        name=name,
        key=key,
        qcount=qcount,
        rcount=rcount,
        latest_date_label=latest_date_label,
        static_preview_html=static_preview_html,
        mock_exam_link=mock_exam_link,
        name_json=json.dumps(name, ensure_ascii=False),
        key_json=json.dumps(key, ensure_ascii=False),
        questions_json=json.dumps(questions, ensure_ascii=False),
        pdfs_json=json.dumps(pdf_index, ensure_ascii=False),
    )
    return html, name, qcount, rcount, bool(pdf_rounds)


LIST_PAGE_TMPL = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9ZGENFSXWC"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-9ZGENFSXWC');
  </script>
  <meta name="naver-site-verification" content="e97ec06f3d64c3b7795ba7724e1f0be02a26fb41" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="img/icon.svg" type="image/svg+xml">
  <title>전국 자격증 기출문제 문제은행 다운로드 모음 ({count}개 시험) | 우아고사</title>
  <meta name="description" content="{count}개 자격증·시험 기출문제를 회차별로 골라 무료 다운로드. 정답 포함 문제은행, 인쇄·PDF 저장 지원.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://wooagosa.wooahouse.com/question-bank.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="전국 자격증 기출문제 문제은행 다운로드 모음 ({count}개 시험) | 우아고사">
  <meta property="og:description" content="{count}개 자격증·시험 기출문제를 회차별로 골라 무료 다운로드. 정답 포함 문제은행, 인쇄·PDF 저장 지원.">
  <meta property="og:url" content="https://wooagosa.wooahouse.com/question-bank.html">
  <meta property="og:locale" content="ko_KR">
  <meta property="og:site_name" content="WooaGosa">
  <link rel="manifest" href="manifest.json">
  <meta name="theme-color" content="#1a3a5c">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css?v=4">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6464921081676309" crossorigin="anonymous"></script>
  <style>
    .bank-search-wrap {{ max-width:640px; margin:0 auto 1.5rem; padding:0 1.25rem; }}
    .bank-search-box {{ width:100%; padding:.85rem 1.1rem; border:1.5px solid var(--border); border-radius:var(--radius); font-size:.95rem; }}
    .bank-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:.75rem; }}
    .bank-card {{ display:block; background:var(--card-bg); border:1.5px solid var(--border); border-radius:var(--radius-sm); padding:1rem 1.1rem; text-decoration:none; transition:var(--trans); }}
    .bank-card:hover {{ border-color:var(--blue); box-shadow:var(--shadow); }}
    .bank-card-name {{ font-weight:700; color:var(--navy); font-size:.92rem; margin-bottom:.3rem; }}
    .bank-card-meta {{ font-size:.78rem; color:var(--text-lt); }}
  </style>
</head>
<body>

<header class="site-header">
  <div class="header-inner">
    <a href="index.html" class="logo"><span class="logo-icon">🚛</span>Wooa<span>Gosa</span></a>
    <nav class="header-nav"><a href="index.html">홈</a><a href="wrong-notes.html">오답노트</a></nav>
  </div>
</header>

<script src="js/wooa-sites-bar.js"></script>

<section class="hero" style="padding:2rem 1.25rem 1.5rem;">
  <h1>전국 자격증 문제은행 다운로드</h1>
  <div class="hero-badges">
    <span class="badge">📚 {count}개 시험</span>
    <span class="badge">✅ 정답 포함</span>
    <span class="badge">🆓 무료</span>
  </div>
</section>

<main>
  <div class="mobile-top-ad">
    <ins class="adsbygoogle" style="display:block;width:100%;height:80px" data-ad-client="ca-pub-6464921081676309" data-ad-slot="7080296704" data-ad-format="auto"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
  </div>

  <div class="bank-search-wrap">
    <input type="text" id="bankSearch" class="bank-search-box" placeholder="시험명 검색 (예: 전기기사, 지게차)">
  </div>

  <div class="page-with-sidebar">
    <div class="gosa-main">
      <div class="bank-grid" id="bankGrid">
{cards_html}
      </div>
    </div>
    <aside class="tool-sidebar">
      <div class="ad-card">
        <ins class="adsbygoogle" style="display:block;width:100%;min-height:250px" data-ad-client="ca-pub-6464921081676309" data-ad-slot="6255378195" data-ad-format="auto" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>
    </aside>
  </div>
</main>

<footer class="site-footer">
  <div class="footer-inner"><p>&copy; 2026 WooaGosa. 본 문제은행은 참고용이며 실제 시험과 다를 수 있습니다.</p></div>
</footer>

<script>
document.getElementById('bankSearch').addEventListener('input', function(e) {{
  const q = e.target.value.trim().toLowerCase();
  document.querySelectorAll('#bankGrid .bank-card').forEach(function(card) {{
    const name = card.dataset.name || '';
    card.style.display = (!q || name.indexOf(q) !== -1) ? '' : 'none';
  }});
}});
</script>

</body>
</html>
"""


def build_list_page(entries):
    cards = []
    for key, name, qcount, rcount in entries:
        cards.append(
            f'        <a class="bank-card" href="download-{key}.html" data-name="{name.lower()}">'
            f'<div class="bank-card-name">{name}</div>'
            f'<div class="bank-card-meta">📚 {qcount}문항 · 🗓 {rcount}개 회차</div></a>'
        )
    return LIST_PAGE_TMPL.format(count=len(entries), cards_html="\n".join(cards))


def main():
    files = sorted(DATA_DIR.glob("*.json"))
    ok = 0
    skipped = 0
    entries = []
    no_pdf_keys = []
    for f in files:
        key = f.stem
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  [스킵] {key}: JSON 파싱 오류 {e}")
            skipped += 1
            continue

        if isinstance(data, dict):
            questions = []
            for v in data.values():
                if isinstance(v, list):
                    questions.extend(v)
        elif isinstance(data, list):
            questions = data
        else:
            questions = []

        if not questions:
            print(f"  [스킵] {key}: 문제 없음")
            skipped += 1
            continue

        html, name, qcount, rcount, has_pdfs = build_page(key, questions)
        out_path = ROOT / f"download-{key}.html"
        out_path.write_text(html, encoding="utf-8")
        entries.append((key, name, qcount, rcount))
        if not has_pdfs:
            no_pdf_keys.append(key)
        ok += 1
        if ok % 50 == 0:
            print(f"  {ok}개 생성됨...")

    entries.sort(key=lambda e: e[1])
    list_html = build_list_page(entries)
    (ROOT / "question-bank.html").write_text(list_html, encoding="utf-8")
    print(f"✓ question-bank.html 생성 (목록 {len(entries)}건)")

    print(f"\n완료: {ok}개 생성, {skipped}개 스킵")
    if no_pdf_keys:
        print(f"\n⚠ PDF를 찾지 못한 시험 {len(no_pdf_keys)}개:")
        for k in no_pdf_keys:
            folder = PDF_FOLDER_OVERRIDE.get(k, NAME_MAP.get(k, k))
            print(f"  - {k} (찾은 폴더명: {folder})")


if __name__ == "__main__":
    main()
