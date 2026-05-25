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
  </div>"""

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
    "title":    "오토바이(이륜자동차) 면허 무료 모의고사 – 학과시험 40문항",
    "desc":     "2종 소형(이륜자동차) 운전면허 무료 모의고사. 회원가입 없이 즉시 시작, 문제은행 800문제 기반, 40문제 랜덤 출제, 오답노트·타이머 제공.",
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
    "title":    "원동기장치자전거(전동킥보드) 면허 무료 모의고사 – 40문항",
    "desc":     "원동기장치자전거(전동킥보드·125cc 이하) 면허 무료 모의고사. 회원가입 없이 즉시 시작, 문제은행 800문제 기반, 40문제 랜덤 출제, 오답노트·타이머 제공.",
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
]

# ── HTML 생성 함수 ──────────────────────────────────────

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
    faq = faq_html(exam["faq"])
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

<nav class="breadcrumb" aria-label="breadcrumb">
  <a href="index.html">홈</a> &rsaquo; <span>{exam["h1"]}</span>
</nav>

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

  <div class="page-with-sidebar">
    <div class="gosa-main">

      {exam["info"]}

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
