/**
 * 문제은행 다운로드 페이지 공용 엔진
 * 페이지별로 window.EXAM_DL_META, window.EXAM_DL_QUESTIONS 를 미리 채워두고 이 스크립트를 로드한다.
 */
(function () {
  const meta = window.EXAM_DL_META || {};
  const questions = window.EXAM_DL_QUESTIONS || [];

  const rounds = {};
  questions.forEach(function (q) {
    const d = q.date || '미상';
    if (!rounds[d]) rounds[d] = [];
    rounds[d].push(q);
  });
  const sortedDates = Object.keys(rounds).sort().reverse();

  function formatDate(d) {
    if (!/^\d{8}$/.test(d)) return d;
    return d.slice(0, 4) + '년 ' + parseInt(d.slice(4, 6), 10) + '월 ' + parseInt(d.slice(6, 8), 10) + '일';
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  const listEl = document.getElementById('roundList');
  if (!listEl) return;

  listEl.innerHTML = sortedDates.map(function (d, i) {
    return '<label class="round-check-item">' +
      '<input type="checkbox" class="round-check" value="' + escapeHtml(d) + '"' + (i === 0 ? ' checked' : '') + '>' +
      '<span>' + escapeHtml(formatDate(d)) + ' 시행 <em>(' + rounds[d].length + '문항)</em></span>' +
      '</label>';
  }).join('');

  function getChecked() {
    return Array.prototype.slice.call(document.querySelectorAll('.round-check:checked')).map(function (el) { return el.value; });
  }

  function renderQuestionHTML(q) {
    const choices = q.choices || {};
    const answers = q.answers || [];
    const choicesHtml = Object.keys(choices).map(function (num) {
      const isAnswer = answers.indexOf(parseInt(num, 10)) !== -1;
      return '<div class="choice-item' + (isAnswer ? ' correct-choice' : '') + '">' + escapeHtml(num) + '. ' + escapeHtml(choices[num]) + '</div>';
    }).join('');
    return '<div class="preview-q">' +
      '<div class="q-meta">' + escapeHtml(formatDate(q.date)) + ' · ' + escapeHtml(q.subject_name || '') + ' · ' + escapeHtml(q.question_no) + '번</div>' +
      '<div class="q-text">' + escapeHtml(q.question) + '</div>' +
      '<div class="q-choices">' + choicesHtml + '</div>' +
      '<div class="q-answer">✅ 정답: ' + escapeHtml(answers.join(', ')) + '번</div>' +
      '</div>';
  }

  const selCountEl = document.getElementById('selCount');
  const previewSection = document.getElementById('previewSection');
  const previewEl = document.getElementById('previewArea');
  const dlBtn = document.getElementById('dlBtn');

  function render() {
    const checked = getChecked();
    let selQuestions = [];
    checked.forEach(function (d) { selQuestions = selQuestions.concat(rounds[d]); });

    selCountEl.textContent = '선택: ' + checked.length + '개 회차 · ' + selQuestions.length + '문항';

    if (selQuestions.length === 0) {
      previewSection.style.display = 'none';
      dlBtn.disabled = true;
      dlBtn.classList.add('btn-disabled');
      return;
    }
    previewSection.style.display = 'block';
    dlBtn.disabled = false;
    dlBtn.classList.remove('btn-disabled');

    const sample = selQuestions.slice(0, 5);
    let html = sample.map(renderQuestionHTML).join('');
    if (selQuestions.length > 5) {
      html += '<p class="preview-more">…외 ' + (selQuestions.length - 5) + '문항 (다운로드 시 전체 포함)</p>';
    }
    previewEl.innerHTML = html;
  }

  listEl.addEventListener('change', render);

  const checkAllBtn = document.getElementById('checkAllBtn');
  const uncheckAllBtn = document.getElementById('uncheckAllBtn');
  if (checkAllBtn) checkAllBtn.addEventListener('click', function () {
    document.querySelectorAll('.round-check').forEach(function (el) { el.checked = true; });
    render();
  });
  if (uncheckAllBtn) uncheckAllBtn.addEventListener('click', function () {
    document.querySelectorAll('.round-check').forEach(function (el) { el.checked = false; });
    render();
  });

  dlBtn.addEventListener('click', function () {
    const checked = getChecked();
    if (!checked.length) return;
    let selQuestions = [];
    checked.forEach(function (d) { selQuestions = selQuestions.concat(rounds[d]); });
    selQuestions.sort(function (a, b) {
      if (a.date !== b.date) return a.date < b.date ? -1 : 1;
      return (a.question_no || 0) - (b.question_no || 0);
    });

    const bodyHtml = selQuestions.map(function (q, i) {
      const choices = q.choices || {};
      const answers = q.answers || [];
      const choicesHtml = Object.keys(choices).map(function (num) {
        return '<div>' + escapeHtml(num) + ') ' + escapeHtml(choices[num]) + '</div>';
      }).join('');
      return '<div class="q">' +
        '<div class="q-no">' + (i + 1) + '. [' + escapeHtml(formatDate(q.date)) + ' · ' + escapeHtml(q.subject_name || '') + '] ' + escapeHtml(q.question) + '</div>' +
        '<div class="choices">' + choicesHtml + '</div>' +
        '<div class="answer">정답: ' + escapeHtml(answers.join(', ')) + '번</div>' +
        '</div>';
    }).join('');

    const fullHtml = '<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">' +
      '<title>' + escapeHtml(meta.name) + ' 문제은행 - wooagosa</title>' +
      '<style>' +
      "body{font-family:'Noto Sans KR',sans-serif;padding:28px;line-height:1.65;color:#1e293b;max-width:820px;margin:0 auto;}" +
      'h1{font-size:1.25rem;border-bottom:2px solid #1a3a5c;padding-bottom:10px;margin-bottom:20px;}' +
      '.q{margin-bottom:22px;page-break-inside:avoid;}' +
      '.q-no{font-weight:700;margin-bottom:6px;}' +
      '.choices div{margin-left:14px;color:#334155;}' +
      '.answer{color:#1a3a5c;font-weight:700;margin-top:6px;}' +
      '.footer-note{margin-top:44px;font-size:.8rem;color:#94a3b8;border-top:1px solid #e2e8f0;padding-top:14px;}' +
      '.print-btn{padding:.6rem 1.2rem;background:#2563eb;color:#fff;border:none;border-radius:8px;font-weight:700;cursor:pointer;font-size:.95rem;}' +
      '@media print{.no-print{display:none;}}' +
      '</style></head><body>' +
      '<div class="no-print" style="margin-bottom:20px;"><button class="print-btn" onclick="window.print()">🖨️ 인쇄 / PDF로 저장</button></div>' +
      '<h1>' + escapeHtml(meta.name) + ' 기출문제 (' + checked.length + '개 회차 · ' + selQuestions.length + '문항)</h1>' +
      bodyHtml +
      '<div class="footer-note">본 자료는 wooagosa.wooahouse.com(우아고사)에서 무료로 제공하는 기출 문제은행입니다. 실제 시행처 정답과 다를 수 있으니 참고용으로 활용하세요.</div>' +
      '</body></html>';

    const win = window.open('', '_blank');
    if (!win) { alert('팝업이 차단되었습니다. 팝업 차단을 해제한 뒤 다시 시도해주세요.'); return; }
    win.document.write(fullHtml);
    win.document.close();
  });

  render();
})();
