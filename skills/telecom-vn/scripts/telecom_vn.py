#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re

PREFIXES = {
    '032':'Viettel','033':'Viettel','034':'Viettel','035':'Viettel','036':'Viettel','037':'Viettel','038':'Viettel','039':'Viettel',
    '086':'Viettel','096':'Viettel','097':'Viettel','098':'Viettel',
    '070':'MobiFone','076':'MobiFone','077':'MobiFone','078':'MobiFone','079':'MobiFone','089':'MobiFone','090':'MobiFone','093':'MobiFone',
    '081':'VinaPhone','082':'VinaPhone','083':'VinaPhone','084':'VinaPhone','085':'VinaPhone','088':'VinaPhone','091':'VinaPhone','094':'VinaPhone',
    '056':'Vietnamobile','058':'Vietnamobile','092':'Vietnamobile',
    '059':'Gmobile','099':'Gmobile'
}

def normalize_phone(phone: str) -> tuple[str, str]:
    digits = re.sub(r'\D', '', phone)
    if digits.startswith('84') and len(digits) == 11:
        national = '0' + digits[2:]
        e164 = '+84' + digits[2:]
    elif digits.startswith('0') and len(digits) == 10:
        national = digits
        e164 = '+84' + digits[1:]
    else:
        national = digits
        e164 = None
    return national, e164


def lookup(phone: str) -> dict:
    national, e164 = normalize_phone(phone)
    prefix = national[:3] if len(national) >= 3 else None
    carrier = PREFIXES.get(prefix)
    return {
        'input': phone,
        'national': national,
        'e164': e164,
        'prefix': prefix,
        'carrier': carrier,
        'is_valid_mobile_length': len(national) == 10 and national.startswith('0')
    }

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Lookup Vietnam mobile carrier by prefix')
    ap.add_argument('phone')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    result = lookup(args.phone)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else '\n'.join(f'{k}: {v}' for k, v in result.items()))
