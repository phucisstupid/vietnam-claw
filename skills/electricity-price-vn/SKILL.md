---
name: electricity-price-vn
description: Estimate Vietnam residential electricity bills from monthly kWh usage using tiered VND pricing and optional VAT. Use when users ask to calculate tiền điện, estimate a household bill from kWh, or see how usage spreads across residential pricing tiers in Vietnam.
---

# Electricity Price VN

Use the bundled script for a quick residential bill estimate.

```bash
python3 "{baseDir}/scripts/electricity_price_vn.py" --kwh 235 --json
```

Common usage:
- `--kwh <number>`: monthly electricity consumption
- `--no-vat`: exclude VAT from the estimate
- `--json`: print structured output

## Workflow

1. Take the user's monthly kWh usage.
2. Apply the configured residential tier prices in order.
3. Return per-tier usage and subtotal.
4. Add VAT unless the user asked to exclude it.

## Output style

Return:
- total kWh
- subtotal before VAT
- VAT
- final total
- tier breakdown

## Notes

- This skill is an estimator based on bundled tier assumptions, not a live EVN tariff fetch.
- If the user needs strict compliance to the latest tariff decision, say so and verify the tier table before relying on the output.
