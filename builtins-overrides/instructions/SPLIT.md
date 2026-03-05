**Summary**
- Splits a string by a separator string and writes the resulting parts into a string array.

**Tags**
- text

**Syntax**
- `SPLIT <text>, <separator>, <outParts> [, <outCount>]`

**Arguments**
- `<text>` (string): string expression to split.
- `<separator>` (string): string expression used as the separator (not a set of characters).
- `<outParts>` (variable term): changeable array variable term to receive the parts.
  - Must be a **string** array variable (1D/2D/3D; character-data arrays are accepted but behave specially).
  - Any indices written in `<outParts>` are ignored for this instruction.
- `<outCount>` (optional, variable term; default `RESULT`): changeable integer variable term to receive the number of split parts.

**Semantics**
- Computes `parts = text.Split(new[] { separator }, StringSplitOptions.None)` (equivalent .NET behavior).
- Writes `parts.Length` into `<outCount>`.
- Writes a prefix of `parts` into `<outParts>`:
  - If `parts.Length > length0`, only the first `length0` parts are written, where `length0` is the destination array’s **first** dimension length.
  - Otherwise, all parts are written.
- Destination addressing rules:
  - 1D array: writes `outParts[i]` starting at `i = 0`.
  - 2D array: writes `outParts[0, i]` starting at `i = 0`.
  - 3D array: writes `outParts[0, 0, i]` starting at `i = 0`.
  - character-data string arrays: always write into character index `0` using the same “fixed earlier indices = 0” rule (e.g. `CVAR[0, i]`).
- Does not clear elements outside the written prefix.

**Errors & validation**
- Argument parsing fails if `<outParts>` is not a changeable array variable term.
- Argument parsing fails if `<outCount>` is provided but is not a changeable integer variable term.
- Runtime error if `<outParts>` is not a string array variable.

**Examples**
```erabasic
#DIM PARTS, 10
SPLIT "a,b,c", ",", PARTS
; RESULT == 3
; PARTS:0 == "a"
; PARTS:1 == "b"
; PARTS:2 == "c"
```

**Progress state**
- complete

