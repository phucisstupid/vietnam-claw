---
name: water-bill-vn
description: Estimate Vietnam household water bills from monthly water usage in cubic meters using bundled tiered pricing assumptions, environmental fee, and VAT. Use when users ask to calculate tiền nước, estimate a water bill from m3 usage, or see the breakdown by usage tier.
---

# Water Bill VN

Use the bundled script for a quick household water-bill estimate.

```bash
python3 "{baseDir}/scripts/water_bill_vn.py" --m3 18 --json
```

Common usage:
- `--m3 <number>`: monthly water usage in cubic meters
- `--no-vat`: exclude VAT
- `--no-env-fee`: exclude environmental fee
- `--json`: print structured output

## Workflow

1. Take the user's monthly water usage in m3.
2. Apply the bundled tier prices in order.
3. Add environmental fee and VAT unless disabled.
4. Return total and tier-by-tier breakdown.

## Notes

- This is a practical estimator with bundled assumptions, not a live utility-tariff lookup.
- Water tariffs vary by locality, user type, and policy period. State that clearly when precision matters.
