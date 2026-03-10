---
name: food-calorie-vn
description: Estimate calories for common Vietnamese foods and drinks from a bundled lookup table with portion-based heuristics. Use when users ask how many calories are in a Vietnamese dish, want a rough meal estimate, or need a simple calorie snapshot for familiar VN foods.
---

# Food Calorie VN

Use the bundled script for quick calorie estimates.

```bash
python3 "{baseDir}/scripts/food_calorie_vn.py" "phở bò" --servings 1.5 --json
```

Common usage:
- pass a Vietnamese dish or drink name
- `--servings <n>`: multiply by serving count
- `--json`: print structured output

## Workflow

1. Normalize the food name to a bundled alias if available.
2. Look up the base calories per portion.
3. Multiply by servings if provided.
4. Return the estimate with a short caution that calories vary by recipe and toppings.

## Notes

- This is a practical heuristic table, not a nutrition database.
- Dish calories can vary a lot by portion size, sugar, oil, broth, and add-ons.
