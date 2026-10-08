#!/usr/bin/env node
/*
 * eli5-design 결과물의 기계 검사. 사람이 봐야 아는 것은 references/final-review.md 네 질문이 맡는다.
 *
 *   node scripts/check_render.cjs out.html
 *   node scripts/check_render.cjs out.html --widths 1440,390 --playwright <playwright-core 경로>
 *
 * playwright-core(또는 playwright)를 찾는 순서: --playwright 인자 → ELI5_PLAYWRIGHT 환경 변수 → require('playwright-core') → require('playwright').
 * 검사: 콘솔 오류, 남은 자리표시자·토큰 누락·외부 요청, 페이지 가로 넘침, SVG 잘림, page 그림 글자 크기(경고),
 *       내부 식별자 노출, report 표지 회귀(page 축·넓은 구간, deck 표지 배치).
 * 측정은 뷰포트 숫자가 아니라 실제 컨테이너 폭으로 하고 1px 오차를 허용한다(스크롤바 유무로 판정이 바뀌지 않게).
 * FAIL이 하나라도 있으면 종료 코드 1.
 */
'use strict';
const path = require('path');
const fs = require('fs');

const SLUGS = ['bar-list', 'charts-points', 'code-block', 'decision-report', 'diff-rows', 'dot-chart', 'eli5-design',
  'explainer-page', 'final-review', 'flow-line', 'kpi-cards', 'metric-list', 'mockup-frame', 'render-unavailable',
  'section-head', 'side-by-side', 'slide-deck', 'step-columns', 'tab-preview', 'thumb-cards', 'timebar'];

function arg(name, fallback) {
  const i = process.argv.indexOf(name);
  return i > 0 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}
function loadPlaywright() {
  const tries = [arg('--playwright'), process.env.ELI5_PLAYWRIGHT, 'playwright-core', 'playwright'].filter(Boolean);
  for (const t of tries) {
    try { return require(t); } catch (e) { /* 다음 후보 */ }
  }
  console.error('playwright-core를 찾지 못했습니다. --playwright <경로> 또는 ELI5_PLAYWRIGHT로 알려 주세요.');
  console.error('렌더 검사를 못 하면 references/render-unavailable.md를 따릅니다.');
  process.exit(2);
}

async function inspect(page, width, slugs) {
  return page.evaluate(({ width, slugs }) => {
    const out = [];
    const fail = (m) => out.push(['FAIL', m]);
    const warn = (m) => out.push(['WARN', m]);
    const TOL = 1;
    const deck = document.querySelector('.d0-deck');
    const doc = document.documentElement;

    // 1. 페이지 가로 넘침: 실제 레이아웃 폭(clientWidth, 스크롤바 제외) 기준
    if (doc.scrollWidth > doc.clientWidth + TOL) fail(`${width}px: 페이지 가로 넘침 ${doc.scrollWidth} > ${doc.clientWidth}`);
    if (deck && deck.getAttribute('data-mode') === 'single') {
      const cur = deck.querySelector('.d0-slide[data-active]');
      if (cur && width >= 1024 && cur.scrollHeight > cur.clientHeight + TOL) warn(`${width}px: 현재 장 내용이 장 높이를 넘침(${cur.id})`);
    }

    // 덱은 세로 나열로 펼쳐 모든 장을 잰다
    if (deck) deck.removeAttribute('data-mode');

    // 2. SVG 잘림: 자식 도형·글자 합집합이 SVG box 안에 있는가
    const shapes = 'path, rect, circle, ellipse, line, polyline, polygon, text';
    document.querySelectorAll('svg[role="img"]').forEach((svg, i) => {
      const r = svg.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return;
      let l = Infinity, t = Infinity, rr = -Infinity, b = -Infinity;
      svg.querySelectorAll(shapes).forEach((el) => {
        const q = el.getBoundingClientRect();
        if (q.width === 0 && q.height === 0) return;
        l = Math.min(l, q.left); t = Math.min(t, q.top); rr = Math.max(rr, q.right); b = Math.max(b, q.bottom);
      });
      if (l === Infinity) return;
      if (svg.closest('.d0-fig[data-variant="ratio"]')) return; // 늘어나는 비율 막대: 둥근 끝을 CSS로 자른다
      const name = (svg.querySelector('title') || {}).textContent || `svg#${i + 1}`;
      if (l < r.left - TOL || t < r.top - TOL || rr > r.right + TOL || b > r.bottom + TOL) {
        fail(`${width}px: SVG 잘림 "${name.trim().slice(0, 40)}" (도형 ${Math.round(l - r.left)},${Math.round(t - r.top)}~${Math.round(rr - r.left)},${Math.round(b - r.top)} / box ${Math.round(r.width)}×${Math.round(r.height)})`);
      }
      // 3. page 그림 글자 렌더 크기(경고): 글자 크기 × SVG 실제 렌더 폭 ÷ viewBox 폭
      if (!svg.closest('.d0-page')) return;
      const vb = svg.viewBox && svg.viewBox.baseVal;
      if (!vb || !vb.width) return;
      const k = r.width / vb.width;
      svg.querySelectorAll('text').forEach((tx) => {
        if (!tx.textContent.trim()) return;
        const px = parseFloat(getComputedStyle(tx).fontSize) * k;
        if (width <= 480 && px < 11 - 0.3) warn(`${width}px: 그림 글자 ${px.toFixed(1)}px < 11 "${tx.textContent.trim().slice(0, 12)}" (${name.trim().slice(0, 30)})`);
        if (width >= 1024 && (px < 13 - 0.3 || px > 20 + 0.3)) warn(`${width}px: 그림 글자 ${px.toFixed(1)}px(13~20 밖) "${tx.textContent.trim().slice(0, 12)}"`);
      });
    });

    // 4. 내부 식별자 노출: 보이는 글에서 정확히 일치하는 slug만
    const skip = 'code, pre, details, script, style, title, desc, q, blockquote, [data-verbatim]';
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const seen = new Set();
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      const p = n.parentElement;
      if (!p || p.closest(skip)) continue;
      for (const s of slugs) {
        if (seen.has(s)) continue;
        if (new RegExp(`(^|[^A-Za-z0-9-])${s}($|[^A-Za-z0-9-])`).test(n.textContent)) { seen.add(s); fail(`내부 식별자 노출: "${s}"`); }
      }
    }

    // 5. report 회귀: page 축·넓은 구간(1024px 이상), deck 표지 배치
    const main = document.querySelector('main.d0-page[data-width="report"]');
    if (main && width >= 1024) {
      const m = main.getBoundingClientRect();
      const L = m.width, C = m.left + L / 2;
      const axis = Math.min(720, L - 64), wide = Math.min(960, L - 64);
      let axisLeft = null;
      main.querySelectorAll(':scope > .d0-header > *, :scope > .d0-section > *').forEach((el) => {
        const q = el.getBoundingClientRect();
        if (q.width === 0) return;
        const isWide = el.classList.contains('d0-wide');
        const want = isWide ? wide : axis;
        const tag = `${el.tagName.toLowerCase()}${el.className ? '.' + String(el.className).split(' ')[0] : ''}`;
        if (Math.abs(q.width - want) > TOL) fail(`${width}px: report 폭 ${Math.round(q.width)} ≠ ${want} (${tag})`);
        if (Math.abs(q.left + q.width / 2 - C) > TOL) fail(`${width}px: report 중심선 어긋남 ${Math.round(q.left + q.width / 2 - C)}px (${tag})`);
        if (!isWide) {
          if (axisLeft === null) axisLeft = q.left;
          else if (Math.abs(q.left - axisLeft) > TOL) fail(`${width}px: report 시작선 어긋남 (${tag})`);
        }
      });
      const h1 = main.querySelector('.d0-header h1');
      if (h1 && axisLeft !== null && Math.abs(h1.getBoundingClientRect().left - axisLeft) > TOL) fail(`${width}px: report 표지 제목이 본문 축 밖`);
    }
    if (deck) {
      deck.querySelectorAll('.d0-slide[data-kind="cover"]').forEach((s) => {
        const cov = s.querySelector('.d0-slide__cover');
        if (!cov || s.getBoundingClientRect().width < 731) return;
        const cols = getComputedStyle(cov).gridTemplateColumns.trim().split(/\s+/).length;
        const kind = s.getAttribute('data-cover') || 'side';
        const want = ['bottom', 'contrast', 'center'].includes(kind) ? 1 : 2;
        if (cols !== want) fail(`${width}px: 표지(${kind}) 열 수 ${cols} ≠ ${want}`);
      });
    }

    // 6. 구조: 남은 자리표시자, 토큰
    if (/\/\*\s*eli5:/.test(document.documentElement.innerHTML)) fail('채우지 않은 자리표시자(/* eli5:… */)가 남아 있음');
    if (!getComputedStyle(doc).getPropertyValue('--d0-blue').trim()) fail('tokens.css가 인라인되지 않음(--d0-blue 없음)');
    return out;
  }, { width, slugs });
}

(async () => {
  const file = process.argv[2];
  if (!file || file.startsWith('--')) { console.error('사용법: node scripts/check_render.cjs out.html [--widths 1440,390] [--playwright 경로]'); process.exit(2); }
  const abs = path.resolve(file);
  if (!fs.existsSync(abs)) { console.error(`파일 없음: ${abs}`); process.exit(2); }
  const widths = arg('--widths', '1440,390').split(',').map(Number).filter(Boolean);
  const { chromium } = loadPlaywright();
  const browser = await chromium.launch();
  const results = [];
  const external = new Set();
  try {
    for (const w of widths) {
      const page = await browser.newPage({ viewport: { width: w, height: w >= 1024 ? 800 : 844 } });
      page.on('console', (m) => { if (m.type() === 'error') results.push(['FAIL', `${w}px: 콘솔 오류 ${m.text().slice(0, 120)}`]); });
      page.on('pageerror', (e) => results.push(['FAIL', `${w}px: 스크립트 오류 ${String(e).slice(0, 120)}`]));
      page.on('request', (r) => { const u = r.url(); if (!/^(file|data|blob|about):/.test(u)) external.add(u.split('?')[0]); });
      await page.goto('file://' + abs, { waitUntil: 'load' });
      await page.waitForTimeout(300);
      results.push(...await inspect(page, w, SLUGS));
      await page.close();
    }
  } finally { await browser.close(); }
  const fonts = [...external].filter((u) => /pretendard/i.test(u));
  if (fonts.length) results.push(['WARN', `폰트 폴백 링크 외부 요청 ${fonts.length}건(넘기기 전 subset_font.py로 없앤다)`]);
  external.forEach((u) => { if (!/pretendard/i.test(u)) results.push(['FAIL', `외부 요청: ${u}`]); });
  const uniq = [...new Map(results.map((r) => [r.join(' '), r])).values()];
  uniq.forEach(([lv, m]) => console.log(`${lv} ${m}`));
  const fails = uniq.filter((r) => r[0] === 'FAIL').length;
  console.log(fails ? `\n${fails}개 실패` : `\n기계 검사 통과(${widths.join('·')}px). 네 질문은 렌더를 보고 따로 답한다.`);
  process.exit(fails ? 1 : 0);
})();
