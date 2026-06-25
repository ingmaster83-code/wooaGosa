"""
시험 유형별 SEO 랜딩 페이지 자동 생성기
각 페이지: 고유 title/description/h1/FAQ + 모드선택 + 시작 버튼
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = Path(r"C:\개인\wooahouse\wooaGosa")

# ── 공통 HTML 조각 ──────────────────────────────────────

GA = """  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9ZGENFSXWC"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-9ZGENFSXWC');
  </script>"""

SITES_BAR = """<div class="our-sites-bar">
  <div class="our-sites-inner">
  <span class="our-sites-label">🏠 우아하우스 패밀리 사이트 · 도구모음</span>
  <div class="our-sites-links">
    <a href="https://wooahouse.com/" target="_blank" rel="noopener">🔗 WooaHouse</a>
    <a href="https://pdfkit.wooahouse.com/" target="_blank" rel="noopener">📄 WooaPDF</a>
    <a href="https://imagekit.wooahouse.com/" target="_blank" rel="noopener">🖼️ WooaImage</a>
    <a href="https://colorkit.wooahouse.com/" target="_blank" rel="noopener">🎨 WooaColor</a>
    <a href="https://textkit.wooahouse.com/" target="_blank" rel="noopener">✏️ WooaText</a>
    <a href="https://qrkit.wooahouse.com/" target="_blank" rel="noopener">📱 WooaQR</a>
    <a href="https://calckit.wooahouse.com/" target="_blank" rel="noopener">🧮 WooaCalc</a>
    <a href="https://fontkit.wooahouse.com/" target="_blank" rel="noopener">🔤 WooaFont</a>
    <a href="https://mactools.wooahouse.com/" target="_blank" rel="noopener">🍎 WooaMac</a>
    <a href="https://pctools.wooahouse.com/" target="_blank" rel="noopener">🖥️ WooaPC</a>
    <a href="https://vskit.wooahouse.com/" target="_blank" rel="noopener">💻 WooaVS</a>
    <a href="https://wooaaudio.wooahouse.com/" target="_blank" rel="noopener">🎵 WooaAudio</a>
    <a href="https://wooavideo.wooahouse.com/" target="_blank" rel="noopener">🎬 WooaVideo</a>
    <a href="https://wooaviewer.wooahouse.com/" target="_blank" rel="noopener">🔍 WooaViewer</a>
    <a href="https://wooadev.wooahouse.com/" target="_blank" rel="noopener">🛠️ WooaDev</a>
    <a href="https://wooaocr.wooahouse.com/" target="_blank" rel="noopener">🔍 WooaOCR</a>
    <a href="https://wooasheet.wooahouse.com/" target="_blank" rel="noopener">📊 WooaSheet</a>
    <a href="https://wooaseo.wooahouse.com/" target="_blank" rel="noopener">🔎 WooaSEO</a>
    <a href="https://wooagosa.wooahouse.com/" class="active">📝 WooaGosa</a>
  </div>
  </div>
</div>"""

SIDEBAR_ADS = """    <aside class="tool-sidebar">
      <div class="ad-card">
        <ins class="adsbygoogle"
             style="display:block;width:100%;min-height:250px"
             data-ad-client="ca-pub-6464921081676309"
             data-ad-slot="1419180025"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
      </div>
      <div class="ad-card">
        <script src="https://ads-partners.coupang.com/g.js"></script>
        <script>
          new PartnersCoupang.G({"id":974224,"trackingCode":"AF5600192","subId":null,"template":"carousel","width":"300","height":"250"});
        </script>
      </div>
    </aside>"""

MOBILE_AD = """  <div class="mobile-top-ad">
    <ins class="adsbygoogle"
         style="display:block;width:100%;height:80px"
         data-ad-client="ca-pub-6464921081676309"
         data-ad-slot="7080296704"
         data-ad-format="auto"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
    <script src="https://ads-partners.coupang.com/g.js"></script>
    <script>
      new PartnersCoupang.G({"id":974224,"trackingCode":"AF5600192","subId":null,"template":"carousel","width":"320","height":"100"});
    </script>
  </div>"""

MOBILE_INLINE_AD = """      <!-- 모바일 인라인 광고 -->
      <div class="mobile-inline-ad">
        <script src="https://ads-partners.coupang.com/g.js"></script>
        <script>
          new PartnersCoupang.G({"id":974224,"trackingCode":"AF5600192","subId":null,"template":"carousel","width":"300","height":"250"});
        </script>
      </div>"""

# ── 공식 사이트 링크 ─────────────────────────────────────
OFFICIAL_LINKS = {
    'safedriving': ("🏛 도로교통공단 공식 홈페이지",      "https://www.safedriving.or.kr/"),
    'history':     ("🏛 한국사능력검정시험 공식 홈페이지", "https://www.historyexam.go.kr/"),
    'korcham':     ("🏛 대한상공회의소 공식 홈페이지",     "https://license.korcham.net/"),
    'kait':        ("🏛 KAIT 공식 홈페이지",              "https://www.kait.or.kr/"),
    'kisa':        ("🏛 KISA 공식 홈페이지",              "https://www.kisa.or.kr/"),
    'welfare':     ("🏛 사회복지사 자격관리센터 홈페이지", "https://www.welfare.net/"),
    'qnet':        ("🏛 큐넷 공식 홈페이지",              "https://www.q-net.or.kr/"),
}

TYPE_TO_LINKS = {
    '1jong-daebyeong': 'safedriving', '1jong-botong':     'safedriving',
    '2jong-botong':    'safedriving', 'motorcycle':        'safedriving',
    'motorbike':       'safedriving',
    'history_basic':   'history',     'history_advanced':  'history',
    'computer_1':      'korcham',     'computer_2':        'korcham',
    'word':            'korcham',
    'net_1':           'kait',        'net_2':             'kait',
    'linux_1':         'kait',        'linux_2':           'kait',
    'info_sec':        'kisa',
    'welfare_1':       'welfare',     'welfare_2':         'welfare',
    'welfare_3':       'welfare',
    # 나머지 전부 qnet (elec_eng/ind, info_proc/ind, hazmat_*, fire_*,
    #                   forklift, excavator, realtor_*, safety_*, elec_craft,
    #                   pastry, bread, korean_cook, gas_*, const_safety_*,
    #                   hvac_*, air_eng, water_eng, elevator_*, energy_*)
}

# ── 시험 유형 정의 ──────────────────────────────────────

EXAMS = [
  {
    "file":     "exam-license-1large.html",
    "type":     "1jong-daebyeong",
    "label":    "1종 대형",
    "count":    60,
    "icon":     "🚛",
    "title":    "1종 대형 면허 무료 모의고사 – 학과시험 60문항",
    "desc":     "1종 대형 운전면허 무료 모의고사. 회원가입 없이 즉시 시작, 최신 문제은행 1,000문제 기반, 60문제 랜덤 출제, 오답노트·타이머 제공.",
    "h1":       "1종 대형 면허 학과시험 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-license-1large.html",
    "badges":   ["🚛 1종 대형", "📋 60문항", "⏱ 80분", "✅ 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>시험 과목</th><td>도로교통법령 및 안전운전</td></tr>
          <tr><th>문항 수</th><td>60문항 (4지선다)</td></tr>
          <tr><th>시험 시간</th><td>80분</td></tr>
          <tr><th>합격 기준</th><td>60점 이상 (36문항 이상 정답)</td></tr>
          <tr><th>응시 대상</th><td>승합차·화물차·특수차량 운전자</td></tr>
          <tr><th>문제 출처</th><td>도로교통공단 문제은행 (2026.3.9 시행)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("1종 대형 면허 합격 기준은?", "60문항 중 36문항(60점) 이상 정답 시 합격입니다. 1종 보통·2종 보통의 70점 기준보다 낮습니다."),
      ("1종 대형과 1종 보통의 차이는?", "1종 대형은 승합·화물·특수차량을 운전할 수 있으며, 학과시험은 60문항(60점 합격)으로 1종 보통(40문항·70점)과 다릅니다."),
      ("문제은행 출처는 어디인가요?", "도로교통공단이 2026년 3월 9일 기준으로 공개한 학과시험 문제은행 PDF를 기반으로 합니다."),
      ("1·2종 문제은행이 같은가요?", "1종 대형·1종 보통·2종 보통은 동일한 1,000문제 통합 문제은행에서 출제됩니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  {
    "file":     "exam-license-1normal.html",
    "type":     "1jong-botong",
    "label":    "1종 보통",
    "count":    40,
    "icon":     "🚗",
    "title":    "1종 보통 면허 무료 모의고사 – 학과시험 40문항",
    "desc":     "1종 보통 운전면허 무료 모의고사. 회원가입 없이 즉시 시작, 최신 문제은행 1,000문제 기반, 40문제 랜덤 출제, 오답노트·타이머 제공.",
    "h1":       "1종 보통 면허 학과시험 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-license-1normal.html",
    "badges":   ["🚗 1종 보통", "📋 40문항", "⏱ 50분", "✅ 70점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>시험 과목</th><td>도로교통법령 및 안전운전</td></tr>
          <tr><th>문항 수</th><td>40문항 (4지선다)</td></tr>
          <tr><th>시험 시간</th><td>40분</td></tr>
          <tr><th>합격 기준</th><td>70점 이상 (28문항 이상 정답)</td></tr>
          <tr><th>응시 대상</th><td>승용·승합·화물차 운전자</td></tr>
          <tr><th>문제 출처</th><td>도로교통공단 문제은행 (2026.3.9 시행)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("1종 보통 학과시험 합격 기준은?", "40문항 중 28문항(70점) 이상 정답 시 합격입니다."),
      ("1종 보통으로 운전할 수 있는 차는?", "승용차, 승합차(10인 이하), 화물차(4톤 이하), 특수차(소형) 등을 운전할 수 있습니다."),
      ("문제은행 출처는 어디인가요?", "도로교통공단이 2026년 3월 9일 기준으로 공개한 학과시험 문제은행 PDF를 기반으로 합니다."),
      ("1종 보통과 2종 보통의 문제가 같나요?", "1종·2종 통합 문제은행 1,000문제에서 랜덤 출제됩니다. 합격 기준도 둘 다 70점으로 동일합니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  {
    "file":     "exam-license-2normal.html",
    "type":     "2jong-botong",
    "label":    "2종 보통",
    "count":    40,
    "icon":     "🚙",
    "title":    "2종 보통 면허 무료 모의고사 – 학과시험 40문항",
    "desc":     "2종 보통 운전면허 무료 모의고사. 회원가입 없이 즉시 시작, 최신 문제은행 1,000문제 기반, 40문제 랜덤 출제, 오답노트·타이머 제공.",
    "h1":       "2종 보통 면허 학과시험 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-license-2normal.html",
    "badges":   ["🚙 2종 보통", "📋 40문항", "⏱ 50분", "✅ 70점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>시험 과목</th><td>도로교통법령 및 안전운전</td></tr>
          <tr><th>문항 수</th><td>40문항 (4지선다)</td></tr>
          <tr><th>시험 시간</th><td>40분</td></tr>
          <tr><th>합격 기준</th><td>70점 이상 (28문항 이상 정답)</td></tr>
          <tr><th>응시 대상</th><td>승용차 운전자 (자동변속기 한정 가능)</td></tr>
          <tr><th>문제 출처</th><td>도로교통공단 문제은행 (2026.3.9 시행)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("2종 보통 학과시험 합격 기준은?", "40문항 중 28문항(70점) 이상 정답 시 합격입니다."),
      ("2종 보통으로 운전할 수 있는 차는?", "승용차 및 승합차(10인 이하)를 운전할 수 있습니다. 자동변속기 한정으로 응시할 수도 있습니다."),
      ("2종 보통과 1종 보통의 차이는?", "2종 보통은 승용차 위주, 1종 보통은 승합·화물까지 운전 가능합니다. 학과시험 문제는 동일한 문제은행에서 출제됩니다."),
      ("문제은행 출처는 어디인가요?", "도로교통공단이 2026년 3월 9일 기준으로 공개한 학과시험 문제은행 PDF를 기반으로 합니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  {
    "file":     "exam-motorcycle.html",
    "type":     "motorcycle",
    "label":    "2종 소형(이륜)",
    "count":    40,
    "icon":     "🏍",
    "title":    "2종 소형 모의고사 40문항 무료 – 오토바이·이륜자동차 학과시험",
    "desc":     "2종 소형 모의고사 40문항 무료 연습. 오토바이·이륜자동차 운전면허 학과시험 문제은행 800문제 기반, 랜덤 출제. 회원가입 없이 브라우저에서 즉시 시작.",
    "h1":       "2종 소형(이륜자동차) 면허 학과시험 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-motorcycle.html",
    "badges":   ["🏍 이륜자동차", "📋 40문항", "⏱ 50분", "✅ 70점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>시험 과목</th><td>도로교통법령 및 안전운전</td></tr>
          <tr><th>문항 수</th><td>40문항 (4지선다)</td></tr>
          <tr><th>시험 시간</th><td>40분</td></tr>
          <tr><th>합격 기준</th><td>70점 이상 (28문항 이상 정답)</td></tr>
          <tr><th>응시 대상</th><td>125cc 초과 이륜자동차 운전자</td></tr>
          <tr><th>문제 출처</th><td>도로교통공단 문제은행 (2026.3.9 시행)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("이륜자동차 학과시험 합격 기준은?", "40문항 중 28문항(70점) 이상 정답 시 합격입니다."),
      ("이륜자동차(2종 소형)와 원동기의 차이는?", "2종 소형은 125cc 초과 오토바이, 원동기는 125cc 이하 오토바이·전동킥보드 등에 해당합니다."),
      ("이륜자동차 문제은행은 1·2종과 다른가요?", "네, 이륜자동차·원동기는 별도 문제은행 800문제를 사용합니다. 1·2종 면허 문제와는 다릅니다."),
      ("문제은행 출처는 어디인가요?", "도로교통공단이 2026년 3월 9일 기준으로 공개한 이륜자동차 학과시험 문제은행 PDF를 기반으로 합니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  {
    "file":     "exam-motorbike.html",
    "type":     "motorbike",
    "label":    "원동기장치자전거",
    "count":    40,
    "icon":     "🛵",
    "title":    "원동기 모의고사 40문항 무료 – 전동킥보드·125cc 이하 학과시험",
    "desc":     "원동기 모의고사 40문항 무료 연습. 전동킥보드·125cc 이하 원동기장치자전거 학과시험 문제은행 800문제 기반, 랜덤 출제. 회원가입 없이 브라우저에서 즉시 시작.",
    "h1":       "원동기장치자전거 면허 학과시험 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-motorbike.html",
    "badges":   ["🛵 원동기", "📋 40문항", "⏱ 50분", "✅ 70점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>시험 과목</th><td>도로교통법령 및 안전운전</td></tr>
          <tr><th>문항 수</th><td>40문항 (4지선다)</td></tr>
          <tr><th>시험 시간</th><td>40분</td></tr>
          <tr><th>합격 기준</th><td>70점 이상 (28문항 이상 정답)</td></tr>
          <tr><th>응시 대상</th><td>125cc 이하 오토바이·전동킥보드 운전자</td></tr>
          <tr><th>문제 출처</th><td>도로교통공단 문제은행 (2026.3.9 시행)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("원동기 면허로 전동킥보드를 탈 수 있나요?", "네. 원동기장치자전거 면허가 있으면 개인형 이동장치(전동킥보드, PM)를 합법적으로 이용할 수 있습니다."),
      ("원동기와 이륜자동차 면허 차이는?", "원동기는 125cc 이하, 2종 소형(이륜)은 125cc 초과 오토바이에 해당합니다. 문제은행은 동일합니다."),
      ("원동기 면허 합격 기준은?", "40문항 중 28문항(70점) 이상 정답 시 합격입니다."),
      ("문제은행 출처는 어디인가요?", "도로교통공단이 2026년 3월 9일 기준으로 공개한 이륜자동차·원동기 학과시험 문제은행 PDF를 기반으로 합니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  {
    "file":     "exam-history-basic.html",
    "type":     "history_basic",
    "label":    "한국사 기본",
    "count":    50,
    "icon":     "📖",
    "title":    "한국사능력검정 기본 무료 모의고사 – 4·5·6급 50문항",
    "desc":     "한국사능력검정시험(한능검) 기본 무료 모의고사. 회원가입 없이 즉시 시작, 4~6급 대비, 기출 50문항, 오답노트 제공.",
    "h1":       "한국사능력검정시험 기본 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-history-basic.html",
    "badges":   ["📖 기본", "📋 50문항", "⏱ 70분", "🏅 4~6급"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>시험 유형</th><td>한국사능력검정시험 기본</td></tr>
          <tr><th>문항 수</th><td>50문항 (4지선다)</td></tr>
          <tr><th>시험 시간</th><td>70분</td></tr>
          <tr><th>급수 기준</th><td>4급: 80점↑ / 5급: 60점↑ / 6급: 50점↑</td></tr>
          <tr><th>주관</th><td>국사편찬위원회</td></tr>
          <tr><th>문제 출처</th><td>국사편찬위원회 기출문제 (71·75·77회)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("한국사능력검정 기본 합격 기준은?", "4급은 80점 이상, 5급은 60점 이상, 6급은 50점 이상입니다. 점수에 따라 해당 급수가 부여됩니다."),
      ("기본과 심화의 차이는?", "기본은 4지선다 50문항(4~6급), 심화는 5지선다 50문항(1~3급)입니다. 취업·학교에 따라 요구 급수가 다릅니다."),
      ("한국사 기본이 필요한 곳은?", "공무원 시험, 교원임용, 일부 공기업 지원 시 6급 이상이 요구됩니다. 취업 우대를 위해 4~5급을 목표로 하는 경우가 많습니다."),
      ("시험은 연 몇 회 시행되나요?", "연 6회 내외 시행됩니다. 국사편찬위원회 공식 사이트에서 일정을 확인하세요."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  {
    "file":     "exam-history-advanced.html",
    "type":     "history_advanced",
    "label":    "한국사 심화",
    "count":    50,
    "icon":     "📚",
    "title":    "한국사능력검정 심화 무료 모의고사 – 1·2·3급 50문항",
    "desc":     "한국사능력검정시험(한능검) 심화 무료 모의고사. 회원가입 없이 즉시 시작, 1~3급 대비, 기출 50문항, 오답노트 제공.",
    "h1":       "한국사능력검정시험 심화 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-history-advanced.html",
    "badges":   ["📚 심화", "📋 50문항", "⏱ 80분", "🏆 1~3급"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>시험 유형</th><td>한국사능력검정시험 심화</td></tr>
          <tr><th>문항 수</th><td>50문항 (5지선다)</td></tr>
          <tr><th>시험 시간</th><td>80분</td></tr>
          <tr><th>급수 기준</th><td>1급: 80점↑ / 2급: 60점↑ / 3급: 50점↑</td></tr>
          <tr><th>주관</th><td>국사편찬위원회</td></tr>
          <tr><th>문제 출처</th><td>국사편찬위원회 기출문제 (70~72·75~77회)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("한국사능력검정 심화 합격 기준은?", "1급은 80점 이상, 2급은 60점 이상, 3급은 50점 이상입니다."),
      ("심화 1급이 필요한 곳은?", "5급 공무원(행정고시), 외교관후보자, 지역인재 7급 등 국가고시와 주요 공기업·금융권에서 심화 2급 이상을 요구합니다."),
      ("공무원 시험에는 어떤 급수가 필요한가요?", "7·9급 국가공무원은 심화 3급 이상, 5급은 2급 이상이 일반적으로 요구됩니다. 기관별로 다를 수 있으니 공고를 확인하세요."),
      ("기출문제 몇 회차가 수록되어 있나요?", "70·71·72·75·76·77회 기출문제가 수록되어 있으며, 총 300문항입니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  {
    "file":     "exam-computer-1.html",
    "type":     "computer_1",
    "label":    "컴활 1급",
    "count":    60,
    "icon":     "🖥️",
    "title":    "컴퓨터활용능력 1급 필기 무료 모의고사 – 60문항 3과목",
    "desc":     "컴퓨터활용능력(컴활) 1급 필기 무료 모의고사. 회원가입 없이 즉시 시작, 3과목(컴퓨터일반·스프레드시트·데이터베이스) 기출 486문항, 60분 타이머, 오답노트 제공.",
    "h1":       "컴퓨터활용능력 1급 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-computer-1.html",
    "badges":   ["🖥️ 컴활 1급", "📋 60문항 · 3과목", "⏱ 60분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>컴퓨터 일반 (20문항)</td></tr>
          <tr><th>2과목</th><td>스프레드시트 일반 (20문항)</td></tr>
          <tr><th>3과목</th><td>데이터베이스 일반 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>60분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 평균 60점↑</td></tr>
          <tr><th>문제 출처</th><td>대한상공회의소 기출문제 (2015~2020년)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("컴활 1급 필기 합격 기준은?", "3과목 각각 40점 이상이면서 평균 60점 이상이어야 합격합니다. 한 과목이라도 40점 미만이면 과락입니다."),
      ("컴활 1급과 2급의 차이는?", "1급은 3과목 60문항, 2급은 2과목 40문항입니다. 1급은 데이터베이스 과목이 추가됩니다."),
      ("필기 합격 후 실기까지 얼마나 걸리나요?", "필기 합격 후 2년 이내에 실기에 합격하면 됩니다. 필기는 2년간 유효합니다."),
      ("기출문제 몇 년도분이 수록되어 있나요?", "2015~2020년 10개 시험 회차의 기출문제 중 텍스트 추출 가능한 486문항이 수록되어 있습니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  {
    "file":     "exam-computer-2.html",
    "type":     "computer_2",
    "label":    "컴활 2급",
    "count":    40,
    "icon":     "💾",
    "title":    "컴퓨터활용능력 2급 필기 무료 모의고사 – 40문항 2과목",
    "desc":     "컴퓨터활용능력(컴활) 2급 필기 무료 모의고사. 회원가입 없이 즉시 시작, 2과목(컴퓨터일반·스프레드시트) 기출 322문항, 40분 타이머, 오답노트 제공.",
    "h1":       "컴퓨터활용능력 2급 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-computer-2.html",
    "badges":   ["💾 컴활 2급", "📋 40문항 · 2과목", "⏱ 40분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>컴퓨터 일반 (20문항)</td></tr>
          <tr><th>2과목</th><td>스프레드시트 일반 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>40분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 평균 60점↑</td></tr>
          <tr><th>문제 출처</th><td>대한상공회의소 기출문제 (2015~2020년)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("컴활 2급 필기 합격 기준은?", "2과목 각각 40점 이상이면서 평균 60점 이상이어야 합격합니다."),
      ("컴활 2급은 어디서 활용되나요?", "공무원 가산점, 취업 우대, 대학 학점 인정 등 다양한 분야에서 활용됩니다. 사무직 취업 시 기본 자격증으로 인정받습니다."),
      ("2급 필기 합격 후 실기 준비는?", "필기 합격 후 2년 이내에 실기 합격 시 최종 자격증이 발급됩니다. 실기는 Excel 실무 작업 위주입니다."),
      ("기출문제 몇 년도분이 수록되어 있나요?", "2015~2020년 10개 시험 회차의 기출문제 중 텍스트 추출 가능한 322문항이 수록되어 있습니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 네트워크관리사 ───────────────────────────────────────
  {
    "file":     "exam-net-1.html",
    "type":     "net_1",
    "label":    "네트워크관리사 1급",
    "count":    60,
    "icon":     "🌐",
    "title":    "네트워크관리사 1급 필기 무료 모의고사 – 60문항 5과목",
    "desc":     "네트워크관리사 1급 필기 무료 모의고사. 회원가입 없이 즉시 시작, TCP/IP·NOS·정보보호 등 5과목, 기출 364문제, 60문항 랜덤 출제, 오답노트·타이머 제공.",
    "h1":       "네트워크관리사 1급 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-net-1.html",
    "badges":   ["🌐 네트워크관리사 1급", "📋 60문항 · 5과목", "⏱ 60분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>TCP/IP</td></tr>
          <tr><th>2과목</th><td>네트워크 일반</td></tr>
          <tr><th>3과목</th><td>NOS (Network Operating System)</td></tr>
          <tr><th>4과목</th><td>네트워크 운용기기</td></tr>
          <tr><th>5과목</th><td>정보보호개론</td></tr>
          <tr><th>시험 시간</th><td>60분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>문제 출처</th><td>KAIT 기출문제 (2020~2026년)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("네트워크관리사 1급 필기 합격 기준은?", "5과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격입니다. 한 과목이라도 40점 미만이면 과락입니다."),
      ("네트워크관리사 1급 과목 구성은?", "TCP/IP, 네트워크 일반, NOS, 네트워크 운용기기, 정보보호개론의 5과목으로 구성되며 총 60문항이 출제됩니다."),
      ("네트워크관리사 1급과 2급의 차이는?", "1급은 5과목 60문항, 2급은 4과목 50문항입니다. 1급은 정보보호개론이 추가되며 난이도가 더 높습니다."),
      ("네트워크관리사 시험은 연 몇 회 시행되나요?", "연 2회(상반기·하반기) 시행됩니다. KAIT(한국정보통신진흥협회) 공식 사이트에서 일정을 확인하세요."),
      ("네트워크관리사 자격증의 활용 분야는?", "IT 인프라 관리, 네트워크 엔지니어, 시스템 관리자 분야에서 활용됩니다. 일부 공공기관과 공기업에서 취업 우대 자격증으로 인정됩니다."),
    ],
  },
  {
    "file":     "exam-net-2.html",
    "type":     "net_2",
    "label":    "네트워크관리사 2급",
    "count":    50,
    "icon":     "🌐",
    "title":    "네트워크관리사 2급 필기 무료 모의고사 – 50문항 4과목",
    "desc":     "네트워크관리사 2급 필기 무료 모의고사. 회원가입 없이 즉시 시작, TCP/IP·NOS 등 4과목, 기출 262문제, 50문항 랜덤 출제, 오답노트·타이머 제공.",
    "h1":       "네트워크관리사 2급 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-net-2.html",
    "badges":   ["🌐 네트워크관리사 2급", "📋 50문항 · 4과목", "⏱ 60분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>TCP/IP</td></tr>
          <tr><th>2과목</th><td>네트워크 일반</td></tr>
          <tr><th>3과목</th><td>NOS (Network Operating System)</td></tr>
          <tr><th>4과목</th><td>네트워크 운용기기</td></tr>
          <tr><th>시험 시간</th><td>60분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>문제 출처</th><td>KAIT 기출문제 (2023~2026년)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("네트워크관리사 2급 필기 합격 기준은?", "4과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격입니다. 한 과목이라도 40점 미만이면 과락입니다."),
      ("네트워크관리사 2급 과목 구성은?", "TCP/IP, 네트워크 일반, NOS, 네트워크 운용기기의 4과목으로 구성되며 총 50문항이 출제됩니다."),
      ("네트워크관리사 2급 취득 후 혜택은?", "IT 취업 우대, 일부 공공기관 가산점, 정보통신 분야 취업 시 기본 자격증으로 인정됩니다."),
      ("네트워크관리사 2급 시험 응시 자격이 따로 있나요?", "응시 자격 제한이 없어 누구나 응시할 수 있습니다. 학력·경력 무관으로 IT 입문자도 도전하기 좋은 자격증입니다."),
      ("네트워크관리사 2급은 어떤 기관에서 시행하나요?", "KAIT(한국정보통신진흥협회)에서 시행하는 민간 자격증입니다. 연 2~3회 정기시험이 진행됩니다."),
    ],
  },
  # ── 리눅스마스터 ─────────────────────────────────────────
  {
    "file":     "exam-linux-1.html",
    "type":     "linux_1",
    "label":    "리눅스마스터 1급",
    "count":    100,
    "icon":     "🐧",
    "title":    "리눅스마스터 1급 필기 무료 모의고사 – 100문항 3과목",
    "desc":     "리눅스마스터 1급 필기 무료 모의고사. 회원가입 없이 즉시 시작, 리눅스 실무·시스템관리·네트워크 3과목, 기출 984문제, 100문항, 오답노트·타이머 제공.",
    "h1":       "리눅스마스터 1급 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-linux-1.html",
    "badges":   ["🐧 리눅스마스터 1급", "📋 100문항 · 3과목", "⏱ 100분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>리눅스 실무의 이해</td></tr>
          <tr><th>2과목</th><td>리눅스 시스템 관리</td></tr>
          <tr><th>3과목</th><td>네트워크 및 서비스의 활용</td></tr>
          <tr><th>시험 시간</th><td>100분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>문제 출처</th><td>KAIT 기출문제 (2016~2023년)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("리눅스마스터 1급 필기 합격 기준은?", "3과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격입니다. 필기 합격 후 2년 이내에 실기에 합격하면 최종 취득입니다."),
      ("리눅스마스터 1급 과목은 어떻게 구성되나요?", "리눅스 실무의 이해, 리눅스 시스템 관리, 네트워크 및 서비스의 활용 3과목으로 총 100문항이 출제됩니다."),
      ("리눅스마스터 1급과 2급의 차이는?", "2급은 2과목 80문항이고 필기만으로 자격이 부여됩니다. 1급은 3과목 100문항에 필기+실기를 모두 통과해야 합니다."),
      ("리눅스마스터 1급 응시 자격이 있나요?", "리눅스마스터 2급 취득자 또는 IT 분야 관련 학력·경력 소지자가 응시할 수 있습니다. 2급과 달리 응시 자격 제한이 있습니다."),
      ("리눅스마스터 1급 자격증의 활용 분야는?", "서버 관리자, 시스템 엔지니어, DevOps, 클라우드 엔지니어 등 IT 인프라 관련 직군에서 높이 평가받습니다."),
    ],
  },
  {
    "file":     "exam-linux-2.html",
    "type":     "linux_2",
    "label":    "리눅스마스터 2급",
    "count":    80,
    "icon":     "🐧",
    "title":    "리눅스마스터 2급 필기 무료 모의고사 – 80문항 2과목",
    "desc":     "리눅스마스터 2급 필기 무료 모의고사. 회원가입 없이 즉시 시작, 리눅스 운영·활용 2과목, 기출 845문제, 80문항 랜덤 출제, 오답노트·타이머 제공.",
    "h1":       "리눅스마스터 2급 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-linux-2.html",
    "badges":   ["🐧 리눅스마스터 2급", "📋 80문항 · 2과목", "⏱ 80분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>리눅스 운영 및 관리</td></tr>
          <tr><th>2과목</th><td>리눅스 활용</td></tr>
          <tr><th>시험 시간</th><td>80분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>특이사항</th><td>필기 합격 시 자격 부여 (실기 없음)</td></tr>
          <tr><th>문제 출처</th><td>KAIT 기출문제 (2020~2023년)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("리눅스마스터 2급 필기 합격 기준은?", "2과목 각각 40점 이상이면서 전과목 평균 60점 이상이면 합격입니다. 2급은 필기만 합격하면 자격이 부여됩니다."),
      ("리눅스마스터 2급은 실기 시험이 없나요?", "네, 리눅스마스터 2급은 필기시험만으로 자격이 부여됩니다. 실기 없이 취득할 수 있어 입문자에게 적합합니다."),
      ("리눅스마스터 2급 응시 자격이 따로 있나요?", "응시 자격 제한이 없습니다. 누구나 응시 가능하므로 리눅스 입문자가 도전하기 좋은 자격증입니다."),
      ("리눅스마스터 2급 취득 후 진로는?", "서버 운영, 웹 호스팅, 시스템 관리 등 리눅스 기반 IT 분야 취업 시 기본 역량 증명에 활용됩니다."),
      ("시험은 연 몇 회 시행되나요?", "연 3~4회 시행됩니다. KAIT(한국정보통신진흥협회) 공식 사이트에서 정확한 일정을 확인하세요."),
    ],
  },
  # ── 워드프로세서 ─────────────────────────────────────────
  {
    "file":     "exam-word.html",
    "type":     "word",
    "label":    "워드프로세서",
    "count":    60,
    "icon":     "📝",
    "title":    "워드프로세서 필기 무료 모의고사 – 60문항 3과목",
    "desc":     "워드프로세서 필기 무료 모의고사. 회원가입 없이 즉시 시작, 워드프로세싱일반·PC운영체제·컴퓨터정보활용 3과목, 기출 617문제, 60문항, 오답노트 제공.",
    "h1":       "워드프로세서 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-word.html",
    "badges":   ["📝 워드프로세서", "📋 60문항 · 3과목", "⏱ 60분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>워드프로세싱 일반</td></tr>
          <tr><th>2과목</th><td>PC 운영 체제</td></tr>
          <tr><th>3과목</th><td>컴퓨터 및 정보활용</td></tr>
          <tr><th>시험 시간</th><td>60분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>대한상공회의소</td></tr>
          <tr><th>문제 출처</th><td>기출문제 (2015~2020년)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("워드프로세서 필기 합격 기준은?", "3과목 각각 40점 이상이면서 전과목 평균 60점 이상이면 합격입니다. 한 과목이라도 40점 미만이면 과락입니다."),
      ("워드프로세서가 '구 1급'이라고 불리는 이유는?", "과거 1급·2급·3급으로 구분되었으나 2016년 단일 등급으로 통합되었습니다. 이 모의고사는 통합 이전 기출문제도 포함합니다."),
      ("워드프로세서 자격증은 어디에 활용되나요?", "사무직 취업, 공무원 가산점, 학교 졸업 요건 등 다양한 분야에서 활용됩니다. 컴퓨터활용능력 자격증과 함께 사무직 기본 자격증으로 인정받습니다."),
      ("워드프로세서 실기 시험도 있나요?", "네, 필기 합격 후 실기 시험도 응시해야 합니다. 실기는 한글 문서 작성 능력을 평가합니다. 필기 합격일로부터 2년간 유효합니다."),
      ("시험은 연 몇 회 시행되나요?", "연 3~4회 시행됩니다. 대한상공회의소 자격평가사업단 공식 사이트에서 시험 일정을 확인하세요."),
    ],
  },
  # ── 전기기사 / 전기산업기사 ──────────────────────────────
  {
    "file":     "exam-elec-eng.html",
    "type":     "elec_eng",
    "label":    "전기기사",
    "count":    100,
    "icon":     "⚡",
    "title":    "전기기사 필기 무료 모의고사 – 100문항 5과목",
    "desc":     "전기기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 전기자기학·전력공학·전기기기·회로이론·전기설비기술기준 5과목, 기출 462문제, 100문항, 오답노트 제공.",
    "h1":       "전기기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-elec-eng.html",
    "badges":   ["⚡ 전기기사", "📋 100문항 · 5과목", "⏱ 150분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>전기자기학 (20문항)</td></tr>
          <tr><th>2과목</th><td>전력공학 (20문항)</td></tr>
          <tr><th>3과목</th><td>전기기기 (20문항)</td></tr>
          <tr><th>4과목</th><td>회로이론 및 제어공학 (20문항)</td></tr>
          <tr><th>5과목</th><td>전기설비기술기준 및 판단기준 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>150분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>문제 출처</th><td>한국산업인력공단 기출문제 (2018~2022년)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("전기기사 필기 합격 기준은?", "5과목 각각 40점(8문항) 이상이면서 전과목 평균 60점(60문항) 이상이어야 합격합니다. 한 과목이라도 40점 미만이면 과락입니다."),
      ("전기기사 필기 과목 구성은?", "전기자기학, 전력공학, 전기기기, 회로이론 및 제어공학, 전기설비기술기준 및 판단기준의 5과목으로 각 20문항, 총 100문항이 출제됩니다."),
      ("전기기사와 전기산업기사의 차이는?", "전기기사는 4년제 대졸 또는 동등한 학력·경력이 필요한 기사 등급이며, 전기산업기사는 2년제 이상 학력으로 응시 가능합니다. 기사 자격이 더 넓은 분야에서 인정됩니다."),
      ("전기기사 응시 자격은?", "관련학과 4년제 대학 졸업(예정)자, 동일 직무분야 기사 이상 취득자, 4년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("전기기사 취득 후 활용 분야는?", "전기 설계·공사·감리, 전기안전관리자, 아파트 전기실, 공장 전기 유지보수 등 광범위한 분야에서 활용됩니다. 취업과 개업 모두 유리한 필수 자격증입니다."),
    ],
  },
  {
    "file":     "exam-elec-ind.html",
    "type":     "elec_ind",
    "label":    "전기산업기사",
    "count":    100,
    "icon":     "⚡",
    "title":    "전기산업기사 필기 무료 모의고사 – 100문항 5과목",
    "desc":     "전기산업기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 전기자기학·전력공학·전기기기·회로이론·전기설비 5과목, 기출 539문제, 100문항, 오답노트 제공.",
    "h1":       "전기산업기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-elec-ind.html",
    "badges":   ["⚡ 전기산업기사", "📋 100문항 · 5과목", "⏱ 150분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>전기자기학 (20문항)</td></tr>
          <tr><th>2과목</th><td>전력공학 (20문항)</td></tr>
          <tr><th>3과목</th><td>전기기기 (20문항)</td></tr>
          <tr><th>4과목</th><td>회로이론 (20문항)</td></tr>
          <tr><th>5과목</th><td>전기설비기술기준 및 판단기준 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>150분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>문제 출처</th><td>한국산업인력공단 기출문제 (2016~2020년)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("전기산업기사 필기 합격 기준은?", "5과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다. 과락(과목당 40점 미만) 시 불합격입니다."),
      ("전기산업기사 과목 구성은?", "전기자기학, 전력공학, 전기기기, 회로이론, 전기설비기술기준 및 판단기준의 5과목 각 20문항, 총 100문항이 출제됩니다."),
      ("전기산업기사 응시 자격은?", "관련학과 2년제 대학 졸업(예정)자, 동일 직무분야 기능사 취득 후 1년 이상 실무경력자, 3년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("전기산업기사와 전기기사 중 어떤 것을 먼저 취득해야 하나요?", "일반적으로 전기산업기사 취득 후 경력을 쌓아 전기기사에 도전합니다. 전기기사가 업무 범위와 대우 면에서 유리합니다."),
      ("전기산업기사 취득 후 활용 분야는?", "전기 공사, 유지보수, 안전관리 보조, 전기직 공무원 시험 가산점 등 다양한 분야에서 활용됩니다."),
    ],
  },
  # ── 정보처리기사 / 정보처리산업기사 ──────────────────────
  {
    "file":     "exam-info-proc.html",
    "type":     "info_proc",
    "label":    "정보처리기사",
    "count":    100,
    "icon":     "🖥️",
    "title":    "정보처리기사 필기 무료 모의고사 – 100문항 5과목",
    "desc":     "정보처리기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 데이터베이스·운영체제·소프트웨어공학 등 5과목, 기출 692문제, 100문항, 오답노트 제공.",
    "h1":       "정보처리기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-info-proc.html",
    "badges":   ["🖥️ 정보처리기사", "📋 100문항 · 5과목", "⏱ 120분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>데이터베이스 (20문항)</td></tr>
          <tr><th>2과목</th><td>전자계산기구조 (20문항)</td></tr>
          <tr><th>3과목</th><td>운영체제 (20문항)</td></tr>
          <tr><th>4과목</th><td>소프트웨어 공학 (20문항)</td></tr>
          <tr><th>5과목</th><td>데이터통신 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>120분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>문제 출처</th><td>한국산업인력공단 기출문제 (2018~2022년)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("정보처리기사 필기 합격 기준은?", "5과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다. 한 과목이라도 40점 미만이면 과락입니다."),
      ("정보처리기사 과목 구성은?", "데이터베이스, 전자계산기구조, 운영체제, 소프트웨어공학, 데이터통신의 5과목으로 각 20문항, 총 100문항이 출제됩니다."),
      ("정보처리기사는 NCS 기반으로 개편되었나요?", "2020년부터 NCS 기반으로 전면 개편되어 소프트웨어 설계·개발·테스팅 등 실무 중심으로 재편되었습니다. 이 모의고사는 개편 이전 기출문제가 수록되어 있습니다."),
      ("정보처리기사 응시 자격은?", "관련학과 4년제 대졸(예정)자, 기사 이상 자격취득자, 산업기사+1년 경력, 4년 이상 실무경력 등이 응시 가능합니다."),
      ("정보처리기사 취득 후 진로는?", "소프트웨어 개발자, 시스템 분석가, IT 컨설턴트, 데이터베이스 관리자 등 IT 전반에서 활용됩니다. 공무원 임용 시 가산점도 적용됩니다."),
    ],
  },
  {
    "file":     "exam-info-ind.html",
    "type":     "info_ind",
    "label":    "정보처리산업기사",
    "count":    100,
    "icon":     "🖥️",
    "title":    "정보처리산업기사 필기 무료 모의고사 – 100문항 5과목",
    "desc":     "정보처리산업기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 데이터베이스·전자계산기·시스템분석 등 5과목, 기출 309문제, 100문항, 오답노트 제공.",
    "h1":       "정보처리산업기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-info-ind.html",
    "badges":   ["🖥️ 정보처리산업기사", "📋 100문항 · 5과목", "⏱ 120분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>데이터베이스 (20문항)</td></tr>
          <tr><th>2과목</th><td>전자계산기구조 (20문항)</td></tr>
          <tr><th>3과목</th><td>시스템분석설계 (20문항)</td></tr>
          <tr><th>4과목</th><td>운영체제 (20문항)</td></tr>
          <tr><th>5과목</th><td>정보통신개론 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>120분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>문제 출처</th><td>한국산업인력공단 기출문제 (2016~2020년)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("정보처리산업기사 필기 합격 기준은?", "5과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다. 과락 시 불합격입니다."),
      ("정보처리산업기사와 정보처리기사의 차이는?", "산업기사는 기사보다 응시 자격 요건이 낮고(2년제 대졸 등), 업무 범위가 다소 제한적입니다. 기사 취득을 목표로 하는 경우 산업기사를 먼저 취득하는 경우가 많습니다."),
      ("정보처리산업기사 응시 자격은?", "관련학과 2년제 대졸(예정)자, 기능사 취득 후 1년 이상 실무경력자, 3년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("정보처리산업기사 과목 구성은?", "데이터베이스, 전자계산기구조, 시스템분석설계, 운영체제, 정보통신개론의 5과목으로 각 20문항, 총 100문항이 출제됩니다."),
      ("정보처리산업기사의 활용 분야는?", "IT 개발 보조, 시스템 운영, 정보통신 분야 취업 시 기본 자격증으로 인정됩니다. 공무원 가산점 적용 직렬도 있습니다."),
    ],
  },
  # ── 정보보안기사 ─────────────────────────────────────────
  {
    "file":     "exam-info-sec.html",
    "type":     "info_sec",
    "label":    "정보보안기사",
    "count":    100,
    "icon":     "🔒",
    "title":    "정보보안기사 필기 무료 모의고사 – 100문항 5과목",
    "desc":     "정보보안기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 시스템보안·네트워크보안·어플리케이션보안 등 5과목, 기출 822문제, 100문항, 오답노트 제공.",
    "h1":       "정보보안기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-info-sec.html",
    "badges":   ["🔒 정보보안기사", "📋 100문항 · 5과목", "⏱ 120분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>시스템 보안 (20문항)</td></tr>
          <tr><th>2과목</th><td>네트워크 보안 (20문항)</td></tr>
          <tr><th>3과목</th><td>어플리케이션 보안 (20문항)</td></tr>
          <tr><th>4과목</th><td>정보보안 일반 (20문항)</td></tr>
          <tr><th>5과목</th><td>정보보안 관리 및 법규 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>120분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>문제 출처</th><td>한국인터넷진흥원(KISA) 기출문제 (2016~2023년)</td></tr>
        </table>
      </div>""",
    "faq": [
      ("정보보안기사 필기 합격 기준은?", "5과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다. 한 과목이라도 40점 미만이면 과락 처리됩니다."),
      ("정보보안기사 과목 구성은?", "시스템 보안, 네트워크 보안, 어플리케이션 보안, 정보보안 일반, 정보보안 관리 및 법규의 5과목으로 각 20문항, 총 100문항이 출제됩니다."),
      ("정보보안기사 응시 자격은?", "관련학과 4년제 대졸(예정)자, 정보보안 관련 실무경력 4년 이상, 기사 이상 자격취득자 등이 응시할 수 있습니다."),
      ("정보보안기사는 어떤 분야에서 필요한가요?", "보안 컨설턴트, 침해대응(IR) 전문가, 보안 관제 운영, CISO 보좌, 공공기관 정보보호담당관 등 사이버 보안 전 분야에서 핵심 자격증으로 인정받습니다."),
      ("정보보안기사와 CISSP의 차이는?", "정보보안기사는 국내 국가기술자격이고, CISSP는 미국 ISC²의 국제 자격증입니다. 국내 공공기관·공기업 취업에는 정보보안기사가, 글로벌 기업에는 CISSP가 더 인정받습니다."),
    ],
  },
  # ── 위험물산업기사 ───────────────────────────────────────
  {
    "file":     "exam-hazmat-ind.html",
    "type":     "hazmat_ind",
    "label":    "위험물산업기사",
    "count":    60,
    "icon":     "🧪",
    "title":    "위험물산업기사 필기 무료 모의고사 – 60문항 4과목",
    "desc":     "위험물산업기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 일반화학·화재예방·위험물취급·안전관리법 4과목, 기출 457문제, 오답노트·타이머 제공.",
    "h1":       "위험물산업기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-hazmat-ind.html",
    "badges":   ["🧪 위험물산업기사", "📋 60문항 · 4과목", "⏱ 90분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>일반화학 (15문항)</td></tr>
          <tr><th>2과목</th><td>화재예방과 소화방법 (15문항)</td></tr>
          <tr><th>3과목</th><td>위험물의 성질과 취급 (20문항)</td></tr>
          <tr><th>4과목</th><td>위험물안전관리법령 (10문항)</td></tr>
          <tr><th>시험 시간</th><td>90분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("위험물산업기사 필기 합격 기준은?", "4과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다. 과락(과목당 40점 미만) 시 불합격입니다."),
      ("위험물산업기사와 위험물기능사의 차이는?", "위험물기능사는 기능사 등급으로 응시 자격 제한이 없고, 위험물산업기사는 산업기사 등급으로 2년제 대졸 또는 관련 경력이 필요합니다. 산업기사가 더 넓은 업무 범위를 가집니다."),
      ("위험물산업기사 응시 자격은?", "관련학과 2년제 대졸(예정)자, 기능사 취득 후 1년 이상 실무경력자, 3년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("위험물산업기사가 필요한 직장은?", "위험물 제조·저장·취급 사업장의 위험물안전관리자로 선임될 수 있습니다. 화학공장, 주유소, 도료·페인트 제조업체 등 다양한 분야에서 활용됩니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 위험물기능사 ─────────────────────────────────────────
  {
    "file":     "exam-hazmat-craft.html",
    "type":     "hazmat_craft",
    "label":    "위험물기능사",
    "count":    60,
    "icon":     "🧪",
    "title":    "위험물기능사 필기 무료 모의고사 – 60문항 기출",
    "desc":     "위험물기능사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 일반화학·화재예방·위험물취급 3과목, 기출 425문제, 오답노트·타이머 제공.",
    "h1":       "위험물기능사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-hazmat-craft.html",
    "badges":   ["🧪 위험물기능사", "📋 60문항 · 3과목", "⏱ 60분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>일반화학 (20문항)</td></tr>
          <tr><th>2과목</th><td>화재예방과 소화방법 (20문항)</td></tr>
          <tr><th>3과목</th><td>위험물의 성질과 취급 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>60분</td></tr>
          <tr><th>합격 기준</th><td>60점 이상 합격</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("위험물기능사 필기 합격 기준은?", "3과목 총점 60점(36문항) 이상이면 합격합니다."),
      ("위험물기능사 응시 자격이 있나요?", "응시 자격 제한이 없습니다. 학력·경력에 무관하게 누구나 응시할 수 있어 취득하기 좋은 기능사 자격증입니다."),
      ("위험물기능사 취득 후 할 수 있는 일은?", "위험물 취급 사업장에서 위험물안전관리자 보조업무를 수행할 수 있습니다. 주유소, 화학공장, 도료업체, 물류창고 등에서 활용됩니다."),
      ("필기 합격 후 실기는 어떻게 준비하나요?", "위험물기능사 실기는 작업형 시험으로, 위험물 취급 실무 능력을 평가합니다. 필기 합격 후 2년 이내에 실기에 합격해야 합니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 소방설비기사 ─────────────────────────────────────────
  {
    "file":     "exam-fire-mech.html",
    "type":     "fire_mech",
    "label":    "소방설비기사 기계",
    "count":    80,
    "icon":     "🔥",
    "title":    "소방설비기사 기계분야 필기 무료 모의고사 – 80문항",
    "desc":     "소방설비기사 기계분야 필기 무료 모의고사. 회원가입 없이 즉시 시작, 소방원론·소방유체역학·소방관련법 등 4과목, 기출 421문제, 오답노트 제공.",
    "h1":       "소방설비기사 기계분야 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-fire-mech.html",
    "badges":   ["🔥 소방설비기사 기계", "📋 80문항 · 4과목", "⏱ 150분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>소방원론 (20문항)</td></tr>
          <tr><th>2과목</th><td>소방유체역학 (20문항)</td></tr>
          <tr><th>3과목</th><td>소방관계법규 (20문항)</td></tr>
          <tr><th>4과목</th><td>소방기계시설의 구조 및 원리 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>150분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("소방설비기사 기계분야 필기 합격 기준은?", "4과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다. 한 과목이라도 40점 미만이면 과락입니다."),
      ("소방설비기사 기계분야와 전기분야의 차이는?", "기계분야는 스프링클러·소화기 등 소방기계설비, 전기분야는 자동화재탐지설비·비상방송 등 소방전기설비를 다룹니다. 둘 다 취득하면 더 많은 현장에 선임될 수 있습니다."),
      ("소방설비기사 응시 자격은?", "관련학과 4년제 대졸(예정)자, 소방설비산업기사 취득 후 1년 이상 경력자, 4년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("소방설비기사 자격증의 활용 분야는?", "소방시설공사업체, 소방안전관리자, 건설현장 소방안전 분야에서 활용됩니다. 소방시설공사 착공신고·완공검사에 소방설비기사 보유자가 필요합니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  {
    "file":     "exam-fire-elec.html",
    "type":     "fire_elec",
    "label":    "소방설비기사 전기",
    "count":    80,
    "icon":     "🔥",
    "title":    "소방설비기사 전기분야 필기 무료 모의고사 – 80문항",
    "desc":     "소방설비기사 전기분야 필기 무료 모의고사. 회원가입 없이 즉시 시작, 소방원론·소방전기일반·소방관련법 등 4과목, 기출 356문제, 오답노트 제공.",
    "h1":       "소방설비기사 전기분야 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-fire-elec.html",
    "badges":   ["🔥 소방설비기사 전기", "📋 80문항 · 4과목", "⏱ 150분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>소방원론 (20문항)</td></tr>
          <tr><th>2과목</th><td>소방전기일반 (20문항)</td></tr>
          <tr><th>3과목</th><td>소방관계법규 (20문항)</td></tr>
          <tr><th>4과목</th><td>소방전기시설의 구조 및 원리 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>150분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("소방설비기사 전기분야 필기 합격 기준은?", "4과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다."),
      ("소방설비기사 전기분야 과목 구성은?", "소방원론, 소방전기일반, 소방관계법규, 소방전기시설의 구조 및 원리의 4과목으로 총 80문항이 출제됩니다."),
      ("소방설비기사 전기분야 취득 후 진로는?", "자동화재탐지설비, 비상경보설비, 유도등, 비상방송설비 등 소방전기시설 공사·감리·점검 분야에서 활동할 수 있습니다."),
      ("소방설비기사 기계와 전기 둘 다 취득해야 하나요?", "반드시 그렇지는 않지만, 둘 다 보유하면 기계·전기 소방설비 모두 취급·감리할 수 있어 취업 경쟁력이 높아집니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 지게차 / 굴착기 운전기능사 ──────────────────────────
  {
    "file":     "exam-forklift.html",
    "type":     "forklift",
    "label":    "지게차운전기능사",
    "count":    60,
    "icon":     "🚜",
    "title":    "지게차운전기능사 필기 무료 모의고사 – 60문항 기출",
    "desc":     "지게차운전기능사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 지게차구조·도로주행·안전관리 3과목, 기출 539문제, 60문항 랜덤 출제, 오답노트 제공.",
    "h1":       "지게차운전기능사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-forklift.html",
    "badges":   ["🚜 지게차운전기능사", "📋 60문항 · 3과목", "⏱ 60분", "✅ 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>지게차 구조 및 작업장치 (20문항)</td></tr>
          <tr><th>2과목</th><td>도로주행 및 화물취급 (20문항)</td></tr>
          <tr><th>3과목</th><td>안전관리 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>60분</td></tr>
          <tr><th>합격 기준</th><td>60점 이상</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("지게차운전기능사 필기 합격 기준은?", "60문항 중 60점(36문항) 이상 맞히면 합격합니다. 과락 기준은 없으며 총점으로만 판정합니다."),
      ("지게차운전기능사 응시 자격이 있나요?", "응시 자격 제한이 없습니다. 만 18세 이상이면 누구나 응시할 수 있습니다."),
      ("지게차 필기와 실기 모두 통과해야 하나요?", "네, 필기 합격 후 실기(운전 조작) 시험에 합격해야 최종 자격증이 발급됩니다. 필기 합격일로부터 2년 이내에 실기를 통과해야 합니다."),
      ("지게차운전기능사 자격의 활용 분야는?", "물류창고, 항만, 건설현장, 제조공장 등에서 지게차 운전자로 취업할 수 있습니다. 물류·유통 업계 취업 시 필수 자격증으로 인정받습니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  {
    "file":     "exam-excavator.html",
    "type":     "excavator",
    "label":    "굴착기운전기능사",
    "count":    60,
    "icon":     "🏗️",
    "title":    "굴착기운전기능사 필기 무료 모의고사 – 60문항 기출",
    "desc":     "굴착기(굴삭기)운전기능사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 굴착기구조·도로주행·안전관리 3과목, 기출 477문제, 오답노트 제공.",
    "h1":       "굴착기운전기능사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-excavator.html",
    "badges":   ["🏗️ 굴착기운전기능사", "📋 60문항 · 3과목", "⏱ 60분", "✅ 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>굴착기 구조 및 작업장치 (20문항)</td></tr>
          <tr><th>2과목</th><td>도로주행 및 토목공사 (20문항)</td></tr>
          <tr><th>3과목</th><td>안전관리 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>60분</td></tr>
          <tr><th>합격 기준</th><td>60점 이상</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("굴착기운전기능사 필기 합격 기준은?", "60문항 중 60점(36문항) 이상이면 합격합니다."),
      ("굴착기와 지게차 자격증을 같이 취득해야 하나요?", "각각 별도 자격증입니다. 건설현장에서는 굴착기, 물류현장에서는 지게차가 주로 사용됩니다. 필요에 맞게 선택하거나 둘 다 취득할 수 있습니다."),
      ("굴착기운전기능사 응시 자격이 있나요?", "응시 자격 제한이 없습니다. 만 18세 이상이면 누구나 응시할 수 있습니다."),
      ("굴착기운전기능사 활용 분야는?", "건설공사, 토목공사, 도로공사, 상하수도 공사 등 건설 현장에서 굴착기(포클레인) 운전자로 취업할 수 있습니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 공인중개사 ───────────────────────────────────────────
  {
    "file":     "exam-realtor-1.html",
    "type":     "realtor_1",
    "label":    "공인중개사 1차",
    "count":    80,
    "icon":     "🏠",
    "title":    "공인중개사 1차 필기 무료 모의고사 – 5지선다 80문항 2과목",
    "desc":     "공인중개사 1차 시험 무료 모의고사. 회원가입 없이 즉시 시작, 부동산학개론·민법 2과목 5지선다, 기출 729문제 기반, 오답노트 제공.",
    "h1":       "공인중개사 1차 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-realtor-1.html",
    "badges":   ["🏠 공인중개사 1차", "📋 80문항 · 2과목", "⏱ 120분", "✅ 과목 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>부동산학개론 (40문항)</td></tr>
          <tr><th>2과목</th><td>민법 및 민사특별법 (40문항)</td></tr>
          <tr><th>시험 시간</th><td>120분</td></tr>
          <tr><th>합격 기준</th><td>각 과목 40점↑ + 2개 과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("공인중개사 1차 합격 기준은?", "부동산학개론·민법 각각 40점(16문항) 이상이면서 두 과목 평균 60점 이상이어야 합격합니다. 한 과목이라도 40점 미만이면 과락입니다."),
      ("공인중개사 1차와 2차를 같은 날 응시하나요?", "네, 1차와 2차를 같은 날 치르며, 1차는 오전, 2차는 오후에 진행됩니다. 1차에 합격해야 2차가 채점됩니다."),
      ("공인중개사 1차 면제 제도가 있나요?", "네, 1차 시험 합격자는 다음 해 1차 시험이 면제됩니다. 2차만 재응시하면 됩니다."),
      ("공인중개사 시험은 연 몇 회 시행되나요?", "연 1회 시행됩니다. 매년 10월 말~11월 초에 시험이 진행됩니다. 한국산업인력공단 공식 사이트에서 일정을 확인하세요."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  {
    "file":     "exam-realtor-2.html",
    "type":     "realtor_2",
    "label":    "공인중개사 2차",
    "count":    120,
    "icon":     "🏠",
    "title":    "공인중개사 2차 필기 무료 모의고사 – 5지선다 120문항 3과목",
    "desc":     "공인중개사 2차 시험 무료 모의고사. 회원가입 없이 즉시 시작, 공인중개사법·부동산공법·부동산공시법 3과목 5지선다, 기출 738문제 기반, 오답노트 제공.",
    "h1":       "공인중개사 2차 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-realtor-2.html",
    "badges":   ["🏠 공인중개사 2차", "📋 120문항 · 3과목", "⏱ 150분", "✅ 과목 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>공인중개사법·중개실무 (40문항)</td></tr>
          <tr><th>2과목</th><td>부동산공법 (40문항)</td></tr>
          <tr><th>3과목</th><td>부동산공시법령·부동산세법 (40문항)</td></tr>
          <tr><th>시험 시간</th><td>150분</td></tr>
          <tr><th>합격 기준</th><td>각 과목 40점↑ + 3개 과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("공인중개사 2차 합격 기준은?", "3과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다. 한 과목이라도 40점 미만이면 과락입니다."),
      ("공인중개사 2차 과목 중 가장 어려운 과목은?", "수험생들이 가장 어렵다고 꼽는 과목은 부동산공법(도시계획법, 건축법 등)입니다. 법령 개정이 잦아 최신 법령 파악이 중요합니다."),
      ("공인중개사 자격 취득 후 어떻게 개업하나요?", "공인중개사 자격 취득 후 실무교육(64시간)을 이수하고, 관할 시·군·구청에 중개사무소 개설 등록을 해야 영업할 수 있습니다."),
      ("합격률이 낮다고 하던데 어느 정도인가요?", "1차·2차 동시 합격률은 보통 20~30% 수준입니다. 꾸준한 기출문제 반복 학습이 핵심 전략입니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 사회복지사 1급 ───────────────────────────────────────
  {
    "file":     "exam-welfare-1.html",
    "type":     "welfare_1",
    "label":    "사회복지사1급 1교시",
    "count":    50,
    "icon":     "👐",
    "title":    "사회복지사 1급 1교시 무료 모의고사 – 5지선다 50문항",
    "desc":     "사회복지사 1급 1교시 무료 모의고사. 회원가입 없이 즉시 시작, 인간행동과사회환경·사회복지조사론 5지선다, 기출 535문제 기반, 오답노트 제공.",
    "h1":       "사회복지사 1급 1교시 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-welfare-1.html",
    "badges":   ["👐 사회복지사1급 1교시", "📋 50문항", "⏱ 50분", "✅ 각 과목 40점↑"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>과목</th><td>사회복지기초 (사회복지학개론·인간행동과사회환경)</td></tr>
          <tr><th>문항 수</th><td>50문항</td></tr>
          <tr><th>시험 시간</th><td>50분</td></tr>
          <tr><th>합격 기준</th><td>각 과목 40점↑ + 전과목 총점 60% 이상</td></tr>
          <tr><th>주관</th><td>한국사회복지사협회</td></tr>
        </table>
      </div>""",
    "faq": [
      ("사회복지사 1급 합격 기준은?", "전 교시 과목 총점의 60% 이상 득점해야 합격합니다. 단, 각 과목 40점 미만이면 과락으로 불합격입니다."),
      ("사회복지사 1급 시험은 몇 교시로 나뉘나요?", "총 3교시로 나뉩니다. 1교시(사회복지기초·50문항), 2교시(사회복지실천·75문항), 3교시(사회복지정책과제도·75문항)으로 구성됩니다."),
      ("사회복지사 1급 응시 자격은?", "사회복지사 2급 자격증 취득 후 1년 이상 실무경력, 또는 관련 학과 졸업 후 실무경력을 충족해야 응시할 수 있습니다."),
      ("시험은 연 몇 회 시행되나요?", "연 1회 시행됩니다. 매년 1월에 시험이 진행되며, 한국사회복지사협회 공식 사이트에서 일정을 확인하세요."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  {
    "file":     "exam-welfare-2.html",
    "type":     "welfare_2",
    "label":    "사회복지사1급 2교시",
    "count":    75,
    "icon":     "👐",
    "title":    "사회복지사 1급 2교시 무료 모의고사 – 5지선다 75문항",
    "desc":     "사회복지사 1급 2교시 무료 모의고사. 회원가입 없이 즉시 시작, 사회복지실천론·기술론·지역사회복지론 5지선다, 기출 714문제 기반, 오답노트 제공.",
    "h1":       "사회복지사 1급 2교시 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-welfare-2.html",
    "badges":   ["👐 사회복지사1급 2교시", "📋 75문항", "⏱ 75분", "✅ 각 과목 40점↑"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>과목</th><td>사회복지실천 (실천론·기술론·가족복지론·집단·지역사회)</td></tr>
          <tr><th>문항 수</th><td>75문항</td></tr>
          <tr><th>시험 시간</th><td>75분</td></tr>
          <tr><th>합격 기준</th><td>각 과목 40점↑ + 전과목 총점 60% 이상</td></tr>
          <tr><th>주관</th><td>한국사회복지사협회</td></tr>
        </table>
      </div>""",
    "faq": [
      ("사회복지사 1급 2교시 과목 구성은?", "사회복지실천론, 사회복지실천기술론, 지역사회복지론, 가족복지론, 집단복지론 등 실천 관련 과목으로 구성됩니다."),
      ("사회복지사 1급 전체 합격률은?", "전체 합격률은 보통 40~50% 수준입니다. 기출문제를 반복적으로 풀고 오답노트를 활용한 학습이 효과적입니다."),
      ("사회복지사 1급 자격증으로 할 수 있는 일은?", "사회복지관, 의료사회복지사, 정신건강사회복지사, 학교사회복지사, 장애인복지관 등 다양한 사회복지 현장에서 전문가로 활동할 수 있습니다."),
      ("1급과 2급 사회복지사의 차이는?", "2급은 학위 취득만으로 부여되지만, 1급은 별도 국가시험을 통과해야 합니다. 1급은 기관장, 팀장 등 직책 및 전문성 인정 측면에서 유리합니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  {
    "file":     "exam-welfare-3.html",
    "type":     "welfare_3",
    "label":    "사회복지사1급 3교시",
    "count":    75,
    "icon":     "👐",
    "title":    "사회복지사 1급 3교시 무료 모의고사 – 5지선다 75문항",
    "desc":     "사회복지사 1급 3교시 무료 모의고사. 회원가입 없이 즉시 시작, 사회복지정책론·행정론·법제론 5지선다, 기출 699문제 기반, 오답노트 제공.",
    "h1":       "사회복지사 1급 3교시 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-welfare-3.html",
    "badges":   ["👐 사회복지사1급 3교시", "📋 75문항", "⏱ 75분", "✅ 각 과목 40점↑"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>과목</th><td>사회복지정책과제도 (사회보장론·사회복지행정론·사회복지법제론 등)</td></tr>
          <tr><th>문항 수</th><td>75문항</td></tr>
          <tr><th>시험 시간</th><td>75분</td></tr>
          <tr><th>합격 기준</th><td>각 과목 40점↑ + 전과목 총점 60% 이상</td></tr>
          <tr><th>주관</th><td>한국사회복지사협회</td></tr>
        </table>
      </div>""",
    "faq": [
      ("사회복지사 1급 3교시 과목 구성은?", "사회보장론, 사회복지정책론, 사회복지행정론, 사회복지법제론, 사회복지조사론 등 정책·제도 관련 과목으로 구성됩니다."),
      ("3교시 과목이 특히 어렵다는데 사실인가요?", "사회복지법제론은 법령 암기가 필요해 수험생들이 까다롭게 느낍니다. 기출문제 반복 학습과 최신 법령 확인이 중요합니다."),
      ("사회복지사 1급 공부 기간은 얼마나 필요한가요?", "개인 차이가 있지만 보통 6개월~1년 정도 준비합니다. 직장을 다니면서 준비하는 경우 1년 이상 소요되기도 합니다."),
      ("사회복지사 1급 시험 접수는 어디서 하나요?", "한국사회복지사협회 홈페이지(welfare.net)에서 접수합니다. 매년 8~9월경 접수를 받습니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 산업안전 ─────────────────────────────────────────────
  {
    "file":     "exam-safety-ind.html",
    "type":     "safety_ind",
    "label":    "산업안전산업기사",
    "count":    100,
    "icon":     "⛑️",
    "title":    "산업안전산업기사 필기 무료 모의고사 – 100문항 5과목",
    "desc":     "산업안전산업기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 안전관리론·인간공학·기계·전기·화학 5과목, 기출문제 기반, 오답노트·타이머 제공.",
    "h1":       "산업안전산업기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-safety-ind.html",
    "badges":   ["⛑️ 산업안전산업기사", "📋 100문항 · 5과목", "⏱ 120분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>산업안전관리론 (20문항)</td></tr>
          <tr><th>2과목</th><td>인간공학 및 시스템안전공학 (20문항)</td></tr>
          <tr><th>3과목</th><td>기계·기구 및 설비 안전관리 (20문항)</td></tr>
          <tr><th>4과목</th><td>전기설비 안전관리 (20문항)</td></tr>
          <tr><th>5과목</th><td>화학설비 안전관리 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>120분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("산업안전산업기사 필기 합격 기준은?", "5과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다. 과락(과목당 40점 미만) 시 불합격입니다."),
      ("산업안전산업기사 응시 자격은?", "관련학과 2년제 대졸(예정)자, 기능사 취득 후 1년 이상 실무경력자, 3년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("산업안전산업기사와 산업안전기사의 차이는?", "산업기사는 기사보다 응시 자격 요건이 낮고, 일부 선임 자격 범위가 다를 수 있습니다. 기사 취득을 목표로 하는 경우 산업기사를 먼저 취득하는 경우가 많습니다."),
      ("산업안전산업기사 자격의 활용 분야는?", "제조업·건설업 등 산업현장의 안전관리자로 선임될 수 있습니다. 산업안전보건법에 따라 일정 규모 이상 사업장에 안전관리자 선임이 의무화되어 있어 취업 수요가 높습니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  {
    "file":     "exam-safety-eng.html",
    "type":     "safety_eng",
    "label":    "산업안전기사",
    "count":    120,
    "icon":     "⛑️",
    "title":    "산업안전기사 필기 무료 모의고사 – 120문항 기출",
    "desc":     "산업안전기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 안전관리론·인간공학·기계·전기·건설 등 5과목, 기출문제 기반, 오답노트·타이머 제공.",
    "h1":       "산업안전기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-safety-eng.html",
    "badges":   ["⛑️ 산업안전기사", "📋 120문항 · 6과목", "⏱ 180분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>안전관리론 (20문항)</td></tr>
          <tr><th>2과목</th><td>인간공학 및 시스템안전공학 (20문항)</td></tr>
          <tr><th>3과목</th><td>기계위험방지기술 (20문항)</td></tr>
          <tr><th>4과목</th><td>전기위험방지기술 (20문항)</td></tr>
          <tr><th>5과목</th><td>화학설비위험방지기술 (20문항)</td></tr>
          <tr><th>6과목</th><td>건설안전기술 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>180분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("산업안전기사 필기 합격 기준은?", "6과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다. 한 과목이라도 40점 미만이면 과락 처리됩니다."),
      ("산업안전기사 응시 자격은?", "관련학과 4년제 대졸(예정)자, 산업안전산업기사 취득 후 1년 이상 경력자, 4년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("산업안전기사가 필요한 사업장은?", "산업안전보건법에 따라 상시 근로자 50인 이상 사업장(건설업은 공사금액 기준)은 안전관리자를 선임해야 합니다. 산업안전기사 보유자는 선임 자격을 갖춥니다."),
      ("산업안전기사 취득 후 전망은?", "중대재해처벌법 시행 이후 기업의 안전관리 투자가 늘면서 수요가 급증하고 있습니다. 대기업·공기업·건설사 등에서 우대하는 자격증입니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 전기기능사 ───────────────────────────────────────────
  {
    "file":     "exam-elec-craft.html",
    "type":     "elec_craft",
    "label":    "전기기능사",
    "count":    60,
    "icon":     "⚡",
    "title":    "전기기능사 필기 무료 모의고사 – 60문항 기출",
    "desc":     "전기기능사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 전기이론·전기기기·전기설비 3과목, 기출문제 기반, 오답노트·타이머 제공.",
    "h1":       "전기기능사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-elec-craft.html",
    "badges":   ["⚡ 전기기능사", "📋 60문항 · 3과목", "⏱ 60분", "✅ 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>전기이론 (20문항)</td></tr>
          <tr><th>2과목</th><td>전기기기 (20문항)</td></tr>
          <tr><th>3과목</th><td>전기설비 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>60분</td></tr>
          <tr><th>합격 기준</th><td>60점 이상 합격 (36문항)</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("전기기능사 필기 합격 기준은?", "60문항 총점 60점(36문항) 이상이면 합격합니다. 과목별 과락 기준은 없습니다."),
      ("전기기능사 응시 자격이 있나요?", "응시 자격 제한이 없습니다. 학력·경력에 무관하게 누구나 응시할 수 있습니다."),
      ("전기기능사 취득 후 할 수 있는 일은?", "전기 공사업체, 한전 하청 업체, 아파트·빌딩 전기 담당자, 전기안전관리자 보조 등 다양한 분야에서 활용됩니다."),
      ("전기기능사와 전기산업기사의 차이는?", "전기기능사는 응시 자격 제한이 없는 기능사 등급이며, 전기산업기사는 2년제 대졸 또는 관련 경력이 필요한 산업기사 등급입니다. 산업기사가 더 넓은 업무 범위를 가집니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 제과기능사 ───────────────────────────────────────────
  {
    "file":     "exam-pastry.html",
    "type":     "pastry",
    "label":    "제과기능사",
    "count":    60,
    "icon":     "🍰",
    "title":    "제과기능사 필기 무료 모의고사 – 60문항 기출",
    "desc":     "제과기능사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 제과이론·재료과학·식품위생학 등 기출문제 기반, 오답노트·타이머 제공.",
    "h1":       "제과기능사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-pastry.html",
    "badges":   ["🍰 제과기능사", "📋 60문항", "⏱ 60분", "✅ 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>시험 과목</th><td>제과이론·재료과학·영양학·식품위생학·식품위생법규</td></tr>
          <tr><th>문항 수</th><td>60문항 (4지선다)</td></tr>
          <tr><th>시험 시간</th><td>60분</td></tr>
          <tr><th>합격 기준</th><td>60점 이상 합격 (36문항)</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("제과기능사 필기 합격 기준은?", "60문항 총점 60점(36문항) 이상이면 합격합니다."),
      ("제과기능사 응시 자격이 있나요?", "응시 자격 제한이 없습니다. 누구나 응시할 수 있어 진입 장벽이 낮습니다."),
      ("제과기능사와 제빵기능사의 차이는?", "제과기능사는 케이크·쿠키·파이 등 과자류, 제빵기능사는 식빵·단과자빵 등 빵류를 다룹니다. 둘 다 취득하면 제과제빵 전반에 종사할 수 있습니다."),
      ("제과기능사 취득 후 진로는?", "베이커리, 제과점, 호텔 제과부, 급식업체, 식품가공 공장 등 다양한 현장에서 활용됩니다. 창업 시 제과 관련 자격증으로 인정됩니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 제빵기능사 ───────────────────────────────────────────
  {
    "file":     "exam-bread.html",
    "type":     "bread",
    "label":    "제빵기능사",
    "count":    60,
    "icon":     "🍞",
    "title":    "제빵기능사 필기 무료 모의고사 – 60문항 기출",
    "desc":     "제빵기능사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 제빵이론·재료과학·식품위생학 등 기출문제 기반, 오답노트·타이머 제공.",
    "h1":       "제빵기능사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-bread.html",
    "badges":   ["🍞 제빵기능사", "📋 60문항", "⏱ 60분", "✅ 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>시험 과목</th><td>제빵이론·재료과학·영양학·식품위생학·식품위생법규</td></tr>
          <tr><th>문항 수</th><td>60문항 (4지선다)</td></tr>
          <tr><th>시험 시간</th><td>60분</td></tr>
          <tr><th>합격 기준</th><td>60점 이상 합격 (36문항)</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("제빵기능사 필기 합격 기준은?", "60문항 총점 60점(36문항) 이상이면 합격합니다."),
      ("제빵기능사 응시 자격이 있나요?", "응시 자격 제한이 없습니다. 누구나 응시할 수 있습니다."),
      ("제빵기능사와 제과기능사를 같이 준비할 수 있나요?", "두 시험의 출제 범위가 상당 부분 겹쳐 같이 준비하는 경우가 많습니다. 식품위생학·재료과학 파트가 공통이며, 제조 이론 부분만 추가로 공부하면 됩니다."),
      ("제빵기능사 실기 시험은 어떻게 되나요?", "식빵·단과자빵 등 지정 품목을 실제로 제조하는 작업형 실기입니다. 필기 합격 후 2년 이내에 실기에 합격해야 최종 취득됩니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 한식조리기능사 ───────────────────────────────────────
  {
    "file":     "exam-korean-cook.html",
    "type":     "korean_cook",
    "label":    "한식조리기능사",
    "count":    60,
    "icon":     "🍲",
    "title":    "한식조리기능사 필기 무료 모의고사 – 60문항 기출",
    "desc":     "한식조리기능사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 한식조리·식품위생·영양학·식품위생법규 등 기출문제 기반, 오답노트·타이머 제공.",
    "h1":       "한식조리기능사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-korean-cook.html",
    "badges":   ["🍲 한식조리기능사", "📋 60문항", "⏱ 60분", "✅ 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>시험 과목</th><td>한식조리·식품학 및 조리원리·공중보건학·식품위생학·식품위생법규</td></tr>
          <tr><th>문항 수</th><td>60문항 (4지선다)</td></tr>
          <tr><th>시험 시간</th><td>60분</td></tr>
          <tr><th>합격 기준</th><td>60점 이상 합격 (36문항)</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("한식조리기능사 필기 합격 기준은?", "60문항 총점 60점(36문항) 이상이면 합격합니다."),
      ("한식조리기능사 응시 자격이 있나요?", "응시 자격 제한이 없습니다. 학력·경력에 무관하게 누구나 응시할 수 있습니다."),
      ("한식조리기능사 취득 후 할 수 있는 일은?", "한식 전문 음식점, 급식업체, 호텔 한식당, 단체급식 조리원 등에서 활용됩니다. 음식점 위생 관리 인력 자격으로도 인정됩니다."),
      ("한식·양식·중식·일식 조리기능사를 다 따야 하나요?", "각 조리 분야별로 별도 자격증이 있으며, 취업 목표 분야에 맞는 자격증을 취득하면 됩니다. 한식 음식점 창업 시에는 한식조리기능사 한 가지로 충분합니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 가스기능사 ───────────────────────────────────────────
  {
    "file":     "exam-gas-craft.html",
    "type":     "gas_craft",
    "label":    "가스기능사",
    "count":    60,
    "icon":     "🔥",
    "title":    "가스기능사 필기 무료 모의고사 – 60문항 기출",
    "desc":     "가스기능사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 연소공학·가스설비·가스안전관리 3과목, 기출문제 기반, 오답노트·타이머 제공.",
    "h1":       "가스기능사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-gas-craft.html",
    "badges":   ["🔥 가스기능사", "📋 60문항 · 3과목", "⏱ 60분", "✅ 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>연소공학 (20문항)</td></tr>
          <tr><th>2과목</th><td>가스설비 (20문항)</td></tr>
          <tr><th>3과목</th><td>가스안전관리 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>60분</td></tr>
          <tr><th>합격 기준</th><td>60점 이상 합격 (36문항)</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("가스기능사 필기 합격 기준은?", "60문항 총점 60점(36문항) 이상이면 합격합니다."),
      ("가스기능사 응시 자격이 있나요?", "응시 자격 제한이 없습니다. 누구나 응시할 수 있습니다."),
      ("가스기능사 취득 후 할 수 있는 일은?", "도시가스 공급시설, LPG 충전소, 가스 배관 공사 현장 등에서 가스 관련 업무를 수행할 수 있습니다."),
      ("가스기능사와 가스산업기사의 차이는?", "가스기능사는 응시 자격 제한이 없는 기능사 등급이며, 가스산업기사는 2년제 대졸 또는 관련 경력이 필요한 산업기사 등급입니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 가스산업기사 ─────────────────────────────────────────
  {
    "file":     "exam-gas-ind.html",
    "type":     "gas_ind",
    "label":    "가스산업기사",
    "count":    60,
    "icon":     "🔥",
    "title":    "가스산업기사 필기 무료 모의고사 – 60문항 기출",
    "desc":     "가스산업기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 연소공학·가스설비·가스안전관리·가스관계법규 4과목, 기출문제 기반, 오답노트·타이머 제공.",
    "h1":       "가스산업기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-gas-ind.html",
    "badges":   ["🔥 가스산업기사", "📋 60문항 · 4과목", "⏱ 90분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>연소공학 (15문항)</td></tr>
          <tr><th>2과목</th><td>가스설비 (15문항)</td></tr>
          <tr><th>3과목</th><td>가스안전관리 (20문항)</td></tr>
          <tr><th>4과목</th><td>가스관계법규 (10문항)</td></tr>
          <tr><th>시험 시간</th><td>90분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("가스산업기사 필기 합격 기준은?", "4과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다."),
      ("가스산업기사 응시 자격은?", "관련학과 2년제 대졸(예정)자, 가스기능사 취득 후 1년 이상 실무경력자, 3년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("가스산업기사 취득 후 진로는?", "도시가스 사업자, LPG 충전소, 가스 관련 제조·판매 업체 등에서 가스안전관리자로 선임될 수 있습니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 가스기사 ─────────────────────────────────────────────
  {
    "file":     "exam-gas-eng.html",
    "type":     "gas_eng",
    "label":    "가스기사",
    "count":    100,
    "icon":     "🔥",
    "title":    "가스기사 필기 무료 모의고사 – 100문항 기출",
    "desc":     "가스기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 연소공학·가스설비·가스안전관리·가스계측·가스관계법규 5과목, 기출문제 기반, 오답노트 제공.",
    "h1":       "가스기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-gas-eng.html",
    "badges":   ["🔥 가스기사", "📋 100문항 · 5과목", "⏱ 150분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>연소공학 (20문항)</td></tr>
          <tr><th>2과목</th><td>가스설비 (20문항)</td></tr>
          <tr><th>3과목</th><td>가스안전관리 (20문항)</td></tr>
          <tr><th>4과목</th><td>가스계측기기 (20문항)</td></tr>
          <tr><th>5과목</th><td>가스관계법규 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>150분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("가스기사 필기 합격 기준은?", "5과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다."),
      ("가스기사 응시 자격은?", "관련학과 4년제 대졸(예정)자, 가스산업기사 취득 후 1년 이상 경력자, 4년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("가스기사 자격의 활용 분야는?", "도시가스 제조·공급 시설, 고압가스 제조·저장·판매 업체에서 안전관리 책임자로 선임될 수 있습니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 건설안전산업기사 ─────────────────────────────────────
  {
    "file":     "exam-const-safety-ind.html",
    "type":     "const_safety_ind",
    "label":    "건설안전산업기사",
    "count":    100,
    "icon":     "🏗️",
    "title":    "건설안전산업기사 필기 무료 모의고사 – 100문항 기출",
    "desc":     "건설안전산업기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 안전관리론·인간공학·기계위험방지·전기위험방지·건설공사안전 5과목, 기출문제 기반.",
    "h1":       "건설안전산업기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-const-safety-ind.html",
    "badges":   ["🏗️ 건설안전산업기사", "📋 100문항 · 5과목", "⏱ 150분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>산업안전관리론 (20문항)</td></tr>
          <tr><th>2과목</th><td>인간공학 및 시스템안전공학 (20문항)</td></tr>
          <tr><th>3과목</th><td>기계위험방지기술 (20문항)</td></tr>
          <tr><th>4과목</th><td>전기위험방지기술 (20문항)</td></tr>
          <tr><th>5과목</th><td>건설공사안전기술 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>150분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("건설안전산업기사 필기 합격 기준은?", "5과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다."),
      ("건설안전산업기사와 산업안전산업기사의 차이는?", "건설안전산업기사는 건설현장 특화 안전 자격이고, 산업안전산업기사는 제조업·일반 산업 전반을 다룹니다. 건설사 취업 시 건설안전 자격이 더 유리합니다."),
      ("건설안전산업기사 응시 자격은?", "관련학과 2년제 대졸(예정)자, 기능사 취득 후 1년 이상 실무경력자, 3년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 건설안전기사 ─────────────────────────────────────────
  {
    "file":     "exam-const-safety-eng.html",
    "type":     "const_safety_eng",
    "label":    "건설안전기사",
    "count":    120,
    "icon":     "🏗️",
    "title":    "건설안전기사 필기 무료 모의고사 – 120문항 기출",
    "desc":     "건설안전기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 안전관리론·인간공학·기계·전기·건설공사·화학설비 6과목, 기출문제 기반, 오답노트 제공.",
    "h1":       "건설안전기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-const-safety-eng.html",
    "badges":   ["🏗️ 건설안전기사", "📋 120문항 · 6과목", "⏱ 180분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>산업안전관리론 (20문항)</td></tr>
          <tr><th>2과목</th><td>인간공학 및 시스템안전공학 (20문항)</td></tr>
          <tr><th>3과목</th><td>기계위험방지기술 (20문항)</td></tr>
          <tr><th>4과목</th><td>전기위험방지기술 (20문항)</td></tr>
          <tr><th>5과목</th><td>건설공사안전기술 (20문항)</td></tr>
          <tr><th>6과목</th><td>화학설비위험방지기술 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>180분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("건설안전기사 필기 합격 기준은?", "6과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다."),
      ("건설안전기사 응시 자격은?", "관련학과 4년제 대졸(예정)자, 건설안전산업기사 취득 후 1년 이상 경력자, 4년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("건설안전기사 수요가 높은 이유는?", "중대재해처벌법 시행 이후 건설현장 안전관리자 선임 의무가 강화됐습니다. 대형 건설사, 건설 감리업체 등에서 필수 자격증으로 취급합니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 공조냉동기계기능사 ───────────────────────────────────
  {
    "file":     "exam-hvac-craft.html",
    "type":     "hvac_craft",
    "label":    "공조냉동기계기능사",
    "count":    60,
    "icon":     "❄️",
    "title":    "공조냉동기계기능사 필기 무료 모의고사 – 60문항 기출",
    "desc":     "공조냉동기계기능사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 냉동공학·공조설비·냉동관계법규 3과목, 기출문제 기반, 오답노트·타이머 제공.",
    "h1":       "공조냉동기계기능사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-hvac-craft.html",
    "badges":   ["❄️ 공조냉동기계기능사", "📋 60문항 · 3과목", "⏱ 60분", "✅ 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>냉동공학 (20문항)</td></tr>
          <tr><th>2과목</th><td>공조설비 (20문항)</td></tr>
          <tr><th>3과목</th><td>냉동관계법규 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>60분</td></tr>
          <tr><th>합격 기준</th><td>60점 이상 합격 (36문항)</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("공조냉동기계기능사 필기 합격 기준은?", "60문항 총점 60점(36문항) 이상이면 합격합니다."),
      ("공조냉동기계기능사 응시 자격이 있나요?", "응시 자격 제한이 없습니다. 누구나 응시할 수 있습니다."),
      ("공조냉동기계기능사 취득 후 할 수 있는 일은?", "냉동·냉장창고, 건물 냉난방 설비(에어컨), 식품 냉장 시설 등의 유지·보수 업무를 담당할 수 있습니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 공조냉동기계기사 ─────────────────────────────────────
  {
    "file":     "exam-hvac-eng.html",
    "type":     "hvac_eng",
    "label":    "공조냉동기계기사",
    "count":    100,
    "icon":     "❄️",
    "title":    "공조냉동기계기사 필기 무료 모의고사 – 100문항 기출",
    "desc":     "공조냉동기계기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 기계열역학·냉동공학·공기조화·냉동공조설비·법규 5과목, 기출문제 기반, 오답노트 제공.",
    "h1":       "공조냉동기계기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-hvac-eng.html",
    "badges":   ["❄️ 공조냉동기계기사", "📋 100문항 · 5과목", "⏱ 150분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>기계열역학 (20문항)</td></tr>
          <tr><th>2과목</th><td>냉동공학 (20문항)</td></tr>
          <tr><th>3과목</th><td>공기조화 (20문항)</td></tr>
          <tr><th>4과목</th><td>냉동공조설비 (20문항)</td></tr>
          <tr><th>5과목</th><td>냉동공조법규 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>150분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("공조냉동기계기사 필기 합격 기준은?", "5과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다."),
      ("공조냉동기계기사 응시 자격은?", "관련학과 4년제 대졸(예정)자, 공조냉동기계산업기사 취득 후 1년 이상 경력자, 4년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("공조냉동기계기사 자격의 활용 분야는?", "건물 냉난방 설비 설계·시공, 산업용 냉동 설비, 클린룸·데이터센터 항온항습 설비 분야에서 활용됩니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 대기환경기사 ─────────────────────────────────────────
  {
    "file":     "exam-air-eng.html",
    "type":     "air_eng",
    "label":    "대기환경기사",
    "count":    100,
    "icon":     "🌬️",
    "title":    "대기환경기사 필기 무료 모의고사 – 100문항 기출",
    "desc":     "대기환경기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 대기오염개론·연소공학·방지기술·공정시험·관계법규 5과목, 기출문제 기반, 오답노트 제공.",
    "h1":       "대기환경기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-air-eng.html",
    "badges":   ["🌬️ 대기환경기사", "📋 100문항 · 5과목", "⏱ 150분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>대기오염개론 (20문항)</td></tr>
          <tr><th>2과목</th><td>연소공학 (20문항)</td></tr>
          <tr><th>3과목</th><td>대기오염방지기술 (20문항)</td></tr>
          <tr><th>4과목</th><td>대기오염공정시험기준 (20문항)</td></tr>
          <tr><th>5과목</th><td>대기환경관계법규 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>150분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("대기환경기사 필기 합격 기준은?", "5과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다."),
      ("대기환경기사 응시 자격은?", "관련학과 4년제 대졸(예정)자, 대기환경산업기사 취득 후 1년 이상 경력자, 4년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("대기환경기사 자격의 활용 분야는?", "굴뚝 배출가스 측정·관리, 환경영향평가, 환경 컨설팅, 공공기관 환경 담당 등으로 진출할 수 있습니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 수질환경기사 ─────────────────────────────────────────
  {
    "file":     "exam-water-eng.html",
    "type":     "water_eng",
    "label":    "수질환경기사",
    "count":    100,
    "icon":     "💧",
    "title":    "수질환경기사 필기 무료 모의고사 – 100문항 기출",
    "desc":     "수질환경기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 수질오염개론·상하수도계획·방지기술·공정시험·관계법규 5과목, 기출문제 기반, 오답노트 제공.",
    "h1":       "수질환경기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-water-eng.html",
    "badges":   ["💧 수질환경기사", "📋 100문항 · 5과목", "⏱ 150분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>수질오염개론 (20문항)</td></tr>
          <tr><th>2과목</th><td>상하수도계획 (20문항)</td></tr>
          <tr><th>3과목</th><td>수질오염방지기술 (20문항)</td></tr>
          <tr><th>4과목</th><td>수질오염공정시험기준 (20문항)</td></tr>
          <tr><th>5과목</th><td>수질환경관계법규 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>150분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("수질환경기사 필기 합격 기준은?", "5과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다."),
      ("수질환경기사 응시 자격은?", "관련학과 4년제 대졸(예정)자, 수질환경산업기사 취득 후 1년 이상 경력자, 4년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("수질환경기사 자격의 활용 분야는?", "하수처리장, 정수장, 폐수처리 업체, 환경 컨설팅, 환경영향평가 업체 등에서 활용됩니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 승강기기능사 ─────────────────────────────────────────
  {
    "file":     "exam-elevator-craft.html",
    "type":     "elevator_craft",
    "label":    "승강기기능사",
    "count":    60,
    "icon":     "🛗",
    "title":    "승강기기능사 필기 무료 모의고사 – 60문항 기출",
    "desc":     "승강기기능사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 승강기개론·승강기보전·안전관리법규 3과목, 기출문제 기반, 오답노트·타이머 제공.",
    "h1":       "승강기기능사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-elevator-craft.html",
    "badges":   ["🛗 승강기기능사", "📋 60문항 · 3과목", "⏱ 60분", "✅ 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>승강기개론 (20문항)</td></tr>
          <tr><th>2과목</th><td>승강기보전 (20문항)</td></tr>
          <tr><th>3과목</th><td>승강기안전관리법규 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>60분</td></tr>
          <tr><th>합격 기준</th><td>60점 이상 합격 (36문항)</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("승강기기능사 필기 합격 기준은?", "60문항 총점 60점(36문항) 이상이면 합격합니다."),
      ("승강기기능사 응시 자격이 있나요?", "응시 자격 제한이 없습니다. 누구나 응시할 수 있습니다."),
      ("승강기기능사 취득 후 할 수 있는 일은?", "엘리베이터·에스컬레이터·무빙워크 등 승강기 설치·정비·점검 업무를 담당할 수 있습니다. 승강기 관련 업체 취업에 필수 자격입니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 승강기기사 ───────────────────────────────────────────
  {
    "file":     "exam-elevator-eng.html",
    "type":     "elevator_eng",
    "label":    "승강기기사",
    "count":    80,
    "icon":     "🛗",
    "title":    "승강기기사 필기 무료 모의고사 – 80문항 기출",
    "desc":     "승강기기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 승강기개론·설계·안전관리·관계법규 4과목, 기출문제 기반, 오답노트·타이머 제공.",
    "h1":       "승강기기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-elevator-eng.html",
    "badges":   ["🛗 승강기기사", "📋 80문항 · 4과목", "⏱ 120분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>승강기개론 (20문항)</td></tr>
          <tr><th>2과목</th><td>승강기설계 (20문항)</td></tr>
          <tr><th>3과목</th><td>승강기안전관리 (20문항)</td></tr>
          <tr><th>4과목</th><td>승강기관계법규 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>120분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("승강기기사 필기 합격 기준은?", "4과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다."),
      ("승강기기사 응시 자격은?", "관련학과 4년제 대졸(예정)자, 승강기기능사 취득 후 3년 이상 경력자, 4년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("승강기기사 자격의 활용 분야는?", "승강기 제조업체, 유지보수 전문업체, 건물 시설관리팀 등에서 승강기안전관리자로 선임될 수 있습니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 에너지관리기능사 ─────────────────────────────────────
  {
    "file":     "exam-energy-craft.html",
    "type":     "energy_craft",
    "label":    "에너지관리기능사",
    "count":    60,
    "icon":     "♨️",
    "title":    "에너지관리기능사 필기 무료 모의고사 – 60문항 기출",
    "desc":     "에너지관리기능사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 연소공학·열관리설비·관계법규 3과목, 기출문제 기반, 오답노트·타이머 제공.",
    "h1":       "에너지관리기능사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-energy-craft.html",
    "badges":   ["♨️ 에너지관리기능사", "📋 60문항 · 3과목", "⏱ 60분", "✅ 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>연소공학 (20문항)</td></tr>
          <tr><th>2과목</th><td>열관리설비 (20문항)</td></tr>
          <tr><th>3과목</th><td>관계법규 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>60분</td></tr>
          <tr><th>합격 기준</th><td>60점 이상 합격 (36문항)</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("에너지관리기능사 필기 합격 기준은?", "60문항 총점 60점(36문항) 이상이면 합격합니다."),
      ("에너지관리기능사 응시 자격이 있나요?", "응시 자격 제한이 없습니다. 누구나 응시할 수 있습니다."),
      ("에너지관리기능사 취득 후 할 수 있는 일은?", "보일러 운전·관리, 열사용 기자재 취급, 산업체 에너지 관리 분야에서 활용됩니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
  # ── 에너지관리기사 ───────────────────────────────────────
  {
    "file":     "exam-energy-eng.html",
    "type":     "energy_eng",
    "label":    "에너지관리기사",
    "count":    100,
    "icon":     "♨️",
    "title":    "에너지관리기사 필기 무료 모의고사 – 100문항 기출",
    "desc":     "에너지관리기사 필기 무료 모의고사. 회원가입 없이 즉시 시작, 연소공학·열역학·계측방법·열설비설계·열관계법규 5과목, 기출문제 기반, 오답노트 제공.",
    "h1":       "에너지관리기사 필기 모의고사",
    "canonical":"https://wooagosa.wooahouse.com/exam-energy-eng.html",
    "badges":   ["♨️ 에너지관리기사", "📋 100문항 · 5과목", "⏱ 150분", "✅ 평균 60점 합격"],
    "info": """<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>1과목</th><td>연소공학 (20문항)</td></tr>
          <tr><th>2과목</th><td>열역학 (20문항)</td></tr>
          <tr><th>3과목</th><td>계측방법 (20문항)</td></tr>
          <tr><th>4과목</th><td>열설비설계 (20문항)</td></tr>
          <tr><th>5과목</th><td>열관계법규 (20문항)</td></tr>
          <tr><th>시험 시간</th><td>150분</td></tr>
          <tr><th>합격 기준</th><td>과목당 40점↑ + 전과목 평균 60점↑</td></tr>
          <tr><th>주관</th><td>한국산업인력공단</td></tr>
        </table>
      </div>""",
    "faq": [
      ("에너지관리기사 필기 합격 기준은?", "5과목 각각 40점 이상이면서 전과목 평균 60점 이상이어야 합격합니다."),
      ("에너지관리기사 응시 자격은?", "관련학과 4년제 대졸(예정)자, 에너지관리산업기사 취득 후 1년 이상 경력자, 4년 이상 실무경력자 등이 응시할 수 있습니다."),
      ("에너지관리기사 자격의 활용 분야는?", "발전소, 제철소, 화학공장 등 대규모 열사용 시설의 에너지관리자로 선임될 수 있습니다. 에너지 절약 전문기업(ESCO)에서도 필수 자격입니다."),
      ("오답 데이터는 어디에 저장되나요?", "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ],
  },
]

# ── 신규 자격증 자동 추가 ────────────────────────────────
import json as _json
from pathlib import Path as _Path

_DATA_DIR = _Path(r"C:\개인\wooahouse\wooaGosa\data")

# 기존 EXAMS에서 이미 등록된 type 목록
_EXISTING_TYPES = {e["type"] for e in EXAMS}

# 기존 영문키 JSON (파서가 FOLDER_TO_KEY로 생성한 파일들) — 이미 위 EXAMS에 포함
_EXISTING_FILES = {
    "air_eng","bread","computer_1","computer_2","const_safety_eng","const_safety_ind",
    "elec_craft","elec_eng","elec_ind","elevator_craft","elevator_eng","energy_craft",
    "energy_eng","excavator","fire_elec","fire_mech","forklift","gas_craft","gas_eng",
    "gas_ind","hazmat_craft","hazmat_ind","history_advanced","history_basic","hvac_craft",
    "hvac_eng","info_ind","info_proc","info_sec","korean_cook","license_1_2","linux_1",
    "linux_2","motorcycle","net_1","net_2","pastry","realtor_1","realtor_2","safety_eng",
    "safety_ind","water_eng","welfare_1","welfare_2","welfare_3","word",
    # 컴퓨터활용능력 cbtestpro버전은 기존 computer_1/2 페이지로 처리
    "컴퓨터활용능력_1급","컴퓨터활용능력_2급",
}


def _auto_count(name):
    if "기능사" in name or "기능장" in name: return 60
    if "산업기사" in name: return 80
    if "기사" in name: return 100
    return 60


def _auto_time(name):
    if "기능사" in name: return 60
    if "기능장" in name: return 90
    if "산업기사" in name: return 150
    if "기사" in name: return 150
    return 90


def _auto_pass(name):
    if "기능사" in name or "기능장" in name: return "60점 이상 (36문항↑)"
    return "과목당 40점↑ + 평균 60점↑"


def _auto_icon(name):
    k = name
    if any(x in k for x in ["전기","전자","전력","통신","철도신호"]): return "⚡"
    if any(x in k for x in ["기계","설비","압연","용접","주조","열처리","금형","판금"]): return "⚙️"
    if any(x in k for x in ["건설","토목","측량","측지","지적","도시","교통"]): return "🏗️"
    if any(x in k for x in ["건축","실내","목공","창호"]): return "🏛️"
    if any(x in k for x in ["화학","화공","화약","가스","위험물","방사선"]): return "🧪"
    if any(x in k for x in ["환경","대기","수질","소음","폐기물","토양","온실"]): return "🌱"
    if any(x in k for x in ["식품","조리","제과","제빵","조주"]): return "🍽️"
    if any(x in k for x in ["농업","농기계","농작업","종자","버섯","원예","임업"]): return "🌾"
    if any(x in k for x in ["소방","방재","화재"]): return "🔥"
    if any(x in k for x in ["안전","산업위생","소음진동","인간공학"]): return "⛑️"
    if any(x in k for x in ["정보","컴퓨터","멀티","전산"]): return "💻"
    if any(x in k for x in ["조선","선체","해양","항로","잠수"]): return "⚓"
    if any(x in k for x in ["미용","이용","한복","섬유","패션","의류"]): return "✂️"
    if any(x in k for x in ["광학","의공","바이오","의료"]): return "🔬"
    if any(x in k for x in ["광산","응용지질","자원"]): return "⛏️"
    if any(x in k for x in ["크레인","지게차","굴착","운전","모터그레이더","양화"]): return "🚜"
    if any(x in k for x in ["철도","차량"]): return "🚂"
    if any(x in k for x in ["승강기"]): return "🛗"
    if any(x in k for x in ["산림","수산","축산"]): return "🌿"
    return "📝"


def _auto_exam(key, name):
    cnt = _auto_count(name)
    t   = _auto_time(name)
    ps  = _auto_pass(name)
    icon = _auto_icon(name)
    html_file = f"exam-{key}.html"
    url  = f"https://wooagosa.wooahouse.com/{html_file}"

    level = "기능사" if "기능사" in name else "기능장" if "기능장" in name else "산업기사" if "산업기사" in name else "기사" if "기사" in name else ""
    choices_str = "4지선다" if "기능사" in name or "기사" in name else "4지선다"

    badges = [f"{icon} {name}", f"📋 {cnt}문항", f"⏱ {t}분", f"✅ {ps[:5]}합격"]

    info = f"""<div class="exam-info-box">
        <h2 class="section-title">시험 안내</h2>
        <table class="info-table">
          <tr><th>자격 종목</th><td>{name}</td></tr>
          <tr><th>문항 수</th><td>{cnt}문항 ({choices_str})</td></tr>
          <tr><th>시험 시간</th><td>{t}분</td></tr>
          <tr><th>합격 기준</th><td>{ps}</td></tr>
          <tr><th>주관 기관</th><td>한국산업인력공단 (큐넷)</td></tr>
        </table>
      </div>"""

    faq = [
        (f"{name} 모의고사는 어떻게 활용하나요?",
         f"기출문제 PDF를 파싱해 {cnt}문항을 랜덤 출제합니다. 랜덤·순서·오답 집중 3가지 모드로 연습할 수 있습니다."),
        (f"{name} 필기 합격 기준은?",
         f"{ps}입니다. 시험 세부 일정은 큐넷(q-net.or.kr)에서 확인하세요."),
        ("문제 출처는 어디인가요?",
         "한국산업인력공단이 시행한 과거 기출문제를 기반으로 합니다. 최신 출제 경향 반영을 위해 정기적으로 업데이트됩니다."),
        ("오답 데이터는 어디에 저장되나요?",
         "모든 오답 데이터는 브라우저 로컬 스토리지에만 저장되며 서버로 전송되지 않습니다."),
    ]

    return {
        "file":      html_file,
        "type":      key,
        "label":     name,
        "count":     cnt,
        "icon":      icon,
        "title":     f"{name} 무료 모의고사 – 기출문제 {cnt}문항",
        "desc":      f"{name} 무료 모의고사. 큐넷 기출문제 기반 {cnt}문항 랜덤 출제, 오답노트·타이머 제공. 회원가입 없이 즉시 시작.",
        "h1":        f"{name} 기출 모의고사",
        "canonical": url,
        "badges":    badges,
        "info":      info,
        "faq":       faq,
    }


# 신규 자격증 스캔 및 EXAMS 확장
for _jf in sorted(_DATA_DIR.glob("*.json")):
    _stem = _jf.stem          # e.g. "가구제작기능사"
    if _stem in _EXISTING_FILES:
        continue
    # 영문 키는 이미 EXAMS에 있음
    if _stem in _EXISTING_TYPES:
        continue
    # 데이터가 있는지 확인
    try:
        _data = _json.loads(_jf.read_text(encoding="utf-8"))
        if not _data:
            continue
    except Exception:
        continue
    EXAMS.append(_auto_exam(_stem, _stem))


# ── HTML 생성 함수 ──────────────────────────────────────

def links_html(exam_type):
    return f'''      <div class="exam-schedule-box">
        <span class="sch-label">📅 시험 일정 · 접수</span>
        <div class="exam-link-btns">
        <a href="https://gosapass.kr/" target="_blank" rel="noopener" class="exam-link-btn">시험일정·접수 바로가기 ↗</a>
        </div>
      </div>'''

def faq_html(items):
    html = '<section style="margin-top:2.5rem;" aria-label="자주 묻는 질문">\n'
    html += '        <h2 class="section-title">자주 묻는 질문</h2>\n'
    html += '        <div class="faq-list">\n'
    for q, a in items:
        html += f"""          <div class="faq-item">
            <button class="faq-question" onclick="toggleFaq(this)">
              {q}
              <span class="faq-icon">+</span>
            </button>
            <div class="faq-answer">
              <div class="faq-answer-inner">{a}</div>
            </div>
          </div>\n"""
    html += '        </div>\n      </section>'
    return html

def make_page(exam):
    badges_html = ' '.join(f'<span class="badge">{b}</span>' for b in exam["badges"])
    faq  = faq_html(exam["faq"])
    lnks = links_html(exam["type"])
    fname = exam["file"]

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
{GA}
  <meta name="naver-site-verification" content="e97ec06f3d64c3b7795ba7724e1f0be02a26fb41" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="img/icon.svg" type="image/svg+xml">
  <title>{exam["title"]} – WooaGosa</title>
  <meta name="description" content="{exam["desc"]}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{exam["canonical"]}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{exam["title"]} – WooaGosa">
  <meta property="og:description" content="{exam["desc"]}">
  <meta property="og:url" content="{exam["canonical"]}">
  <meta property="og:locale" content="ko_KR">
  <meta property="og:site_name" content="WooaGosa">
  <link rel="manifest" href="manifest.json">
  <meta name="theme-color" content="#1a3a5c">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6464921081676309" crossorigin="anonymous"></script>
  <style>
    .exam-info-box {{ margin-bottom: 1.5rem; }}
    .info-table {{ width: 100%; border-collapse: collapse; font-size: .9rem; }}
    .info-table th, .info-table td {{ padding: .55rem .75rem; border-bottom: 1px solid var(--border); text-align: left; }}
    .info-table th {{ width: 7rem; color: var(--text-mid); font-weight: 600; background: var(--bg); }}
    .mode-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
      gap: .75rem; margin-top: 1rem;
    }}
    .mode-card {{
      background: var(--card-bg); border: 2px solid var(--border);
      border-radius: var(--radius-sm); padding: 1rem;
      cursor: pointer; transition: var(--trans); text-align: center;
    }}
    .mode-card:hover {{ border-color: var(--blue); background: #eff6ff; }}
    .mode-card.active {{ border-color: var(--blue); background: #dbeafe; }}
    .mode-card .mode-icon {{ font-size: 1.6rem; margin-bottom: .4rem; }}
    .mode-card .mode-name {{ font-weight: 700; font-size: .9rem; color: var(--navy); }}
    .mode-card .mode-desc {{ font-size: .78rem; color: var(--text-mid); margin-top: .25rem; }}
    .start-bar {{
      background: var(--card-bg); border: 1px solid var(--border);
      border-radius: var(--radius); padding: 1.25rem 1.5rem;
      display: flex; align-items: center; justify-content: space-between;
      gap: 1rem; flex-wrap: wrap; box-shadow: var(--shadow);
      margin-top: 1.25rem;
    }}
    .breadcrumb {{ max-width:1200px; margin:.75rem auto; padding:0 1.25rem; font-size:.85rem; color:var(--text-mid); }}
    .breadcrumb a {{ color:var(--text-mid); text-decoration:none; }}
    .breadcrumb a:hover {{ color:var(--blue); }}
    .exam-schedule-box {{
      background: var(--card-bg); border: 1px solid var(--border);
      border-radius: var(--radius-sm); padding: .9rem 1.25rem;
      margin-bottom: 1.5rem; display: flex; align-items: center;
      gap: .75rem; flex-wrap: wrap;
    }}
    .sch-label {{ font-weight: 700; color: var(--navy); font-size: .9rem; flex-shrink: 0; }}
    .exam-link-btns {{ display: flex; gap: .5rem; flex-wrap: wrap; }}
    .exam-link-btn {{
      display: inline-flex; align-items: center; gap: .3rem;
      padding: .45rem .95rem; background: var(--bg);
      border: 1.5px solid var(--border); border-radius: var(--radius-sm);
      color: var(--navy); font-weight: 600; font-size: .82rem;
      text-decoration: none; transition: var(--trans); white-space: nowrap;
    }}
    .exam-link-btn:hover {{ border-color: var(--blue); color: var(--blue); background: #eff6ff; }}
  </style>
</head>
<body>

<header class="site-header">
  <div class="header-inner">
    <a href="index.html" class="logo">
      <span class="logo-icon">{exam["icon"]}</span>
      Wooa<span>Gosa</span>
    </a>
    <nav class="header-nav">
      <a href="index.html">홈</a>
      <a href="wrong-notes.html">오답노트</a>
    </nav>
  </div>
</header>

{SITES_BAR}

<section class="hero" style="padding:2rem 1.25rem 1.5rem;">
  <h1>{exam["h1"]}</h1>
  <div class="hero-badges">
    {badges_html}
    <span class="badge">📝 오답노트</span>
    <span class="badge">🆓 무료</span>
  </div>
</section>

<main>

{MOBILE_AD}

<nav class="breadcrumb" aria-label="breadcrumb">
  <a href="index.html">홈</a> &rsaquo; <span>{exam["h1"]}</span>
</nav>

  <div class="page-with-sidebar">
    <div class="gosa-main">

      {exam["info"]}

{lnks}

      <section aria-label="풀기 방식 선택">
        <h2 class="section-title">풀기 방식 선택</h2>
        <div class="mode-grid">
          <div class="mode-card active" data-mode="random" onclick="selectMode('random',this)">
            <div class="mode-icon">🎲</div>
            <div class="mode-name">랜덤 {exam["count"]}문제</div>
            <div class="mode-desc">무작위 {exam["count"]}문제<br>타이머 있음</div>
          </div>
          <div class="mode-card" data-mode="sequential" onclick="selectMode('sequential',this)">
            <div class="mode-icon">📋</div>
            <div class="mode-name">전체 순서대로</div>
            <div class="mode-desc">처음부터 순서대로<br>시간 제한 없음</div>
          </div>
          <div class="mode-card" data-mode="wrong" onclick="selectMode('wrong',this)">
            <div class="mode-icon">🔁</div>
            <div class="mode-name">오답 집중</div>
            <div class="mode-desc">틀린 문제만 반복<br>최대 {exam["count"]}문제</div>
          </div>
        </div>
        <div class="start-bar">
          <div style="font-size:.95rem; color:var(--text-mid);">
            선택: <strong style="color:var(--navy);">{exam["label"]}</strong> ·
            <strong id="sb-mode" style="color:var(--navy);">랜덤 {exam["count"]}문제</strong>
          </div>
          <button class="btn btn-primary btn-lg" onclick="startExam()">시험 시작 →</button>
        </div>
      </section>

{MOBILE_INLINE_AD}

      {faq}

    </div>

{SIDEBAR_ADS}

  </div>
</main>

<footer class="site-footer">
  <p>© 2026 WooaGosa · <a href="https://wooahouse.com" target="_blank">WooaHouse</a></p>
</footer>

<script src="js/sites-bar.js"></script>
<script>
  let selectedMode = 'random';

  function selectMode(mode, el) {{
    selectedMode = mode;
    document.querySelectorAll('.mode-card').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    const names = {{ random:'랜덤 {exam["count"]}문제', sequential:'전체 순서대로', wrong:'오답 집중' }};
    document.getElementById('sb-mode').textContent = names[mode] || mode;
  }}

  function startExam() {{
    location.href = `exam.html?type={exam["type"]}&mode=${{selectedMode}}&label={exam["label"].replace(" ", "%20")}&count={exam["count"]}`;
  }}

  function toggleFaq(btn) {{
    btn.closest('.faq-item').classList.toggle('open');
  }}
</script>
<script>
  if ('serviceWorker' in navigator) {{
    navigator.serviceWorker.register('sw.js').catch(() => {{}});
  }}
</script>
</body>
</html>'''

# ── 파일 생성 ──────────────────────────────────────────

for exam in EXAMS:
    path = OUT_DIR / exam["file"]
    content = make_page(exam)
    path.write_text(content, encoding='utf-8')
    print(f"✓ {exam['file']}")

print(f"\n총 {len(EXAMS)}개 페이지 생성 완료")
