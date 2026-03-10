#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from urllib.request import Request, urlopen

API_URL = 'https://www.vietcombank.com.vn/api/exchangerates?date='


def fetch_rates(currency: str | None = None) -> dict:
    req = Request(API_URL, headers={'User-Agent': 'v-claw-bank-rate-vn/1.0', 'Accept': 'application/json'})
    with urlopen(req, timeout=15) as resp:
        data = json.load(resp)
    rows = data.get('Data', [])
    if currency:
        rows = [r for r in rows if r.get('currencyCode', '').upper() == currency.upper()]
    return {
        'bank': 'Vietcombank',
        'source_url': API_URL,
        'updated_at': data.get('UpdatedDate'),
        'count': len(rows),
        'rows': [
            {
                'currency': r.get('currencyCode'),
                'name': r.get('currencyName'),
                'buy_cash': r.get('cash'),
                'buy_transfer': r.get('transfer'),
                'sell': r.get('sell'),
            }
            for r in rows
        ]
    }


def main():
    ap = argparse.ArgumentParser(description='Fetch Vietnam bank exchange rates from Vietcombank public endpoint')
    ap.add_argument('--currency', help='Currency code such as USD, EUR, JPY')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    result = fetch_rates(args.currency)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"bank: {result['bank']}")
        print(f"updated_at: {result['updated_at']}")
        for row in result['rows']:
            print(f"- {row['currency']}: cash={row['buy_cash']} transfer={row['buy_transfer']} sell={row['sell']}")

if __name__ == '__main__':
    main()
