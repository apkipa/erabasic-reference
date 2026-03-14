**Summary**
- `PRINTSINGLED` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLED [<raw text>]`
- `PRINTSINGLED;[<raw text>]`

**Arguments**
- `<raw text>` (optional, raw text, default `""`): raw literal text, not an expression.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLED ...`

**Progress state**
- complete
