**Summary**
- `PRINTSINGLED` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTSINGLED [<raw text>]`
- `PRINTSINGLED;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLED ...`

**Progress state**
- complete
