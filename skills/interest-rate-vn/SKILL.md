---
name: interest-rate-vn
description: Fetch Vietnam bank savings-interest snapshots from public no-key sources and summarize deposit rates by term for common banks. Use when users ask about lãi suất tiết kiệm in Vietnam, compare banks by tenor, or want a quick monthly/quarterly/yearly term snapshot.
---

# Interest Rate VN

Use public bank or financial comparison pages to summarize savings-deposit rates.

Use the bundled script for a quick Saigonbank savings snapshot:

```bash
python3 "{baseDir}/scripts/interest_rate_vn.py" --tenor "6 months" --tenor "12 months" --json
```

Common usage:
- `--tenor <label>`: tenor like `6 months` or `12 months` (repeatable)
- `--json`: print structured JSON

## Quick workflow

1. Identify the requested tenor if present, such as `1 tháng`, `3 tháng`, `6 tháng`, `12 tháng`, or `24 tháng`.
2. Identify the bank if specified. If omitted, compare a few major banks.
3. Fetch the relevant public page with `web_fetch` or `browser`.
4. Extract only the tenors relevant to the user's question.
5. Return rates with source and any important conditions shown on-page, such as online-only or minimum deposit requirements.

## Good defaults

If the user says only `lãi suất tiết kiệm hôm nay`, prioritize a compact comparison for:
- 6 months
- 12 months
- 24 months

Use a few major banks rather than too many rows.

## Response style

Keep it compact:

- `Bank A — 6T X%, 12T Y%, 24T Z%`
- `Bank B — 6T X%, 12T Y%, 24T Z%`

Then add one-line takeaway such as which bank is highest for the requested tenor.

## Notes

- Rates often differ by channel: counter, online, or promotional products. Preserve that context when visible.
- Prefer exact tenor labels from the page over inferred conversions.
- If multiple products appear on the same bank page, choose the plain retail savings product unless the user asked for something else.
- Do not guess missing terms.
