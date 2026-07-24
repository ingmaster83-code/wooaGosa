/**
 * exam.js – 시험 진행 로직
 *
 * URL 파라미터:
 *   type  = 'license12' | 'motorcycle'
 *   mode  = 'random' | 'sequential' | 'wrong'
 *   count = 숫자 (선택, 기본 40)
 */

/* ── 전역 상태 ─────────────────────────────────── */
const params  = new URLSearchParams(location.search);
const TYPE    = params.get('type')  || 'license12';
const MODE    = params.get('mode')  || 'random';

const FILE = (() => {
  if (TYPE === 'motorcycle' || TYPE === 'motorbike') return 'motorcycle';
  if (TYPE === 'history_basic')    return 'history_basic';
  if (TYPE === 'history_advanced') return 'history_advanced';
  if (TYPE === 'computer_1')       return 'computer_1';
  if (TYPE === 'computer_2')       return 'computer_2';
  if (TYPE === 'net_1')            return 'net_1';
  if (TYPE === 'net_2')            return 'net_2';
  if (TYPE === 'linux_1')          return 'linux_1';
  if (TYPE === 'linux_2')          return 'linux_2';
  if (TYPE === 'word')             return 'word';
  if (TYPE === 'elec_eng')         return 'elec_eng';
  if (TYPE === 'elec_ind')         return 'elec_ind';
  if (TYPE === 'info_proc')        return 'info_proc';
  if (TYPE === 'info_ind')         return 'info_ind';
  if (TYPE === 'info_sec')         return 'info_sec';
  if (TYPE === 'hazmat_ind')       return 'hazmat_ind';
  if (TYPE === 'hazmat_craft')     return 'hazmat_craft';
  if (TYPE === 'fire_mech')        return 'fire_mech';
  if (TYPE === 'fire_elec')        return 'fire_elec';
  if (TYPE === 'forklift')         return 'forklift';
  if (TYPE === 'excavator')        return 'excavator';
  if (TYPE === 'realtor_1')        return 'realtor_1';
  if (TYPE === 'realtor_2')        return 'realtor_2';
  if (TYPE === 'welfare_1')        return 'welfare_1';
  if (TYPE === 'welfare_2')        return 'welfare_2';
  if (TYPE === 'welfare_3')        return 'welfare_3';
  if (TYPE === 'safety_ind')       return 'safety_ind';
  if (TYPE === 'safety_eng')       return 'safety_eng';
  if (TYPE === 'elec_craft')       return 'elec_craft';
  if (TYPE === 'pastry')           return 'pastry';
  if (TYPE === 'bread')            return 'bread';
  if (TYPE === 'korean_cook')      return 'korean_cook';
  if (TYPE === 'gas_craft')        return 'gas_craft';
  if (TYPE === 'gas_ind')          return 'gas_ind';
  if (TYPE === 'gas_eng')          return 'gas_eng';
  if (TYPE === 'const_safety_ind') return 'const_safety_ind';
  if (TYPE === 'const_safety_eng') return 'const_safety_eng';
  if (TYPE === 'hvac_craft')       return 'hvac_craft';
  if (TYPE === 'hvac_eng')         return 'hvac_eng';
  if (TYPE === 'air_eng')          return 'air_eng';
  if (TYPE === 'water_eng')        return 'water_eng';
  if (TYPE === 'elevator_craft')   return 'elevator_craft';
  if (TYPE === 'elevator_eng')     return 'elevator_eng';
  if (TYPE === 'energy_craft')     return 'energy_craft';
  if (TYPE === 'energy_eng')       return 'energy_eng';
  // 신규 자격증: type을 그대로 파일명으로 사용
  return TYPE;
})();

const DEFAULT_COUNT = {
  'history_basic': 50, 'history_advanced': 50,
  'computer_1': 60, 'computer_2': 40,
  'net_1': 60, 'net_2': 50,
  'linux_1': 100, 'linux_2': 80,
  'word': 60,
  'elec_eng': 100, 'elec_ind': 100,
  'info_proc': 100, 'info_ind': 100, 'info_sec': 100,
  'hazmat_ind': 60, 'hazmat_craft': 60,
  'fire_mech': 80, 'fire_elec': 80,
  'forklift': 60, 'excavator': 60,
  'realtor_1': 80, 'realtor_2': 120,
  'welfare_1': 50, 'welfare_2': 75, 'welfare_3': 75,
  'safety_ind': 100, 'safety_eng': 120,
  'elec_craft': 60, 'pastry': 60, 'bread': 60, 'korean_cook': 60,
  'gas_craft': 60, 'gas_ind': 60, 'gas_eng': 100,
  'const_safety_ind': 100, 'const_safety_eng': 120,
  'hvac_craft': 60, 'hvac_eng': 100,
  'air_eng': 100, 'water_eng': 100,
  'elevator_craft': 60, 'elevator_eng': 80,
  'energy_craft': 60, 'energy_eng': 100,
};
function autoCount(f) {
  if (f.includes('기능사') || f.includes('기능장') || f.includes('운전기능사')) return 60;
  if (f.includes('산업기사')) return 80;
  if (f.includes('기사')) return 100;
  return 60;
}
const COUNT = parseInt(params.get('count') || String(DEFAULT_COUNT[FILE] || autoCount(FILE)));

const DATA_URL_MAP = {
  'license12':        'data/license_1_2.json',
  'motorcycle':       'data/motorcycle.json',
  'history_basic':    'data/history_basic.json',
  'history_advanced': 'data/history_advanced.json',
  'computer_1':       'data/computer_1.json',
  'computer_2':       'data/computer_2.json',
  'net_1':            'data/net_1.json',
  'net_2':            'data/net_2.json',
  'linux_1':          'data/linux_1.json',
  'linux_2':          'data/linux_2.json',
  'word':             'data/word.json',
  'elec_eng':         'data/elec_eng.json',
  'elec_ind':         'data/elec_ind.json',
  'info_proc':        'data/info_proc.json',
  'info_ind':         'data/info_ind.json',
  'info_sec':         'data/info_sec.json',
  'hazmat_ind':       'data/hazmat_ind.json',
  'hazmat_craft':     'data/hazmat_craft.json',
  'fire_mech':        'data/fire_mech.json',
  'fire_elec':        'data/fire_elec.json',
  'forklift':         'data/forklift.json',
  'excavator':        'data/excavator.json',
  'realtor_1':        'data/realtor_1.json',
  'realtor_2':        'data/realtor_2.json',
  'welfare_1':        'data/welfare_1.json',
  'welfare_2':        'data/welfare_2.json',
  'welfare_3':        'data/welfare_3.json',
  'safety_ind':       'data/safety_ind.json',
  'safety_eng':       'data/safety_eng.json',
  'elec_craft':       'data/elec_craft.json',
  'pastry':           'data/pastry.json',
  'bread':            'data/bread.json',
  'korean_cook':      'data/korean_cook.json',
  'gas_craft':        'data/gas_craft.json',
  'gas_ind':          'data/gas_ind.json',
  'gas_eng':          'data/gas_eng.json',
  'const_safety_ind': 'data/const_safety_ind.json',
  'const_safety_eng': 'data/const_safety_eng.json',
  'hvac_craft':       'data/hvac_craft.json',
  'hvac_eng':         'data/hvac_eng.json',
  'air_eng':          'data/air_eng.json',
  'water_eng':        'data/water_eng.json',
  'elevator_craft':   'data/elevator_craft.json',
  'elevator_eng':     'data/elevator_eng.json',
  'energy_craft':     'data/energy_craft.json',
  'energy_eng':       'data/energy_eng.json',
};
const DATA_URL = DATA_URL_MAP[FILE] || `data/${FILE}.json`;

// 시험 유형 표시명 (URL label 파라미터 우선, 없으면 type으로 매핑)
const TYPE_LABELS = {
  '1jong-daebyeong':   '1종 대형',
  '1jong-botong':      '1종 보통',
  '2jong-botong':      '2종 보통',
  'motorcycle':        '2종 소형(이륜)',
  'motorbike':         '원동기장치자전거',
  'license12':         '1·2종 면허',
  'history_basic':     '한국사 기본',
  'history_advanced':  '한국사 심화',
  'computer_1':        '컴퓨터활용능력 1급',
  'computer_2':        '컴퓨터활용능력 2급',
  'net_1':             '네트워크관리사 1급',
  'net_2':             '네트워크관리사 2급',
  'linux_1':           '리눅스마스터 1급',
  'linux_2':           '리눅스마스터 2급',
  'word':              '워드프로세서',
  'elec_eng':          '전기기사',
  'elec_ind':          '전기산업기사',
  'info_proc':         '정보처리기사',
  'info_ind':          '정보처리산업기사',
  'info_sec':          '정보보안기사',
  'hazmat_ind':        '위험물산업기사',
  'hazmat_craft':      '위험물기능사',
  'fire_mech':         '소방설비기사 기계분야',
  'fire_elec':         '소방설비기사 전기분야',
  'forklift':          '지게차운전기능사',
  'excavator':         '굴착기운전기능사',
  'realtor_1':         '공인중개사 1차',
  'realtor_2':         '공인중개사 2차',
  'welfare_1':         '사회복지사1급 1교시',
  'welfare_2':         '사회복지사1급 2교시',
  'welfare_3':         '사회복지사1급 3교시',
  'safety_ind':        '산업안전산업기사',
  'safety_eng':        '산업안전기사',
  'elec_craft':        '전기기능사',
  'pastry':            '제과기능사',
  'bread':             '제빵기능사',
  'korean_cook':       '한식조리기능사',
  'gas_craft':         '가스기능사',
  'gas_ind':           '가스산업기사',
  'gas_eng':           '가스기사',
  'const_safety_ind':  '건설안전산업기사',
  'const_safety_eng':  '건설안전기사',
  'hvac_craft':        '공조냉동기계기능사',
  'hvac_eng':          '공조냉동기계기사',
  'air_eng':           '대기환경기사',
  'water_eng':         '수질환경기사',
  'elevator_craft':    '승강기기능사',
  'elevator_eng':      '승강기기사',
  'energy_craft':      '에너지관리기능사',
  'energy_eng':        '에너지관리기사',
};
const typeLabel = params.get('label') || TYPE_LABELS[TYPE] || TYPE;

let allQuestions  = [];   // 전체 문제 데이터
let examQuestions = [];   // 현재 시험에 사용할 문제
let current       = 0;    // 현재 문제 인덱스
let userAnswers   = [];   // 사용자 답 [{selected:[], correct:bool}]
let timerHandle   = null;
let secondsLeft   = 0;
let examStarted   = false;

/* ── 구간 나누기 (페이지뷰/광고) ─────────────────
 * 10문제마다 실제 페이지를 새로고침해서 광고가 새로 노출되도록 함.
 * 문제 수가 10개 미만인 시험(오답노트 복습 등)은 경계에 도달하지 않아 자동으로 영향 없음.
 */
const SEGMENT_SIZE = 10;
const SEGMENTED = true;
const PROGRESS_KEY = 'wooagosa_segprogress';
const AUTO_CONTINUE_KEY = 'wooagosa_segautocontinue'; // 구간 버튼으로 넘어온 새로고침인지 구분
let examEndTime = null; // SEGMENTED 전용: 절대 종료 시각(ms). 새로고침에도 타이머 유지.
let pendingResume = null; // 이어하기 선택 화면에서 사용할 저장된 진행상태

function saveProgress() {
  if (!SEGMENTED) return;
  sessionStorage.setItem(PROGRESS_KEY, JSON.stringify({
    file: FILE, mode: MODE, count: COUNT,
    ids: examQuestions.map(q => q.id),
    userAnswers, current, examEndTime,
  }));
}

function loadProgress() {
  if (!SEGMENTED) return null;
  try {
    const raw = sessionStorage.getItem(PROGRESS_KEY);
    if (!raw) return null;
    const p = JSON.parse(raw);
    if (p.file !== FILE || p.mode !== MODE || p.count !== COUNT) return null;
    return p;
  } catch (e) { return null; }
}

function clearProgress() {
  sessionStorage.removeItem(PROGRESS_KEY);
}

/* ── DOM 참조 ──────────────────────────────────── */
const elTitle      = document.getElementById('exam-title');
const elProgress   = document.getElementById('exam-progress');
const elTimer      = document.getElementById('timer');
const elProgressBar= document.getElementById('progress-bar');
const elQuestion   = document.getElementById('question-area');
const elNavPrev    = document.getElementById('btn-prev');
const elNavNext    = document.getElementById('btn-next');
const elNavSubmit  = document.getElementById('btn-submit');
const elModalOvl   = document.getElementById('modal-overlay');
const elModalMsg   = document.getElementById('modal-msg');
const elModalOk    = document.getElementById('modal-ok');
const elModalCancel= document.getElementById('modal-cancel');

/* ── 초기화 ────────────────────────────────────── */
window.addEventListener('DOMContentLoaded', async () => {
  elTitle.textContent = typeLabel + ' 모의고사';
  // 로고 아이콘 업데이트
  const logoIcon = document.getElementById('logo-icon');
  if (logoIcon) {
    const ICONS = {
      'history_basic': '📜', 'history_advanced': '📜',
      'motorcycle': '🏍', 'motorbike': '🛵',
      'computer_1': '💻', 'computer_2': '💻',
      'net_1': '🌐', 'net_2': '🌐',
      'linux_1': '🐧', 'linux_2': '🐧',
      'word': '📝',
      'elec_eng': '⚡', 'elec_ind': '⚡',
      'info_proc': '🖥️', 'info_ind': '🖥️',
      'info_sec': '🔒',
      'hazmat_ind': '🧪', 'hazmat_craft': '🧪',
      'fire_mech': '🔥', 'fire_elec': '🔥',
      'forklift': '🚜', 'excavator': '🏗️',
      'realtor_1': '🏠', 'realtor_2': '🏠',
      'welfare_1': '👐', 'welfare_2': '👐', 'welfare_3': '👐',
      'safety_ind': '⛑️', 'safety_eng': '⛑️',
      'elec_craft': '⚡', 'pastry': '🍰', 'bread': '🍞', 'korean_cook': '🍲',
      'gas_craft': '🔥', 'gas_ind': '🔥', 'gas_eng': '🔥',
      'const_safety_ind': '🏗️', 'const_safety_eng': '🏗️',
      'hvac_craft': '❄️', 'hvac_eng': '❄️',
      'air_eng': '🌬️', 'water_eng': '💧',
      'elevator_craft': '🛗', 'elevator_eng': '🛗',
      'energy_craft': '♨️', 'energy_eng': '♨️',
    };
    logoIcon.textContent = ICONS[TYPE] || '📝';
  }
  await loadData();

  const saved = loadProgress();
  const isAutoContinue = sessionStorage.getItem(AUTO_CONTINUE_KEY) === '1';
  sessionStorage.removeItem(AUTO_CONTINUE_KEY);
  const hasRealProgress = saved && saved.userAnswers.some(a => a.submitted);

  if (saved && !isAutoContinue && hasRealProgress) {
    // 구간 버튼이 아닌 다른 경로(껐다 재접속 등)로 들어온 경우에만 선택지 제공
    pendingResume = saved;
    renderResumeChoice(saved);
    return;
  }

  if (saved) {
    restoreFromSaved(saved);
  } else {
    startFreshExam();
  }

  renderQuestion();
  startTimer();
  examStarted = true;
});

function restoreFromSaved(saved) {
  examQuestions = saved.ids.map(id => allQuestions.find(q => q.id === id)).filter(Boolean);
  userAnswers   = saved.userAnswers;
  current       = saved.current;
  examEndTime   = saved.examEndTime;
  secondsLeft   = Math.max(0, Math.round((examEndTime - Date.now()) / 1000));
}

function startFreshExam() {
  buildExam();
  if (SEGMENTED) {
    examEndTime = Date.now() + secondsLeft * 1000;
    saveProgress();
  }
}

/* ── 이어하기 선택 화면 (SEGMENTED 전용) ─────────── */
function renderResumeChoice(saved) {
  const doneCount = saved.userAnswers.filter(a => a.submitted).length;
  const total = saved.userAnswers.length;
  elQuestion.innerHTML = `
    <div class="question-card" style="text-align:center;padding:2.5rem 1.5rem;">
      <div style="font-size:2.2rem;margin-bottom:.5rem;">📝</div>
      <h3 style="margin:0 0 .5rem;">풀다 만 시험이 있어요</h3>
      <p style="color:var(--text-mid);margin:0 0 1.5rem;">${doneCount} / ${total}번까지 진행했습니다. 이어서 풀까요?</p>
      <div class="exam-nav" style="justify-content:center;">
        <button class="btn btn-secondary" onclick="startOverExam()">새로 시작하기</button>
        <button class="btn btn-primary btn-lg" onclick="resumeExam()">이어서 풀기 →</button>
      </div>
    </div>`;
}

function resumeExam() {
  restoreFromSaved(pendingResume);
  pendingResume = null;
  renderQuestion();
  startTimer();
  examStarted = true;
}

function startOverExam() {
  pendingResume = null;
  clearProgress();
  startFreshExam();
  renderQuestion();
  startTimer();
  examStarted = true;
}

async function loadData() {
  const res = await fetch(DATA_URL);
  allQuestions = await res.json();
}

function buildExam() {
  if (MODE === 'wrong') {
    const wrongList = getWrongList().filter(w => w.file === FILE);
    if (wrongList.length === 0) {
      alert('오답 노트가 비어 있습니다. 먼저 일반 모의고사를 풀어보세요.');
      history.back();
      return;
    }
    const wrongIds = new Set(wrongList.map(w => w.qId));
    examQuestions = allQuestions.filter(q => wrongIds.has(q.id));
    if (examQuestions.length > COUNT) {
      examQuestions = shuffle(examQuestions).slice(0, COUNT);
    }
  } else if (MODE === 'sequential') {
    examQuestions = [...allQuestions];
  } else {
    // random
    examQuestions = shuffle([...allQuestions]).slice(0, Math.min(COUNT, allQuestions.length));
  }

  userAnswers = examQuestions.map(() => ({ selected: [], submitted: false, correct: false }));
  const FULL_TIME = {
    'history_basic':    70 * 60,
    'history_advanced': 80 * 60,
    'computer_1':       60 * 60,
    'computer_2':       40 * 60,
    'net_1':            60 * 60,
    'net_2':            60 * 60,
    'linux_1':         100 * 60,
    'linux_2':          80 * 60,
    'word':             60 * 60,
    'elec_eng':        150 * 60,
    'elec_ind':        150 * 60,
    'info_proc':       120 * 60,
    'info_ind':        120 * 60,
    'info_sec':        120 * 60,
    'hazmat_ind':       90 * 60,
    'hazmat_craft':     60 * 60,
    'fire_mech':       150 * 60,
    'fire_elec':       150 * 60,
    'forklift':         60 * 60,
    'excavator':        60 * 60,
    'realtor_1':       120 * 60,
    'realtor_2':       150 * 60,
    'welfare_1':        50 * 60,
    'welfare_2':        75 * 60,
    'welfare_3':        75 * 60,
    'safety_ind':      120 * 60,
    'safety_eng':      180 * 60,
    'elec_craft':       60 * 60,
    'pastry':           60 * 60,
    'bread':            60 * 60,
    'korean_cook':      60 * 60,
    'gas_craft':        60 * 60,
    'gas_ind':          90 * 60,
    'gas_eng':         150 * 60,
    'const_safety_ind':150 * 60,
    'const_safety_eng':180 * 60,
    'hvac_craft':       60 * 60,
    'hvac_eng':        150 * 60,
    'air_eng':         150 * 60,
    'water_eng':       150 * 60,
    'elevator_craft':   60 * 60,
    'elevator_eng':    120 * 60,
    'energy_craft':     60 * 60,
    'energy_eng':      150 * 60,
  };
  secondsLeft = MODE === 'sequential'
    ? examQuestions.length * 96
    : (FULL_TIME[FILE] || COUNT * 75);
}

/* ── 문제 렌더링 ────────────────────────────────── */
function renderQuestion() {
  const q    = examQuestions[current];
  const ua   = userAnswers[current];
  const isMulti = q.answers.length > 1;

  // 진행 상황
  elProgress.textContent = `${current + 1} / ${examQuestions.length}`;
  elProgressBar.style.width = `${((current + 1) / examQuestions.length) * 100}%`;
  updateNavButtons();

  // 구간(10문제) 완료 시점: 실제 페이지 새로고침으로 넘어가는 중간 화면
  const isLastQuestion = current === examQuestions.length - 1;
  if (SEGMENTED && ua.submitted && (current + 1) % SEGMENT_SIZE === 0 && !isLastQuestion) {
    renderSegmentBreak();
    return;
  }

  // HTML 빌드
  let html = `
    <div class="question-card">
      <div class="question-meta">
        <span class="q-num">Q${current + 1}</span>
        ${isMulti ? '<span class="q-tag multi">복수 정답</span>' : ''}
        ${q.is_video ? '<span class="q-tag video">동영상 문제</span>' : ''}
      </div>
      <div class="question-text">${escHtml(q.question)}</div>
  `;

  if (q.situation) {
    html += `<div class="situation-box">📍 ${escHtml(q.situation)}</div>`;
  }

  html += `<div class="choices-list">`;

  for (const [numStr, text] of Object.entries(q.choices)) {
    const num = parseInt(numStr);
    let cls = 'choice-btn';
    const isSelected = ua.selected.includes(num);
    if (ua.submitted) {
      const isCorrectAns = q.answers.includes(num);
      if (isCorrectAns && isSelected) cls += ' correct';
      else if (!isCorrectAns && isSelected) cls += ' wrong';
      else if (isCorrectAns && !isSelected) cls += ' correct-mark';
    } else if (isSelected) {
      cls += ' selected';
    }

    html += `
      <button class="${cls}" data-num="${num}" onclick="selectChoice(${num})" ${ua.submitted ? 'disabled' : ''}>
        <span class="choice-num">${num}</span>
        <span>${escHtml(text)}</span>
      </button>`;
  }

  html += `</div>`;

  // 해설 (제출 후, 해설이 있을 때만)
  if (ua.submitted && q.explanation) {
    html += `<div class="explain-box visible">
      <strong>🔍 해설</strong>
      <span>${escHtml(q.explanation)}</span>
    </div>`;
  }

  html += `
    <div class="report-error">
      <a href="${buildReportMailto(q)}" target="_blank" rel="noopener noreferrer">🚩 문제에 오류가 있으면 신고 부탁드립니다</a>
    </div>`;

  html += `</div>`;  // question-card

  // 제출 버튼 / 다음 버튼
  if (!ua.submitted) {
    html += `<div class="exam-nav">
      <button class="btn btn-secondary" onclick="confirmQuit()">시험 종료</button>
      <button class="btn btn-primary btn-lg" onclick="submitAnswer()">답안 제출</button>
    </div>`;
  } else {
    const isLast = current === examQuestions.length - 1;
    html += `<div class="exam-nav">
      <button class="btn btn-secondary" onclick="navigate(-1)" ${current === 0 ? 'disabled' : ''}>◀ 이전</button>
      ${isLast
        ? `<button class="btn btn-primary btn-lg" onclick="finishExam()">결과 보기 →</button>`
        : `<button class="btn btn-primary btn-lg" onclick="navigate(1)">다음 문제 ▶</button>`
      }
    </div>`;
  }

  elQuestion.innerHTML = html;
}

/* ── 구간 완료 화면 (SEGMENTED 전용) ─────────────── */
function renderSegmentBreak() {
  const segStart = current - SEGMENT_SIZE + 1;
  const segAnswers = userAnswers.slice(segStart, current + 1);
  const correctCount = segAnswers.filter(a => a.correct).length;

  elQuestion.innerHTML = `
    <div class="question-card" style="text-align:center;padding:2.5rem 1.5rem;">
      <div style="font-size:2.2rem;margin-bottom:.5rem;">✅</div>
      <h3 style="margin:0 0 .5rem;">${segStart + 1}~${current + 1}번 완료!</h3>
      <p style="color:var(--text-mid);margin:0 0 1.5rem;">이번 구간 정답 ${correctCount} / ${SEGMENT_SIZE}</p>
      <button class="btn btn-primary btn-lg" onclick="goToNextSegment()">다음 ${SEGMENT_SIZE}문제 이어풀기 →</button>
    </div>`;
}

function goToNextSegment() {
  current += 1;
  saveProgress();
  sessionStorage.setItem(AUTO_CONTINUE_KEY, '1');
  location.reload();
}

/* ── 답 선택 ────────────────────────────────────── */
function selectChoice(num) {
  const ua = userAnswers[current];
  if (ua.submitted) return;
  const q = examQuestions[current];
  const isMulti = q.answers.length > 1;

  if (isMulti) {
    const idx = ua.selected.indexOf(num);
    if (idx === -1) ua.selected.push(num);
    else ua.selected.splice(idx, 1);
  } else {
    ua.selected = [num];
  }
  renderQuestion();
}

/* ── 답안 제출 ──────────────────────────────────── */
function submitAnswer() {
  const ua = userAnswers[current];
  if (ua.selected.length === 0) {
    alert('답을 선택해 주세요.');
    return;
  }
  const q = examQuestions[current];
  ua.submitted = true;

  // 정답 판정 (선택한 것이 정답 세트와 같아야 함)
  const sortedSelected = [...ua.selected].sort();
  const sortedAnswers  = [...q.answers].sort();
  ua.correct = JSON.stringify(sortedSelected) === JSON.stringify(sortedAnswers);

  // 오답 노트 업데이트
  if (ua.correct) {
    recordCorrect(FILE, q.id);
  } else {
    recordWrong(FILE, q.id);
  }

  saveProgress();
  renderQuestion();
}

/* ── 네비게이션 ─────────────────────────────────── */
function navigate(dir) {
  const newIdx = current + dir;
  if (newIdx < 0 || newIdx >= examQuestions.length) return;
  current = newIdx;
  saveProgress();
  renderQuestion();
  window.scrollTo(0, 0);
}

function updateNavButtons() {
  // 버튼은 renderQuestion 내부의 HTML로 생성되므로 별도 처리 불필요
}

/* ── 타이머 ─────────────────────────────────────── */
function startTimer() {
  renderTimer();
  timerHandle = setInterval(() => {
    secondsLeft = SEGMENTED
      ? Math.max(0, Math.round((examEndTime - Date.now()) / 1000))
      : secondsLeft - 1;
    renderTimer();
    if (secondsLeft <= 0) {
      clearInterval(timerHandle);
      finishExam();
    }
  }, 1000);
}

function renderTimer() {
  const m = Math.floor(secondsLeft / 60);
  const s = secondsLeft % 60;
  elTimer.textContent = `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
  elTimer.className = 'timer';
  if (secondsLeft < 60) elTimer.classList.add('danger');
  else if (secondsLeft < 180) elTimer.classList.add('warning');
}

/* ── 시험 종료 ──────────────────────────────────── */
function finishExam() {
  clearInterval(timerHandle);
  // 결과 데이터 저장
  const results = {
    type: TYPE,
    typeLabel,
    mode: MODE,
    questions: examQuestions,
    userAnswers,
    timestamp: Date.now(),
  };
  sessionStorage.setItem('wooagosa_result', JSON.stringify(results));
  clearProgress();
  location.href = 'result.html';
}

/* ── 종료 확인 모달 ─────────────────────────────── */
function confirmQuit() {
  if (confirm('시험을 종료하고 결과를 보시겠습니까?\n아직 풀지 않은 문제는 오답으로 처리됩니다.')) {
    // 미제출 문제는 오답 처리
    userAnswers.forEach((ua, i) => {
      if (!ua.submitted) {
        ua.submitted = true;
        ua.correct = false;
        recordWrong(FILE, examQuestions[i].id);
      }
    });
    finishExam();
  }
}

/* ── 유틸 ───────────────────────────────────────── */
function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function buildReportMailto(q) {
  const subject = `[WooaGosa 오류 신고] ${FILE} - 문제 ID ${q.id}`;
  const body = `시험: ${FILE}\n문제 ID: ${q.id}\n출제일자: ${q.date || ''}\n문제 번호: ${q.question_no || ''}\n\n문제 내용:\n${q.question}\n\n어떤 오류가 있는지 알려주세요 (예: 보기 내용이 이상해요 / 정답이 틀린 것 같아요 / 해설이 잘못됐어요 등):\n`;
  return `mailto:wooahouse02@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

function escHtml(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/\n/g, '<br>');
}
