#!/usr/bin/env python3
"""HTTP 회수 — 자바스크립트를 실행하지 않고 응답만 받는다."""

import gzip
import ssl
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_UA = "search-visibility-audit/1.0 (+skill: search-visibility)"
MAX_BYTES = 3_000_000


def fetch(url, ua=DEFAULT_UA, timeout=10.0, max_bytes=MAX_BYTES):
    """(status, final_url, headers, body, hops, error)를 돌려준다. 예외를 던지지 않는다."""
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Encoding": "gzip"})
    hops = 0

    class Counter(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            nonlocal hops
            hops += 1
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    opener = urllib.request.build_opener(Counter, urllib.request.HTTPSHandler(context=ctx))
    try:
        with opener.open(req, timeout=timeout) as resp:
            raw = resp.read(max_bytes)
            if resp.headers.get("Content-Encoding") == "gzip":
                try:
                    raw = gzip.decompress(raw)
                except OSError:
                    pass
            charset = resp.headers.get_content_charset() or "utf-8"
            return (resp.status, resp.geturl(), dict(resp.headers),
                    raw.decode(charset, "replace"), hops, None)
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read(max_bytes).decode("utf-8", "replace")
        except Exception:  # noqa: BLE001 - 본문은 부가 정보다
            pass
        return exc.code, url, dict(exc.headers or {}), body, hops, None
    except Exception as exc:  # noqa: BLE001 - 네트워크 오류도 관측 결과다
        return None, url, {}, "", hops, "{}: {}".format(type(exc).__name__, exc)


def header(headers, name):
    """HTTP/2는 헤더 이름을 소문자로 준다. 대소문자를 무시하고 찾는다."""
    for key, value in (headers or {}).items():
        if key.lower() == name.lower():
            return value
    return ""


def head_status(url, ua=DEFAULT_UA, timeout=10.0):
    """본문을 받지 않고 상태 코드만 확인한다(자산 실존 확인용)."""
    status, _, headers, _, _, error = fetch(url, ua, timeout, max_bytes=2048)
    return status, header(headers, "Content-Type").split(";")[0], error


def join(base, path):
    return urllib.parse.urljoin(base, path)


def same_origin(a, b):
    pa, pb = urllib.parse.urlparse(a), urllib.parse.urlparse(b)
    return (pa.scheme, pa.netloc) == (pb.scheme, pb.netloc)
