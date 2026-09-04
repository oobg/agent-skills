# 모션과 배경

이 디자인의 움직임은 여섯 가지뿐이다. 그 밖의 효과를 추가하지 않는다.

## 실측 사실

- CSS `transition`은 문서 전체에 **한 줄**: `color .4s cubic-bezier(.44,0,.56,1)`.
- `box-shadow` **0회**, `backdrop-filter` **0회**, CSS 그라디언트 **0회**.
- `filter: blur(10px)` 31회 — 글로우는 전부 블러 레이어로 만든다.
- `@keyframes` 0개. 반복 모션은 JS가 transform으로 돌린다.

이징은 `cubic-bezier(0.44, 0, 0.56, 1)` 하나로 통일한다. 대칭형 ease-in-out이라
등장과 퇴장이 같은 속도로 느껴진다. 바운스·스프링을 섞지 않는다.

## 1. 등장 (fade + rise)

스크롤로 뷰포트에 들어올 때 한 번. 요소당 1회, 되돌리지 않는다.

```css
.ds-appear {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity var(--ds-dur) var(--ds-ease),
              transform var(--ds-dur) var(--ds-ease);
}
.ds-appear[data-visible="true"] { opacity: 1; transform: none; }
```

`IntersectionObserver`로 `data-visible`을 켠다. 같은 섹션 안에서는 60~80ms 간격
스태거까지만. 그 이상 늘리면 느리다고 느껴진다.

## 2. 스택 카드

`position: sticky; top: 40px`. 다음 카드가 이전 카드를 덮으며 올라온다.
카드 배경이 불투명 검정이라 겹침이 자연스럽게 가려진다.

- 카드는 3~4장까지. 그 이상은 스크롤이 길어져 이탈한다.
- 축소·회전을 얹지 않는다. 겹침만으로 충분하다.

## 3. 단어 단위 스크롤 리빌

큰 문장(48px/400/자간 -0.04em)이 `--ds-text-dim`(#666)에서 흰색으로 바뀐다.
스크롤에 연동해 단어 단위로 앞에서부터 밝아진다.

**이 문장은 단독 섹션이 아니다.** 실측 원본에서 문장 바로 아래 **64px** 간격으로
1224×1000 제품 비주얼이 붙는다. 문장은 그 비주얼의 캡션 역할을 하고, 히어로에서
문장, 비주얼까지가 한 흐름으로 읽힌다. 문장만 따로 떼어 빈 화면에 놓으면
페이지가 끊겨 보인다. 이것이 이 블록에서 가장 자주 나오는 실수다.

```text
다크 히어로
  ↓ 120px
리빌 문장 (2줄)
  ↓ 64px
대형 비주얼 (제품 목업)
```

### 진행률은 문장의 뷰포트 위치로 잡는다

sticky로 고정하지 않는다. 일반 흐름 그대로 두고, 문장이 화면을 지나가는 동안
채운다. 실측값(뷰포트 900px 기준)은 이렇다.

| 문장 상단의 뷰포트 y | 채움 |
| --- | --- |
| 750 (83%) | 0% |
| 600 (67%) | 15% |
| 450 (50%) | **46%** |
| 300 (33%) | 60% |
| 150 (17%) | 77% |

```js
const rv = document.querySelector(".ds-reveal");
const words = [...rv.querySelectorAll("span")];
const tick = () => {
  const top = rv.getBoundingClientRect().top;
  const vh = innerHeight;
  // 화면 83% 지점에서 시작해 8% 지점에서 최대
  const p = Math.max(0, Math.min(1, (vh * 0.83 - top) / (vh * 0.75)));
  const lit = p * 0.8 * words.length;          // 끝까지 채우지 않는다
  words.forEach((w, i) => w.dataset.lit = i < lit);
};
addEventListener("scroll", tick, {passive: true});
addEventListener("resize", tick);
tick();
```

- **완주시키지 않는다.** 실측 원본은 52단어 중 42개(81%)에서 멈추고, 마지막 줄은
  회색으로 남는다. 다 채우면 그냥 흰 문장이 되어 대비가 사라진다.
- 문장이 화면 **정중앙에 왔을 때 절반**이 기준점이다. 이보다 빠르면 채워지는
  과정을 볼 수 없고, 느리면 지나가 버린 뒤에 채워진다.
- 진행 구간은 뷰포트 높이의 **0.75배**. 요소 자신의 높이를 분모로 쓰면 두 줄짜리
  문장에서 구간이 100px대로 줄어 순식간에 끝난다.
- 문장은 두 줄 이내. 페이지당 1~2회.
- `prefers-reduced-motion: reduce`면 처음부터 전부 흰색으로 둔다.

## 4. 로고 마퀴

2560px 트랙을 `transform: translateX`로 무한 이동. 두 줄을 반대 방향으로 흘린다.
hover 정지 없음, 속도는 한 바퀴 40~60초 수준으로 느리게.

## 5. 배경 글로우

히어로 배경은 **자동재생 무음 루프 mp4** + PNG 포스터다. 빛이 아주 느리게
움직인다. CSS 그라디언트로 흉내 내지 않는다. 직접 만든다면:

**면적 제약이 제일 중요하다.** 히어로 포스터를 픽셀 집계하면 지배색이
`#050505`이고 근검정이 압도적이다. 글로우는 배경이 아니라 **한쪽 구석의 빛**이다.

- 히어로 면적의 **1/3 이하**만 덮는다. 절반을 넘으면 보라 배경이 되어 버린다.
- 위치는 우측 상단 한 곳. 대칭으로 두 개 놓지 않는다.
- 가장 밝은 지점도 화면 밖으로 반쯤 걸치게 둬서 원의 윤곽이 보이지 않게 한다.
- 보라 계열 한 색. 무지개 그라디언트를 만들지 않는다.

```css
.ds-hero { position: relative; overflow: hidden; background: var(--ds-bg); }
.ds-glow {
  position: absolute;
  right: -18%; top: -35%;        /* 반쯤 잘라 윤곽을 없앤다 */
  width: 780px; aspect-ratio: 1;
  border-radius: 50%;
  background: var(--ds-accent);
  filter: blur(180px);
  opacity: 0.42;                  /* 0.5를 넘기지 않는다 */
  pointer-events: none;
}
```

두 번째 레이어를 겹칠 때는 더 작고(≤60%) 더 흐리게, 색만 살짝 밝은 보라로.
콘텐츠는 `position: relative; z-index: 1`로 글로우 위에 올린다.

**정적으로 두지 않는다.** 원본은 루프 영상이라 빛이 계속 움직인다. CSS로 대체할
때는 레이어를 아주 느리게 표류시킨다.

```css
@keyframes ds-drift-a{
  from{transform:translate3d(0,0,0) scale(1)}
  to  {transform:translate3d(-9%,7%,0) scale(1.14)}
}
.ds-glow{animation:ds-drift-a 26s var(--ds-ease) infinite alternate;will-change:transform}
.ds-glow.b{animation:ds-drift-a 34s var(--ds-ease) infinite alternate-reverse}
```

- 주기 **20~40초**. 그보다 빠르면 배경이 아니라 애니메이션으로 읽힌다.
- 레이어마다 주기와 방향을 어긋나게 둔다. 같이 움직이면 패턴이 드러난다.
- 움직이는 것은 `transform`뿐. `opacity`·`filter`를 함께 애니메이션하면
  매 프레임 블러를 다시 계산해 렉이 생긴다.
- 이동 폭은 레이어 크기의 10% 안팎. 크게 움직이면 면적 상한이 깨진다.
- CTA 배너 같은 작은 면의 글로우도 같은 방식으로 움직인다.

비디오를 쓰면 `autoplay muted playsinline preload="metadata"` + poster 필수.

## 6. 페이지 전환 — 세로 슬랫 커튼

페이지를 옮길 때 화면을 **다섯 개의 세로 슬랫**으로 나눠 검정으로 덮는다.
각 슬랫 안에서 왼쪽에서 오른쪽으로 차오르고, 다 덮이면 새 페이지가 그 아래에 있다.

실측 진행값(슬랫 폭 240px 기준): 59 → 151 → 206 → 235 → 240px.
같은 프레임에서 덮인 면의 색이 `#c1c1c1` → `#5f5f5f` → `#252525` → `#060606`으로
짙어진다. 폭 비율과 불투명도가 **같은 값 하나로 함께 움직인다**는 뜻이다.
폭 63%면 불투명도도 63%다.

```html
<div class="ds-curtain" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
```

```css
.ds-curtain{
  position:fixed; inset:0; z-index:15;      /* 내비(20)보다 아래 */
  display:grid; grid-template-columns:repeat(5,1fr);
  pointer-events:none; visibility:hidden;
}
.ds-curtain[data-on="true"]{visibility:visible}
.ds-curtain i{
  display:block; background:var(--ds-bg);
  transform:scaleX(0); transform-origin:left center; opacity:0;
}
.ds-curtain[data-on="true"] i{animation:ds-curtain 220ms var(--ds-ease) forwards}
@keyframes ds-curtain{
  from{transform:scaleX(0); opacity:0}
  to  {transform:scaleX(1); opacity:1}
}
```

- **슬랫은 5개.** 더 늘리면 블라인드가 되고, 줄이면 그냥 와이프가 된다.
- **내비는 덮지 않는다.** 커튼의 `z-index`를 내비보다 낮게 둬서 헤더가 자리를
  지키게 한다. 화면이 통째로 사라지지 않아 위치 감각이 유지된다.
- 슬랫에 지연(stagger)을 주지 않는다. 다섯 개가 동시에 움직인다.
- 지속 시간은 **200~250ms**. 캡처 지연 때문에 실측은 ±50ms 오차가 있다.
  300ms를 넘기면 이동이 느리게 느껴진다.
- `transform`과 `opacity`만 움직인다. `width`를 애니메이션하면 매 프레임
  레이아웃을 다시 계산한다.

**커튼 색이 다음 페이지의 히어로 색과 같아야 한다.** 실측 사이트는 모든 페이지가
다크 히어로로 시작해서, 검정 커튼이 그대로 새 페이지의 첫 화면으로 이어진다.
그래서 커튼을 걷는 동작이 아예 필요 없다. 덮은 뒤 그냥 사라지면 된다.
도착 페이지 상단이 밝다면 커튼을 200ms 정도로 페이드아웃시켜 이음매를 지운다.

## 접근성

```css
@media (prefers-reduced-motion: reduce) {
  .ds-appear { opacity: 1; transform: none; transition: none; }
  .ds-logo-track, .ds-glow { animation: none; }
  .ds-curtain { display: none; }   /* 전환은 즉시 교체 */
  .ds-reveal span { color: var(--ds-text); }
  video { display: none; }  /* poster 이미지로 대체 */
}
```
