/**
 * ad-dev-placeholder.js
 * 로컬 프리뷰(localhost 등)에서는 AdSense가 절대 채워지지 않아 <ins class="adsbygoogle">
 * 자리가 빈 공간으로 보인다. 이 스크립트는 로컬 환경에서만 그 자리에 눈에 띄는
 * placeholder를 대신 띄워서 광고 위치를 바로 확인할 수 있게 한다.
 * 실제 배포 도메인에서는 아무 동작도 하지 않는다 (raw <ins> 태그와
 * wooa-sidebar.js 등이 JS로 나중에 삽입하는 <ins> 태그 모두 감지한다).
 */
(function () {
  var isLocal = /^(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])$/.test(location.hostname) ||
    location.protocol === 'file:';
  if (!isLocal) return;

  var style = document.createElement('style');
  style.textContent =
    '.ad-dev-placeholder{background:repeating-linear-gradient(45deg,#f5f5f5,#f5f5f5 10px,#ebebeb 10px,#ebebeb 20px);' +
    'border:2px dashed #ccc;border-radius:8px;padding:16px;text-align:center;color:#999;' +
    'font-size:.8rem;font-weight:500;min-height:50px;display:flex;align-items:center;justify-content:center;' +
    'width:100%;box-sizing:border-box;}' +
    '.coupang-dev-placeholder{background:repeating-linear-gradient(45deg,#fff7f0,#fff7f0 10px,#ffece0 10px,#ffece0 20px);' +
    'border:2px dashed #ff8a3d;border-radius:8px;padding:16px;text-align:center;color:#c2540a;' +
    'font-size:.8rem;font-weight:500;min-height:50px;display:flex;align-items:center;justify-content:center;' +
    'width:100%;box-sizing:border-box;}';
  document.head.appendChild(style);

  function decorate(ins) {
    if (ins.dataset.adDevDone) return;
    ins.dataset.adDevDone = '1';
    var slot = ins.getAttribute('data-ad-slot') || '?';
    var box = document.createElement('div');
    box.className = 'ad-dev-placeholder';
    box.textContent = '📢 광고 영역 (slot: ' + slot + ')';
    ins.style.display = 'none';
    ins.insertAdjacentElement('afterend', box);
  }

  // 쿠팡 파트너스(PartnersCoupang.G)는 로컬에서도 스크립트가 로드는 되지만, 도메인
  // 미등록이라 <ins style="display:none"><iframe src="...ads-partners.coupang.com/widgets.html?id=..."></ins>
  // 형태로 "숨긴 채" 삽입만 되고 절대 안 보이게 됨. 이 iframe을 찾아서 바로 뒤에
  // placeholder 박스를 달아준다(ins 자체를 강제로 보이게 하진 않음 — 안이 비어있어서 의미 없음).
  function decorateCoupangIns(ins) {
    if (ins.dataset.adDevDone) return;
    ins.dataset.adDevDone = '1';
    var iframe = ins.querySelector('iframe[src*="ads-partners.coupang.com"]');
    var m = iframe && iframe.src.match(/[?&]id=(\d+)/);
    var id = m ? m[1] : '?';
    var box = document.createElement('div');
    box.className = 'coupang-dev-placeholder';
    box.textContent = '🛒 쿠팡 파트너스 영역 (id: ' + id + ')';
    ins.insertAdjacentElement('afterend', box);
  }

  function scan() {
    document.querySelectorAll('ins.adsbygoogle').forEach(decorate);
    document.querySelectorAll('ins').forEach(function (ins) {
      if (ins.querySelector('iframe[src*="ads-partners.coupang.com"]')) decorateCoupangIns(ins);
    });
  }

  scan();
  new MutationObserver(scan).observe(document.documentElement, { childList: true, subtree: true });
})();
