---
name: license-plate-vn
description: Look up Vietnamese vehicle license plate prefixes and return the likely province/city plus a simple series hint when available. Use when users ask a biển số xe belongs to which province, want a quick registration-region lookup, or need a lightweight interpretation of a Vietnamese plate string.
---

# License Plate VN

Use the bundled script for quick province lookup from a Vietnamese vehicle plate.

```bash
python3 "{baseDir}/scripts/license_plate_vn.py" "51A-123.45" --json
```

Common usage:
- pass a plate like `30A-123.45`, `51A-123.45`, or `59M2-123.45`
- `--json`: print structured output

## Workflow

1. Normalize the plate by removing separators and uppercasing.
2. Read the first two digits as the registration prefix.
3. Map the prefix to the likely province/city.
4. When possible, return a simple series hint such as passenger car or truck-oriented group.

## Notes

- Prefix lookups are practical heuristics, not a legal registry query.
- Some locations use multiple prefixes.
- Series letters are only a lightweight hint and should not be overclaimed.
