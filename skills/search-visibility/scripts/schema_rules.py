#!/usr/bin/env python3
"""엔진별 구조화 데이터 규칙표 — 데이터만 둔다. 판정 로직은 checks_schema.py에 있다.

구글과 네이버는 같은 schema.org 어휘를 쓰지만 **필수 속성이 서로 다르다.** 네이버는
BreadcrumbList에서 `name`을 필수로, `position`을 필수아님으로 둔다. 구글은 반대에 가깝다.
한쪽 표로 양쪽을 판정하면 반드시 한 레인을 오판하므로 표를 엔진별로 분리한다.

표마다 출처 URL을 남긴다. 엔진이 정책을 바꾸면 그 항목만 고치고 나머지는 건드리지 않는다.

규칙 스키마:
    "required"    — 없으면 그 엔진에서 FAIL
    "either"      — [[a, b, c]] 꼴. 각 묶음에서 최소 하나는 있어야 한다
    "recommended" — 없으면 CHECK. 구글 문서는 "적지만 완전하고 정확한 것"을 권하므로
                    개수로 압박하지 않는다
    "source"      — 근거 URL
"""

# 규칙은 타입마다 **목록**이다. 같은 타입이 부모에 따라 다른 필수 속성을 갖기 때문이다.
# ListItem이 그렇다 — BreadcrumbList 안에서는 name이 필수이고 ItemList(캐러셀) 안에서는
# image가 필수다. 하나로 합치면 둘 중 하나가 반드시 거짓 실패한다.
#
# 규칙 스키마:
#     "within"      — 이 조상 타입 아래일 때만 적용. 없으면 어디서나 적용
#     "required"    — 없으면 그 엔진에서 FAIL. `offers.price`처럼 점 경로를 쓸 수 있다
#     "either"      — [[a, b]] 꼴. 각 묶음에서 최소 하나
#     "nested"      — 이 속성 안에서도 값을 찾는다(BreadcrumbList의 item처럼)
#     "text"        — 있을 때 Text 형태여야 하는 속성. 숫자·불리언이면 FAIL.
#                     {"@value": "...", "@language": "ko"}는 정상으로 인정한다
#     "enum"        — {속성: [허용값]}. 벗어나면 FAIL
#     "recommended" — 없어도 FAIL이 아니다. 엔진당 한 줄로 집계해 CHECK로 낸다
#     "source"      — 근거 URL

# ── 구글 ──────────────────────────────────────────────────────────────────
# 출처: https://developers.google.com/search/docs/appearance/structured-data/
# "필수 속성이 누락된 항목은 리치 결과로 표시되지 않습니다"(sd-policies, 완전성).
#
# 옮기면서 확인한 것.
# 1. Article과 Organization은 **필수 속성이 아예 없다.** 문서가 "필수 속성은 없습니다"라고
#    명시한다. 없는 필수를 만들어 실패로 찍지 않는다.
# 2. Product는 문서가 둘로 갈렸다. 제품 스니펫(구매 불가 페이지)과 판매자 등록정보(구매
#    가능 페이지)의 필수가 다르다. 어느 쪽을 의도했는지는 마크업만으로 갈리지 않으므로
#    느슨한 쪽(제품 스니펫)으로 판정한다. 판매자 등록정보는 여기에 image·offers가 더 붙는다.
# 3. FAQPage는 표에 없다. 2026-05-07부로 구글 검색에서 표시가 중단됐고 2026-06-15에
#    문서 자체가 삭제됐다. 필수 속성을 물을 대상이 아니다(checks_schema에서 따로 알린다).
GOOGLE = {
    "Article": [{
        "required": [], "either": [],
        "recommended": ["headline", "image", "datePublished", "dateModified", "author"],
        "source": "https://developers.google.com/search/docs/appearance/structured-data/article",
    }],
    "Organization": [{
        "required": [], "either": [],
        "recommended": ["name", "url", "logo", "sameAs", "address", "telephone"],
        "source": "https://developers.google.com/search/docs/appearance/structured-data/organization",
    }],
    "Product": [{
        # 원문: review·aggregateRating·offers 중 하나가 필요하다.
        "required": ["name"], "text": ["name"],
        "either": [["review", "aggregateRating", "offers"]],
        # offers를 쓰면 가격이 어딘가에 있어야 한다. 존재만 세면 @type 없는 offers와
        # AggregateOffer가 가격 없이 통과한다.
        "conditional": [{"if": "offers",
                         "either": ["offers.price", "offers.lowPrice",
                                    "offers.priceSpecification.price"]}],
        "recommended": ["image", "brand", "description", "sku"],
        "source": "https://developers.google.com/search/docs/appearance/structured-data/product-snippet",
    }],
    "AggregateOffer": [{
        "required": ["lowPrice", "priceCurrency"], "either": [],
        "recommended": ["highPrice", "offerCount"],
        "source": "https://developers.google.com/search/docs/appearance/structured-data/product-snippet",
    }],
    "Offer": [{
        # offers의 존재가 아니라 그 안의 price가 요건이다. 존재만 세면
        # {"currency": "USD"}처럼 가격 없는 객체가 통과한다.
        # priceCurrency는 판매자 등록정보에서는 price가 있으면 조건부 필수이나,
        # 여기서는 느슨한 쪽(제품 스니펫)을 기준으로 두어 권장에 남긴다.
        "required": [],
        "either": [["price", "priceSpecification.price"]],
        "recommended": ["priceCurrency", "availability", "priceValidUntil"],
        "enum": {"availability": [
            "BackOrder", "Discontinued", "InStock", "InStoreOnly", "LimitedAvailability",
            "OnlineOnly", "OutOfStock", "PreOrder", "PreSale", "SoldOut"]},
        "source": "https://developers.google.com/search/docs/appearance/structured-data/product-snippet",
    }],
    "SoftwareApplication": [{
        # 네이버와 정면으로 갈리는 자리다. 구글은 offers.price와 평점을 필수로 걸고
        # applicationCategory를 권장으로 내린다. 네이버는 applicationCategory가 필수다.
        "required": ["name", "offers.price"], "text": ["name"],
        "either": [["aggregateRating", "review"]],
        "recommended": ["applicationCategory", "operatingSystem"],
        "enum": {"applicationCategory": [
            "GameApplication", "SocialNetworkingApplication", "TravelApplication",
            "ShoppingApplication", "SportsApplication", "LifestyleApplication",
            "BusinessApplication", "DesignApplication", "DeveloperApplication",
            "DriverApplication", "EducationalApplication", "HealthApplication",
            "FinanceApplication", "SecurityApplication", "BrowserApplication",
            "CommunicationApplication", "DesktopEnhancementApplication",
            "EntertainmentApplication", "MultimediaApplication", "HomeApplication",
            "UtilitiesApplication", "ReferenceApplication"]},
        "source": "https://developers.google.com/search/docs/appearance/structured-data/software-app",
    }],
    "BreadcrumbList": [{
        "required": ["itemListElement"], "either": [], "recommended": [],
        "source": "https://developers.google.com/search/docs/appearance/structured-data/breadcrumb",
    }],
    "ListItem": [{
        # item은 필수 목록에 있으나 "트레일의 마지막 항목이면 필수가 아니다"라는 면제가
        # 붙는다. 마지막인지 판정하려면 목록 문맥이 필요하고, 틀리면 정상 마크업을
        # 실패로 찍는다. 그래서 item은 권장으로 내리고 name·position만 필수로 본다.
        "within": "BreadcrumbList",
        "required": ["name", "position"], "either": [], "nested": "item",
        "recommended": ["item"],
        "source": "https://developers.google.com/search/docs/appearance/structured-data/breadcrumb",
    }],
    "Review": [{
        # itemReviewed는 다른 타입에 중첩된 리뷰면 생략한다. 중첩 여부를 보고 거는
        # 대신 권장으로 내린다 — 중첩이 정상 사용이라 필수로 걸면 거짓 실패가 난다.
        # 출처의 필수는 reviewRating의 존재가 아니라 그 안의 ratingValue다.
        # author도 Person·Organization 객체여야 하므로 문자열 author를 걸러 낸다.
        "required": ["author", "reviewRating.ratingValue"], "either": [], "node": ["author"],
        # itemReviewed는 다른 타입에 중첩되면 생략하는 것이 정상이다.
        # 권장 목록에 두면 올바른 중첩 마크업이 매번 결손으로 찍힌다.
        "recommended": ["datePublished"],
        "source": "https://developers.google.com/search/docs/appearance/structured-data/review-snippet",
    }],
    "AggregateRating": [{
        "required": ["ratingValue"],
        "either": [["ratingCount", "reviewCount"]],
        "recommended": ["bestRating", "worstRating"],
        "source": "https://developers.google.com/search/docs/appearance/structured-data/review-snippet",
    }],
}

# 구글이 리치 결과를 내린 타입. 마크업이 틀린 게 아니라 소비 표면이 사라진 것이므로
# 필수 속성 결손과 섞지 않고 따로 알린다. AEO·GEO 소비자에게는 여전히 유효할 수 있다.
GOOGLE_RETIRED = {
    "FAQPage": "2026-05-07부로 구글 검색에 표시되지 않는다(2026-06-15 문서 삭제). "
               "2023-09부터는 정부·보건 사이트로 제한돼 있었다.",
    "HowTo": "구글 리치 결과에서 내려갔다. 네이버는 여전히 지원한다.",
}

# ── 네이버 ────────────────────────────────────────────────────────────────
# 출처: https://searchadvisor.naver.com/guide/structured-data-*
# 각 문서의 "타입 및 속성" 표에서 필수여부 칸을 그대로 옮겼다.
#
# 옮기면서 확인한 것 두 가지.
# 1. 네이버의 필수는 얇다. 대부분 1~3개이고, 구글이 필수로 거는 author·datePublished·
#    publisher 계열은 14개 문서 어디에도 없다. 대신 검색 카드에 실제로 찍히는 필드
#    (Restaurant openingHours, Movie actor)를 필수로 올린다.
# 2. 문서가 자기 안에서 어긋나는 자리가 있다. 아래 주석에 그 자리를 남긴다.
#
# JobPosting과 VideoObject는 제외했다. 두 타입은 마크업만으로 성립하지 않고 네이버 제휴와
# 수집요청 API 연동이 전제라, 마크업 결손으로 판정하면 제휴가 없는 사이트를 매번 실패로
# 찍는다. 필요하면 사람이 위 문서를 직접 본다.
NAVER = {
    "BreadcrumbList": [{
        "required": [], "either": [], "recommended": [],
        "source": "https://searchadvisor.naver.com/guide/structured-data-breadcrumb",
    }],
    "ListItem": [
        {   # 이동 경로. position은 네이버에서 필수가 아니다(구글과 갈리는 자리).
            "within": "BreadcrumbList",
            "required": ["name"], "either": [], "nested": "item",
            "recommended": ["position"],
            "source": "https://searchadvisor.naver.com/guide/structured-data-breadcrumb",
        },
        {   # 캐러셀. 네이버 문서의 image 필수는 **캐러셀용 ItemList**에 대한 것인데,
            # ItemList는 목차·관련글·장단점에도 쓰이는 범용 타입이고 둘은 마크업만으로
            # 갈리지 않는다. 필수로 걸면 이미지 없는 정상 목록이 매번 실패하므로
            # 권장으로 내린다. 구글 제품 스니펫의 장단점 예제도 여기 걸렸었다.
            "within": "ItemList",
            "required": [], "either": [], "nested": "item",
            "recommended": ["image", "name", "url", "position"],
            "source": "https://searchadvisor.naver.com/guide/structured-data-carousel",
        },
    ],
    "PostalAddress": [{
        "required": ["streetAddress"], "either": [],
        "recommended": ["postalCode", "addressRegion", "addressLocality"],
        "source": "https://searchadvisor.naver.com/guide/structured-data-address",
    }],
    "SoftwareApplication": [{
        "required": ["name", "applicationCategory"], "either": [],
        "text": ["name", "applicationCategory"],
        "recommended": ["operatingSystem", "url", "screenshot", "description"],
        "source": "https://searchadvisor.naver.com/guide/structured-data-software",
    }],
    "HowToStep": [{
        # 표는 HowTo 아래 있으나 text는 예제에서 step 안에 있다. HowTo 노드 자체에 걸면
        # step으로 나눈 정상 마크업이 전부 실패하므로 step에 건다.
        "within": "HowTo",
        "required": ["text"], "either": [], "recommended": ["image", "url"],
        "source": "https://searchadvisor.naver.com/guide/structured-data-howto",
    }],
    "AggregateRating": [{
        # 원문 [주1]: ratingCount 또는 reviewCount 중 하나가 반드시 있어야 노출된다.
        "required": ["ratingValue"],
        "either": [["ratingCount", "reviewCount"]],
        "recommended": ["bestRating"],
        "source": "https://searchadvisor.naver.com/guide/structured-data-rating",
    }],
    "Review": [{
        # 네이버 공식 예제도 평점을 reviewRating 안에 둔다. Review 노드에서 찾으면
        # 예제 그대로 쓴 마크업이 결손으로 찍힌다.
        "required": ["reviewBody"], "either": [],
        "recommended": ["reviewRating.ratingValue", "reviewRating.bestRating"],
        "source": "https://searchadvisor.naver.com/guide/structured-data-review",
    }],
    "Restaurant": [{
        "required": ["name", "openingHours"], "either": [], "text": ["name"],
        "recommended": ["telephone", "image", "url", "servesCuisine", "priceRange"],
        "source": "https://searchadvisor.naver.com/guide/structured-data-restaurant",
    }],
    "Movie": [{
        "required": ["name", "actor"], "either": [],
        "recommended": ["director", "genre", "image", "description"],
        "source": "https://searchadvisor.naver.com/guide/structured-data-movie",
    }],
    "TVSeries": [{
        # 감독은 director가 아니라 creator다. Movie와 다르다.
        "required": ["name", "actor"], "either": [],
        "recommended": ["creator", "genre", "image", "description"],
        "source": "https://searchadvisor.naver.com/guide/structured-data-tvseries",
    }],
    "Recipe": [{
        # 문서 불일치: 속성표는 recipeInstruction(단수), 예제는 recipeInstructions(복수).
        # 어느 쪽을 써도 통과시킨다. 문서가 정하지 못한 것을 우리가 정해 실패로 찍지 않는다.
        "required": [],
        "either": [["recipeInstruction", "recipeInstructions"]],
        "recommended": ["name", "image", "recipeYield", "totalTime", "recipeIngredient"],
        "source": "https://searchadvisor.naver.com/guide/structured-data-recipe",
    }],
}

# 네이버 "사이트 연관채널" — 타입표가 아니라 위치 요건이 붙는 별도 규칙이다.
# 원문: Person 혹은 Organization에 name·url·sameAs가 모두 필수이고,
#       "사이트의 루트 페이지에 기입된 구조화 데이터"여야 인식된다.
NAVER_CHANNEL = {
    "types": None,          # ORGANIZATION_TYPES + Person. 아래에서 채운다
    "type_label": "Person 또는 Organization",
    "required": ["name", "url", "sameAs"],
    "root_only": True,
    "source": "https://searchadvisor.naver.com/guide/structured-data-channel",
}

# 네이버가 연관채널로 분석한다고 밝힌 채널.
# **문서는 채널 이름만 나열하고 도메인을 적지 않는다.** 아래 도메인 중 예제에 실제로
# 나온 것은 blog.naver.com, smartstore.naver.com, facebook.com 셋뿐이고 나머지는
# 이름에서 우리가 대응시킨 추정이다. 판정을 FAIL로 쓰지 않고 CHECK로만 쓰는 이유다.
NAVER_CHANNEL_DOMAINS = {
    "tv.naver.com": "네이버TV",
    "blog.naver.com": "네이버 블로그",
    "smartstore.naver.com": "스마트스토어",
    "kin.naver.com": "지식iN",
    "chzzk.naver.com": "치지직",
    "daangn.com": "당근",
    "threads.net": "스레드",
    "threads.com": "스레드",
    "instagram.com": "인스타그램",
    "youtube.com": "유튜브",
    "story.kakao.com": "카카오스토리",
    "pf.kakao.com": "카카오톡 채널",
    "tistory.com": "티스토리",
    "tiktok.com": "틱톡",
    "facebook.com": "페이스북",
    "x.com": "X(트위터)",
    "twitter.com": "X(트위터)",
}

# LLMO가 노리는 표면은 NEO와 다르다(llmo.md 1절). 같은 sameAs 배열이 두 레인을
# 서로 다른 목표 집합으로 상대하므로, 건수 하나로 뭉쳐 판정하면 둘 다 놓친다.
LLMO_SURFACES = {
    "wikipedia.org": "위키백과",
    "wikidata.org": "위키데이터",
    "namu.wiki": "나무위키",
    "github.com": "GitHub",
    "apps.apple.com": "앱스토어",
    "play.google.com": "구글플레이",
    "youtube.com": "유튜브",
    "linkedin.com": "LinkedIn",
    "crunchbase.com": "Crunchbase",
}

# 값 형식이 기계로 갈리는 속성.
DATE_PROPS = ("datePublished", "dateModified", "dateCreated", "datePosted",
              "validThrough", "validFrom", "uploadDate", "startDate", "endDate", "expires",
              # 구글은 priceValidUntil을 ISO 8601로 명시하고, 지난 날짜면 제품 스니펫이
              # 표시되지 않을 수 있다고 적는다. foundingDate도 ISO 8601 날짜다.
              "priceValidUntil", "foundingDate")
URL_PROPS = ("url", "contentUrl", "embedUrl", "thumbnailUrl", "sameAs", "screenshot")
# 네이버는 totalTime·duration에 ISO-8601 duration을 요구한다(PT30M 꼴).
DURATION_PROPS = ("totalTime", "duration", "cookTime", "prepTime")
# 음수·지수 표기는 네이버 문서가 명시적으로 금지한다.
NUMERIC_PROPS = ("ratingValue", "bestRating", "worstRating", "ratingCount",
                 "reviewCount", "position")

# 오타 탐지용 상용 타입. 이 목록에 없다고 틀린 것이 아니므로 FAIL이 아니라 CHECK다.
# schema.org 어휘 전체는 800종이 넘어 여기에 담지 않는다.
KNOWN_TYPES = {
    "Organization", "Person", "WebSite", "WebPage", "Article", "BlogPosting",
    "NewsArticle", "TechArticle", "Product", "Offer", "AggregateOffer", "Review",
    "AggregateRating", "Rating", "FAQPage", "Question", "Answer", "HowTo", "HowToStep",
    "BreadcrumbList", "ListItem", "ItemList", "SoftwareApplication", "WebApplication",
    "MobileApplication", "VideoObject", "ImageObject", "AudioObject", "MediaObject",
    "PostalAddress", "ContactPoint", "Place", "LocalBusiness", "Restaurant", "Recipe",
    "JobPosting", "Event", "Course", "Book", "Movie", "TVSeries", "TVEpisode",
    "Corporation", "EducationalOrganization", "GovernmentOrganization", "NGO",
    "OnlineStore", "SearchAction", "EntryPoint", "Service", "Brand", "CollectionPage",
    "ProfilePage", "AboutPage", "ContactPage", "QAPage", "Dataset", "SpecialAnnouncement",
    "OpeningHoursSpecification", "GeoCoordinates", "MonetaryAmount", "PriceSpecification",
    "VideoGame", "Blog", "Periodical", "Episode", "Season", "PodcastEpisode", "FAQPage",
    "HowToSection", "HowToTip", "QuantitativeValue", "PropertyValue", "Country", "Language",
    "UnitPriceSpecification", "MerchantReturnPolicy", "OfferShippingDetails", "Occupation",
}

# 이 속성 아래에 놓인 엔티티는 **무엇을 가리키는지 밝히는 자리**이지 그 페이지의
# 리치 결과 주체가 아니다. Review의 itemReviewed에 든 Product에 가격과 평점을 요구하면,
# 리뷰를 정상적으로 마크업한 페이지가 매번 실패한다. 규칙 대조에서만 빼고 값 형식
# 검사는 그대로 적용한다 — 참조된 엔티티라도 날짜와 URL은 형식을 지켜야 한다.
REFERENCE_PROPS = {
    "itemReviewed", "about", "mentions", "subjectOf", "isPartOf", "mainEntityOfPage",
    "publisher", "author", "creator", "provider", "brand", "seller", "sourceOrganization",
    "isRelatedTo", "isSimilarTo", "worksFor", "memberOf", "parentOrganization",
}

# 출처가 같은 문서에서 같은 필수로 지원한다고 밝힌 서브타입. 문자열 완전일치만 보면
# 구글 공식 예제의 @type(NewsArticle, MobileApplication)이 표에 없어 검사를 빠져나간다.
TYPE_ALIASES = {
    "NewsArticle": "Article", "BlogPosting": "Article", "TechArticle": "Article",
    "MobileApplication": "SoftwareApplication", "WebApplication": "SoftwareApplication",
}

# 연관채널을 담을 수 있는 타입. 구글은 "가장 구체적인 Organization 하위유형"을 권하므로
# OnlineStore·LocalBusiness로 선언한 루트가 흔하다. Organization 문자열만 보면 그것들이
# name·url·sameAs를 다 갖추고도 미선언으로 찍힌다.
ORGANIZATION_TYPES = {
    "Organization", "Corporation", "OnlineStore", "OnlineBusiness", "LocalBusiness",
    "Store", "NGO", "EducationalOrganization", "GovernmentOrganization", "MedicalOrganization",
    "SportsOrganization", "Airline", "Restaurant", "NewsMediaOrganization", "Project",
}

ENGINE_TABLES = {"google": GOOGLE, "naver": NAVER}
ENGINE_LABEL = {"google": "구글", "naver": "네이버"}

NAVER_CHANNEL["types"] = tuple(sorted(ORGANIZATION_TYPES | {"Person"}))
