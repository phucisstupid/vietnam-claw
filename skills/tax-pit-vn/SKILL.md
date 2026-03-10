---
name: tax-pit-vn
description: Calculate Vietnam personal income tax (PIT) from gross or taxable monthly salary using common resident-labor assumptions, including insurance deductions and dependent deductions when provided. Use when users ask to estimate net salary, gross-up from net, or explain PIT brackets for Vietnam payroll.
---

# Tax PIT VN

Use this skill for practical Vietnam payroll estimates under common salaried-employee assumptions.

## Default assumptions

Use these defaults unless the user gives different rules:
- resident employee with labor contract
- monthly calculation
- mandatory employee-side insurance applied on the insurance salary base when relevant
- personal deduction: `11,000,000 VND/month`
- dependent deduction: `4,400,000 VND/month/dependent`
- employee insurance rates on insurable salary:
  - social insurance: `8%`
  - health insurance: `1.5%`
  - unemployment insurance: `1%`
- PIT progressive monthly brackets on taxable income:
  1. up to `5,000,000`: `5%`
  2. `>5,000,000` to `10,000,000`: `10%`
  3. `>10,000,000` to `18,000,000`: `15%`
  4. `>18,000,000` to `32,000,000`: `20%`
  5. `>32,000,000` to `52,000,000`: `25%`
  6. `>52,000,000` to `80,000,000`: `30%`
  7. above `80,000,000`: `35%`

Use the bundled script for straightforward monthly gross-to-net estimates:

```bash
python3 "{baseDir}/scripts/tax_pit_vn.py" --gross 30000000 --dependents 1 --json
```

Common usage:
- `--gross <vnd>`: monthly gross salary
- `--dependents <n>`: number of registered dependents
- `--no-insurance`: skip employee insurance deductions for simplified estimates
- `--insurance-base <vnd>`: override the insurable salary base if needed
- `--json`: print structured output

## Workflow

### Gross to net

1. Collect:
   - gross salary
   - number of dependents
   - whether gross includes mandatory insurance base or the user wants a simplified estimate
2. Compute employee insurance deductions.
3. Compute taxable income:
   - `taxable = gross - employee_insurance - personal_deduction - dependent_deduction`
4. Floor taxable income at zero.
5. Apply progressive PIT brackets.
6. Compute net:
   - `net = gross - employee_insurance - PIT`

### Net to gross

1. Ask for the same assumptions because reverse calculation depends heavily on them.
2. Use iterative gross-up if needed.
3. State clearly that reverse estimates are approximate unless the assumptions are fixed.

## Output style

Show the breakdown, not just the final number:
- gross salary
- insurance deductions
- personal deduction
- dependent deduction
- taxable income
- PIT
- net salary

## Notes

- Vietnam payroll rules can change. If the user needs strict legal compliance, call it an estimate unless a maintained rule source is bundled.
- Distinguish between `gross`, `taxable income`, and `net`; users often mix them up.
- If the user provides annual figures, convert carefully and say whether you are using monthly or annual treatment.
