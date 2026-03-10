#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re

PREFIXES = {
    '11': 'Cao Bằng', '12': 'Lạng Sơn', '14': 'Quảng Ninh', '15': 'Hải Phòng', '17': 'Thái Bình', '18': 'Nam Định',
    '19': 'Phú Thọ', '20': 'Thái Nguyên', '21': 'Yên Bái', '22': 'Tuyên Quang', '23': 'Hà Giang', '24': 'Lào Cai',
    '25': 'Lai Châu', '26': 'Sơn La', '27': 'Điện Biên', '28': 'Hòa Bình', '29': 'Hà Nội', '30': 'Hà Nội',
    '31': 'Hà Nội', '32': 'Hà Nội', '33': 'Hà Nội', '34': 'Hải Dương', '35': 'Ninh Bình', '36': 'Thanh Hóa',
    '37': 'Nghệ An', '38': 'Hà Tĩnh', '43': 'Đà Nẵng', '47': 'Đắk Lắk', '48': 'Đắk Nông', '49': 'Lâm Đồng',
    '50': 'TP. Hồ Chí Minh', '51': 'TP. Hồ Chí Minh', '52': 'TP. Hồ Chí Minh', '53': 'TP. Hồ Chí Minh', '54': 'TP. Hồ Chí Minh',
    '59': 'TP. Hồ Chí Minh', '60': 'Đồng Nai', '61': 'Bình Dương', '62': 'Long An', '63': 'Tiền Giang', '64': 'Vĩnh Long',
    '65': 'Cần Thơ', '66': 'Đồng Tháp', '67': 'An Giang', '68': 'Kiên Giang', '69': 'Cà Mau', '70': 'Tây Ninh',
    '71': 'Bến Tre', '72': 'Bà Rịa - Vũng Tàu', '73': 'Quảng Bình', '74': 'Quảng Trị', '75': 'Thừa Thiên Huế',
    '76': 'Quảng Ngãi', '77': 'Bình Định', '78': 'Phú Yên', '79': 'Khánh Hòa', '81': 'Gia Lai', '82': 'Kon Tum',
    '83': 'Sóc Trăng', '84': 'Trà Vinh', '85': 'Ninh Thuận', '86': 'Bình Thuận', '88': 'Vĩnh Phúc', '89': 'Hưng Yên',
    '90': 'Hà Nam', '92': 'Quảng Nam', '93': 'Bình Phước', '94': 'Bạc Liêu', '95': 'Hậu Giang', '97': 'Bắc Kạn',
    '98': 'Bắc Giang', '99': 'Bắc Ninh'
}
SERIES_HINTS = {
    'A': 'xe con dưới 9 chỗ hoặc phương tiện tương đương',
    'B': 'xe chở khách, xe tải nhẹ hoặc nhóm thương mại tùy loại đăng ký',
    'C': 'xe tải, bán tải hoặc phương tiện chở hàng',
    'D': 'xe van hoặc phương tiện chuyên dùng theo nhóm cấp biển',
    'LD': 'xe doanh nghiệp có vốn nước ngoài / thuê nước ngoài (legacy group)',
    'MĐ': 'xe máy điện',
}

def lookup(plate: str) -> dict:
    raw = plate.strip().upper()
    norm = re.sub(r'[^A-Z0-9Đ]', '', raw)
    prefix = norm[:2] if len(norm) >= 2 else None
    series = None
    m = re.match(r'^(\d{2})([A-ZĐ]{1,2})', norm)
    if m:
        prefix, series = m.group(1), m.group(2)
    return {
        'input': plate,
        'normalized': norm,
        'prefix': prefix,
        'province': PREFIXES.get(prefix),
        'series': series,
        'series_hint': SERIES_HINTS.get(series[0] if series and series not in SERIES_HINTS else series) if series else None,
    }

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Lookup Vietnam vehicle license plate prefix')
    ap.add_argument('plate')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    result = lookup(args.plate)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else '\n'.join(f'{k}: {v}' for k, v in result.items()))
