**Summary**
- `PRINTSINGLES` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTSINGLES <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLES ...`

**Progress state**
- complete
