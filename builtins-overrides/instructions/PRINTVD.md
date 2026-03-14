**Summary**
- `PRINTVD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTVD <expr1> [, <expr2> ...]`

**Arguments**
- `<expr1>` (int|string): first expression to evaluate and append.
- `<expr2>` (optional, int|string): each additional comma-separated expression to evaluate and append; may repeat zero or more times.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVD ...`

**Progress state**
- complete
