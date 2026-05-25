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
  return 'license12';
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
};
const COUNT = parseInt(params.get('count') || String(DEFAULT_COUNT[FILE] || '40'));

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
};
const DATA_URL = DATA_URL_MAP[FILE] || 'data/license_1_2.json';

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
};
const typeLabel = params.get('label') || TYPE_LABELS[TYPE] || '모의고사';

let allQuestions  = [];   // 전체 문제 데이터
let examQuestions = [];   // 현재 시험에 사용할 문제
let current       = 0;    // 현재 문제 인덱스
let userAnswers   = [];   // 사용자 답 [{selected:[], correct:bool}]
let timerHandle   = null;
let secondsLeft   = 0;
let examStarted   = false;

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
    };
    logoIcon.textContent = ICONS[TYPE] || '🚗';
  }
  await loadData();
  buildExam();
  renderQuestion();
  startTimer();
  examStarted = true;
});

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

  // 해설 (제출 후)
  if (ua.submitted) {
    html += `<div class="explain-box visible">
      <strong>🔍 해설</strong>
      <span>${escHtml(q.explanation)}</span>
    </div>`;
  }

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

  renderQuestion();
}

/* ── 네비게이션 ─────────────────────────────────── */
function navigate(dir) {
  const newIdx = current + dir;
  if (newIdx < 0 || newIdx >= examQuestions.length) return;
  current = newIdx;
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
    secondsLeft--;
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

function escHtml(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/\n/g, '<br>');
}
