---
name: telecom-vn
description: Normalize Vietnamese mobile phone numbers and infer the likely carrier from the mobile prefix. Use when users share a Vietnam phone number and want a quick nhà mạng check, normalized +84 format, or basic validity sanity check.
---

# Telecom VN

Use the bundled script for quick carrier lookup by prefix.

```bash
python3 "{baseDir}/scripts/telecom_vn.py" "0981234567" --json
```

Common usage:
- pass a phone number in national or `+84` format
- `--json`: print structured output

## Workflow

1. Strip separators and normalize the phone number.
2. Convert to national and `+84` format when possible.
3. Read the first three digits of the national mobile number.
4. Map the prefix to a likely carrier such as Viettel, VinaPhone, or MobiFone.

## Notes

- Prefix mapping is best-effort and does not reflect number portability.
- For full phone normalization workflows, pair this with the separate `vn-phone` skill.
