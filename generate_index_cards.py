#!/usr/bin/env python3
"""
신규 자격증 카드를 index.html에 추가하는 스크립트.
기존 45개 제외한 신규 자격증을 카테고리별로 정리해 삽입.
"""
import sys, json, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = Path(r"C:\개인\wooahouse\wooaGosa\data")
INDEX    = Path(r"C:\개인\wooahouse\wooaGosa\index.html")

SKIP = {
    "air_eng","bread","computer_1","computer_2","const_safety_eng","const_safety_ind",
    "elec_craft","elec_eng","elec_ind","elevator_craft","elevator_eng","energy_craft",
    "energy_eng","excavator","fire_elec","fire_mech","forklift","gas_craft","gas_eng",
    "gas_ind","hazmat_craft","hazmat_ind","history_advanced","history_basic","hvac_craft",
    "hvac_eng","info_ind","info_proc","info_sec","korean_cook","license_1_2","linux_1",
    "linux_2","motorcycle","motorcycle_verify","net_1","net_2","pastry","realtor_1",
    "realtor_2","safety_eng","safety_ind","water_eng","welfare_1","welfare_2","welfare_3",
    "word","컴퓨터활용능력_1급","컴퓨터활용능력_2급",
}

def get_icon(name):
    if any(x in name for x in ["전기공사","전기기능장","전기철도","전자기사","전자산업","전자출판","전자캐드","의료전자"]): return "⚡"
    if any(x in name for x in ["기계","설비","압연","용접","열처리","금형","판금","표면처리","정밀측정","컴퓨터응용","제품응용"]): return "⚙️"
    if any(x in name for x in ["토목","건설재료","콘크리트","측량","지적","도시계획","교통기사","교통산업"]): return "🏗️"
    if any(x in name for x in ["건축","실내건축","전산응용건축"]): return "🏛️"
    if any(x in name for x in ["화공","화약","금속","제선","제강","주조","축로"]): return "🧪"
    if any(x in name for x in ["환경","소음진동","토양","폐기물","온실가스"]): return "🌱"
    if any(x in name for x in ["방사선","초음파","자기비","침투비","와전류","누설비"]): return "🔬"
    if any(x in name for x in ["소방시설","방재","산업위생","방수산업","인간공학","농작업안전"]): return "⛑️"
    if any(x in name for x in ["가스기능장","에너지관리기능장","에너지관리산업","신재생에너지","위험물기능장"]): return "⚡"
    if any(x in name for x in ["승강기산업"]): return "🛗"
    if any(x in name for x in ["공조냉동기계산업"]): return "❄️"
    if any(x in name for x in ["조선","선체","잠수","해양","항로표지"]): return "⚓"
    if any(x in name for x in ["철도","항공"]): return "🚂"
    if any(x in name for x in ["농업기계","농림토양","산림","임산","임업","유기농업","원예기능","시설원예","식물보호","버섯","종자","수산","어로","축산","생물분류"]): return "🌿"
    if any(x in name for x in ["식품","식육","조주","제과기능장"]): return "🍽️"
    if any(x in name for x in ["의류","섬유","패션","한복","귀금속","보석","세탁","목공예","석공예","피아노"]): return "✂️"
    if any(x in name for x in ["미용","이용장","이용사"]): return "💇"
    if any(x in name for x in ["사무자동화","멀티미디어","정보기기"]): return "💻"
    if any(x in name for x in ["시각디자인","제품디자인","컬러리스트","인쇄","전자출판","사진기능"]): return "🎨"
    if any(x in name for x in ["조경","스포츠","텔레마케팅","가맹거래","기상기사","응용지질","포장기사","포장산업","광학","바이오","자연생태","의공","화재감식","화훼"]): return "📝"
    if "가구" in name: return "🪑"
    return "📝"

def get_count(name):
    if "기능사" in name or "기능장" in name: return 60
    if "산업기사" in name: return 80
    if "기사" in name: return 100
    return 60

# 카테고리 정의 (순서 중요 — 이름 매칭 순서)
CATEGORIES = [
    ("⚡ 전기·전자", lambda n: any(x in n for x in ["전기공사","전기기능장","전기철도","전자기사","전자산업기사","전자캐드","전자출판","의료전자"])),
    ("⚙️ 기계·설비·금속", lambda n: any(x in n for x in ["기계","설비보전","압연","용접","열처리","금형","판금","표면처리","정밀측정","컴퓨터응용","제품응용","제선","제강","주조","축로"])),
    ("🏗️ 토목·측량·건설재료", lambda n: any(x in n for x in ["토목","건설재료","콘크리트","측량","지적","도시계획","교통기사","교통산업"])),
    ("🏛️ 건축·실내", lambda n: any(x in n for x in ["건축기사","건축산업","건축설비","건축목","건축일반","실내건축","전산응용건축"])),
    ("🚜 건설기계·운반기계", lambda n: any(x in n for x in ["건설기계","모터그레이더","타워크레인","천장크레인","컨테이너크레인","양화장치","농기계운전"])),
    ("🧪 화학·화공·위험물", lambda n: any(x in n for x in ["화공","화약","화학분석","바이오화학","금속재료","금속도장"])),
    ("🌱 환경", lambda n: any(x in n for x in ["대기환경산업","수질환경산업","소음진동","토양환경","폐기물","온실가스","환경기능사"])),
    ("🔬 비파괴검사", lambda n: any(x in n for x in ["비파괴검사"])),
    ("⛑️ 안전·보건·방재", lambda n: any(x in n for x in ["소방시설","방재기사","방수산업","산업위생","인간공학","농작업안전"])),
    ("⚡ 에너지·가스·위험물(추가)", lambda n: any(x in n for x in ["에너지관리기능장","에너지관리산업기사","신재생에너지","가스기능장","위험물기능장"])),
    ("🛗 승강기·공조냉동(추가)", lambda n: any(x in n for x in ["승강기산업","공조냉동기계산업"])),
    ("⚓ 조선·해양·항로", lambda n: any(x in n for x in ["조선산업","선체건조","잠수","해양","항로표지"])),
    ("🚂 철도·항공", lambda n: any(x in n for x in ["철도","항공기사","항공산업"])),
    ("🌿 농림·수산·축산·환경생태", lambda n: any(x in n for x in ["농업기계","농림토양","산림","임산가공","임업종묘","유기농업","원예기능사","시설원예","식물보호","버섯","종자","수산","어로산업","축산","생물분류","자연생태"])),
    ("🍽️ 식품·조리", lambda n: any(x in n for x in ["식품","식육","조주기능사","제과기능장"])),
    ("✂️ 섬유·패션·공예·뷰티", lambda n: any(x in n for x in ["의류기사","섬유디자인","패션","한복","귀금속","보석가공","세탁","목공예","석공예","피아노","미용","이용사","이용장"])),
    ("🎨 디자인·인쇄·사진", lambda n: any(x in n for x in ["시각디자인","제품디자인","컬러리스트","인쇄기능","전자출판","사진기능"])),
    ("💻 사무·IT(추가)", lambda n: any(x in n for x in ["사무자동화","멀티미디어","정보기기운용"])),
    ("📝 기타·전문자격", lambda n: True),  # 나머지 전부
]

# 신규 자격증 로드
new_exams = []
for jf in sorted(DATA_DIR.glob("*.json")):
    stem = jf.stem
    if stem in SKIP or stem.isascii():
        continue
    try:
        data = json.loads(jf.read_text(encoding='utf-8'))
        q_cnt = len(data)
    except:
        continue
    if q_cnt == 0:
        continue
    new_exams.append((stem, q_cnt))

print(f"신규 자격증: {len(new_exams)}개")

# 카테고리별 분류
categorized = {cat: [] for cat, _ in CATEGORIES}
for name, q_cnt in new_exams:
    for cat, fn in CATEGORIES:
        if fn(name):
            categorized[cat].append((name, q_cnt))
            break

# HTML 생성
html_sections = []
for cat, fn in CATEGORIES:
    items = categorized[cat]
    if not items:
        continue
    cards = []
    for name, q_cnt in items:
        icon = get_icon(name)
        cnt  = get_count(name)
        disp_name = name.replace("_", " ")
        cards.append(f"""          <a class="exam-card" href="exam-{name}.html">
            <span class="card-icon">{icon}</span>
            <span class="card-title">{disp_name} 필기</span>
            <span class="card-sub">4지선다 · {cnt}문항</span>
            <span class="card-count">기출 {q_cnt}문제</span>
          </a>""")
    section = f"""
      <!-- {cat} -->
      <section class="exam-section">
        <h2 class="section-title">{cat}</h2>
        <div class="exam-grid">
{''.join(chr(10) + c for c in cards)}

        </div>
      </section>"""
    html_sections.append(section)

new_html = "\n".join(html_sections)

# index.html에 삽입
content = INDEX.read_text(encoding='utf-8')

# 기존에 이미 삽입된 신규 블록이 있으면 제거 후 재삽입
marker_start = "<!-- ===신규자격증START=== -->"
marker_end   = "<!-- ===신규자격증END=== -->"
if marker_start in content:
    content = re.sub(
        re.escape(marker_start) + r'.*?' + re.escape(marker_end),
        '',
        content,
        flags=re.DOTALL
    )

insert_target = "    </div><!-- /.gosa-main -->"
block = f"{marker_start}\n{new_html}\n      {marker_end}\n      "
content = content.replace(insert_target, block + insert_target)

INDEX.write_text(content, encoding='utf-8')
print(f"index.html 업데이트 완료 ({len(new_exams)}개 카드 추가)")

# 카테고리별 통계
for cat, fn in CATEGORIES:
    items = categorized[cat]
    if items:
        print(f"  {cat}: {len(items)}개")
