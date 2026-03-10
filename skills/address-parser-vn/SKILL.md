---
name: address-parser-vn
description: Parse and normalize Vietnamese addresses into practical components such as street/house number, ward-level unit, district-level unit, and province/city. Use when users paste shipping addresses, want cleaner formatting, need accent-insensitive normalization, or ask to split an address into structured fields.
---

# Address Parser VN

Use lightweight heuristics to split Vietnamese addresses into useful shipping-style fields.

Use the bundled script for quick structured parsing:

```bash
python3 "{baseDir}/scripts/address_parser_vn.py" "12 Nguyen Hue, Phuong Ben Nghe, Quan 1, TP HCM" --json
```

Common usage:
- pass the full address as one quoted argument
- `--json`: print structured output

## Workflow

1. Preserve the original address text.
2. Normalize whitespace, commas, repeated separators, and obvious OCR noise.
3. Split from right to left because Vietnamese addresses usually end with province/city, then district-level unit, then ward-level unit, then street/house details.
4. Extract these fields when possible:
   - `recipient` if clearly present on a separate line
   - `phone` if present
   - `line1` for house number, alley, street, apartment, building
   - `ward`
   - `district`
   - `province`
5. If province/city matching is ambiguous, use the separate `viet-geo` skill for accent-insensitive normalization and province metadata.
6. If a phone number is present, use the `vn-phone` skill when the user needs normalization.

## Parsing hints

Common tokens:
- ward-level: `phường`, `xã`, `thị trấn`
- district-level: `quận`, `huyện`, `thị xã`, `thành phố`
- province-level: `tỉnh`, `thành phố`

Common normalization examples:
- `tp hcm`, `tphcm`, `sai gon` -> `TP. Hồ Chí Minh`
- `hn`, `ha noi` -> `Hà Nội`

## Response style

When the user wants structure, return fields explicitly:

- `line1:` ...
- `ward:` ...
- `district:` ...
- `province:` ...
- `phone:` ...

When confidence is partial, say which segment is uncertain instead of forcing a bad parse.

## Notes

- Vietnamese addresses are messy and often omit prefixes like `Phường` or `Quận`; use best-effort heuristics.
- Do not silently rewrite meaningful building or apartment details.
- Preserve the original text when returning a normalized version.
