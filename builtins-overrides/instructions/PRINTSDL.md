**Summary**
- `PRINTSDL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTSDL <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSDL ...`

**Progress state**
- complete
