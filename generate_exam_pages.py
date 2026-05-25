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
    "title":    "1종 대형 면허 학과시험 모의고사 무료",
    "desc":     "1종 대형 운전면허 학과시험 무료 모의고사. 최신 문제은행 1,000문제 기반, 60문제 랜덤 출제, 오답노트·타이머 제공. 브라우저에서 바로 시작.",
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
    "title":    "1종 보통 면허 학과시험 모의고사 무료",
    "desc":     "1종 보통 운전면허 학과시험 무료 모의고사. 최신 문제은행 1,000문제 기반, 40문제 랜덤 출제, 오답노트·타이머 제공. 회원가입 없이 바로 시작.",
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
    "title":    "2종 보통 면허 학과시험 모의고사 무료",
    "desc":     "2종 보통 운전면허 학과시험 무료 모의고사. 최신 문제은행 1,000문제 기반, 40문제 랜덤 출제, 오답노트·타이머 제공. 브라우저에서 바로 시작.",
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
    "title":    "이륜자동차(오토바이) 면허 학과시험 모의고사 무료",
    "desc":     "2종 소형(이륜자동차) 운전면허 학과시험 무료 모의고사. 문제은행 800문제 기반, 40문제 랜덤 출제, 오답노트·타이머 제공.",
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
    "title":    "원동기장치자전거(전동킥보드) 면허 학과시험 모의고사 무료",
    "desc":     "원동기장치자전거 운전면허 학과시험 무료 모의고사. 전동킥보드·125cc 이하 오토바이, 문제은행 800문제 기반, 오답노트·타이머 제공.",
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
    "title":    "한국사능력검정시험 기본 모의고사 무료",
    "desc":     "한국사능력검정시험(한능검) 기본 무료 모의고사. 4급·5급·6급 대비, 4지선다 50문항, 오답노트 제공. 기출문제 기반으로 브라우저에서 바로 시작.",
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
    "title":    "한국사능력검정시험 심화 모의고사 무료",
    "desc":     "한국사능력검정시험(한능검) 심화 무료 모의고사. 1급·2급·3급 대비, 5지선다 50문항, 오답노트 제공. 기출문제 기반으로 브라우저에서 바로 시작.",
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
    "title":    "컴퓨터활용능력 1급 필기 모의고사 무료",
    "desc":     "컴퓨터활용능력(컴활) 1급 필기 무료 모의고사. 3과목(컴퓨터일반·스프레드시트·데이터베이스), 기출 486문항, 60분 타이머, 오답노트 제공.",
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
    "title":    "컴퓨터활용능력 2급 필기 모의고사 무료",
    "desc":     "컴퓨터활용능력(컴활) 2급 필기 무료 모의고사. 2과목(컴퓨터일반·스프레드시트), 기출 322문항, 40분 타이머, 오답노트 제공.",
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
