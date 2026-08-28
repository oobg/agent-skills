#!/usr/bin/env python3
"""구조화 데이터 관측 — 하나의 마크업을 엔진별 규칙표에 각각 대조한다.

파일을 엔진별로 나누지 않는 이유는 입력이 같기 때문이다. 같은 HTML, 같은 JSON-LD
블록을 두 번 받을 이유가 없고, 무엇보다 **두 표를 동시에 봐야 나오는 판정**이 있다.
`position` 없는 BreadcrumbList는 구글에서 실패하고 네이버에서 통과하며, 그 두 줄이
붙어 있어야 읽힌다. 나누면 그 대조가 사라진다.

판정은 엔진별로 갈린다. 규칙표는 schema_rules.py에 데이터로만 있다.
"""

import datetime
import re
from urllib.parse import urlsplit

import parse
import schema_rules as rules

ISO_DATE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})"
                      r"(?:([T ])\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?)?$")
# ISO 8601은 정밀도를 줄인 표기(2026, 2026-08)와 주·서수 표기도 허용한다.
# 전체 날짜만 받으면 유효한 값을 거짓 실패로 찍는다.
ISO_COARSE = re.compile(r"^\d{4}(-\d{2})?$")
ISO_ALT = re.compile(r"^\d{4}-(W\d{2}(-\d)?|\d{3})$")
# ISO 8601은 가장 작은 단위에 소수를 허용한다. PT1.5H와 P1.5D는 유효한 값이므로
# 정수만 받으면 정상 마크업이 거짓 실패한다.
ISO_DURATION = re.compile(r"^P(?!$)(\d+(\.\d+)?Y)?(\d+(\.\d+)?M)?(\d+(\.\d+)?W)?"
                          r"(\d+(\.\d+)?D)?"
                          r"(T(?=\d)(\d+(\.\d+)?H)?(\d+(\.\d+)?M)?(\d+(\.\d+)?S)?)?$")
NUMERIC = re.compile(r"^\d+(\.\d+)?$")
SAMPLE = 3                      # 메시지에 예시로 붙이는 최대 개수


def _date_state(value):
    """"ok" | "space" | "bad" — 형식과 달력 유효성을 함께 본다.

    형식만 보면 2026-99-99가 통과한다. 반대로 날짜와 시간을 공백으로 잇는 표기는
    ISO 8601이 아니지만 실무에서 흔해, 거짓 실패로 찍지 않고 확인 항목으로 내린다.
    """
    if ISO_COARSE.match(value) or ISO_ALT.match(value):
        return "coarse"
    hit = ISO_DATE.match(value)
    if not hit:
        return "bad"
    try:
        datetime.date(int(hit.group(1)), int(hit.group(2)), int(hit.group(3)))
    except ValueError:
        return "bad"
    return "space" if hit.group(4) == " " else "ok"


def _is_text(value):
    """Text로 인정되는 형태인가.

    {"@value": "이름", "@language": "ko"}는 **정상 JSON-LD다.** str만 통과시키면
    다국어 사이트가 거짓 실패한다. 숫자와 불리언만 걸러내는 것이 이 검사의 목적이다.
    """
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, dict):
        inner = value.get("@value")
        return isinstance(inner, str) and bool(inner.strip())
    if isinstance(value, list):
        return any(_is_text(v) for v in value)
    return False


def _objects(value, idmap=None):
    """중첩 조회 대상이 되는 dict들. @id 참조는 실제 노드까지 따라간다.

    @graph 안에서 노드를 @id로 서로 참조하는 형태는 흔한 출력이다. 참조를 안 따라가면
    `"offers": {"@id": "...#offer"}`처럼 값이 다른 노드에 있는 정상 마크업이 거짓 실패한다.
    """
    out = []
    for item in ([value] if isinstance(value, dict)
                 else value if isinstance(value, list) else []):
        if not isinstance(item, dict):
            continue
        out.append(item)
        ref = item.get("@id")
        if idmap and isinstance(ref, str):
            target = idmap.get(ref)
            if target is not None and target is not item:
                out.append(target)
    return out


def _utc_date(value):
    """비교용 UTC 날짜. 못 구하면 None.

    문자열 사전순으로 비교하면 타임존과 정밀도 차이에서 거짓 판정이 난다.
    +09:00과 Z를 섞어 쓰거나 한쪽만 시각까지 적으면 정상 마크업이 역전으로 찍힌다.
    날짜까지만 비교하면 두 경우 모두 사라지고, 남는 신호(날짜가 실제로 앞선다)는 지킨다.
    """
    if _date_state(value) in ("bad", "coarse"):
        return None
    body = value.replace(" ", "T", 1)
    if "T" not in body:
        try:
            return datetime.date.fromisoformat(body)
        except ValueError:
            return None
    txt = body[:-1] + "+00:00" if body.endswith("Z") else body
    try:
        stamp = datetime.datetime.fromisoformat(txt)
    except ValueError:
        return None                      # Python 3.9는 일부 표기를 못 읽는다
    if stamp.tzinfo is not None:
        stamp = stamp.astimezone(datetime.timezone.utc)
    return stamp.date()


def _all_objects(node, out):
    """JSON-LD 트리의 모든 dict를 모은다.

    규칙 대조는 @type이 있어야 하지만 **값 형식 검사는 그렇지 않다.** @type 없는 중첩
    객체를 빼면 `@type` 생략이 검사를 끄는 스위치가 된다 — 그 안의 음수 평점과 상대경로
    URL이 통째로 안 보인다. 손으로 쓴 JSON-LD에서 흔한 형태이고, JSON-LD는 속성 range로
    타입이 정해지므로 무효 마크업이라 부를 수도 없다.
    """
    if isinstance(node, list):
        for item in node:
            _all_objects(item, out)
        return
    if not isinstance(node, dict):
        return
    out.append(node)
    for key, value in node.items():
        if key != "@context" and isinstance(value, (dict, list)):
            _all_objects(value, out)


def _label(node):
    """메시지에 쓸 노드 이름. 타입만으로는 어느 노드인지 구분되지 않는다."""
    types = parse.node_types(node) or ["(타입 없음)"]
    for key in ("name", "headline", "@id"):
        value = node.get(key)
        if isinstance(value, str) and value.strip():
            return "{} '{}'".format(types[0], value.strip()[:24])
    return types[0]


def _has(node, prop):
    """속성이 실제로 값을 갖는가. 빈 문자열과 빈 배열은 없는 것으로 센다."""
    value = node.get(prop)
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def _id_map(objects):
    """@id → 그 id를 가진 가장 내용이 많은 노드. 참조 해석에 쓴다."""
    out = {}
    for node in objects:
        ref = node.get("@id")
        if isinstance(ref, str) and ref.strip():
            if len(node) > len(out.get(ref, {})):
                out[ref] = node
    return out


def _present(node, path, nested=None, idmap=None):
    """중첩 속성과 점 경로까지 본다.

    두 가지를 처리한다.
    ① `item` 같은 대체 위치 — BreadcrumbList의 name은 ListItem에 직접 있을 수도,
       item 객체 안에 있을 수도 있다. 구글 문서가 두 형태를 모두 인정한다.
    ② `offers.price` 같은 점 경로 — 구글이 요구하는 것은 offers의 존재가 아니라
       그 안의 price다. 존재만 세면 {"currency": "USD"}가 통과한다.
    """
    head, _, rest = path.partition(".")
    if rest:
        return any(_present(inner, rest, None, idmap)
                   for inner in _objects(node.get(head), idmap))
    if _has(node, head):
        return True
    if not nested:
        return False
    return any(_has(inner, head) for inner in _objects(node.get(nested), idmap))


def _string_values(raw):
    """속성값에서 문자열만 뽑는다.

    dict를 그대로 순회하면 **키가 값으로 새어 나온다.** screenshot이 ImageObject면
    "@type"·"url" 같은 키가 URL 검사에 걸려 거짓 FAIL이 난다. 객체 안의 url은
    그 객체가 별도 노드로 회수될 때 검사되므로 여기서 버려도 잃는 것이 없다.
    """
    if isinstance(raw, str):
        return [raw.strip()] if raw.strip() else []
    if isinstance(raw, list):
        out = []
        for item in raw:
            out.extend(_string_values(item))
        return out
    if isinstance(raw, dict):
        # {"@value": ...}와 {"@id": ...}는 값 자체를 담은 형태이므로 읽는다.
        # ImageObject 같은 본격 객체는 별도 노드로 회수되므로 여기서 다루지 않는다.
        for key in ("@value", "@id"):
            inner = raw.get(key)
            if isinstance(inner, str) and inner.strip():
                return [inner.strip()]
    return []


def _walk_typed(node, ctx, ancestors, out, referenced=False):
    """@type을 가진 노드를 조상 타입과 함께 회수한다.

    조상이 필요한 이유는 같은 타입의 필수 속성이 부모에 따라 갈리기 때문이다.
    ListItem은 BreadcrumbList 아래에서는 name이, ItemList(캐러셀) 아래에서는 image가
    필수다. 부모를 모르면 둘 중 하나는 반드시 거짓 실패한다.

    parse.jsonld_pairs는 최상위와 @graph만 펼친다. 네이버 PostalAddress처럼 다른 노드
    안에 중첩되는 타입은 그 방식으로 안 보이므로 여기서 따로 훑는다. 기존 검사들이 쓰는
    평탄화 결과를 바꾸지 않으려고 parse 쪽을 건드리지 않고 여기에 둔다.
    """
    if isinstance(node, list):
        for item in node:
            _walk_typed(item, ctx, ancestors, out, referenced)
        return
    if not isinstance(node, dict):
        return
    ctx = node.get("@context", ctx)
    types = parse.node_types(node)
    if types:
        out.append((ctx, node, ancestors, referenced))
        ancestors = ancestors + tuple(t for t in types if t)
    for key, value in node.items():
        if key != "@context" and isinstance(value, (dict, list)):
            _walk_typed(value, ctx, ancestors, out,
                        referenced or key in rules.REFERENCE_PROPS)


def _pick_rule(variants, ancestors):
    """조상에 맞는 규칙 변형을 고른다. 맞는 것이 없으면 무조건 규칙만 쓴다."""
    for rule in variants:
        within = rule.get("within")
        if within and within in ancestors:
            return rule
    for rule in variants:
        if not rule.get("within"):
            return rule
    return None


def _check_context(typed, add):
    """@context가 없으면 소비자가 블록을 통째로 무시한다. 두 엔진 공통이다."""
    if not typed:
        return
    missing = [n for c, n, _, _ in typed if parse.context_state(c) == "none"]
    other = [c for c, _, _, _ in typed if parse.context_state(c) == "other"]
    if missing:
        add(("FAIL", "@context",
             "노드 {}건에 없음 — 두 엔진 모두 무시한다: {}".format(
                 len(missing), ", ".join(_label(n) for n in missing[:SAMPLE]))))
    elif other:
        add(("CHECK", "@context",
             "schema.org가 아닌 @context {}건: {}".format(
                 len(other), ", ".join(str(c)[:40] for c in other[:SAMPLE]))))
    else:
        add(("OK", "@context", "노드 {}건 전부 schema.org".format(len(typed))))


def _check_types(nodes, add):
    """상용 타입에 없는 이름은 오타일 수 있다. 희귀 타입도 여기 걸리므로 FAIL이 아니다."""
    unknown = sorted({t for n in nodes for t in parse.node_types(n)
                      if t and t not in rules.KNOWN_TYPES})
    if unknown:
        add(("CHECK", "타입 이름",
             "상용 목록에 없는 타입 {}종 — 오타이면 마크업 전체가 무효다: {}".format(
                 len(unknown), ", ".join(unknown[:5]))))


def _check_retired(nodes, add):
    """구글이 리치 결과를 내린 타입.

    마크업이 틀린 것이 아니라 소비 표면이 사라진 것이다. 필수 속성 결손과 섞으면
    "고치면 된다"로 읽히므로 따로 알린다. AEO·GEO 소비자에게는 여전히 유효할 수 있다.
    """
    seen = {t for n in nodes for t in parse.node_types(n) if t in rules.GOOGLE_RETIRED}
    for typ in sorted(seen):
        add(("CHECK", "구글 리치 결과",
             "{} — {}".format(typ, rules.GOOGLE_RETIRED[typ])))


def _check_engine(engine, typed, add, idmap=None):
    """한 엔진의 규칙표로만 판정한다. 다른 엔진의 필수 속성은 여기서 보지 않는다."""
    table = rules.ENGINE_TABLES[engine]
    name = rules.ENGINE_LABEL[engine]
    misses, enum_bad, text_bad, rec_missing, matched = [], [], [], [], 0
    for _, node, ancestors, referenced in typed:
        if referenced:
            # 참조 자리에 놓인 엔티티다. 그 페이지의 리치 결과 주체가 아니므로
            # 필수 속성을 묻지 않는다.
            continue
        for typ in parse.node_types(node):
            # 출처가 같은 필수로 지원한다고 밝힌 서브타입은 상위 규칙으로 대조한다.
            key = typ if typ in table else rules.TYPE_ALIASES.get(typ)
            rule = _pick_rule(table.get(key) or [], ancestors)
            if rule is None:
                continue
            matched += 1
            nested = rule.get("nested")
            # 항목마다 스스로 무엇이 문제인지 말하게 한다. 뒤에 "없음"을 한 번 붙이면
            # "author가 객체가 아님 없음" 같은 문장이 나온다.
            gone = ["{} 없음".format(p) for p in rule.get("required", [])
                    if not _present(node, p, nested, idmap)]
            for group in rule.get("either", []):
                if not any(_present(node, p, nested, idmap) for p in group):
                    gone.append("{} 중 하나 없음".format(" 또는 ".join(group)))
            for cond in rule.get("conditional", []):
                if (_present(node, cond["if"], nested, idmap)
                        and not any(_present(node, p, nested, idmap) for p in cond["either"])):
                    gone.append("{}가 있으면 {} 중 하나가 필요".format(
                        cond["if"], " 또는 ".join(cond["either"])))
            for prop in rule.get("node", []):
                # 문자열 author처럼 값은 있으나 객체가 아닌 경우다.
                if node.get(prop) is not None and not _objects(node.get(prop), idmap):
                    gone.append("{}가 객체가 아님".format(prop))
            if gone:
                misses.append("{}: {}".format(_label(node), ", ".join(gone)))
            for prop in rule.get("text", []):
                # 없는 것은 required가 본다. 여기서는 있는데 형태가 틀린 것만 본다.
                if prop in node and not _is_text(node[prop]):
                    text_bad.append("{}.{}={}".format(typ, prop, repr(node[prop])[:20]))
            short = [p for p in rule.get("recommended", [])
                     if not _present(node, p, nested, idmap)]
            if short:
                rec_missing.append("{}({})".format(typ, ", ".join(short[:4])))
            for prop, allowed in (rule.get("enum") or {}).items():
                for value in _string_values(node.get(prop)):
                    if value.rsplit("/", 1)[-1] not in allowed:
                        enum_bad.append("{}.{}={} (허용: {} 등 {}종)".format(
                            typ, prop, value[:20], ", ".join(allowed[:2]), len(allowed)))
    if not matched:
        # 침묵은 "문제 없음"으로 읽힌다. 대조를 안 한 것과 통과한 것은 다르다.
        add(("CHECK", "{} 필수속성".format(name),
             "대조 대상 없음 — 관측된 타입 중 {} 규칙표에 있는 것이 없다. "
             "{}가 지원하는 타입인지 문서에서 확인한다".format(name, name)))
    elif misses:
        add(("FAIL", "{} 필수속성".format(name),
             "{}건 결손: {}".format(len(misses), " / ".join(misses[:SAMPLE]))))
    else:
        add(("OK", "{} 필수속성".format(name), "대조한 {}건 충족".format(matched)))
    if text_bad:
        add(("FAIL", "{} 값 자료형".format(name),
             "Text여야 하는 속성이 아님 {}건: {}".format(
                 len(text_bad), ", ".join(text_bad[:SAMPLE]))))
    if enum_bad:
        add(("FAIL", "{} 열거값".format(name),
             "허용되지 않는 값 {}건: {}".format(len(enum_bad), ", ".join(enum_bad[:SAMPLE]))))
    if rec_missing:
        # 속성마다 한 줄을 내면 CHECK가 노이즈가 된다. 엔진당 한 줄로 집계한다.
        # 구글 문서는 권장 속성이 많을수록 표시 가능성이 커진다고 하면서도, 부정확한
        # 값을 채우느니 적고 정확한 편이 낫다고 한다. 관측만 내고 개수로 압박하지 않는다.
        add(("CHECK", "{} 권장속성".format(name),
             "결손 {}건 — 필수는 아니나 표시 가능성을 낮춘다: {}{}".format(
                 len(rec_missing), " / ".join(rec_missing[:SAMPLE]),
                 " 외 {}건".format(len(rec_missing) - SAMPLE) if len(rec_missing) > SAMPLE else "")))


def _check_values(objects, add):
    """날짜·기간·숫자·URL은 형식이 기계로 갈린다."""
    bad_date, bad_url, bad_dur, bad_num = [], [], [], []
    reversed_dates, space_date, scheme_rel = [], [], []
    for node in objects:
        for prop in rules.DATE_PROPS:
            raw = node.get(prop)
            if raw is None:
                continue
            values = _string_values(raw)
            if not values:
                # 숫자나 객체를 날짜로 넣은 경우다. 침묵하면 검사한 것처럼 읽힌다.
                bad_date.append("{}={}".format(prop, repr(raw)[:20]))
                continue
            for value in values:
                state = _date_state(value)
                if state == "bad":
                    bad_date.append("{}={}".format(prop, value[:20]))
                elif state == "space":
                    space_date.append("{}={}".format(prop, value[:20]))
        pub = next(iter(_string_values(node.get("datePublished"))), None)
        mod = next(iter(_string_values(node.get("dateModified"))), None)
        if pub and mod:
            pub_d, mod_d = _utc_date(pub), _utc_date(mod)
            if pub_d and mod_d and mod_d < pub_d:
                reversed_dates.append("{}: 수정 {} < 발행 {}".format(_label(node), mod, pub))
        for prop in rules.DURATION_PROPS:
            value = node.get(prop)
            if isinstance(value, str) and value.strip() and not ISO_DURATION.match(value.strip()):
                bad_dur.append("{}={}".format(prop, value.strip()[:20]))
        for prop in rules.NUMERIC_PROPS:
            value = node.get(prop)
            if isinstance(value, bool) or value is None:
                continue
            if isinstance(value, (int, float)):
                if value < 0:
                    bad_num.append("{}={}".format(prop, value))
            elif isinstance(value, str) and value.strip() and not NUMERIC.match(value.strip()):
                # 네이버 문서가 음수와 지수 표기를 명시적으로 금지한다.
                bad_num.append("{}={}".format(prop, value.strip()[:20]))
        for prop in rules.URL_PROPS:
            for value in _string_values(node.get(prop)):
                if value.startswith("//"):
                    # 스킴 상대 URL. 해석은 되지만 두 엔진 다 절대 경로를 요구한다.
                    # 상대 경로와 같은 결함이 아니므로 줄을 나눈다.
                    scheme_rel.append("{}={}".format(prop, value[:30]))
                elif not value.startswith(("http://", "https://")):
                    bad_url.append("{}={}".format(prop, value[:30]))
    if bad_date:
        add(("FAIL", "날짜 형식",
             "형식이 아니거나 달력에 없는 날 {}건: {}".format(
                 len(bad_date), ", ".join(bad_date[:SAMPLE]))))
    if space_date:
        add(("CHECK", "날짜 구분자",
             "T가 아닌 공백으로 이었다 {}건 — 두 엔진 문서는 T로 적는다: {}".format(
                 len(space_date), ", ".join(space_date[:SAMPLE]))))
    if reversed_dates:
        add(("CHECK", "날짜 정합",
             "수정일이 발행일보다 이르다: {}".format(", ".join(reversed_dates[:SAMPLE]))))
    if bad_dur:
        add(("FAIL", "기간 형식",
             "ISO 8601 duration이 아닌 값 {}건 (PT30M 꼴): {}".format(
                 len(bad_dur), ", ".join(bad_dur[:SAMPLE]))))
    if bad_num:
        add(("FAIL", "숫자 형식",
             "음수이거나 숫자가 아닌 값 {}건: {}".format(len(bad_num), ", ".join(bad_num[:SAMPLE]))))
    if scheme_rel:
        add(("CHECK", "URL 스킴",
             "스킴 상대 URL {}건 — 두 엔진 다 절대 경로를 요구한다: {}".format(
                 len(scheme_rel), ", ".join(scheme_rel[:SAMPLE]))))
    if bad_url:
        add(("FAIL", "URL 형식",
             "절대 경로가 아닌 값 {}건: {}".format(len(bad_url), ", ".join(bad_url[:SAMPLE]))))


def _domains(values):
    """sameAs 값에서 호스트를 뽑는다. www.는 떼고 본다."""
    out = []
    for value in values:
        host = urlsplit(value).netloc.lower()
        out.append(host[4:] if host.startswith("www.") else host)
    return out


def _match_surface(hosts, catalog):
    """호스트가 카탈로그의 도메인으로 끝나면 그 표면으로 센다."""
    hit = {}
    for host in hosts:
        for domain, label in catalog.items():
            if host == domain or host.endswith("." + domain):
                hit[label] = domain
    return hit


def _check_channels(nodes, same_as, is_root, add, naver=True):
    """NEO와 LLMO는 같은 sameAs 배열을 서로 다른 목표 집합으로 상대한다.

    건수 하나로 판정하면 둘 다 놓친다. GitHub·LinkedIn만 걸린 사이트는 LLMO에는
    유효하지만 네이버 연관채널로는 0건이다.
    """
    hosts = _domains(same_as)
    naver_hit = _match_surface(hosts, rules.NAVER_CHANNEL_DOMAINS)
    llmo_hit = _match_surface(hosts, rules.LLMO_SURFACES)

    if naver and is_root:
        spec = rules.NAVER_CHANNEL
        holders = [n for n in nodes if any(t in spec["types"] for t in parse.node_types(n))]
        if not holders:
            add(("CHECK", "네이버 연관채널",
                 "루트에 {} 노드가 없다 — 연관채널은 루트 페이지 선언만 인식된다".format(
                     spec["type_label"])))
        else:
            # 세 속성은 **한 노드 안에** 있어야 한다. 노드를 가로질러 any로 세면
            # name만 있는 Organization과 url만 있는 Person이 합쳐져 통과한다.
            full = [n for n in holders if all(_has(n, p) for p in spec["required"])]
            if not full:
                best = max(holders, key=lambda n: sum(_has(n, p) for p in spec["required"]))
                gone = [p for p in spec["required"] if not _has(best, p)]
                add(("FAIL", "네이버 연관채널",
                     "{}에 {} 없음 — 세 속성이 한 노드에 모두 있어야 한다".format(
                         _label(best), ", ".join(gone))))
            elif not naver_hit:
                add(("CHECK", "네이버 연관채널",
                     "sameAs {}건이나 인식 채널 0건: {}".format(
                         len(same_as), ", ".join(sorted(set(hosts))[:SAMPLE]) or "없음")))
            else:
                add(("OK", "네이버 연관채널",
                     "인식 채널 {}건: {}".format(len(naver_hit), ", ".join(sorted(naver_hit)))))
    elif naver and same_as:
        add(("CHECK", "네이버 연관채널",
             "이 페이지는 루트가 아니다 — 연관채널 판정은 루트에서만 한다"))

    if same_as:
        add(("OK" if llmo_hit else "CHECK", "LLMO 표면",
             "{}건 연결: {}".format(len(llmo_hit), ", ".join(sorted(llmo_hit))) if llmo_hit
             else "sameAs {}건 중 학습 표면(위키·앱스토어·저장소) 0건".format(len(same_as))))


def audit_schema(html, final_url, engines=("google", "naver"), report_parse_errors=False):
    """구조화 데이터를 엔진별로 관측한다. 판정은 엔진마다 따로 나온다.

    report_parse_errors는 이 모듈을 단독으로 쓸 때만 켠다. crawl_audit 경로에서는
    checks_page가 같은 오류를 이미 내므로 켜면 같은 줄이 두 번 나온다.
    """
    out = {"checks": []}
    add = out["checks"].append

    pairs, ld_errors = parse.jsonld_pairs(html)
    out["jsonld_parse_errors"] = ld_errors
    if ld_errors and report_parse_errors:
        add(("FAIL", "JSON-LD 파싱",
             "{}블록이 JSON으로 읽히지 않는다 — 두 엔진 모두 그 블록을 무시한다".format(ld_errors)))
    typed = []
    for ctx, node in pairs:
        _walk_typed(node, ctx, (), typed)
    nodes = [n for _, n, _, _ in typed]
    micro = parse.microdata_types(html)
    out["microdata_types"] = micro
    out["schema_node_count"] = len(nodes)

    if not nodes:
        if micro:
            # 네이버는 Microdata와 JSON-LD를 나란히 권장한다. JSON-LD만 세면
            # Microdata로 마크업한 사이트가 '없음'으로 잘못 관측된다.
            add(("CHECK", "구조화 데이터 형식",
                 "JSON-LD 0건이나 Microdata {}종 관측: {} — 속성 대조는 하지 않았다".format(
                     len(micro), ", ".join(micro[:5]))))
        return out
    if micro:
        add(("CHECK", "구조화 데이터 형식",
             "JSON-LD와 Microdata가 함께 있다 (Microdata {}종) — 내용이 어긋나지 않는지 본다".format(
                 len(micro))))

    # 값 형식은 @type 없는 중첩 객체 안에서도 검사한다. 규칙 대조와 대상이 다르다.
    objects = []
    for _, node in pairs:
        _all_objects(node, objects)
    idmap = _id_map(objects)

    _check_context(typed, add)
    _check_types(nodes, add)
    if "google" in engines:
        _check_retired(nodes, add)
    for engine in engines:
        _check_engine(engine, typed, add, idmap)
    _check_values(objects, add)

    same_as = []
    for node in nodes:
        same_as.extend(_string_values(node.get("sameAs")))
    is_root = urlsplit(final_url or "").path.rstrip("/") == ""
    # 연관채널은 네이버 규칙이라 엔진 게이트에 걸린다. LLMO 표면은 레인이 달라
    # 엔진과 무관하게 늘 본다 — sameAs 하나가 두 레인을 상대하기 때문이다.
    _check_channels(nodes, sorted(set(same_as)), is_root, add, "naver" in engines)
    return out
