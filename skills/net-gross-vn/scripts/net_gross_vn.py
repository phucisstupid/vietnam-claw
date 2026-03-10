#!/usr/bin/env python3
from __future__ import annotations
import argparse, json

PERSONAL_DEDUCTION = 11_000_000
DEPENDENT_DEDUCTION = 4_400_000
INS_RATE = 0.105
BRACKETS = [
    (5_000_000, 0.05), (10_000_000, 0.10), (18_000_000, 0.15), (32_000_000, 0.20), (52_000_000, 0.25), (80_000_000, 0.30), (float('inf'), 0.35)
]

def pit(taxable: float) -> float:
    if taxable <= 0: return 0.0
    tax = 0.0; lower = 0.0
    for upper, rate in BRACKETS:
        portion = min(taxable, upper) - lower
        if portion > 0: tax += portion * rate
        if taxable <= upper: break
        lower = upper
    return tax

def gross_to_net(gross: float, dependents: int = 0):
    ins = gross * INS_RATE
    dep = dependents * DEPENDENT_DEDUCTION
    taxable = max(0.0, gross - ins - PERSONAL_DEDUCTION - dep)
    tax = pit(taxable)
    net = gross - ins - tax
    return {'mode':'gross_to_net','gross':round(gross),'insurance_deduction':round(ins),'taxable_income':round(taxable),'pit':round(tax),'net':round(net),'dependents':dependents}

def net_to_gross(net: float, dependents: int = 0):
    lo, hi = net, max(net * 2, 20_000_000)
    while gross_to_net(hi, dependents)['net'] < net:
        hi *= 1.5
    for _ in range(80):
        mid = (lo + hi) / 2
        if gross_to_net(mid, dependents)['net'] < net:
            lo = mid
        else:
            hi = mid
    res = gross_to_net(hi, dependents)
    res['mode'] = 'net_to_gross'
    res['target_net'] = round(net)
    return res

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Convert Vietnam monthly salary between gross and net using common assumptions')
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--gross', type=float)
    g.add_argument('--net', type=float)
    ap.add_argument('--dependents', type=int, default=0)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    result = gross_to_net(args.gross, args.dependents) if args.gross is not None else net_to_gross(args.net, args.dependents)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else '\n'.join(f'{k}: {v}' for k, v in result.items()))
