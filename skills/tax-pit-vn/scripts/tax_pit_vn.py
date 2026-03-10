#!/usr/bin/env python3
from __future__ import annotations
import argparse, json

PERSONAL_DEDUCTION = 11_000_000
DEPENDENT_DEDUCTION = 4_400_000
SI_RATE = 0.08
HI_RATE = 0.015
UI_RATE = 0.01
BRACKETS = [
    (5_000_000, 0.05),
    (10_000_000, 0.10),
    (18_000_000, 0.15),
    (32_000_000, 0.20),
    (52_000_000, 0.25),
    (80_000_000, 0.30),
    (float('inf'), 0.35),
]


def calc_progressive_tax(taxable: float) -> float:
    if taxable <= 0:
        return 0.0
    tax = 0.0
    lower = 0.0
    for upper, rate in BRACKETS:
        portion = min(taxable, upper) - lower
        if portion > 0:
            tax += portion * rate
        if taxable <= upper:
            break
        lower = upper
    return tax


def calc_from_gross(gross: float, dependents: int = 0, insurance: bool = True, insurance_base: float | None = None):
    base = gross if insurance_base is None else min(gross, insurance_base)
    ins = base * (SI_RATE + HI_RATE + UI_RATE) if insurance else 0.0
    dep = dependents * DEPENDENT_DEDUCTION
    taxable = max(0.0, gross - ins - PERSONAL_DEDUCTION - dep)
    pit = calc_progressive_tax(taxable)
    net = gross - ins - pit
    return {
        'gross': round(gross),
        'insurance_deduction': round(ins),
        'personal_deduction': PERSONAL_DEDUCTION,
        'dependent_deduction': round(dep),
        'taxable_income': round(taxable),
        'pit': round(pit),
        'net': round(net),
        'assumptions': {
            'insurance_enabled': insurance,
            'dependents': dependents,
            'insurance_base': round(base),
        }
    }


def main():
    p = argparse.ArgumentParser(description='Estimate Vietnam PIT from monthly gross salary')
    p.add_argument('--gross', type=float, required=True)
    p.add_argument('--dependents', type=int, default=0)
    p.add_argument('--no-insurance', action='store_true')
    p.add_argument('--insurance-base', type=float)
    p.add_argument('--json', action='store_true')
    args = p.parse_args()
    result = calc_from_gross(args.gross, args.dependents, not args.no_insurance, args.insurance_base)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for k, v in result.items():
            print(f'{k}: {v}')

if __name__ == '__main__':
    main()
