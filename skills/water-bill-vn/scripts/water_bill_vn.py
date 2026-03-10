#!/usr/bin/env python3
from __future__ import annotations
import argparse, json

# Best-effort generic tier table (m3/month) for household estimation.
TIERS = [
    (10, 5973),
    (10, 7052),
    (10, 8669),
    (float('inf'), 15929),
]
VAT_RATE = 0.05
ENV_FEE_RATE = 0.10  # environmental protection fee over water charge


def calc_bill(m3: float, vat: bool = True, env_fee: bool = True):
    remaining = m3
    start = 0
    rows = []
    subtotal = 0.0
    for limit, price in TIERS:
        if remaining <= 0:
            break
        used = remaining if limit == float('inf') else min(remaining, limit)
        amount = used * price
        end = start + used
        rows.append({
            'from_m3': int(start + 1),
            'to_m3': None if limit == float('inf') else int(end),
            'used_m3': used,
            'unit_price_vnd': price,
            'amount_vnd': round(amount),
        })
        subtotal += amount
        remaining -= used
        start = end
    env = subtotal * ENV_FEE_RATE if env_fee else 0.0
    vat_amount = (subtotal + env) * VAT_RATE if vat else 0.0
    total = subtotal + env + vat_amount
    return {
        'm3': m3,
        'water_charge_vnd': round(subtotal),
        'environment_fee_vnd': round(env),
        'vat_vnd': round(vat_amount),
        'total_vnd': round(total),
        'tiers': rows,
        'assumptions': {'vat': vat, 'environment_fee': env_fee}
    }

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Estimate Vietnam household water bill from m3 usage')
    ap.add_argument('--m3', type=float, required=True)
    ap.add_argument('--no-vat', action='store_true')
    ap.add_argument('--no-env-fee', action='store_true')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    result = calc_bill(args.m3, vat=not args.no_vat, env_fee=not args.no_env_fee)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else '\n'.join(f'{k}: {v}' for k, v in result.items()))
