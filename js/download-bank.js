/**
 * 문제은행 다운로드 페이지 공용 엔진
 * 페이지별로 window.EXAM_DL_META, window.EXAM_DL_QUESTIONS, window.EXAM_DL_PDFS 를 미리 채워두고 이 스크립트를 로드한다.
 * 회차는 한 번에 하나만 선택할 수 있다(라디오 버튼).
 * 다운로드 버튼을 누르면 pdf-preview.html이 새 탭으로 열리고, 그 탭에서 실제 원본 PDF를 미리본 뒤 다운로드한다.
 */
(function () {
  const meta = window.EXAM_DL_META || {};
  const questions = window.EXAM_DL_QUESTIONS || [];
  const pdfs = window.EXAM_DL_PDFS || {};

  const rounds = {};
  questions.forEach(function (q) {
    const d = q.date || '';
    if (!rounds[d]) rounds[d] = [];
    rounds[d].push(q);
  });

  // 다운로드 가능한(=PDF가 실제로 있는) 회차만 노출
  const allDates = new Set(Object.keys(rounds));
  Object.keys(pdfs).forEach(function (d) { allDates.add(d); });
  const sortedDates = Array.from(allDates)
    .filter(function (d) { return pdfs[d] && pdfs[d].length; })
    .sort()
    .reverse();

  function formatDate(d) {
    if (!d) return '전체 자료';
    if (!/^\d{8}$/.test(d)) return d;
    return d.slice(0, 4) + '년 ' + parseInt(d.slice(4, 6), 10) + '월 ' + parseInt(d.slice(6, 8), 10) + '일';
  }

  function roundLabel(d) {
    return d ? formatDate(d) + ' 시행' : '전체 자료';
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  const listEl = document.getElementById('roundList');
  if (!listEl) return;

  if (!sortedDates.length) {
    listEl.innerHTML = '<p class="preview-more">현재 다운로드 가능한 PDF가 없습니다. 준비 중입니다.</p>';
    return;
  }

  listEl.innerHTML = sortedDates.map(function (d, i) {
    const qcount = (rounds[d] || []).length;
    const fcount = (pdfs[d] || []).length;
    const qLabel = qcount ? ' <em>(' + qcount + '문항)</em>' : '';
    return '<label class="round-check-item">' +
      '<input type="radio" name="roundSelect" class="round-check" value="' + escapeHtml(d) + '"' + (i === 0 ? ' checked' : '') + '>' +
      '<span>' + escapeHtml(roundLabel(d)) + qLabel + ' · <em>PDF ' + fcount + '개</em></span>' +
      '</label>';
  }).join('');

  function getSelected() {
    const el = document.querySelector('.round-check:checked');
    return el ? el.value : null;
  }

  const selCountEl = document.getElementById('selCount');
  const dlBtn = document.getElementById('dlBtn');

  function render() {
    const d = getSelected();
    const selFiles = d !== null ? (pdfs[d] || []) : [];

    selCountEl.textContent = '선택: ' + (d !== null ? 1 : 0) + '개 회차 · PDF ' + selFiles.length + '개';

    if (d === null || !selFiles.length) {
      dlBtn.disabled = true;
      dlBtn.classList.add('btn-disabled');
      return;
    }
    dlBtn.disabled = false;
    dlBtn.classList.remove('btn-disabled');
  }

  listEl.addEventListener('change', render);

  dlBtn.addEventListener('click', function () {
    const d = getSelected();
    if (d === null) return;
    const files = pdfs[d] || [];
    if (!files.length) { alert('선택한 회차에 다운로드 가능한 PDF가 없습니다.'); return; }

    const params = new URLSearchParams();
    files.forEach(function (f) {
      params.append('f', f.path);
      params.append('k', f.kind);
    });
    if (meta.name) params.set('name', meta.name);
    params.set('round', roundLabel(d));

    window.open('pdf-preview.html?' + params.toString(), '_blank');
  });

  render();
})();
