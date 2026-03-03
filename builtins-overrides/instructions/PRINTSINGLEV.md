**Summary**
- `PRINTSINGLEV` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTSINGLEV <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEV ...`

**Progress state**
- complete
