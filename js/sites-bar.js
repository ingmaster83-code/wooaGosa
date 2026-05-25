// WooaHouse Family Bar – 마우스 휠 가로 스크롤
(function () {
  var bar = document.querySelector('.our-sites-bar');
  if (!bar) return;
  bar.addEventListener('wheel', function (e) {
    if (e.deltaY !== 0) {
      e.preventDefault();
      bar.scrollLeft += e.deltaY;
    }
  }, { passive: false });
})();
