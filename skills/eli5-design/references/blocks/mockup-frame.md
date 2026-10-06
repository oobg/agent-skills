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
- A/B는 같은 데이터·같은 높이. 1100px 이상 2열, 그 아래 세로. 완성 예는 [preview-compare.html](../examples/preview-compare.html) ③.

## 스니펫

```html
<div class="d0-demos">
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
</div>
```

```css
.d0-demos { display: grid; gap: 28px; }
@media (min-width: 1100px) { .d0-demos { grid-template-columns: 1fr 1fr; } }
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

## 금지

- 눌러도 반응하지 않는 가짜 프로토타입, 프레임 밖으로 나오는 모달·막(`showModal()` 포함).
- 고스트 카드에 가짜 문장 채우기(자리만 잡는다), 시안마다 다른 높이·데이터.
- `iframe src`로 다른 파일·URL 불러오기(artifact에서 끊긴다), `sandbox` 없는 iframe.
- 실제 파일 다운로드·외부 전송. 결과는 토스트로만 알린다. 프레임 안 `main` 요소, `div`에 `role="dialog"`(네이티브 `dialog` 우선).
