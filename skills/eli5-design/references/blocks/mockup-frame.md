# mockup-frame — 눌러 보는 미니 앱

결과 화면을 설명하지 않고 **프레임 안에서 직접 눌러 보게** 한다. 시안 비교에서는 같은 크기 프레임 두 개를 나란히 둔다.

## 해부 구조

- 시안 하나 = `article.d0-demo` → `header`(시안 이름 h3 + `처음부터` 버튼) → 프레임(`.d0-frame`).
- 프레임 = 고정 높이 600px(640px 이하에서는 높이 auto, 최소 520px), 1px grey-200 테두리, 안쪽 grey-50 바탕.
- 프레임 안 앱(`.d0-app`) = `header`(앱 이름 + 주 버튼 하나) → `section`(고스트 카드: 글자 없는 흰 면 2~3장, `aria-hidden`).
  페이지에 `main`이 이미 있으므로 프레임 안에서는 `main`을 쓰지 않는다(문서당 하나).
- 주 버튼을 누르면 `dialog`가 프레임 **안에서** 열린다. 모달(가운데, 단계형) 또는 오른쪽 패널(`.d0-panel`, 한 화면). 막(scrim)은 프레임만 덮는다.
- 모달 = 진행 막대(`<progress>`) + 단계 라벨(`1 / 2`) + 제목(h4) → 단계마다 `fieldset`(라디오 2~5개) → 바닥(닫기 · 이전 · 다음/내보내기).
- 끝내면 프레임 안 토스트(`output`, 암묵 role status)로 결과를 한 줄 알린다. 실제 다운로드·전송은 하지 않는다.

**dialog 선택.** `showModal()`은 최상위 레이어로 올라가 프레임 밖 전체 화면을 덮으므로 쓰지 않는다. `dialog.show()`로
프레임 안에 띄우고, 뒤 앱은 `inert`, Esc 닫기·Tab 순환·포커스 복귀는 JS가 맡는다. 그래서 `aria-modal="true"`를 붙인다.

## 언제 쓰나 / 변형

- compare 시안 변형, preview에서 "이 화면에서 어떻게 받나"를 보여 줄 때. 와이어프레임으로 충분하면 [diagram.md](diagram.md) (d).
- `data-variant="modal"`: 하나씩 묻기(단계마다 fieldset 하나). `data-variant="panel"`: 오른쪽 패널(`.d0-panel`)에 모든 fieldset을 한 번에.
  `.d0-sheet`는 tab-preview의 표 클래스이므로 이 블록에서 쓰지 않는다.
- A/B는 같은 데이터·같은 높이. 화면을 실제 크기로 견주는 동시 비교라 `.d0-wide`(오른쪽만 프레임 끝까지) 안 `.d0-cols`(넓은 구간 분할선)로 960px 이상 2열, 그 아래 세로다([shell.md](shell.md) 넓은 구간 (a)). 작은 와이어 두 장을 견주는 정도면 축 안 `.d0-cols`로 충분하다. 완성 예는 [preview-compare.html](../examples/preview-compare.html) ③.
- 눌러 볼 필요 없이 화면의 한 곳을 짚어 보이면 아래 [Screenshot spotlight](#screenshot-spotlight-figured0-shot)(`figure.d0-shot`)를 쓴다.

## 스니펫

```html
<div class="d0-wide"><div class="d0-demos d0-cols">
  <article class="d0-demo" data-demo data-variant="modal" data-state="idle">
    <header class="d0-demo__head"><h3>A. 하나씩 묻기</h3><button type="button" class="d0-link" data-reset>처음부터</button></header>
    <div class="d0-frame">
      <div class="d0-app">
        <header class="d0-app__top"><b>주문 관리</b><button type="button" class="d0-btn" data-variant="primary" data-open>내보내기</button></header>
        <section class="d0-app__body" aria-hidden="true"><div class="d0-ghost"></div><div class="d0-ghost" data-size="tall"></div></section>
      </div>
      <div class="d0-scrim" hidden></div>
      <dialog class="d0-modal" aria-modal="true" aria-labelledby="mA-t">
        <progress class="d0-modal__bar" max="2" value="1" aria-label="단계 진행" data-bar></progress>
        <header class="d0-modal__head"><small data-step-label>1 / 2</small><h4 id="mA-t">내보내기</h4></header>
        <div class="d0-modal__body">
          <fieldset><legend>어느 기간을 받을까요?</legend>
            <label class="d0-opt"><input type="radio" name="a-range" value="오늘">오늘</label>
            <label class="d0-opt"><input type="radio" name="a-range" value="이번 주">이번 주</label></fieldset>
          <fieldset><legend>어떤 모양으로 받을까요?</legend>
            <label class="d0-opt"><input type="radio" name="a-kind" value="팀별 합계">팀별 합계</label>
            <label class="d0-opt"><input type="radio" name="a-kind" value="상품 × 일자">상품 × 일자</label></fieldset>
        </div>
        <footer class="d0-modal__foot"><button type="button" class="d0-btn" data-variant="ghost" data-close>닫기</button>
          <span><button type="button" class="d0-btn" data-back>이전</button> <button type="button" class="d0-btn" data-variant="primary" data-next>다음</button></span></footer>
      </dialog>
      <output class="d0-toast" hidden></output>
    </div>
  </article>
  <!-- B 시안: 위 article을 복사해 다음만 바꾼다.
       article data-variant="panel" · h3 "B. 한 화면에서 고르기" · dialog class="d0-modal d0-panel"
       · progress.d0-modal__bar 줄과 <small data-step-label> 삭제 · aria-labelledby/h4 id를 mB-t로 · 라디오 name을 b-range·b-kind로.
       data-open·data-close·data-back·data-next·data-reset은 그대로 둔다(JS가 찾는다). -->
</div></div>
```

```css
/* .d0-demos의 2열 격자는 .d0-cols(정본 assets/page.css)가 만든다 */
.d0-demo { display: grid; gap: 12px; min-width: 0; }
.d0-demo__head { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.d0-link { min-height: 24px; padding: 2px 4px; border: 0; background: none; color: var(--d0-blue-dark); font-size: var(--d0-text-compact); font-weight: 600; }
.d0-frame { position: relative; display: grid; height: 600px; overflow: hidden; border: 1px solid var(--d0-grey-200); border-radius: var(--d0-radius-card); background: var(--d0-grey-50); }
.d0-frame [hidden] { display: none !important; }
.d0-app { display: grid; grid-template-rows: auto 1fr; min-height: 0; }
.d0-app__top { display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 12px 16px; background: #fff; border-bottom: 1px solid var(--d0-grey-200); }
.d0-app__body { display: grid; gap: 12px; align-content: start; padding: 16px; }
.d0-ghost { height: 88px; border-radius: var(--d0-radius-card); background: #fff; }
.d0-ghost[data-size="tall"] { height: 200px; }
.d0-btn { display: inline-flex; align-items: center; justify-content: center; height: 36px; padding: 0 14px; border: 0; border-radius: var(--d0-radius-control); background: var(--d0-grey-100); color: var(--d0-grey-900); font-size: 14px; font-weight: 600; white-space: nowrap; transition: transform var(--d0-dur-fast) var(--d0-ease); }
.d0-btn:active { transform: scale(0.97); }
.d0-btn[data-variant="primary"] { background: var(--d0-blue-dark); color: #fff; }
.d0-btn[data-variant="ghost"] { background: transparent; color: var(--d0-grey-700); }
.d0-btn:disabled { background: var(--d0-grey-100); color: var(--d0-grey-600); cursor: not-allowed; }
.d0-scrim { position: absolute; inset: 0; background: color-mix(in srgb, var(--d0-grey-900) 32%, transparent); }
.d0-modal { position: absolute; inset: 0; z-index: 1; width: calc(100% - 32px); max-width: 440px; height: fit-content; max-height: calc(100% - 32px); margin: auto; padding: 0; border: 0; border-radius: var(--d0-radius-card); background: #fff; color: inherit; box-shadow: var(--d0-shadow-overlay); }
.d0-modal[open] { display: flex; flex-direction: column; overflow: hidden; animation: d0-in var(--d0-dur) var(--d0-ease); }
.d0-panel { inset: 0 0 0 auto; width: min(100%, 360px); height: 100%; max-height: none; margin: 0; border-radius: 0; }
.d0-panel[open] { animation-name: d0-slide; }
.d0-modal__bar { display: block; flex: none; width: 100%; height: 3px; border: 0; appearance: none; background: var(--d0-grey-100); }
.d0-modal__bar::-webkit-progress-bar { background: var(--d0-grey-100); }
.d0-modal__bar::-webkit-progress-value { background: var(--d0-blue); transition: width var(--d0-dur) var(--d0-ease); }
.d0-modal__bar::-moz-progress-bar { background: var(--d0-blue); }
.d0-modal__head { display: grid; gap: 2px; padding: 16px 20px 4px; }
.d0-modal__head small { color: var(--d0-blue-dark); font-size: var(--d0-meta); font-weight: 600; }
.d0-modal__head h4 { margin: 0; font-size: 17px; font-weight: 700; letter-spacing: var(--d0-tracking-title); }
.d0-modal__body { flex: 1; display: grid; gap: 20px; align-content: start; padding: 12px 20px; overflow: auto; }
.d0-modal__body fieldset { display: grid; gap: 8px; margin: 0; padding: 0; border: 0; }
.d0-modal__body legend { margin-bottom: 8px; padding: 0; font-size: 15px; font-weight: 600; }
.d0-opt { display: flex; align-items: center; gap: 10px; min-height: 44px; padding: 0 14px; border-radius: var(--d0-radius-control); background: var(--d0-grey-50); font-size: 14px; cursor: pointer; }
.d0-opt:has(:checked) { background: var(--d0-blue-light); color: var(--d0-blue-dark); font-weight: 600; }
.d0-opt input { margin: 0; accent-color: var(--d0-blue-dark); }
.d0-modal__foot { display: flex; justify-content: space-between; gap: 8px; padding: 12px 20px 16px; border-top: 1px solid var(--d0-grey-100); }
.d0-toast { position: absolute; left: 50%; bottom: 16px; z-index: 2; transform: translateX(-50%); width: max-content; max-width: calc(100% - 32px); padding: 10px 16px; border-radius: var(--d0-radius-control); background: var(--d0-grey-900); color: #fff; font-size: var(--d0-text-compact); box-shadow: var(--d0-shadow-overlay); }
@keyframes d0-in { from { opacity: 0; transform: translateY(8px); } }
@keyframes d0-slide { from { opacity: 0; transform: translateX(16px); } }
@media (max-width: 640px) { .d0-frame { height: auto; min-height: 520px; } }
```

```js
var shutters = []; // 한 번에 시안 하나만 연다(aria-modal dialog가 둘 열리지 않게)
document.querySelectorAll('[data-demo]').forEach(function (demo) {
  var $ = function (s) { return demo.querySelector(s); };
  var dlg = $('dialog'), app = $('.d0-app'), scrim = $('.d0-scrim'), toast = $('.d0-toast'), opener = $('[data-open]');
  var sets = Array.prototype.slice.call(dlg.querySelectorAll('fieldset'));
  var next = $('[data-next]'), back = $('[data-back]'), bar = $('[data-bar]'), label = $('[data-step-label]');
  var panel = demo.dataset.variant === 'panel', st = { open: false, step: 0, done: '' };
  var picked = function (fs) { var r = fs.querySelector('input:checked'); return r ? r.value : ''; };
  function render() {
    var last = panel || st.step === sets.length - 1;
    sets.forEach(function (fs, i) { fs.hidden = !panel && i !== st.step; });
    if (bar) { bar.max = sets.length; bar.value = st.step + 1; }
    if (label) label.textContent = (st.step + 1) + ' / ' + sets.length;
    next.textContent = last ? '내보내기' : '다음';
    next.disabled = (panel ? sets : [sets[st.step]]).some(function (fs) { return !picked(fs); });
    back.hidden = panel || st.step === 0;
    scrim.hidden = !st.open;
    app.inert = st.open;
    if (st.open && !dlg.open) dlg.show();
    if (!st.open && dlg.open) dlg.close();
    toast.hidden = !st.done;
    toast.textContent = st.done;
    demo.dataset.state = st.open ? 'open' : st.done ? 'done' : 'idle';
  }
  function focusStep() { var fs = sets[panel ? 0 : st.step]; (fs.querySelector(':checked') || fs.querySelector('input')).focus(); }
  function close() { st.open = false; render(); opener.focus(); }
  function shut() { if (st.open) { st.open = false; render(); } }
  shutters.push(shut);
  opener.addEventListener('click', function () {
    shutters.forEach(function (f) { if (f !== shut) f(); });
    st = { open: true, step: 0, done: '' }; render(); focusStep();
  });
  dlg.addEventListener('change', render);
  next.addEventListener('click', function () {
    if (!panel && st.step < sets.length - 1) { st.step++; render(); focusStep(); return; }
    st.done = sets.map(picked).join(' · ') + ' 파일을 만들었어요(데모)';
    close();
  });
  back.addEventListener('click', function () { st.step--; render(); focusStep(); });
  $('[data-close]').addEventListener('click', close);
  scrim.addEventListener('click', close);
  dlg.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { e.preventDefault(); close(); return; }
    if (e.key !== 'Tab') return;
    var f = Array.prototype.filter.call(dlg.querySelectorAll('input, button'), function (el) { return !el.disabled && el.offsetParent; });
    var first = f[0], end = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); end.focus(); }
    else if (!e.shiftKey && document.activeElement === end) { e.preventDefault(); first.focus(); }
  });
  $('[data-reset]').addEventListener('click', function () {
    dlg.querySelectorAll('input').forEach(function (i) { i.checked = false; });
    st = { open: false, step: 0, done: '' }; render(); opener.focus();
  });
  render();
});
```

- 처음 상태는 닫힘(`open: false`)이다. 주 버튼을 눌러야 dialog가 열리고, 한 시안을 열면 다른 시안은 닫힌다.
- 상태는 시안마다 객체 하나(`{ open, step, done }`)와 `render()` 하나. 모든 조작은 상태를 바꾸고 `render()`를 부른다.
- 시안 상태는 `article[data-state="idle|open|done"]`으로 노출한다. 스타일 분기가 필요하면 이 값을 쓴다.
- 라디오는 Tab으로 그룹 하나에 한 번 머문다(네이티브 동작). Tab 순환은 보이는 입력·버튼만 돈다.

## 별도 HTML 페이지를 프레임에 넣을 때

이미 만든 HTML 한 장을 프레임 안에 그대로 보여 줘야 하면 `iframe`을 쓴다. **`iframe src`(파일 경로·URL)는 금지다.** artifact 샌드박스에서
다른 파일을 불러오지 못해 빈 프레임이 된다. 페이지를 base64로 내장하고 `srcdoc`에 풀어 넣는다. `sandbox="allow-scripts"` 하나만 준다.

```html
<div class="d0-frame">
  <iframe class="d0-frame__page" title="주문 관리 화면 시안" sandbox="allow-scripts" loading="lazy"
    data-page64="PCFkb2N0eXBlIGh0bWw+…"></iframe>
</div>
<script>
document.querySelectorAll('iframe[data-page64]').forEach(function (f) {
  var bin = atob(f.dataset.page64);
  var bytes = Uint8Array.from(bin, function (c) { return c.charCodeAt(0); });
  f.srcdoc = new TextDecoder().decode(bytes); // 한글이 깨지지 않게 UTF-8로 푼다
});
</script>
```

```css
.d0-frame__page { width: 100%; height: 100%; border: 0; background: #fff; }
```

- base64는 `base64 -i page.html`(macOS) 또는 `base64 -w0 page.html`로 만든다. 내장 페이지도 외부 요청 0이어야 한다(토큰·폰트 인라인).
- `allow-same-origin`을 더하지 않는다. 내장 페이지 스크립트가 바깥 페이지에 닿지 않게 한다.
- `title`은 필수다(프레임의 접근 이름). 프레임 높이 규칙은 위와 같다(600px, 640px 이하 최소 520px).

## 여러 페이지를 창으로 보여 주기 — 페이지 갤러리 (`data-variant="gallery"`)

페이지 여러 장을 노트북 창 모양 프레임 하나에 담고 탭으로 갈아 끼우며 보여 준다. 위 srcdoc 내장 규칙(base64 → `srcdoc`, `sandbox="allow-scripts"`만, `src` 금지)을 그대로 따른다.

**레이아웃: 뷰포트 높이 전부.**

- 갤러리 섹션은 `height: 100vh; height: 100dvh`(`min-height`가 아니다)이고 행은 `auto auto minmax(0, 1fr)`(제목 · 탭 · 창)이다. 창이 남은 높이를 채우고, 내용이 넘치면 창 iframe이 줄어든다(`min-height: 0`, `flex: 1 1 0`). 섹션이 정확히 뷰포트 높이여야 맞춤 뒤 위아래로 미세 조절할 일이 없다. **고정 높이(600px 등)를 쓰지 않는다.** 창이 중간에 끝나 "어느 정도 가다가 막히는" 느낌을 주지 않기 위해서다.
- 640px 이하에서도 같은 규칙이다. 모바일 브라우저 주소창이 오르내려도 높이가 흔들리지 않게 `dvh`를 쓴다. 갤러리는 **페이지의 마지막 섹션**에 둔다(뒤에 섹션이 이어지면 100vh 섹션이 흐름을 끊는다).
- 이 변형은 위 "고정 높이 600px" 규칙의 예외다. 같은 페이지의 일반 `.d0-frame`은 그대로 600px.

**스크롤 맞춤(스냅).** 사용자가 스크롤을 **완전히 멈춘 뒤에만**, 갤러리 근처면 섹션 맨 위를 뷰포트 맨 위에 부드럽게 맞춘다.

- CSS 스냅(`scroll-snap-type`, `scroll-snap-align`, `scroll-snap-stop`)을 쓰지 않는다. 관성 스크롤 중간에 붙잡혀 "끌려가는" 느낌을 준다. 맞춤은 JS가 맡는다.
- 멈춤 판정: `scrollend` 이벤트(미지원이면 마지막 `scroll` 뒤 160ms 디바운스). 그때도 `wheel`·`touchmove`·`keydown` 입력이 160ms 안에 있었거나 손가락이 화면에 닿아 있으면 기다렸다 다시 본다.
- 범위: 섹션 `top`이 뷰포트 높이의 ±25% 안일 때만 `window.scrollTo({ top: 섹션 절대 top, behavior: 'smooth' })`. 그 밖이면 건드리지 않는다.
- 맞춤이 만든 `scrollend`로 다시 맞추지 않는다(플래그, 1초 안전 해제). 맞추는 중 새 입력이 오면 플래그를 풀고 사용자에게 넘긴다.
- 탭·기기 토글을 누르거나 창(iframe) 안으로 포커스가 들어간 직후(600ms)는 맞추지 않는다. `prefers-reduced-motion: reduce`면 맞추지 않는다.

```css
html { scrollbar-gutter: stable; } /* 스냅 속성 없음 */
.d0-section[data-fill="viewport"] {
  height: 100vh; height: 100dvh;
  grid-template-rows: auto minmax(0, 1fr); /* 제목 · 갤러리(탭 · 창) */
}
.d0-gallery, .d0-gallery__panel { display: grid; grid-template-rows: auto minmax(0, 1fr); min-height: 0; }
.d0-gallery__frame { flex: 1 1 0; min-height: 0; }
```

```js
(function () {
  var sec = document.querySelector('[data-fill="viewport"]');
  if (!sec) return;
  var gal = sec.querySelector('.d0-gallery');
  var QUIET = 160, RANGE = 0.25;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var lastInput = 0, lastGallery = 0, touching = false, scrolling = false, aligning = false, alignTimer = 0, idleTimer = 0;
  function now() { return Date.now(); }
  function input() { lastInput = now(); if (aligning) { aligning = false; clearTimeout(alignTimer); } }
  window.addEventListener('wheel', input, { passive: true });
  window.addEventListener('touchmove', input, { passive: true });
  window.addEventListener('keydown', input);
  window.addEventListener('touchstart', function () { touching = true; input(); }, { passive: true });
  window.addEventListener('touchend', function () { touching = false; input(); }, { passive: true });
  window.addEventListener('touchcancel', function () { touching = false; }, { passive: true });
  function mark() { lastGallery = now(); } // 탭·토글 조작, iframe 안으로 포커스 이동(window blur)
  if (gal) ['pointerdown', 'keydown', 'focusin'].forEach(function (t) { gal.addEventListener(t, mark); });
  window.addEventListener('blur', mark);
  function busy() { return touching || now() - lastGallery < 600; }
  function settle() {
    if (aligning) { aligning = false; clearTimeout(alignTimer); return; } // 맞춤이 만든 scrollend
    if (scrolling) return; // 다시 움직이기 시작했으면 다음 멈춤에서 본다
    var wait = QUIET - (now() - lastInput);
    if (wait > 0) { clearTimeout(idleTimer); idleTimer = setTimeout(settle, wait); return; }
    if (reduce.matches || busy()) return;
    var top = sec.getBoundingClientRect().top;
    if (Math.abs(top) < 1 || Math.abs(top) > window.innerHeight * RANGE) return;
    aligning = true;
    alignTimer = setTimeout(function () { aligning = false; }, 1000);
    window.scrollTo({ top: top + window.pageYOffset, behavior: 'smooth' });
  }
  function stopped() { scrolling = false; settle(); }
  var hasEnd = 'onscrollend' in window;
  window.addEventListener('scroll', function () {
    scrolling = true;
    if (!hasEnd) { clearTimeout(idleTimer); idleTimer = setTimeout(stopped, QUIET); }
  }, { passive: true });
  if (hasEnd) window.addEventListener('scrollend', stopped);
})();
```

**스크롤 가둠.** 창 안 스크롤이 끝에 닿아도 바깥 페이지가 따라 움직이지 않게 한다.

- 내장 문서 `head`에 `<style>html{overflow-y:scroll;scrollbar-gutter:stable}html,body{overscroll-behavior:contain}</style>`를 넣는다(base64로 만들기 전에 주입). 탭을 오갈 때 짧은 페이지와 긴 페이지의 가로 폭이 달라 보이는 시프트를 막는다. iframe 루트에서는 `scrollbar-gutter: stable`만으로 폭을 예약하지 못하는 브라우저가 있으므로 `overflow-y: scroll`로 스크롤바 자리를 늘 둔다.
- 바깥 창 컨테이너(`.d0-win__body`)에도 `overscroll-behavior: contain`. 창 안에 스크롤 컨테이너를 따로 두면 거기에도 `scrollbar-gutter: stable`. 갤러리를 담은 페이지 자신의 `html`에도 `scrollbar-gutter: stable`(shell 기본 CSS)을 둔다.

**창 테두리(노트북 창).**

- 타이틀바 높이 36~40px, grey-50 바탕, 아래 1px grey-200. 왼쪽 신호등 점 3개(12px 원, `--d0-red`·`--d0-orange`·`--d0-green`, `aria-hidden`), 가운데 현재 페이지 제목(13px grey-600, 탭을 바꾸면 갱신), 오른쪽 "새 탭에서 열기" 버튼.
- 창 전체는 `--d0-radius-card`, 1px grey-200 테두리, `--d0-shadow-overlay`. 그림자는 "떠 있는 창"이라는 예외로만 허용한다.
- **신호등은 장식이다.** 의미색 예산·대비 게이트에서 제외한다(상태를 뜻하지 않고, 누를 수도 없다). 점 3개 말고 다른 곳에 red·orange·green을 쓰지 않는다.

**탭.** `role="tablist"` + 탭마다 `role="tab"`(`aria-selected`, `aria-controls`), 패널은 `role="tabpanel"`.

- 화살표 키(← →, Home, End)로 이동하고 선택된 탭만 `tabindex="0"`(roving). 키로 옮기면 선택도 같이 바뀐다.
- **처음엔 첫 탭만 로드한다.** 나머지 iframe은 `srcdoc`가 비어 있다가 처음 선택할 때 base64를 푼다. 이미 푼 탭은 다시 풀지 않는다.
- 탭 이름은 페이지 제목과 같은 말. `iframe`에는 `title`을 둔다.

```html
<section class="d0-gallery" data-variant="gallery" aria-labelledby="gal-t">
  <h2 id="gal-t">화면 세 장을 직접 넘겨 보세요</h2>
  <div class="d0-gallery__top">
    <div class="d0-tabs" role="tablist" aria-label="페이지">
      <button type="button" role="tab" id="gt-1" aria-selected="true" aria-controls="gp-1" tabindex="0">목록</button>
      <button type="button" role="tab" id="gt-2" aria-selected="false" aria-controls="gp-2" tabindex="-1">상세</button>
    </div>
    <!-- 기기 토글: PC 화면과 모바일 화면을 둘 다 보여 줄 때만 둔다 -->
    <div class="d0-device" role="group" aria-label="미리보기 화면">
      <button type="button" data-device-set="desktop" aria-pressed="true">PC</button>
      <button type="button" data-device-set="mobile" aria-pressed="false">모바일</button>
    </div>
  </div>
  <div class="d0-win" data-device="desktop">
    <div class="d0-win__bar">
      <span class="d0-win__dots" aria-hidden="true"><i></i><i></i><i></i></span>
      <span class="d0-win__title" data-win-title>목록</span>
      <button type="button" class="d0-link" data-open-tab>새 탭에서 열기</button>
    </div>
    <div class="d0-phone__status" aria-hidden="true">
      <span>9:41</span><i class="d0-phone__island"></i>
      <svg width="26" height="12" viewBox="0 0 26 12"><rect x="0.5" y="0.5" width="22" height="11" rx="3" fill="none" stroke="currentColor"/><rect x="2.5" y="2.5" width="15" height="7" rx="1.5" fill="currentColor"/><rect x="24" y="4" width="2" height="4" rx="1" fill="currentColor"/></svg>
    </div>
    <div class="d0-win__body">
      <div role="tabpanel" id="gp-1" aria-labelledby="gt-1"><iframe class="d0-frame__page" title="목록 화면 시안" sandbox="allow-scripts" data-page64="PCFkb2N0eXBl…"></iframe></div>
      <div role="tabpanel" id="gp-2" aria-labelledby="gt-2" hidden><iframe class="d0-frame__page" title="상세 화면 시안" sandbox="allow-scripts" data-page64="PCFkb2N0eXBl…"></iframe></div>
    </div>
    <div class="d0-phone__home" aria-hidden="true"></div>
  </div>
</section>
```

```css
.d0-gallery { display: grid; grid-template-rows: auto auto 1fr; gap: 12px; min-height: 100vh; min-height: 100dvh; padding-block: 24px; }
.d0-tabs { display: flex; gap: 4px; overflow-x: auto; }
.d0-tabs [role="tab"] { min-height: 44px; padding: 0 14px; border: 0; border-radius: var(--d0-radius-control); background: transparent; color: var(--d0-grey-600); font-size: 14px; font-weight: 600; white-space: nowrap; }
.d0-tabs [aria-selected="true"] { background: var(--d0-blue-light); color: var(--d0-blue-dark); }
.d0-win { display: grid; grid-template-rows: auto 1fr; min-height: 0; overflow: hidden; border: 1px solid var(--d0-grey-200); border-radius: var(--d0-radius-card); background: #fff; box-shadow: var(--d0-shadow-overlay); }
.d0-win__bar { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 10px; min-height: 38px; padding: 0 12px; background: var(--d0-grey-50); border-bottom: 1px solid var(--d0-grey-200); }
.d0-win__dots { display: flex; gap: 8px; }
.d0-win__dots i { width: 12px; height: 12px; border-radius: 50%; }
.d0-win__dots i:nth-child(1) { background: var(--d0-red); }
.d0-win__dots i:nth-child(2) { background: var(--d0-orange); }
.d0-win__dots i:nth-child(3) { background: var(--d0-green); }
.d0-win__bar .d0-link { justify-self: end; }
.d0-win__title { overflow: hidden; color: var(--d0-grey-600); font-size: 13px; text-overflow: ellipsis; white-space: nowrap; }
.d0-win__body { position: relative; min-height: 0; overflow: hidden; overscroll-behavior: contain; }
.d0-win__body [role="tabpanel"] { height: 100%; }
.d0-win__body [hidden] { display: none; }
@media (max-width: 640px) { .d0-win { min-height: 480px; } .d0-win__bar { grid-template-columns: auto 1fr auto; } }
```

```js
document.querySelectorAll('[data-variant="gallery"]').forEach(function (g) {
  var tabs = Array.prototype.slice.call(g.querySelectorAll('[role="tab"]'));
  var title = g.querySelector('[data-win-title]'), cur = 0;
  var HEAD = '<style>html{overflow-y:scroll;scrollbar-gutter:stable}html,body{overscroll-behavior:contain}</style>';
  function html(f) { // base64 → UTF-8, head에 스크롤 가둠 주입
    var bytes = Uint8Array.from(atob(f.dataset.page64), function (c) { return c.charCodeAt(0); });
    var s = new TextDecoder().decode(bytes);
    return /<\/head>/i.test(s) ? s.replace(/<\/head>/i, HEAD + '</head>') : HEAD + s;
  }
  function load(i) {
    var f = g.querySelector('#' + tabs[i].getAttribute('aria-controls') + ' iframe');
    if (!f.srcdoc) f.srcdoc = html(f); // 처음 선택할 때만 푼다
  }
  function select(i, focus) {
    cur = i;
    tabs.forEach(function (t, k) {
      t.setAttribute('aria-selected', k === i);
      t.tabIndex = k === i ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = k !== i;
    });
    title.textContent = tabs[i].textContent;
    load(i);
    if (focus) tabs[i].focus();
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(i); });
    t.addEventListener('keydown', function (e) {
      var n = { ArrowRight: (i + 1) % tabs.length, ArrowLeft: (i - 1 + tabs.length) % tabs.length, Home: 0, End: tabs.length - 1 }[e.key];
      if (n === undefined) return;
      e.preventDefault(); select(n, true);
    });
  });
  g.querySelector('[data-open-tab]').addEventListener('click', function () {
    var f = g.querySelector('#' + tabs[cur].getAttribute('aria-controls') + ' iframe');
    var url = URL.createObjectURL(new Blob([html(f)], { type: 'text/html' }));
    window.open(url, '_blank', 'noopener');
  });
  select(0);
});
```

- "새 탭에서 열기"는 내장한 HTML을 Blob URL로 연다. 미리보기 샌드박스가 팝업을 막으면 버튼을 `hidden`으로 두고 창 제목만 남긴다(눌러도 반응 없는 버튼을 두지 않는다).
- 창 안 페이지도 외부 요청 0, `allow-same-origin` 금지 규칙이 같다.

### 기기 프레임 (`data-device="desktop|mobile"`)

갤러리 창(`.d0-win`)의 모양을 보여 줄 화면에 맞춘다. **어떤 프레임으로 보여 줄지는 콘텐츠가 정한다.**

| 콘텐츠 | 프레임 | 토글 |
|---|---|---|
| PC 화면 미리보기(관리자·대시보드·문서 페이지) | `desktop` 노트북 창 | 없음 |
| 모바일 화면(앱·모바일 웹) | `mobile` 폰 | 없음(`data-device="mobile"`로 시작) |
| 반응형이라 둘 다 해당 | 처음은 `desktop` | "PC / 모바일" 토글 |

- **desktop** = 위 노트북 창 그대로(타이틀바 38px, 신호등 점 3개, 가운데 제목, 오른쪽 새 탭 링크).
- **mobile** = 폰. 바깥 베젤 8px `--d0-grey-900`, 모서리 44px, `--d0-shadow-overlay`. 화면 폭 **375px 고정**(내장 페이지 `innerWidth`가 375),
  위 상태줄 40px(시각 "9:41" · 다이내믹 아일랜드 알약 하나 · 배터리 SVG), 아래 홈 인디케이터 줄 120×5px. 상태줄·홈 줄은 `aria-hidden`.
  노트북 창 타이틀바는 숨긴다(새 탭 링크도 함께 사라진다. 새 탭은 PC 폭으로 열리므로 폰 모드에서는 두지 않는다).
- **이 폰 규칙(폭 375px 고정·최소 높이)은 iframe으로 실제 페이지를 넣을 때만 적용한다.** 정적 그림(SVG·미니 마크업) 둘레의 축소 프레임은 `patterns/preview.md` 규칙(폭 140~200px, 베젤 6px, 모서리 28px)을 따른다.
- 폰 높이는 창 행(`1fr`)의 남은 높이를 채우되 **최대 812px, 최소 560px**, 가로 가운데. 폰 화면 iframe도 내장 문서 `head` 주입으로 `overscroll-behavior: contain`.
- 토글은 탭 줄 오른쪽에 버튼 2개(`aria-pressed`)를 `role="group"`으로 묶는다. 타이틀바 안에 두지 않는다(폰 모드에서 사라진다).
  **iframe을 다른 부모로 옮기지 않는다.** 옮기면 `srcdoc`이 다시 로드된다. 같은 iframe에 창 모양(`data-device`)만 바꾼다.
- **640px 이하 화면에서는 폰 프레임을 겹치지 않는다.** 베젤까지 391px라 343px 본문에 들어가지 않고, 작은 화면은 그 자체가 폰이다.
  폰 스타일은 `min-width: 641px`에서만 적용하고 토글은 숨긴다. 이때 창은 본문 폭 노트북 창이며 내장 페이지는 본문 폭(약 341px)으로 보인다.
  `innerWidth = 375` 검증은 641px 이상 뷰포트의 mobile 모드에서 한다.
- 베젤·아일랜드·상태줄·홈 줄은 장식이다. 의미색 예산·대비 게이트에서 제외한다(신호등 점과 같은 예외). 상태줄 아이콘은 글리프 대신 SVG로 그린다(서브셋 폰트에 없는 기호를 피한다).

```css
.d0-gallery__top { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px; min-width: 0; }
.d0-gallery__top .d0-tabs { flex: 1 1 auto; min-width: 0; }
.d0-device { display: inline-flex; flex: none; gap: 2px; padding: 3px; border-radius: var(--d0-radius-control); background: var(--d0-grey-100); }
.d0-device button { height: 30px; padding: 0 12px; border: 0; border-radius: var(--d0-radius-sm); background: transparent; color: var(--d0-grey-700); font-size: var(--d0-text-compact); font-weight: 600; }
.d0-device button[aria-pressed="true"] { background: var(--d0-blue-light); color: var(--d0-blue-dark); }
.d0-phone__status, .d0-phone__home { display: none; }
@media (min-width: 641px) {
  .d0-win[data-device="mobile"] { justify-self: center; width: 391px; max-height: 812px; min-height: 560px; grid-template-rows: auto 1fr auto; border: 8px solid var(--d0-grey-900); border-radius: 44px; }
  .d0-win[data-device="mobile"] .d0-win__bar { display: none; }
  .d0-win[data-device="mobile"] .d0-phone__status { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; height: 40px; padding: 0 24px; background: #fff; color: var(--d0-grey-900); font-size: 14px; font-weight: 600; font-variant-numeric: tabular-nums; }
  .d0-phone__island { width: 96px; height: 26px; border-radius: 999px; background: var(--d0-grey-900); }
  .d0-phone__status svg { justify-self: end; }
  .d0-win[data-device="mobile"] .d0-phone__home { display: grid; place-items: center; height: 22px; background: #fff; }
  .d0-phone__home::before { content: ""; width: 120px; height: 5px; border-radius: 999px; background: var(--d0-grey-900); }
}
@media (max-width: 640px) { .d0-device { display: none; } }
```

```js
// 갤러리 스크립트의 forEach 안, select(0) 앞에 둔다
var win = g.querySelector('.d0-win'), devs = Array.prototype.slice.call(g.querySelectorAll('[data-device-set]'));
devs.forEach(function (b) {
  b.addEventListener('click', function () {
    win.dataset.device = b.dataset.deviceSet; // iframe은 그대로, 창 모양만 바뀐다
    devs.forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
  });
});
```

- `box-sizing: border-box` 전제다(391px = 베젤 8px × 2 + 화면 375px). 탭을 바꿔도 기기 선택은 유지한다.

## Screenshot spotlight (`figure.d0-shot`)

실제 화면 한 장에서 **봐야 할 곳 하나**를 밝히고 나머지는 흐리게 한다. 화면 내용이 주인공이라 프레임 크롬(타이틀바·신호등·베젤)은 두지 않는다.
page에서 화면 상자는 축 폭을 채우고 주석은 그 아래에 둔다. 주석을 화면 옆 열에 두려면 figure를 `.d0-wide` 바로 안에 두고 2열 분할선을 따른다(960px 이상, 화면 7 | 주석 5는 `data-split="7-5"`, [shell.md](shell.md) 넓은 구간 (b)·2열 (b)). 넓은 구간은 오른쪽만 프레임 끝까지 늘어나고 화면 열의 왼쪽은 축 시작선 그대로다.
구도는 Spotlight([composition.md](../composition.md)), deck에서는 `data-kind="screenshot"` 슬라이드가 이 블록을 쓴다.
**축 폭 화면과 넓은 구간 2열 격자는 page 전용이다.** 덱 슬라이드에서는 [slide-deck.md](slide-deck.md) screenshot 덱 격자(화면 열이 몸 높이를 채우고 주석·캡션은 오른쪽 열)가 이 격자를 덮는다. 화면·spot·dim·번호 규칙은 덱에서도 그대로다.

**해부 구조.**

- `figure.d0-shot` = 화면 상자 `div.d0-shot__screen` → 주석 `p.d0-shot__note` 1~3개 → `figcaption` 한 줄.
- 화면 상자 = 화면 하나(이미지 `img`, 정적 미니 마크업, 또는 화면 SVG) + `span.d0-shot__spot` 1~3개. 폭은 놓인 자리(축, 2열 열, `.d0-wide` 안 화면 열)를 채우고, 1px grey-200 테두리, `--d0-radius-card`, 흰 바탕, 그림자 없음.
- **spot.** 위치는 화면 상자 기준 백분율 인라인 변수 `style="--x:..%;--y:..%;--w:..%;--h:..%"`(왼쪽·위·폭·높이). 2px blue 테두리, `--d0-radius-sm`.
  왼쪽 위 모서리에 번호 배지(`b.d0-shot__num`, 24px blue-dark 원 + 흰 숫자 5.5:1). 위치 변수는 `--d0-*`가 아니다(토큰을 새로 만들지 않는다).
- **dim.** 주인공 spot 하나(`data-dim`)의 바깥을 반투명 막으로 덮는다. 기본은 grey 막(grey-900 14%, 12~16% 범위)이다. 대부분의 앱 화면은 바탕이 희어서 흰 막은 거의 보이지 않는다. 어둡거나 진한 화면(사진, 진한 바탕의 화면)만 흰 막(`data-dim="white"`, `#fff` 62%)을 고른다.
  막은 spot의 `outline`이 화면 상자 끝까지 번지는 단단한 경계다. 그라디언트·blur·두꺼운 그림자, 16%보다 짙은 막은 쓰지 않는다. 화면 상자의 `overflow: hidden`이 막을 자른다.
  **spot 안은 원래 화면 그대로 보인다.** 막은 spot 바깥(`outline`)에만 있고 spot에는 `background`를 칠하지 않는다(spot 안이 검게·회색으로 렌더되면 결함이다). 테두리와 번호만 화면 위에 얹는다.
- **spot이 둘 이상이면** dim은 하나만 건다(막이 서로를 덮는다). 나머지 spot은 테두리와 번호만 둔다. spot은 3개까지다.
- **주석.** `p.d0-shot__note`마다 spot과 같은 번호 배지 + 한 문장. 번호가 짝을 맺는다. 화면 아래에 쌓이고, `.d0-wide` 안 960px 이상에서만 화면 오른쪽 열에 놓인다.

**pins와의 관계.** 번호로 그림과 설명을 짝짓는 방식은 [diagram.md](diagram.md) (g) pins를 그대로 확장한다. 다른 점은 셋이다.
pins는 글자 없는 SVG 위의 점이고 d0-shot은 실제 화면 위의 **사각 영역**이다. d0-shot은 바깥을 **흐린다**. d0-shot은 정적이다(hover 연동이 필요하면 pins를 쓴다).

```html
<figure class="d0-shot">
  <div class="d0-shot__screen">
    <img src="…" alt="주문 관리 화면. 위쪽 바에 내보내기 버튼, 아래에 주문 표가 있어요." width="1280" height="800">
    <span class="d0-shot__spot" data-dim data-num="below" style="--x:74%;--y:3%;--w:22%;--h:11%" aria-hidden="true"><b class="d0-shot__num">1</b></span>
    <span class="d0-shot__spot" style="--x:4%;--y:20%;--w:40%;--h:10%" aria-hidden="true"><b class="d0-shot__num">2</b></span>
  </div>
  <p class="d0-shot__note"><b class="d0-shot__num">1</b>내보내기는 오른쪽 위 버튼 하나로 시작해요.</p>
  <p class="d0-shot__note"><b class="d0-shot__num">2</b>기간은 표 위 필터에서 먼저 골라요.</p>
  <figcaption>버튼 하나만 누르면 돼요. 필터는 고른 그대로 따라가요.</figcaption>
</figure>
```

```css
.d0-shot { display: grid; gap: 12px 28px; align-content: start; min-width: 0; margin: 0; }
.d0-shot__screen { position: relative; overflow: hidden; border: 1px solid var(--d0-grey-200); border-radius: var(--d0-radius-card); background: #fff; }
.d0-shot__screen > :is(img, svg) { display: block; width: 100%; height: auto; max-width: none; }
.d0-shot__spot {
  position: absolute; background: none; /* spot 안은 원래 화면 그대로 */ left: var(--x); top: var(--y); width: var(--w); height: var(--h);
  border: 2px solid var(--d0-blue); border-radius: var(--d0-radius-sm); pointer-events: none;
}
/* dim: spot 바깥을 단단한 경계의 반투명 막으로 덮는다(blur·그라디언트 없음). 화면 상자의 overflow가 자른다 */
.d0-shot__spot:not([data-dim]) { z-index: 1; } /* 막이 DOM 순서와 무관하게 다른 spot의 테두리·번호를 덮지 않게 */
.d0-shot__spot[data-dim] { outline: 200vmax solid color-mix(in srgb, var(--d0-grey-900) 14%, transparent); } /* 기본: grey 막 12~16% */
.d0-shot__spot[data-dim="white"] { outline-color: color-mix(in srgb, #fff 62%, transparent); } /* 어둡거나 진한 화면일 때만 */
.d0-shot__num {
  display: inline-grid; place-items: center; flex: none; width: 24px; height: 24px; border-radius: 999px;
  background: var(--d0-blue-dark); color: #fff; font-size: 13px; font-weight: 600; font-variant-numeric: tabular-nums; line-height: 1;
}
.d0-shot__spot .d0-shot__num { position: absolute; left: -12px; top: -12px; }
.d0-shot__spot[data-num="below"] .d0-shot__num { top: calc(100% + 6px); left: 0; } /* 화면 위 끝에 붙은 spot: 번호를 아래로 */
.d0-shot__note { display: flex; align-items: baseline; gap: 10px; margin: 0; color: var(--d0-grey-800); font-size: 15px; }
.d0-shot__note .d0-shot__num { transform: translateY(-1px); }
.d0-shot figcaption { color: var(--d0-grey-600); font-size: var(--d0-text-compact); }
@media (min-width: 960px) {
  /* page 전용: .d0-wide 바로 안에서만 화면 | 주석. 분할선은 .d0-cols와 같다(12열, 열 사이 48px). 남는 높이는 마지막 행이 받아 주석이 위로 붙는다. 덱은 slide-deck.md 덱 격자가 덮는다 */
  .d0-wide > .d0-shot { grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: 48px; grid-template-rows: repeat(3, auto) 1fr; align-items: start; }
  .d0-wide > .d0-shot .d0-shot__screen { grid-column: 1 / span 6; grid-row: 1 / span 4; }
  .d0-wide > .d0-shot .d0-shot__note { grid-column: 7 / span 6; }
  .d0-wide > .d0-shot[data-split="7-5"] .d0-shot__screen { grid-column: 1 / span 7; }
  .d0-wide > .d0-shot[data-split="7-5"] .d0-shot__note { grid-column: 8 / span 5; }
  .d0-wide > .d0-shot figcaption { grid-column: 1 / -1; }
}
```

- **위치 재기.** spot 변수 = 화면 이미지 픽셀 좌표 ÷ 이미지 크기 × 100%(예: 1280×800 화면의 버튼 (947, 24)~(1229, 112) → `--x:74%;--y:3%;--w:22%;--h:11%`). 상자가 화면과 같은 비율로 줄어 375px에서도 같은 곳을 가리킨다.
- **375px.** 화면은 폭 100%(약 343px)로 줄고 spot·번호는 같은 자리를 따라간다. 번호 배지는 24px 그대로다. spot 높이가 24px보다 작아지면 영역을 넓게 잡는다. 주석은 화면 아래로 내려간다. 가로 스크롤은 없다.
  번호는 spot 왼쪽 위 모서리 밖(`left: -12px; top: -12px`)에 붙는다. spot이 화면 위 끝에 붙어(`--y` 5% 미만) 번호가 잘리면 `data-num="below"`로 번호를 spot 아래에 두고,
  왼쪽 끝에 붙으면 spot을 안쪽으로 4% 이상 들인다. 375px에서 두 너비 모두 번호가 잘리지 않는지 본다.
- **접근성.** 화면은 `img`면 `alt`로 화면을 한 문장 설명하고, 미니 마크업이면 `aria-hidden` + 화면 SVG면 `role="img"`와 `<title>`. spot과 그 번호는 장식이라 `aria-hidden`이다.
  뜻은 주석 `p`가 텍스트로 순서대로 전한다(번호 숫자도 텍스트로 읽힌다). 위치를 색으로만 말하지 않는다: 주석에 "오른쪽 위"처럼 자리를 쓴다.
- **대비.** spot 테두리 blue는 spot 안쪽(막 없는 화면) 기준 흰 바탕 3.99로 3:1을 넘는다. 번호 배지는 막에 덮이지 않는다(다른 spot은 `z-index`로 막 위에 둔다). 번호는 blue-dark 위 흰 글자 5.5다. 막에 덮인 화면 글자는 맥락일 뿐이라 정보를 싣지 않는다(정보는 주석에 쓴다).
- **색 비율.** 번호 배지와 spot 테두리만 blue 계열이다. 막은 색 비율에 세지 않는다(옅은 면).
- 실제 화면이 없으면 [diagram.md](diagram.md) (d) 와이어프레임 SVG를 화면 자리에 넣는다. 화면 크롬(창 타이틀바, 폰 베젤)이 필요하면 갤러리 기기 프레임을 쓰고 spotlight와 섞지 않는다.

## 금지

- 눌러도 반응하지 않는 가짜 프로토타입, 프레임 밖으로 나오는 모달·막(`showModal()` 포함).
- 갤러리 창을 고정 높이로 두기, CSS 스크롤 스냅(`scroll-snap-type`·`scroll-snap-align`, 특히 `scroll-snap-stop: always`)으로 갤러리를 붙잡기, 스크롤 도중(입력 160ms 안·`scrollend` 전)에 맞추기, 갤러리 뒤에 다른 섹션 잇기, 신호등 점을 의미색(상태 표시)으로 쓰기.
- 640px 이하 화면에 폰 베젤 겹치기(가로 스크롤), 기기를 바꿀 때 iframe을 다른 부모로 옮기기(다시 로드), iframe 폰 화면 폭을 375px 아닌 값으로 두기(정적 그림의 축소 프레임은 예외).
- 고스트 카드에 가짜 문장 채우기(자리만 잡는다), 시안마다 다른 높이·데이터.
- `iframe src`로 다른 파일·URL 불러오기(artifact에서 끊긴다), `sandbox` 없는 iframe.
- 실제 파일 다운로드·외부 전송. 결과는 토스트로만 알린다. 프레임 안 `main` 요소, `div`에 `role="dialog"`(네이티브 `dialog` 우선).
- d0-shot에 그라디언트·blur·두꺼운 그림자·짙은 막(grey 16%·흰 62% 초과), spot 안에 칠한 배경(화면이 가려진다), 축 안에서 화면 옆에 주석 열 두기(옆 열은 `.d0-wide` 안에서만), 진한 화면에 grey 막(대비가 사라진다), dim 둘 이상, spot 4개 이상, 번호 없는 spot, 주석 없이 spot만 두기, 화면 크롬(타이틀바·베젤) 두르기, 위치를 px로 고정해 375px에서 어긋나기.
