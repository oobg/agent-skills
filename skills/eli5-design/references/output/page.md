# page — 한 장짜리 시각 문서 출력

출력 형식은 두 가지다. 기본은 한 장짜리 페이지(`page`)이고, 이 파일은 그 출력 규칙이다. 한 장씩 넘기는 발표 덱은 [deck.md](deck.md)다.
패턴과 공용 블록이 **무엇을 말할지** 정하고, 출력 형식은 **어떻게 보여 줄지** 정한다. page와 deck은 Pattern·Block을 공유할 수 있지만, 정보 구조·밀도·구도는 출력 형식에 맞게 다시 구성한다.

골격·타이포·본문 축·색의 마크업과 CSS 정본은 [shell](../blocks/shell.md)이다. 구도·강조 3단계·밀도 리듬은 [composition](../composition.md)이 정본이다. 이 파일은 page의 파일 형식과 이름표를 정한다.

## 언제 page인가

- 혼자 읽어도 이해되는 시각 문서다. 구조 + 맥락 + 근거 + 조건 + 해석을 담는다.
- 혼자 읽는 한 장짜리 문서면 page다. 신호가 없으면 page다. 발표·화면 공유 신호가 있으면 [deck.md](deck.md)를 연다.
- page는 [explanation](../blocks/explanation.md)·[evidence](../blocks/evidence.md)로 맥락까지 담는다. 패턴 파일과 함께 연다. 말투는 해요체다(SKILL.md 말투).

## 루트 마크업

```html
<main class="d0-page" data-recipe="postmortem">
  <section class="d0-section" data-pattern="incident" aria-labelledby="sec-a">…</section>
</main>
```

- 섹션마다 `data-pattern="compare|flow|preview|report|guide|timeline|incident|faq"`를 단다(`main > section`).
  패턴 변형은 같은 섹션의 `data-variant`로 단다. 레시피를 썼으면 `<main class="d0-page" data-recipe="...">`(선택). 패턴이 없는 섹션은 `data-pattern`을 생략한다.
- 이름표일 뿐 스타일은 바꾸지 않는다. 변형 이름표 목록과 예전 이름표 옮기기는 [patterns.md](../patterns.md) 이름표 절이 정본이다.

## 파일 형식

- **단일 self-contained HTML 파일**을 만든다. 호스트에 artifact 발행 기능이 있으면 발행한다.
- **폰트.** 결과물 HTML을 넘기는 모든 경우(파일 전달, artifact 발행)의 기본은 `scripts/subset_font.py`로 페이지 글자만 담은 Pretendard 서브셋 `@font-face`를 인라인해 외부 요청을 0건으로 만드는 것이다. 발행 여부와 무관하다.
  도구를 못 쓸 때(파이썬·원본 폰트 없음)만 Pretendard Variable jsDelivr `<link>` 하나를 두고, 외부 요청이 1건 남으며 artifact에서는 링크가 막혀 시스템 폰트로 대체된다고 사용자에게 알린다.
  그 밖의 외부 리소스는 없다. CSS·SVG·JS는 인라인이다.
- 인라인 `@font-face`는 메인 `<style>` **앞**의 별도 `<style>`이다. "tokens.css는 메인 `<style>` 맨 앞" 규칙([day0.md](../day0.md))과 충돌하지 않는다.
- **넘기기 직전 폰트 인라인.** 결과물 HTML을 넘기면(파일·artifact 모두) 글자를 다 고친 뒤 `scripts/subset_font.py`로 서브셋 `@font-face`를 만들어
  jsDelivr `<link>` 자리에 넣는다(글자가 바뀌면 다시 만든다). 도구가 없으면 링크를 두고 외부 요청과 시스템 폰트 대체 가능성을 알린다.
- **라이트 온리.** `:root { color-scheme: light; }`와 `body` 배경색을 명시해 다크 호스트에서도 깨지지 않게 한다. 다크 팔레트를 추가하지 않는다.
  예외는 덱의 장면 전환 장뿐이다: 표지·섹션·마무리 장(`data-kind="cover|section|closing"`)에만 `data-surface="dark"`(blue-dark 풀블리드 면 + 흰 글자, 덱당 1~3장)를 쓸 수 있다. 본문 장·Impact·page에는 쓰지 않는다([slide-deck.md](../blocks/slide-deck.md) 진한 면 절).
- 모바일 폭에서 좌우 16px 거터, 가로 스크롤 없음.
- **높이 720px 프레임.** 갤러리 iframe처럼 높이 약 720px 프레임(1280×720)에 넣을 페이지는 첫 SVG 도식의 위쪽 절반 이상이 720px 안에 든다(1280×800에서는 원칙 2번대로 전부 보인다). 머리 260 + 첫 그림 렌더 높이 390이 합계 기준이다(정본: [shell.md](../blocks/shell.md) 첫 화면 높이 예산).
- **한 artifact 안 여러 페이지.** 탭으로 고른 페이지를 iframe으로 보여 줄 때 같은 artifact의 다른 파일을 `src`로 부르지 않는다(뷰어 샌드박스에서 연결이 끊긴다).
  각 페이지 HTML을 base64 JSON으로 내장하고, 탭을 고르면 `TextDecoder`로 풀어 `iframe.srcdoc`에 넣는다. iframe은 `sandbox="allow-scripts"`이고 `allow-same-origin`은 주지 않는다.
  새 탭 열기는 같은 HTML로 만든 Blob URL을 쓰고, 막히면 "새 탭을 열 수 없어요. 이 화면에서 보세요" 같은 안내 문구를 보여 준다.
- 예시 데이터는 전부 합성이다. 실제 회사·제품·사람·티켓 번호처럼 보이는 값을 쓰지 않는다.
- 외부 사이트 링크와 레퍼런스 사이트 이름을 페이지에 넣지 않는다.

## 게이트

page는 [gates.md](../gates.md) 공통 게이트와 [gates/page.md](../gates/page.md)만 읽고, PAGE DEPTH(의미) → HARD → 접근성 → VISUAL → WARNING 순서로 본다. page 전용 항목까지 모두 적용한다.
