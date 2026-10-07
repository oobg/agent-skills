/* 한 장 모드: 준비가 끝나면 마지막에 data-mode="single"을 붙인다. 중간에 실패하면 세로 나열 그대로다. */
(function () {
  var deck = document.querySelector('.d0-deck');
  if (!deck) return;
  var slides = Array.prototype.slice.call(deck.querySelectorAll('.d0-slide'));
  var nav = deck.querySelector('.d0-deck__nav');
  if (!slides.length || !nav) return;
  var btnPrev = nav.querySelector('[data-deck="prev"]');
  var btnNext = nav.querySelector('[data-deck="next"]');
  var outNow = nav.querySelector('[data-deck-now]');
  var outTotal = nav.querySelector('[data-deck-total]');
  var TEXT = 'input, textarea, select, [contenteditable]:not([contenteditable="false"]), [role="tablist"], [role="slider"]';
  var CTRL = 'button, a[href], summary, [role="button"]';
  var idx = -1;

  function indexOfId(id) {
    for (var i = 0; i < slides.length; i++) if (slides[i].id === id) return i;
    return -1;
  }
  function fromHash() {
    var id = '';
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (err) { id = ''; }
    return id ? indexOfId(id) : -1;
  }
  /* 브라우저는 해시 대상 장(tabindex="-1")에 스스로 포커스를 준다. 해시 진입·이동에서는 그 포커스를 풀어 링이 생기지 않게 한다 */
  function dropSlideFocus() {
    var a = document.activeElement;
    if (a && slides.indexOf(a) >= 0) a.blur();
  }
  function show(i, opt) {
    opt = opt || {};
    i = Math.max(0, Math.min(slides.length - 1, i));
    if (i === idx) { if (opt.from === 'hash') dropSlideFocus(); return; }
    var old = slides[idx];
    var a = document.activeElement;
    /* 포커스는 키보드로 넘길 때(opt.from === 'key')와 사라지는 장 안 컨트롤(목차 링크 등)에 포커스가 있을 때만 새 장으로 옮긴다.
       해시 진입·이동은 장을 보여 주기만 하고 포커스를 주지 않는다 */
    var inner = !!(old && a && a !== old && old.contains(a));
    var moveFocus = opt.from !== 'hash' && (opt.from === 'key' || inner);
    slides.forEach(function (s, k) {
      if (k === i) s.setAttribute('data-active', ''); else s.removeAttribute('data-active');
    });
    idx = i;
    slides[i].scrollTop = 0;
    if (outNow) outNow.textContent = String(i + 1);
    if (btnPrev) btnPrev.setAttribute('aria-disabled', String(i === 0));
    if (btnNext) btnNext.setAttribute('aria-disabled', String(i === slides.length - 1));
    if (opt.hash !== false) {
      try { history.replaceState(null, '', '#' + slides[i].id); } catch (err) { /* srcdoc 등: 주소 동기화 생략 */ }
    }
    if (moveFocus) slides[i].focus({ preventScroll: true });
    else if (opt.from === 'hash') dropSlideFocus();
  }
  /* 장 안이 넘치면 Space·PageDown은 먼저 장 안을 스크롤한다. 스크롤했으면 true */
  function pageWithin(dir) {
    var s = slides[idx];
    if (s.scrollHeight - s.clientHeight < 2) return false;
    if (dir > 0 && s.scrollTop + s.clientHeight >= s.scrollHeight - 1) return false;
    if (dir < 0 && s.scrollTop <= 0) return false;
    s.scrollBy(0, dir * s.clientHeight * 0.85);
    return true;
  }
  function toggleFullscreen() {
    try {
      var p = document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
      if (p && p.catch) p.catch(function () {});
    } catch (err) { /* 전체 화면을 못 쓰는 환경 */ }
  }

  document.addEventListener('keydown', function (e) {
    if (e.defaultPrevented || e.altKey || e.ctrlKey || e.metaKey || e.isComposing) return;
    var t = e.target && e.target.closest ? e.target : null;
    if (t && t.closest(TEXT)) return;                     /* 입력 칸: 모든 키를 그대로 둔다 */
    var k = e.key, d = 0, paging = false;
    if (k === ' ' || k === 'Spacebar' || k === 'Enter') {
      if (k === 'Enter' || (t && t.closest(CTRL))) return; /* 버튼·링크의 Space·Enter는 그 컨트롤 몫 */
      d = e.shiftKey ? -1 : 1; paging = true;
    }
    else if (k === 'ArrowRight') d = 1;
    else if (k === 'ArrowLeft') d = -1;
    else if (k === 'PageDown') { d = 1; paging = true; }
    else if (k === 'PageUp') { d = -1; paging = true; }
    else if (k === 'Home') { e.preventDefault(); show(0, { from: 'key' }); return; }
    else if (k === 'End') { e.preventDefault(); show(slides.length - 1, { from: 'key' }); return; }
    else if (k === 'f' || k === 'F') { toggleFullscreen(); return; }
    else return;
    e.preventDefault();
    if (paging && pageWithin(d)) return;
    show(idx + d, { from: 'key' });
  });

  deck.addEventListener('click', function (e) {
    var t = e.target && e.target.closest ? e.target : null;
    if (!t) return;
    var b = t.closest('button[data-deck]');
    if (b) {
      var act = b.getAttribute('data-deck');
      if (act === 'prev') show(idx - 1);
      else if (act === 'next') show(idx + 1);
      else if (act === 'toc') {
        var toc = deck.querySelector('.d0-slide[data-kind="toc"]');
        show(toc ? slides.indexOf(toc) : 0);
      }
      return;
    }
    var a = t.closest('a[href^="#"]');
    if (!a) return;
    var i = indexOfId(a.getAttribute('href').slice(1));
    if (i < 0) return;
    e.preventDefault();
    show(i);
  });
  window.addEventListener('hashchange', function () {
    var i = fromHash();
    if (i >= 0) show(i, { hash: false, from: 'hash' });
  });

  /* 스와이프: 터치·펜만. 가로 이동 > 세로 이동이고 48px 넘으면 넘긴다 */
  var sx = null, sy = 0, pid = null;
  deck.addEventListener('pointerdown', function (e) {
    if (e.pointerType === 'mouse') return;
    sx = e.clientX; sy = e.clientY; pid = e.pointerId;
  });
  deck.addEventListener('pointerup', function (e) {
    if (sx === null || e.pointerId !== pid) return;
    var dx = e.clientX - sx, dy = e.clientY - sy;
    sx = null;
    if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 48) show(idx + (dx < 0 ? 1 : -1));
  });
  deck.addEventListener('pointercancel', function () { sx = null; });

  /* iframe(srcdoc) 안: 누르면 프레임이 키 입력을 받게 한다 */
  var framed = true;
  try { framed = window.self !== window.top; } catch (err) { framed = true; }
  if (framed) {
    document.addEventListener('pointerdown', function () {
      try { window.focus(); } catch (err) { /* 무시 */ }  /* 슬라이드에 포커스를 주지 않는다: 넘길 때마다 포커스 링이 생긴다 */
    });
  }

  if (outTotal) outTotal.textContent = String(slides.length);
  var start = fromHash();
  show(start >= 0 ? start : 0, { hash: false, from: start >= 0 ? 'hash' : '' });
  if (start >= 0) window.addEventListener('load', dropSlideFocus);  /* 로드 끝에 해시 대상에 생긴 포커스도 푼다 */
  deck.setAttribute('data-mode', 'single');               /* 여기까지 왔을 때만 한 장 모드 */
})();
