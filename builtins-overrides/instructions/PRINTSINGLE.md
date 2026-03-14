**Summary**
- `PRINTSINGLE` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLE [<raw text>]`
- `PRINTSINGLE;[<raw text>]`

**Arguments**
- `<raw text>` (optional, raw text, default `""`): raw literal text, not an expression.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLE ...`

**Progress state**
- complete
