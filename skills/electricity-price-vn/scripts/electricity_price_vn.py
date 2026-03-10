#!/usr/bin/env python3
from __future__ import annotations
import argparse, json

TIERS = [
    (50, 1806),
    (50, 1866),
    (100, 2167),
    (100, 2729),
    (100, 3050),
    (float('inf'), 3151),
]
VAT_RATE = 0.10


def calc_bill(kwh: float, vat: bool = True):
    remaining = kwh
    start = 0
    rows = []
    subtotal = 0.0
    for limit, price in TIERS:
        if remaining <= 0:
            break
        used = remaining if limit == float('inf') else min(remaining, limit)
        amount = used * price
        end = start + used
        rows.append({'from_kwh': int(start + 1), 'to_kwh': None if limit == float('inf') else int(end), 'used_kwh': used, 'unit_price_vnd': price, 'amount_vnd': round(amount)})
        subtotal += amount
        remaining -= used
        start = end
    vat_amount = subtotal * VAT_RATE if vat else 0.0
    total = subtotal + vat_amount
    return {'kwh': kwh, 'subtotal_vnd': round(subtotal), 'vat_vnd': round(vat_amount), 'total_vnd': round(total), 'tiers': rows}

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Estimate Vietnam residential electricity bill from tiered pricing')
    ap.add_argument('--kwh', type=float, required=True)
    ap.add_argument('--no-vat', action='store_true')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    result = calc_bill(args.kwh, vat=not args.no_vat)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else '\n'.join(f'{k}: {v}' for k, v in result.items()))
