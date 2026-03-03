**Summary**
- `PRINTVL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTVL <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVL ...`

**Progress state**
- complete
