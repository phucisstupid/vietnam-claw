#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from urllib.request import Request, urlopen

URL = 'https://www.saigonbank.com.vn/en/quick-access/savings'


def fetch_text() -> str:
    req = Request(URL, headers={'User-Agent': 'v-claw-interest-rate-vn/1.0'})
    with urlopen(req, timeout=15) as resp:
        return resp.read().decode('utf-8', 'replace')


def parse_rates(text: str) -> tuple[str | None, list[dict]]:
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = clean.replace('&nbsp;', ' ')
    clean = re.sub(r'\s+', ' ', clean)
    eff = None
    m = re.search(r'Interest rate for savings account in VND for individual.*?Effective date:?\s*([0-9 ]+/[0-9]{2}/[0-9]{4})', clean, re.I)
    if m:
        eff = m.group(1).replace(' ', '')
    start = clean.rfind('Interest rate for savings account in VND for individual')
    end = clean.find('Interest rate for current account in VND for individual and corporate clients', start + 1)
    block = clean[start:end] if start != -1 and end != -1 else clean
    pattern = re.compile(r'(\d{2})\s*(week|weeks|month|months)\s+([0-9],[0-9]{2})%', re.I)
    rows = []
    for num, unit, rate in pattern.findall(block):
        n = int(num)
        base = 'week' if unit.lower().startswith('week') else 'month'
        tenor = f"{n} {base if n == 1 else base + 's'}"
        rows.append({'tenor': tenor, 'rate_percent': rate.replace(',', '.')})
    seen = set()
    out = []
    for r in rows:
        if r['tenor'] in seen:
            continue
        seen.add(r['tenor'])
        out.append(r)
    return eff, out


def _norm_tenor(t: str) -> str:
    m = re.search(r'(\d+)\s*(week|weeks|month|months)', t.lower())
    if not m:
        return t.strip().lower()
    n = int(m.group(1))
    base = 'week' if m.group(2).startswith('week') else 'month'
    return f"{n} {base if n == 1 else base + 's'}"


def select_tenors(rows: list[dict], tenors: list[str] | None):
    if not tenors:
        return rows
    norm = {_norm_tenor(t) for t in tenors}
    return [r for r in rows if _norm_tenor(r['tenor']) in norm]


def main():
    ap = argparse.ArgumentParser(description='Fetch VN savings interest snapshot from Saigonbank public page')
    ap.add_argument('--tenor', action='append', help='Tenor like "6 months" or "12 months"; repeatable')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    text = fetch_text()
    eff, rows = parse_rates(text)
    rows = select_tenors(rows, args.tenor)
    result = {'bank': 'Saigonbank', 'source_url': URL, 'effective_date': eff, 'rows': rows}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"bank: {result['bank']}")
        print(f"effective_date: {result['effective_date']}")
        for r in result['rows']:
            print(f"- {r['tenor']}: {r['rate_percent']}%")

if __name__ == '__main__':
    main()
