#!/usr/bin/env node
/*
 * eli5-design 결과물의 기계 검사. 사람이 봐야 아는 것은 references/final-review.md 네 질문이 맡는다.
 *
 *   node scripts/check_render.cjs out.html
 *   node scripts/check_render.cjs out.html --widths 1440,390 --playwright <playwright-core 경로>
 *
 * playwright-core(또는 playwright)를 찾는 순서: --playwright 인자 → ELI5_PLAYWRIGHT 환경 변수 → require('playwright-core') → require('playwright').
 * 검사: 콘솔 오류, 남은 자리표시자·토큰 누락·외부 요청, 페이지 가로 넘침, SVG 잘림, page 그림 글자 크기(경고),
 *       page 넓은 구간 속 작은 그림, page 그림 간 글자 크기 불일치, 내부 식별자 노출, report 표지 회귀(page 축·넓은 구간, deck 표지 배치).
 * 측정은 뷰포트 숫자가 아니라 실제 컨테이너 폭으로 하고 1px 오차를 허용한다(스크롤바 유무로 판정이 바뀌지 않게).
 * page면 넓은 화면 전체 스크린숏과 본보기 세 장을 나란히 붙인 <out>.compare.png를 만든다.
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

    // 3-1. page 넓은 구간 속 작은 그림: 축(viewBox 560)·축 2열(360)용으로 그린 글자 있는 그림을 .d0-wide에 넣으면 그 그림만 커진다.
    //      허용은 diagrams/index.md의 viewBox 폭: 넓은 구간 바로 안 750, 넓은 구간 2열 칸 480. 글자 없는 그림·그림 안 가로 스크롤은 보지 않는다.
    const vbw = (svg) => (svg.viewBox && svg.viewBox.baseVal && svg.viewBox.baseVal.width) || 0;
    const texts = (svg) => [...svg.querySelectorAll('text.d0-s-text')].filter((t) => t.textContent.trim() && t.getBBox().width > 0);
    const label = (svg, i) => ((svg.querySelector('title') || {}).textContent || `svg#${i + 1}`).trim().slice(0, 30);
    const figs = [...document.querySelectorAll('.d0-page svg[role="img"]')];
    if (width >= 1024) {
      figs.forEach((svg, i) => {
        if (!svg.closest('.d0-wide') || svg.closest('.d0-fig__scroll') || !texts(svg).length) return;
        const inCols = !!svg.closest('.d0-cols');
        const min = inCols ? 480 : 750;
        if (vbw(svg) < min) fail(`작은 그림을 넓은 구간에 넣음 — 축 폭으로 옮기거나 viewBox ${min}로 다시 그린다: "${label(svg, i)}" viewBox ${vbw(svg)}${inCols ? '(2열 칸)' : ''}`);
      });
    }

    // 3-2. page 그림 간 글자 크기: 그림마다 .d0-s-text 렌더 크기 중앙값과, 축에 놓은 viewBox 560 기준 그림(잠깐 넣었다 뺀다)을 견준다.
    //      번호 원(.d0-s-num) 같은 다른 클래스 글자, 일부러 줄인 그림(data-fit="compact")과 그림 안 가로 스크롤은 뺀다.
    //      임계 1.35: 승인 본보기는 1440 16.8~18.0px(1.07)·390 11.6~12.8px(1.10). 정본 배치(축·틀 끔·축 2열 360·넓은 구간 750·
    //      넓은 구간 2열 480·7/5)를 한 장에 모으면 1440에서 축 2열 14.3px 대 7/5 칸 18.4px(1.29)가 가장 벌어져 그 위에 둔다.
    //      preview-compare는 글자 그림이 하나라 판별력이 없다.
    const sec = document.querySelector('.d0-page > .d0-section');
    if (sec) {
      const probe = document.createElement('figure');
      probe.className = 'd0-fig';
      probe.innerHTML = '<svg viewBox="0 0 560 60" role="img"><text class="d0-s-text" x="8" y="30">기준</text></svg>';
      sec.appendChild(probe);
      const ps = probe.querySelector('svg');
      const ref = parseFloat(getComputedStyle(ps.querySelector('text')).fontSize) * ps.getBoundingClientRect().width / 560;
      probe.remove();
      const meds = [];
      figs.forEach((svg, i) => {
        const r = svg.getBoundingClientRect();
        if (r.width < 2 || svg.closest('.d0-fig__scroll, .d0-fig[data-fit="compact"]') || !vbw(svg)) return;
        const xs = texts(svg).map((t) => parseFloat(getComputedStyle(t).fontSize) * r.width / vbw(svg)).sort((a, b) => a - b);
        if (xs.length) meds.push({ name: label(svg, i), px: xs[xs.length >> 1] });
      });
      const all = [{ name: '축 그림 기준', px: ref }, ...meds];
      const lo = all.reduce((a, b) => (b.px < a.px ? b : a)), hi = all.reduce((a, b) => (b.px > a.px ? b : a));
      if (hi.px / lo.px > 1.35) fail(`${width}px: 그림 글자 크기 불일치 ${(hi.px / lo.px).toFixed(2)} > 1.35 — "${hi.name}" ${hi.px.toFixed(1)}px ↔ "${lo.name}" ${lo.px.toFixed(1)}px. 놓는 곳의 viewBox 폭으로 다시 그린다`);
    }

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

// 내 page 넓은 화면 전체(왼쪽)와 본보기 세 장을 세로로 이은 것(오른쪽)을 같은 높이로 줄여 한 장에 붙인다. 폭 1600·높이 3200 이하.
async function compare(browser, shot, abs) {
  const ex = [1, 2, 3].map((n) => path.join(__dirname, '..', 'references', 'examples', `explainer-skills-mcp-${n}.jpg`));
  const uri = (buf, type) => `data:${type};base64,${buf.toString('base64')}`;
  const page = await browser.newPage({ viewport: { width: 1600, height: 800 } });
  await page.setContent(`<body style="margin:0;background:#fff"><div id="row" style="display:flex;gap:16px;align-items:flex-start;padding:16px">
    <img id="mine" style="flex:none" src="${uri(shot.buf, 'image/png')}"><div id="ex" style="flex:none;display:flex;flex-direction:column">${ex.map((e) => `<img src="${uri(fs.readFileSync(e), 'image/jpeg')}">`).join('')}</div></div></body>`);
  await page.waitForFunction(() => [...document.images].every((i) => i.complete && i.naturalWidth));
  const size = await page.evaluate(() => {
    const mine = document.getElementById('mine'), exs = [...document.querySelectorAll('#ex img')];
    const exW = exs[0].naturalWidth, exH = exs.reduce((a, i) => a + i.naturalHeight * exW / i.naturalWidth, 0);
    const aspect = mine.naturalWidth / mine.naturalHeight + exW / exH; // 같은 높이 H일 때 두 칸 폭의 합 = H × aspect
    const H = Math.min(3200, (1600 - 48) / aspect);
    mine.style.height = `${H}px`;
    exs.forEach((i) => { i.style.width = `${H * exW / exH}px`; });
    const r = document.getElementById('row').getBoundingClientRect();
    return { w: Math.ceil(r.width), h: Math.ceil(r.height) };
  });
  const out = abs.replace(/\.html?$/i, '') + '.compare.png';
  await page.setViewportSize({ width: Math.min(1600, size.w), height: size.h });
  await page.screenshot({ path: out, clip: { x: 0, y: 0, width: Math.min(1600, size.w), height: size.h } });
  await page.close();
  return out;
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
  let isPage = false;
  let shot = null;
  const shotW = widths.find((w) => w >= 1024) || Math.max(...widths);
  try {
    for (const w of widths) {
      const page = await browser.newPage({ viewport: { width: w, height: w >= 1024 ? 800 : 844 } });
      page.on('console', (m) => { if (m.type() === 'error') results.push(['FAIL', `${w}px: 콘솔 오류 ${m.text().slice(0, 120)}`]); });
      page.on('pageerror', (e) => results.push(['FAIL', `${w}px: 스크립트 오류 ${String(e).slice(0, 120)}`]));
      page.on('request', (r) => { const u = r.url(); if (!/^(file|data|blob|about):/.test(u)) external.add(u.split('?')[0]); });
      await page.goto('file://' + abs, { waitUntil: 'load' });
      await page.waitForTimeout(300);
      if (!isPage) isPage = await page.evaluate(() => !document.querySelector('.d0-deck') && !!document.querySelector('main.d0-page'));
      results.push(...await inspect(page, w, SLUGS));
      if (isPage && w === shotW) {
        const box = await page.evaluate(() => { const f = document.querySelector('.d0-page > *').getBoundingClientRect(); return { x: Math.max(0, f.left - 136), w: Math.min(innerWidth, f.width + 272), h: document.documentElement.scrollHeight }; /* 사이드 노트(틀 밖 96px)까지 */ });
        shot = { buf: await page.screenshot({ fullPage: true, clip: { x: box.x, y: 0, width: box.w, height: box.h } }), w: box.w, h: box.h };
      }
      await page.close();
    }
    if (shot) results.compare = await compare(browser, shot, abs);
  } finally { await browser.close(); }
  const fonts = [...external].filter((u) => /pretendard/i.test(u));
  if (fonts.length) results.push(['WARN', `폰트 폴백 링크 외부 요청 ${fonts.length}건(넘기기 전 subset_font.py로 없앤다)`]);
  external.forEach((u) => { if (!/pretendard/i.test(u)) results.push(['FAIL', `외부 요청: ${u}`]); });
  const uniq = [...new Map(results.map((r) => [r.join(' '), r])).values()];
  uniq.forEach(([lv, m]) => console.log(`${lv} ${m}`));
  const fails = uniq.filter((r) => r[0] === 'FAIL').length;
  console.log(fails ? `\n${fails}개 실패` : `\n기계 검사 통과(${widths.join('·')}px). 네 질문은 렌더를 보고 따로 답한다.`);
  if (results.compare) console.log(`\n${results.compare}\n이 이미지를 열어 본보기(오른쪽)가 그림으로 보인 곳을 내가(왼쪽) 글·격자·아이콘으로 때운 곳을 찾는다. 배치·그림 종류·비유 사물은 본보기와 스킬 문서 예시를 따라 하지 않고 주제에 맞게 다채롭게 둔다.`);
  process.exit(fails ? 1 : 0);
})();
