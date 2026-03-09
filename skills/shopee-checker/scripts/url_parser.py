#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from urllib.parse import parse_qs, unquote, urlparse

_SHOPEE_PRODUCT_PATH_RE = re.compile(r"^/product/(\d+)/(\d+)(?:/.*)?$", re.IGNORECASE)
_SHOPEE_SLUG_RE = re.compile(r"^/(?P<slug>.*?)-i\.(?P<shop_id>\d+)\.(?P<item_id>\d+)(?:/.*)?$", re.IGNORECASE)
_DEEP_PRODUCT_RE = re.compile(r"(?:^|/)product/(?P<shop_id>\d+)/(?P<item_id>\d+)(?:$|[/?#])", re.IGNORECASE)
_MARKET_RE = re.compile(r"shopee\.(?P<market>[a-z.]+)$", re.IGNORECASE)
_QUERY_ID_KEYS = {
    "shopid": "shop_id",
    "itemid": "item_id",
    "shop_id": "shop_id",
    "item_id": "item_id",
    "shopid[]": "shop_id",
    "itemid[]": "item_id",
}
_SHOPEE_SHORT_HOSTS = {"shp.ee"}
_SHOPEE_SHORT_SUBDOMAIN_SUFFIX = ".shp.ee"


def _ensure_scheme(url: str) -> str:
    text = url.strip()
    if "://" in text:
        return text
    return f"https://{text}"


def _is_shopee_host(host: str) -> bool:
    if not host:
        return False
    if host.startswith("s.shopee.") or host in _SHOPEE_SHORT_HOSTS or host.endswith(_SHOPEE_SHORT_SUBDOMAIN_SUFFIX):
        return True
    if host == "shopee.vn":
        return True
    return ".shopee." in host or host.startswith("shopee.")


def _host_type(host: str) -> str:
    if host.startswith("s.shopee.") or host in _SHOPEE_SHORT_HOSTS or host.endswith(_SHOPEE_SHORT_SUBDOMAIN_SUFFIX):
        return "short"
    if host == "shopee.vn" or host.startswith("shopee."):
        return "marketplace"
    if ".shopee." in host:
        return "subdomain"
    return "other"


def _extract_market(host: str) -> str | None:
    match = _MARKET_RE.search(host)
    if not match:
        return None
    return match.group("market")


def _to_int(value: str | None) -> int | None:
    if value is None:
        return None
    value = value.strip()
    if not value.isdigit():
        return None
    return int(value)


def _extract_ids_from_query(parsed_query: dict[str, list[str]]) -> tuple[int | None, int | None]:
    values: dict[str, int] = {}
    for key, raw_values in parsed_query.items():
        normalized_key = key.strip().lower()
        target_field = _QUERY_ID_KEYS.get(normalized_key)
        if not target_field or not raw_values:
            continue
        numeric = _to_int(raw_values[0])
        if numeric is not None:
            values[target_field] = numeric
    return values.get("shop_id"), values.get("item_id")


def _extract_ids_from_deeplink(parsed_query: dict[str, list[str]]) -> tuple[int | None, int | None]:
    for raw_values in parsed_query.values():
        for raw in raw_values:
            decoded = unquote(raw or "")
            match = _DEEP_PRODUCT_RE.search(decoded)
            if match:
                return int(match.group("shop_id")), int(match.group("item_id"))
    return None, None


def _canonical_product_url(shop_id: int | None, item_id: int | None) -> str | None:
    if shop_id is None or item_id is None:
        return None
    return f"https://shopee.vn/product/{shop_id}/{item_id}"


def parse_shopee_product_url(url: str) -> dict[str, str | int | bool | None]:
    if not url or not url.strip():
        raise ValueError("URL is required")

    prepared = _ensure_scheme(url)
    parsed = urlparse(prepared)

    host = parsed.netloc.lower()
    host_no_port = host.split(":", 1)[0]
    is_deeplink = parsed.scheme.lower() == "shopee"
    if not is_deeplink and not _is_shopee_host(host_no_port):
        raise ValueError("Not a Shopee URL")

    result: dict[str, str | int | bool | None] = {
        "original_url": url,
        "normalized_url": f"{parsed.scheme}://{parsed.netloc}{parsed.path}" + (f"?{parsed.query}" if parsed.query else ""),
        "host": host_no_port or None,
        "market": _extract_market(host_no_port) if host_no_port else None,
        "host_type": "app_deeplink" if is_deeplink else _host_type(host_no_port),
        "is_short_url": (_host_type(host_no_port) == "short") if host_no_port else False,
        "url_type": "short_link" if ((_host_type(host_no_port) == "short") if host_no_port else False) else "unknown_shopee",
        "is_product_url": False,
        "shop_id": None,
        "item_id": None,
        "slug": None,
        "canonical_product_url": None,
    }

    path_match = _SHOPEE_PRODUCT_PATH_RE.match(parsed.path)
    if path_match:
        result["shop_id"] = int(path_match.group(1))
        result["item_id"] = int(path_match.group(2))
        result["url_type"] = "product_path"
        result["is_product_url"] = True
        result["canonical_product_url"] = _canonical_product_url(result["shop_id"], result["item_id"])
        return result

    slug_match = _SHOPEE_SLUG_RE.match(parsed.path)
    if slug_match:
        slug = slug_match.group("slug").strip().strip("/")
        result["slug"] = slug or None
        result["shop_id"] = int(slug_match.group("shop_id"))
        result["item_id"] = int(slug_match.group("item_id"))
        result["url_type"] = "slug"
        result["is_product_url"] = True
        result["canonical_product_url"] = _canonical_product_url(result["shop_id"], result["item_id"])
        return result

    query = parse_qs(parsed.query)
    shop_id, item_id = _extract_ids_from_query(query)
    if shop_id is None or item_id is None:
        deep_shop_id, deep_item_id = _extract_ids_from_deeplink(query)
        shop_id = shop_id if shop_id is not None else deep_shop_id
        item_id = item_id if item_id is not None else deep_item_id

    if shop_id is not None and item_id is not None:
        result["shop_id"] = shop_id
        result["item_id"] = item_id
        result["url_type"] = "query_or_deeplink_ids"
        result["is_product_url"] = True
        result["canonical_product_url"] = _canonical_product_url(shop_id, item_id)

    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse Shopee product URL metadata.")
    parser.add_argument("url", help="Shopee product URL")
    parser.add_argument("--json", action="store_true", help="Print as JSON")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = parse_shopee_product_url(args.url)
    except ValueError as err:
        raise SystemExit(f"Invalid input: {err}") from err

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for key, value in result.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
