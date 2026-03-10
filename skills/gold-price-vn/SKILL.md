---
name: gold-price-vn
description: Fetch Vietnam gold price snapshots from public no-key web sources and summarize buy/sell prices for common products such as SJC, PNJ, rings, and jewelry gold. Use when users ask about current giá vàng in Vietnam, want a quick buy/sell snapshot, or need a short comparison across common categories.
---

# Gold Price VN

Use the PNJ public gold price page as the default source. It renders a visible table in the browser with update time, region, gold type, buy price, and sell price.

Current implementation note: this skill is browser-driven and works best through `browser.open` + `browser.snapshot` or page evaluation after render.

Default source:
- `https://giavang.pnj.com.vn/`

## Quick workflow

1. Open the PNJ gold price page with the browser tool.
2. Take a snapshot after the page finishes rendering.
3. Read the visible table headed `Bảng giá vàng`.
4. Return the update timestamp plus the most relevant rows for the user's request.
5. If the user did not specify a type, prioritize these rows when present:
   - `SJC`
   - `PNJ`
   - `Nhẫn Trơn PNJ 999.9`
   - major jewelry purity rows such as `999.9`, `999`, `916 (22K)`, `750 (18K)`

## Browser pattern

Use a snapshot-driven flow instead of brittle CSS selectors.

Example:

```text
browser.open url=https://giavang.pnj.com.vn/
browser.snapshot
```

Look for:
- heading/text: `Bảng giá vàng`
- update line: `Giá vàng ngày: ...`
- unit line: usually `Đơn vị: ngàn đồng/lượng`
- table columns: `Khu vực`, `Loại vàng`, `Giá mua`, `Giá bán`

## Response format

Keep replies compact and practical. Include:
- source name
- fetch/update time shown on page
- unit shown on page
- 3-8 relevant rows depending on the question

Suggested style:

- `SJC (TPHCM): mua X, bán Y`
- `PNJ (Hà Nội): mua X, bán Y`
- `Nhẫn Trơn PNJ 999.9: mua X, bán Y`

If multiple regions show the same values, say so instead of repeating every row.

## Notes

- PNJ is a public web source, not an official state API contract.
- Prices can change intraday; prefer the timestamp shown on the page over the local fetch time.
- The page may list values in `ngàn đồng/lượng`; preserve the original unit unless the user asks for conversion.
- If the page fails to render or is unavailable, report the fetch failure clearly and say the result is best-effort.
- If the user asks for another brand and the current source does not expose it clearly, say so rather than guessing.
