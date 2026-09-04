# 모션과 배경

움직임은 여섯 가지뿐이다. 등장 · 스택 · 리빌 · 마퀴 · 글로우 · 전환.
그 밖의 효과를 추가하지 않는다.

## 이 시스템의 모션 규칙

- **이징은 하나다.** `cubic-bezier(0.22, 1, 0.36, 1)`. 앞이 빠르고 끝이 길어
  요소가 도착한 자리에 얹히는 느낌을 준다. 바운스·스프링을 섞지 않는다.
- **지속 시간은 두 단.** 위치가 바뀌면 320ms(`--ds-dur-enter`), 색만 바뀌면
  160ms(`--ds-dur-state`).
- **움직이는 속성은 `transform`과 `opacity`뿐.** `width`·`height`·`top`을
  애니메이션하면 매 프레임 레이아웃을 다시 계산한다.
- **그림자로 깊이를 만들지 않는다.** 이 디자인에 `box-shadow`는 0이고,
  깊이는 면의 겹침과 글로우가 만든다.
- **hover에서 확대·이동하지 않는다.** 색만 바꾼다.

이징을 하나로 묶는 이유는 취향이 아니다. 화면마다 다른 이징을 쓰면 같은 제품의
움직임이 서로 다른 물리 법칙을 따르는 것으로 읽히고, 그 어긋남은 이유를 짚기
어려운 채로 남는다.

## 1. 등장 (fade + rise)

스크롤로 뷰포트에 들어올 때 한 번. 요소당 1회, 되돌리지 않는다.

```css
.ds-appear {
  opacity: 0;
  transform: translateY(var(--ds-rise));      /* 16px */
  transition: opacity var(--ds-dur-enter) var(--ds-ease),
              transform var(--ds-dur-enter) var(--ds-ease);
}
.ds-appear[data-visible="true"] { opacity: 1; transform: none; }
```

`IntersectionObserver`로 `data-visible`을 켠다. 같은 섹션 안에서는 60~80ms 간격
스태거까지만. 그 이상 늘리면 화면이 조립되는 과정을 보게 되어 느리다고 느껴진다.

**되돌리지 않는 이유**: 스크롤을 올렸을 때 요소가 다시 사라지면 읽던 자리를
잃는다. 등장은 연출이 아니라 도착 신호다.

## 2. 스택 카드

`position: sticky; top: var(--ds-sticky-top)`. 다음 카드가 이전 카드를 덮으며
올라온다. 카드 배경이 불투명 검정이라 겹침이 자연스럽게 가려진다.

- 카드는 3~4장까지. 그 이상은 스크롤이 길어져 이탈한다.
- 축소·회전을 얹지 않는다. 겹침만으로 충분하다.
- `top`은 내비 높이 + 24다. 카드가 내비에 닿으면 둘이 한 덩어리로 보인다.

## 3. 단어 단위 스크롤 리빌

큰 문장(48px/400/자간 -0.03em)이 `--ds-ink-mute`에서 `--ds-ink`로 바뀐다.
스크롤에 연동해 단어 단위로 앞에서부터 밝아진다.

**이 문장은 단독 섹션이 아니다.** 문장 아래 `--ds-space-6`(64px) 간격으로 대형
제품 비주얼이 붙는다. 문장은 그 비주얼의 캡션 역할을 하고, 히어로에서 문장,
비주얼까지가 한 흐름으로 읽힌다. 문장만 따로 떼어 빈 화면에 놓으면 페이지가
끊겨 보인다. 이것이 이 블록에서 가장 자주 나오는 실수다.

```text
다크 히어로
  ↓ 세로 리듬 (128px)
리빌 문장 (2줄)
  ↓ 64px
대형 비주얼 (제품 목업)
```

### 진행률은 문장의 뷰포트 위치로 잡는다

sticky로 고정하지 않는다. 일반 흐름 그대로 두고, 문장이 화면을 지나가는 동안
채운다. 기준점은 하나다 — **문장이 화면 정중앙에 왔을 때 절반이 채워진다.**

```js
const rv = document.querySelector(".ds-reveal");
const words = [...rv.querySelectorAll("span")];
const START = 0.85;   // 화면 85% 지점에서 시작
const SPAN = 0.75;    // 뷰포트 높이의 0.75배 동안 진행
const CAP = 0.8;      // 끝까지 채우지 않는다
const tick = () => {
  const top = rv.getBoundingClientRect().top;
  const vh = innerHeight;
  const p = Math.max(0, Math.min(1, (vh * START - top) / (vh * SPAN)));
  const lit = p * CAP * words.length;
  words.forEach((w, i) => (w.dataset.lit = i < lit));
};
addEventListener("scroll", tick, { passive: true });
addEventListener("resize", tick);
tick();
```

- **완주시키지 않는다.** 마지막 다섯째쯤은 회색으로 남긴다. 다 채우면 그냥 흰
  문장이 되어 대비가 사라지고, 무엇이 진행 중이었는지도 안 보인다.
- **진행 구간은 뷰포트 높이의 0.75배.** 요소 자신의 높이를 분모로 쓰면 두 줄짜리
  문장에서 구간이 100px대로 줄어 순식간에 끝난다.
- 문장은 두 줄 이내. 페이지당 1~2회.
- `prefers-reduced-motion: reduce`면 처음부터 전부 `--ds-ink`로 둔다.

## 4. 로고 마퀴

콘텐츠를 **두 벌 복제**한 트랙을 `translateX(-50%)`까지 이동시키고 되감는다.
폭을 픽셀로 박으면 항목이 하나 늘 때마다 이음매가 튄다.

```css
@keyframes ds-marquee { to { transform: translateX(-50%) } }
.ds-strip-track { animation: ds-marquee 48s linear infinite; }
.ds-strip-track[data-dir="reverse"] { animation-direction: reverse; }
```

- 이징은 `linear`다. 마퀴는 도착하는 움직임이 아니라 흐르는 움직임이라
  가속·감속이 붙으면 맥박처럼 읽힌다. 여섯 모션 중 유일한 예외다.
- 한 바퀴 45~60초. 두 줄을 쓸 때는 반대 방향으로 흘린다.
- hover 정지를 붙이지 않는다. 읽으라고 두는 자리가 아니다.

## 5. 배경 글로우

히어로 배경의 빛은 **블러 레이어**로 만든다. CSS 그라디언트로 흉내 내지 않는다.

**면적 제약이 제일 중요하다.** 글로우는 배경이 아니라 **한쪽 구석의 빛**이다.
화면 대부분은 검정으로 남아야 한다.

- 히어로 면적의 **1/3 이하**만 덮는다. 절반을 넘으면 포인트색 배경이 되어 버린다.
- 위치는 한 곳. 대칭으로 두 개 놓지 않는다.
- 가장 밝은 지점도 화면 밖으로 반쯤 걸치게 둬서 원의 윤곽이 보이지 않게 한다.
- 포인트 계열 한 색. 무지개 그라디언트를 만들지 않는다.

```css
.ds-hero { position: relative; overflow: hidden; background: var(--ds-void); }
.ds-glow {
  position: absolute;
  right: -18%; top: -35%;         /* 반쯤 잘라 윤곽을 없앤다 */
  width: 720px; aspect-ratio: 1;
  border-radius: 50%;
  background: var(--ds-accent-glow);
  filter: blur(180px);
  opacity: 0.4;                    /* 0.5를 넘기지 않는다 */
  pointer-events: none;
}
```

**정적으로 두지 않는다.** 멈춘 글로우는 배경 이미지로 읽히고, 그 순간 히어로가
죽은 화면이 된다. 레이어를 아주 느리게 표류시킨다.

```css
@keyframes ds-drift {
  from { transform: translate3d(0, 0, 0) scale(1) }
  to   { transform: translate3d(-9%, 7%, 0) scale(1.14) }
}
.ds-glow { animation: ds-drift 26s var(--ds-ease) infinite alternate; will-change: transform }
.ds-glow[data-layer="2"] { animation: ds-drift 34s var(--ds-ease) infinite alternate-reverse }
```

- 주기 **20~40초**. 그보다 빠르면 배경이 아니라 애니메이션으로 읽힌다.
- 레이어마다 주기와 방향을 어긋나게 둔다. 같이 움직이면 패턴이 드러난다.
- 두 번째 레이어는 더 작고(≤60%) 더 흐리게 둔다.
- 움직이는 것은 `transform`뿐. `opacity`·`filter`를 함께 애니메이션하면
  매 프레임 블러를 다시 계산해 렉이 생긴다.
- 콘텐츠는 `position: relative; z-index: 1`로 글로우 위에 올린다.

영상을 쓴다면 `autoplay muted playsinline preload="metadata"` + poster가 필수다.

## 6. 페이지 전환 — 한 장의 커튼

페이지를 옮길 때 검정 면 한 장이 **아래에서 위로 올라와** 화면을 덮는다.
다 덮이면 새 페이지가 그 아래에 있다.

```html
<div class="ds-curtain" aria-hidden="true"></div>
```

```css
.ds-curtain {
  position: fixed; inset: 0; z-index: 15;   /* 내비(20)보다 아래 */
  background: var(--ds-void);
  transform: scaleY(0); transform-origin: bottom center;
  pointer-events: none; visibility: hidden;
}
.ds-curtain[data-on="true"] {
  visibility: visible;
  animation: ds-curtain 200ms var(--ds-ease) forwards;
}
@keyframes ds-curtain { to { transform: scaleY(1) } }
```

- **한 장이다.** 여러 조각으로 쪼개면 블라인드가 되고, 조각의 개수와 순서가
  그 자체로 눈길을 끌어 이동이라는 목적을 가린다.
- **불투명도를 함께 움직이지 않는다.** 면은 처음부터 불투명하고 크기만 바뀐다.
  둘을 같이 움직이면 반투명한 중간 상태에서 두 페이지가 겹쳐 보인다.
- **내비는 덮지 않는다.** 커튼의 `z-index`를 내비보다 낮게 둬서 헤더가 자리를
  지키게 한다. 화면이 통째로 사라지지 않아 위치 감각이 유지된다.
- 지속 시간 **200ms**. 250ms를 넘기면 이동이 느리게 느껴진다.

**커튼 색이 다음 페이지의 첫 화면과 같아야 한다.** 모든 페이지가 다크 히어로로
시작하므로 검정 커튼이 그대로 새 페이지의 첫 화면으로 이어지고, 그래서 커튼을
걷는 동작이 아예 필요 없다. 덮은 뒤 그냥 사라지면 된다. 도착 페이지 상단이
밝다면 커튼을 160ms 페이드아웃시켜 이음매를 지운다.

## 접근성

```css
@media (prefers-reduced-motion: reduce) {
  .ds-appear { opacity: 1; transform: none; transition: none; }
  .ds-strip-track, .ds-glow { animation: none; }
  .ds-curtain { display: none; }        /* 전환은 즉시 교체 */
  .ds-reveal span { color: var(--ds-ink); }
  video { display: none; }              /* poster 이미지로 대체 */
}
```

`prefers-reduced-motion` 분기는 선택이 아니다. 리빌은 특히 그렇다 — 모션이
꺼진 환경에서 대기 상태 회색(`--ds-ink-mute`, 2.69:1)이 그대로 남으면 그 문장은
읽을 수 없는 텍스트가 된다.
