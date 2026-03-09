---
name: fuel-price-vn
description: Fetch Vietnam fuel prices from public no-key web sources and return current gasoline/diesel price snapshots. Use when users ask about current xăng dầu prices in Vietnam.
---

# Fuel Price VN

Use the script for current Vietnam fuel price snapshots:

```bash
python3 "{baseDir}/scripts/fuel_price_vn.py" --json
```

Common usage:

- `--json`: print structured JSON
- `--limit <n>`: keep the first N parsed price rows (default: 6)

Workflow:

1. Run the script when users ask about current Vietnam fuel prices.
2. Return the parsed price rows, source URL, and fetch timestamp.
3. If the source is unavailable, return the fetch error clearly.

Scope note: this skill depends on a live public source and is best-effort HTML parsing, not an official API contract.