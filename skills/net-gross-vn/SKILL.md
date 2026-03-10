---
name: net-gross-vn
description: Convert Vietnam monthly salary between gross and net under common resident-employee assumptions, including mandatory employee insurance and PIT. Use when users ask gross-to-net, net-to-gross, or want a practical payroll conversion for Vietnam salaries.
---

# Net Gross VN

Use the bundled script for practical salary conversion.

```bash
python3 "{baseDir}/scripts/net_gross_vn.py" --gross 30000000 --dependents 1 --json
```

Common usage:
- `--gross <vnd>`: convert gross monthly salary to net
- `--net <vnd>`: estimate gross needed to reach a target net salary
- `--dependents <n>`: registered dependents
- `--json`: print structured output

## Workflow

1. Determine whether the user gave gross or net.
2. Apply common employee-side insurance assumptions.
3. Compute PIT using monthly progressive brackets.
4. Return the full breakdown, not just the final figure.

## Notes

- This is a practical estimator, not legal payroll advice.
- Reverse net-to-gross uses iterative approximation.
- If the user's payroll setup has special insurance caps or nonstandard benefits, say the output is approximate.
