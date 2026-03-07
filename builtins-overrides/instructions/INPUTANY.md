**Summary**
- Waits for a text input, then stores it in `RESULT` if it parses as a signed 64-bit integer; otherwise stores it in `RESULTS`.

**Tags**
- io

**Syntax**
- `INPUTANY`

**Arguments**
- None.

**Semantics**
- Enters an input wait (`InputType = AnyValue`).
- Like other non-primitive value waits, clicking a selectable **normal-output button** can submit one value/text on the mouse-click completion path.
- See also: `input-flow.md` (shared submission paths, segment draining/discard rules, and `MesSkip` interaction).
- On completion:
  - If the submitted text parses as a signed 64-bit integer, assigns it to `RESULT`.
  - Otherwise assigns the submitted text to `RESULTS`.
  - This same rule is used when the submitted text came from a clicked normal-output button.
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
