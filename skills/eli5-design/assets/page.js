// 미니 격자: <div data-grid='{"rows":8,"cols":6,"label":"…"}'>를 글자 없는 표 썸네일 SVG로 바꾼다(같은 seed면 같은 모양).
(function () {
  var NS = 'http://www.w3.org/2000/svg';
  function grid(spec) {
    var W = 160, H = 96, P = 3, head = spec.headRow !== false, key = spec.keyCol !== false;
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.setAttribute('role', 'img');
    var t = document.createElementNS(NS, 'title');
    t.textContent = spec.label || '표 모양';
    svg.appendChild(t);
    var s = spec.seed || 1;
    var rnd = function () { s = (s * 9301 + 49297) % 233280; return s / 233280; };
    var cw = (W - P * 2) / spec.cols, rh = (H - P * 2) / spec.rows;
    for (var r = 0; r < spec.rows; r++) {
      for (var c = 0; c < spec.cols; c++) {
        var cls = 'd0-s-cell';
        if (head && r === 0) cls = 'd0-s-head';
        else if (key && c === 0) cls = 'd0-s-key';
        else if ((spec.sumCol && c === spec.cols - 1) || (spec.sumRow && r === spec.rows - 1)) cls = 'd0-s-sum';
        else if (rnd() < (spec.blanks || 0)) continue;
        var e = document.createElementNS(NS, 'rect');
        e.setAttribute('x', P + c * cw + 1); e.setAttribute('y', P + r * rh + 1);
        e.setAttribute('width', Math.max(cw - 2, 1)); e.setAttribute('height', Math.max(rh - 2, 1));
        e.setAttribute('rx', 2); e.setAttribute('class', cls);
        svg.appendChild(e);
      }
    }
    return svg;
  }
  document.querySelectorAll('[data-grid]').forEach(function (el) {
    try { el.replaceWith(grid(JSON.parse(el.dataset.grid))); } catch (err) { /* 잘못된 스펙은 그대로 둔다 */ }
  });
})();
// 번호 핀 연동: 범례 항목 hover·focus, 핀 hover에 그림의 data-active-pin만 바꾼다. 떠나도 마지막 번호를 유지한다.
document.querySelectorAll('.d0-fig[data-variant="pins"][data-active-pin]').forEach(function (fig) {
  function pick(e) {
    var el = e.target.closest && e.target.closest('.d0-pins > .d0-pin[data-pin], .d0-pins__key > [data-pin]');
    if (el && fig.contains(el)) fig.setAttribute('data-active-pin', el.getAttribute('data-pin'));
  }
  fig.addEventListener('mouseover', pick);
  fig.addEventListener('focusin', pick);
});
