**Summary**
- Waits for a text input, then stores it as either an integer (`RESULT`) or a string (`RESULTS`) depending on whether it parses as a 64-bit integer.

**Tags**
- io

**Syntax**
- `INPUTANY`

**Arguments**
- None.

**Semantics**
- Enters an input wait (`InputType = AnyValue`).
- See also: `input-flow.md` (shared submission paths, segment draining/discard rules, and `MesSkip` interaction).
- On completion:
  - If the submitted text parses as a signed 64-bit integer, assigns it to `RESULT`.
  - Otherwise assigns the submitted text to `RESULTS`.
- Does **not** clear the “other” result:
  - If an integer is accepted, `RESULTS` remains unchanged.
  - If a string is accepted, `RESULT` remains unchanged.
- Empty input is accepted as a string `""` (which produces no visible echo because printing an empty string outputs nothing).
- This instruction is **not** skipped by output skipping (`SKIPDISP`) because it is not a print-skip instruction.

**Errors & validation**
- (none)

**Examples**
```erabasic
INPUTANY
IF RESULTS != ""
  PRINTFORML "string: " + RESULTS
ELSE
  PRINTFORML "int: " + RESULT
ENDIF
```

**Progress state**
- complete
