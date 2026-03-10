#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re

PROVINCE_ALIASES = {
    'tp hcm': 'TP. Hồ Chí Minh', 'tphcm': 'TP. Hồ Chí Minh', 'hcm': 'TP. Hồ Chí Minh', 'sai gon': 'TP. Hồ Chí Minh', 'ho chi minh': 'TP. Hồ Chí Minh',
    'ha noi': 'Hà Nội', 'hn': 'Hà Nội'
}


def norm_spaces(s: str) -> str:
    s = s.replace('\n', ', ')
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\s*,\s*', ', ', s)
    return s.strip(' ,')


def normalize_province(s: str) -> str:
    key = re.sub(r'[.]', '', s.lower()).strip()
    return PROVINCE_ALIASES.get(key, s.strip())


def parse_address(text: str) -> dict:
    original = text.strip()
    compact = re.sub(r'\D', '', original)
    phone = None
    m = re.search(r'(84|0)\d{9,10}$', compact)
    if m:
        phone = m.group(0)
    text = norm_spaces(original)
    parts = [p.strip() for p in text.split(',') if p.strip()]
    if phone and parts and re.sub(r'\D', '', parts[-1]) == phone:
        parts.pop()
    recipient = None
    if len(parts) >= 2 and not any(k in parts[0].lower() for k in ['phường','quận','huyện','đường','street','ward','district','tp','tỉnh']):
        if re.search(r'[A-Za-zÀ-ỹ]', parts[0]) and not re.search(r'\d', parts[0]):
            recipient = parts.pop(0)
    province = district = ward = None
    if parts:
        province = normalize_province(parts[-1])
        parts = parts[:-1]
    if parts and re.search(r'\b(quận|quan|huyện|huyen|thị xã|thi xa|thành phố|thanh pho|tp\.?|q\.)\b', parts[-1], re.I):
        district = parts[-1]; parts = parts[:-1]
    if parts and re.search(r'\b(phường|phuong|xã|xa|thị trấn|thi tran|p\.)\b', parts[-1], re.I):
        ward = parts[-1]; parts = parts[:-1]
    elif parts and district and not re.search(r'\d', parts[-1]):
        ward = parts[-1]; parts = parts[:-1]
    line1 = ', '.join(parts) if parts else None
    return {
        'original': original,
        'recipient': recipient,
        'phone': phone,
        'line1': line1,
        'ward': ward,
        'district': district,
        'province': province,
    }


def main():
    ap = argparse.ArgumentParser(description='Parse Vietnamese address into practical fields')
    ap.add_argument('address', nargs='+')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    result = parse_address(' '.join(args.address))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for k, v in result.items():
            print(f'{k}: {v}')

if __name__ == '__main__':
    main()
