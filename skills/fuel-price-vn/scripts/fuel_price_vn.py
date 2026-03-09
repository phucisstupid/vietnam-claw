#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from html import unescape
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SOURCE_URL = "https://www.globalpetrolprices.com/Vietnam/gasoline_prices/"

_ROW_RE = re.compile(r"<tr[^>]*>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*</tr>", re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def _strip_html(text: str) -> str:
    no_tags = _TAG_RE.sub(" ", unescape(text))
    return _WS_RE.sub(" ", no_tags).strip()


def _fetch_html(url: str, timeout: float = 12.0) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": "v-claw-fuel-price-vn/1.0",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_price_rows(html: str, limit: int = 6) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for left, right in _ROW_RE.findall(html):
        label = _strip_html(left)
        value = _strip_html(right)
        if not label or not value:
            continue
        if len(label) > 80 or len(value) > 120:
            continue
        if label.lower() in {"currency", "u.s. gallon", "liter"}:
            continue
        rows.append({"label": label, "value": value})

    cleaned: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for row in rows:
        pair = (row["label"], row["value"])
        if pair in seen:
            continue
        seen.add(pair)
        cleaned.append(row)
        if len(cleaned) >= limit:
            break
    return cleaned


def fetch_fuel_prices(limit: int = 6) -> dict[str, object]:
    if limit < 1:
        raise ValueError("limit must be >= 1")
    try:
        html = _fetch_html(SOURCE_URL)
    except HTTPError as err:
        raise RuntimeError(f"Fuel price source returned HTTP {err.code}") from err
    except URLError as err:
        raise RuntimeError(f"Fuel price source unavailable: {err.reason}") from err
    except TimeoutError as err:
        raise RuntimeError("Fuel price source timed out") from err

    rows = parse_price_rows(html, limit=limit)
    if not rows:
        raise RuntimeError("Fuel price page format was not recognized")

    return {
        "country": "Vietnam",
        "source": "GlobalPetrolPrices public page",
        "source_url": SOURCE_URL,
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "rows": rows,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Vietnam fuel price snapshot from a public source")
    parser.add_argument("--limit", type=int, default=6, help="Max parsed rows to return (default: 6)")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = fetch_fuel_prices(limit=args.limit)
    except ValueError as err:
        raise SystemExit(f"Invalid input: {err}") from err
    except RuntimeError as err:
        raise SystemExit(f"Fetch error: {err}") from err

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"country: {result['country']}")
    print(f"source: {result['source']}")
    print("rows:")
    for row in result["rows"]:
        print(f"- {row['label']}: {row['value']}")


if __name__ == "__main__":
    main()
