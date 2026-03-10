#!/usr/bin/env python3
from __future__ import annotations
import argparse, json

FOODS = {
    'pho bo': {'kcal': 450, 'portion': '1 tô'},
    'pho ga': {'kcal': 400, 'portion': '1 tô'},
    'bun bo hue': {'kcal': 650, 'portion': '1 tô'},
    'com tam suon': {'kcal': 700, 'portion': '1 phần'},
    'banh mi thit': {'kcal': 430, 'portion': '1 ổ'},
    'banh mi trung': {'kcal': 380, 'portion': '1 ổ'},
    'goi cuon': {'kcal': 90, 'portion': '1 cuốn'},
    'cha gio': {'kcal': 130, 'portion': '1 cuốn'},
    'bun cha': {'kcal': 600, 'portion': '1 phần'},
    'hu tieu': {'kcal': 500, 'portion': '1 tô'},
    'mi quang': {'kcal': 520, 'portion': '1 tô'},
    'tra sua': {'kcal': 350, 'portion': '1 ly'},
    'ca phe sua da': {'kcal': 120, 'portion': '1 ly'},
}
ALIASES = {
    'phở bò':'pho bo','phở gà':'pho ga','bún bò huế':'bun bo hue','cơm tấm sườn':'com tam suon',
    'bánh mì thịt':'banh mi thit','bánh mì trứng':'banh mi trung','gỏi cuốn':'goi cuon','chả giò':'cha gio',
    'bún chả':'bun cha','hủ tiếu':'hu tieu','mì quảng':'mi quang','trà sữa':'tra sua','cà phê sữa đá':'ca phe sua da'
}

def normalize(name: str) -> str:
    s = name.strip().lower()
    return ALIASES.get(s, s)


def lookup(food: str, servings: float = 1.0) -> dict:
    key = normalize(food)
    base = FOODS.get(key)
    if not base:
        return {'query': food, 'matched': None, 'found': False}
    total = round(base['kcal'] * servings)
    return {'query': food, 'matched': key, 'found': True, 'portion': base['portion'], 'kcal_per_portion': base['kcal'], 'servings': servings, 'estimated_kcal': total}

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Estimate calories for common Vietnamese foods')
    ap.add_argument('food', nargs='+')
    ap.add_argument('--servings', type=float, default=1.0)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    result = lookup(' '.join(args.food), args.servings)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else '\n'.join(f'{k}: {v}' for k, v in result.items()))
