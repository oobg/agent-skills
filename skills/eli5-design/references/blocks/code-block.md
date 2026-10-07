# code-block — 붙여 넣을 코드

## 해부 구조

- `figure.d0-code` 하나 = 상단 바 `figcaption.d0-code__bar`(왼쪽 라벨 + 상태 문구, 오른쪽 복사 버튼) → `pre` > `code`.
- 라벨은 코드를 넣을 곳 한 단어(`터미널`, `설정 파일`, `대화창`)다. 언어 이름보다 독자가 붙여 넣을 장소를 쓴다.
- 코드는 여러 줄을 허용하고 자동 줄바꿈하지 않는다. 긴 줄은 `pre` 안에서만 가로로 스크롤한다(`overflow-x: auto`).
  스크롤 상자는 키보드로 닿도록 `tabindex="0"` + `role="group"` + `aria-label`을 둔다. 페이지 가로 스크롤은 금지다.
- 프롬프트 기호(`$`, `>`)는 `span.d0-code__prompt aria-hidden="true"`로 감싸 복사·선택 대상에서 뺀다(`user-select: none`, JS가 복사 전 제거).
- 색: 코드 면 grey-900 + 흰 글자(16.56), 바 grey-800 + 라벨 grey-300(7.38), 버튼 흰 글자(11.67) + 1px grey-500 테두리(3.65).
  shell.md 기본 포커스 링(blue-dark)은 grey-800 위 2.12라 버튼은 흰 링(11.67)을 따로 둔다. hover 면은 grey-700(흰 글자 7.65).
- 크기: 코드 13px(`--d0-text-compact`), 행간 `--d0-leading-body`, 패딩 14px 16px, radius `--d0-radius-control`. 라벨 12px(`--d0-meta`). 버튼 높이 32px.
- **글꼴 예외.** 코드만 시스템 모노 스택(`ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`)을 쓴다. tokens.css에 모노 토큰이 없어서다.
  모노 글자는 `scripts/subset_font.py` 서브셋 대상이 아니다(Pretendard 서브셋은 그대로 만든다).
- **동작.** 복사 버튼은 `hidden`으로 시작하고 JS가 연다(JS 없으면 버튼 없이 코드만 보인다).
  누르면 `navigator.clipboard.writeText`로 복사하고, 성공하면 버튼 글자가 2초 동안 `복사했어요`로 바뀌며 상태 문구(`output`, `aria-live="polite"`)가 같은 말을 읽어 준다.
  샌드박스 iframe은 `writeText`를 부르면 권한 정책 위반이 콘솔에 남으므로, 호출 전에 `permissionsPolicy`·`featurePolicy`의 `allowsFeature('clipboard-write')`가 `false`면 바로 폴백으로 간다.
  Mac 판별은 `navigator.userAgentData.platform`(`macOS`)을 먼저 보고 대소문자를 가리지 않는다.
  클립보드를 못 쓰면(파일로 연 페이지, artifact 샌드박스 등) 코드 전체를 선택하고 `선택했어요. ⌘C로 복사하세요`(Windows·Linux는 `Ctrl+C`)를 상태 문구로 보여 준다.

## 언제 쓰나 / 변형

- 독자가 그대로 붙여 넣을 명령·설정·문구가 있을 때. guide 따라하기에서는 checklist 행의 `<details>` 안에 둔다([guide.md](../patterns/guide.md)).
- 코드 블록은 **그림 블록이 아니다.** 첫 화면 섹션의 그림 게이트에 세지 않는다. 혼자 섹션을 채우지 않고 checklist·accordion 행 안이나 그림 옆 설명 칸에 붙인다.
- 줄 길이 규칙(축 한 줄 안에 끝나는 글)의 예외다(코드 줄). 대신 한 블록은 10줄 이내로 쓰고, 더 길면 파일로 받게 하고 파일 이름만 보인다.
- 붙여 넣을 값 중 독자가 바꿔야 하는 부분은 `<자리표시>`로 쓰고 블록 아래 결과 한 줄에서 무엇으로 바꾸는지 말한다.

## 스니펫

```html
<figure class="d0-code">
  <figcaption class="d0-code__bar">
    <span class="d0-code__label">터미널</span>
    <output class="d0-code__status" aria-live="polite"></output>
    <button type="button" class="d0-code__copy" hidden>복사</button>
  </figcaption>
  <pre tabindex="0" role="group" aria-label="터미널 명령"><code><span class="d0-code__prompt" aria-hidden="true">$ </span>npx order-export init --team "팀 A"
<span class="d0-code__prompt" aria-hidden="true">$ </span>npx order-export schedule --at 09:00</code></pre>
</figure>
```

```css
.d0-code { margin: 0; min-width: 0; max-width: 100%; overflow: hidden; border-radius: var(--d0-radius-control); background: var(--d0-grey-900); }
.d0-code__bar { display: flex; align-items: center; gap: 8px; min-height: 44px; padding: 6px 8px 6px 16px; background: var(--d0-grey-800); }
.d0-code__label { flex: none; color: var(--d0-grey-300); font-size: var(--d0-meta); font-weight: 600; }
.d0-code__status { flex: 1; min-width: 0; color: var(--d0-grey-300); font-size: var(--d0-meta); text-align: right; }
.d0-code__copy {
  display: inline-flex; align-items: center; flex: none; height: 32px; padding: 0 12px;
  border: 1px solid var(--d0-grey-500); border-radius: var(--d0-radius-sm);
  background: transparent; color: #fff; font: inherit; font-size: var(--d0-text-compact); font-weight: 600; cursor: pointer;
  transition: background-color var(--d0-dur-fast) var(--d0-ease);
}
.d0-code__copy[hidden] { display: none; }
.d0-code__copy:hover { background: var(--d0-grey-700); }
.d0-code__copy:focus-visible { outline: 2px solid #fff; outline-offset: 2px; }
.d0-code pre { margin: 0; padding: 14px 16px; overflow-x: auto; white-space: pre; }
.d0-code pre:focus-visible { outline: 2px solid #fff; outline-offset: -4px; }
.d0-code code {
  color: #fff; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: var(--d0-text-compact); line-height: var(--d0-leading-body); letter-spacing: 0;
}
.d0-code__prompt { color: var(--d0-grey-300); user-select: none; -webkit-user-select: none; }
@media (prefers-reduced-motion: reduce) { .d0-code__copy { transition: none; } }
```

```js
document.querySelectorAll('.d0-code').forEach(function (block) {
  var btn = block.querySelector('.d0-code__copy');
  var status = block.querySelector('.d0-code__status');
  var code = block.querySelector('code');
  var label = btn.textContent;
  var timer;
  var p = (navigator.userAgentData && navigator.userAgentData.platform) || navigator.platform || '';
  var mac = /mac|iphone|ipad/i.test(p);
  var policy = document.permissionsPolicy || document.featurePolicy;
  var blocked = !!(policy && policy.allowsFeature && policy.allowsFeature('clipboard-write') === false);
  btn.hidden = false;
  function text() {
    var copy = code.cloneNode(true);
    copy.querySelectorAll('[aria-hidden="true"]').forEach(function (el) { el.remove(); });
    return copy.textContent;
  }
  function done() {
    clearTimeout(timer);
    btn.textContent = '복사했어요';
    status.textContent = '복사했어요';
    timer = setTimeout(function () { btn.textContent = label; status.textContent = ''; }, 2000);
  }
  function fallback() {
    var range = document.createRange();
    range.selectNodeContents(code);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
    clearTimeout(timer);
    btn.textContent = label;
    status.textContent = '선택했어요. ' + (mac ? '⌘C' : 'Ctrl+C') + '로 복사하세요';
  }
  btn.addEventListener('click', function () {
    if (blocked || !navigator.clipboard || !navigator.clipboard.writeText) { fallback(); return; }
    navigator.clipboard.writeText(text()).then(done, fallback);
  });
});
```

## 금지

- 코드 블록을 그림 대신 섹션의 주인공으로 두기, 코드만 담은 섹션.
- 코드 면에 다른 색(구문 강조 무지개, blue 면), 줄 번호, 창 점 세 개 같은 장식.
- 자동 줄바꿈으로 명령을 둘로 쪼개 보이기, 페이지 전체 가로 스크롤.
- 복사 대상에 `$`·프롬프트 기호 포함하기, JS 없이도 보이는 복사 버튼, 실패해도 `복사했어요`를 띄우기.
- 버튼 테두리 grey-600(grey-800 위 2.33)이나 blue-dark 포커스 링(2.12)처럼 어두운 바 위에서 안 보이는 값.
- 실제 토큰·비밀번호·사내 주소가 든 예시. 예시 값은 합성 값만 쓴다.
