// 모션: 섹션 직계 블록을 한 번 드러내고(60ms 순차), 안의 .d0-draw 경로를 그린다.
(function () {
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var groups = document.querySelectorAll('.d0-header, .d0-section');
  if (!groups.length) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.setAttribute('data-in', '');
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  groups.forEach(function (g) {
    Array.prototype.forEach.call(g.children, function (el, i) {
      el.setAttribute('data-reveal', '');
      el.style.transitionDelay = (i * 60) + 'ms';
      io.observe(el);
    });
  });
  document.documentElement.setAttribute('data-motion', 'on');
})();
