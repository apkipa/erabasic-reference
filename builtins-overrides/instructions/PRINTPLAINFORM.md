**Summary**
- Like `PRINTPLAIN`, but reads its argument as a FORM/formatted string.

**Tags**
- io

**Syntax**
- `PRINTPLAINFORM`
- `PRINTPLAINFORM <FORM string>`

**Arguments**
- `<FORM string>` (optional, FORM/formatted string; default `""`): scanned by the FORM analyzer (supports `%...%` and `{...}` placeholders).

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Evaluates the FORM argument to a string, then appends it as a “plain” segment (no automatic button conversion).
- Does not add a newline and does not flush by itself.

**Errors & validation**
- FORM parsing errors follow the engine’s normal FORM rules.

**Examples**
```erabasic
PRINTPLAINFORM HP: {HP}/{MAXHP}  [0] Not a button
PRINTL
```

**Progress state**
- complete
