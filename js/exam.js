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
const DEFAULT_COUNT = {
  'history_basic': 50, 'history_advanced': 50,
  'computer_1': 60, 'computer_2': 40,
};
const COUNT   = parseInt(params.get('count') || String(DEFAULT_COUNT[FILE] || '40'));

const FILE = (() => {
  if (TYPE === 'motorcycle' || TYPE === 'motorbike') return 'motorcycle';
  if (TYPE === 'history_basic')    return 'history_basic';
  if (TYPE === 'history_advanced') return 'history_advanced';
  if (TYPE === 'computer_1')       return 'computer_1';
  if (TYPE === 'computer_2')       return 'computer_2';
  return 'license12';
})();

const DATA_URL_MAP = {
  'license12':        'data/license_1_2.json',
  'motorcycle':       'data/motorcycle.json',
  'history_basic':    'data/history_basic.json',
  'history_advanced': 'data/history_advanced.json',
  'computer_1':       'data/computer_1.json',
  'computer_2':       'data/computer_2.json',
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
  // 한국사: 기본 70분, 심화 80분 / 컴활: 1급 60분, 2급 40분 / 운전면허: 문제당 75초
  const FULL_TIME = {
    'history_basic':    70 * 60,
    'history_advanced': 80 * 60,
    'computer_1':       60 * 60,
    'computer_2':       40 * 60,
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
