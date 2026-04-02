**Summary**
- Tries a list of candidate `$label` targets and jumps to the first one that exists; otherwise jumps to `ENDFUNC` (end of the list).

**Tags**
- calls

**Syntax**
```text
TRYGOTOLIST
    FUNC <formString>
    ...
ENDFUNC
```

- Header line: `TRYGOTOLIST`
- Item lines: `FUNC <formString>` (see `FUNC`; this variant forbids subnames and arguments)
- Terminator line: `ENDFUNC`

**Arguments**
- Each `FUNC` item provides a label name as a **FORM/formatted string expression** (evaluated to a string at runtime).

**Semantics**
- Structural notes:
  - The lines between `TRYGOTOLIST` and `ENDFUNC` are list items, not a normal executable block body (same model as `TRYCALLLIST`).
- Runtime algorithm:
  - For each `FUNC` item in source order:
    - Evaluate the candidate name to a string.
    - Resolve it as a `$label` inside the **current function**.
    - If it exists, jump to it and stop searching.
  - If no candidate exists, jump to the `ENDFUNC` line (then continue after it).

**Errors & validation**
- Load-time structure errors (the line is marked as error) follow `TRYCALLLIST`.
- Additional load-time restriction: in a `TRYGOTOLIST` block, each `FUNC` item must be a plain candidate name only:
  - no `[...]` subname segment
  - no argument list (neither `(... )` nor `, ...`)

**Examples**
```erabasic
TRYGOTOLIST
    FUNC LABEL_{RESULT}
    FUNC LABEL_DEFAULT
ENDFUNC
```

**Progress state**
- complete
