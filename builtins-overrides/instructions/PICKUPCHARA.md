**Summary**
- Keeps only the selected registered characters, reorders them to match the selection order, and deletes the rest.

**Tags**
- characters

**Syntax**
- `PICKUPCHARA <charaID> [, <charaID> ... ]`

**Arguments**
- `<charaID>` (int): selects a currently registered character index.

**Semantics**
- Evaluates all arguments left-to-right.
- For ordinary expressions, each value must be a valid current character index.
- If an argument is the variable `MASTER`, `TARGET`, or `ASSI`, a negative value is ignored instead of rejected.
- After evaluation, the engine removes duplicate non-negative selections while preserving first-appearance order.
- The selected characters are moved to the front of the character list in that deduplicated order, and all remaining characters are deleted.
- `MASTER`, `TARGET`, and `ASSI` are then rebound to the new indices of their old characters if those characters survived; otherwise they become `-1`.

**Errors & validation**
- Parse / argument-validation error if no argument is supplied.
- Runtime error if an ordinary argument is outside the current character range.
- `MASTER`, `TARGET`, and `ASSI` participate with their current numeric values. Their negative case is ignored; other invalid values are not guaranteed to succeed.

**Examples**
- `PICKUPCHARA MASTER, TARGET`
- `PICKUPCHARA 3, 1, 3`

**Progress state**
- complete
