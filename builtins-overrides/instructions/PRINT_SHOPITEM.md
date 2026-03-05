**Summary**
- Prints a grid of items currently for sale in the shop (based on `ITEMSALES`), including their indices and prices.

**Tags**
- io

**Syntax**
- `PRINT_SHOPITEM`

**Arguments**
- None.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Let:
  - `sales = ITEMSALES` (numeric array)
  - `names = ITEMNAME` (CSV name list; string array)
  - `prices = ITEMPRICE` (numeric array)
- Iterates `i` such that `0 <= i < length`, where:
  - `length = min(sales.Length, names.Length)`, then
  - if `length > prices.Length`, `length = prices.Length`.
- An item is considered “for sale” iff:
  - `sales[i] != 0`, and
  - `names[i] != null`.
- For each `i` that is for sale:
  - Let `name = names[i]` (engine also guards against null by treating it as `""`, but the sale predicate rejects null names).
  - Let `price = prices[i]`.
  - Format the cell text as:
    - If `MoneyFirst` is true: `[{i}] {name}({MoneyLabel}{price})`
    - Otherwise: `[{i}] {name}({price}{MoneyLabel})`
  - Prints the cell using `PRINTC`-style formatting with left alignment.
  - Increments a per-line cell counter and flushes every `PrintCPerLine` cells when `PrintCPerLine > 0`.
- After finishing the loop, it flushes pending output and refreshes the display.
- This instruction does not automatically append a trailing newline.

**Errors & validation**
- None specific to this instruction.

**Examples**
- `PRINT_SHOPITEM`

**Progress state**
- complete
