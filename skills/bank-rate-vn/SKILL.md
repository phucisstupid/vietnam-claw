---
name: bank-rate-vn
description: Fetch Vietnam bank exchange-rate snapshots from public no-key bank pages and summarize buy/sell/transfer rates for common currencies such as USD, EUR, JPY, and GBP. Use when users ask for tỷ giá ngân hàng in Vietnam, want a quick bank comparison, or need a current buy/sell snapshot from one or more banks.
---

# Bank Rate VN

Use public bank exchange-rate pages and return a compact snapshot.

Use the bundled script for Vietcombank public exchange-rate snapshots:

```bash
python3 "{baseDir}/scripts/bank_rate_vn.py" --currency USD --json
```

Common usage:
- `--currency <code>`: currency code such as `USD`, `EUR`, `JPY`
- `--json`: print structured JSON

## Quick workflow

1. Identify the currency the user cares about, defaulting to `USD` if omitted.
2. Identify the bank if specified. If not specified, prefer common banks with public pages such as Vietcombank or BIDV.
3. Fetch the public rate page with `web_fetch` for static pages, or `browser` if the page is rendered dynamically.
4. Extract the visible fields for the requested currency. Common columns are:
   - cash buy
   - transfer buy
   - sell
5. Return the bank name, timestamp if shown, currency, and the extracted rates.

## Good defaults

If the user only says things like `tỷ giá USD hôm nay`, prioritize:
- Vietcombank
- BIDV
- VietinBank
- ACB

If comparing banks, keep the reply short and practical. Highlight:
- highest buy rate
- lowest sell rate
- timestamp/source used

## Response style

Prefer bullet points, for example:

- `Vietcombank — USD: mua tiền mặt X, mua chuyển khoản Y, bán Z`
- `BIDV — USD: mua tiền mặt X, mua chuyển khoản Y, bán Z`

Then add one-line takeaway if comparison was requested.

## Notes

- Bank pages are public web sources, not stable APIs.
- Some banks split rates by cash vs transfer; preserve the labels instead of collapsing them.
- If a page renders poorly or blocks fetching, say the result is best-effort and switch to another public bank page if that still answers the user's question.
- Do not guess missing rates.
