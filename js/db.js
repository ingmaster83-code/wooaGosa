/**
 * db.js – localStorage 기반 오답 노트 관리
 */

const DB_KEY = 'wooagosa_wrong_v1';

function loadDB() {
  try {
    return JSON.parse(localStorage.getItem(DB_KEY) || '{}');
  } catch (e) {
    return {};
  }
}
function saveDB(db) {
  try { localStorage.setItem(DB_KEY, JSON.stringify(db)); } catch (e) {}
}

/**
 * 오답 기록 추가
 * @param {string} file - 'license12' | 'motorcycle'
 * @param {number} qId - 문제 번호
 */
function recordWrong(file, qId) {
  const db = loadDB();
  const key = `${file}:${qId}`;
  if (!db[key]) db[key] = { file, qId, count: 0, lastWrong: null };
  db[key].count++;
  db[key].lastWrong = new Date().toISOString();
  saveDB(db);
}

/**
 * 정답 맞히면 카운트 감소 (0 미만으로는 내려가지 않음)
 */
function recordCorrect(file, qId) {
  const db = loadDB();
  const key = `${file}:${qId}`;
  if (db[key]) {
    db[key].count = Math.max(0, db[key].count - 1);
    if (db[key].count === 0) delete db[key];
    saveDB(db);
  }
}

/**
 * 오답 목록 반환 (count > 0 인 것만)
 * @returns Array<{file, qId, count, lastWrong}>
 */
function getWrongList() {
  const db = loadDB();
  return Object.values(db)
    .filter(v => v.count > 0)
    .sort((a, b) => b.count - a.count);
}

/**
 * 오답 노트 통계
 */
function getWrongStats() {
  const db = loadDB();
  const items = Object.values(db).filter(v => v.count > 0);
  const cnt = key => items.filter(v => v.file === key).length;
  return {
    total:            items.length,
    license12:        cnt('license12'),
    motorcycle:       cnt('motorcycle'),
    history_basic:    cnt('history_basic'),
    history_advanced: cnt('history_advanced'),
    computer_1:       cnt('computer_1'),
    computer_2:       cnt('computer_2'),
    net_1:            cnt('net_1'),
    net_2:            cnt('net_2'),
    linux_1:          cnt('linux_1'),
    linux_2:          cnt('linux_2'),
    word:             cnt('word'),
    elec_eng:         cnt('elec_eng'),
    elec_ind:         cnt('elec_ind'),
    info_proc:        cnt('info_proc'),
    info_ind:         cnt('info_ind'),
    info_sec:         cnt('info_sec'),
  };
}

/**
 * 특정 문제 오답 횟수
 */
function getWrongCount(file, qId) {
  const db = loadDB();
  return (db[`${file}:${qId}`] || { count: 0 }).count;
}

/**
 * 오답 노트 전체 초기화
 */
function clearAllWrong() {
  localStorage.removeItem(DB_KEY);
}
