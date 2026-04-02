**Summary**
- Encodes a string into Unicode scalar values and writes them into `RESULT:*`.

**Tags**
- string

**Syntax**
- `ENCODETOUNI`
- `ENCODETOUNI <formString>`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): the string to encode.

**Semantics**
- Evaluates `<formString>` to a string `s`.
- Let `cap = length(RESULT_ARRAY) - 1` (because `RESULT:0` stores the length).
  - If `len(s) > cap`, runtime error.
- Produces an integer sequence of length `len(s)` by applying the platform’s UTF-16 conversion at each string index:
  - For each index `i` in `0 <= i < len(s)`, compute `code[i] = ConvertToUtf32(s, i)`.
  - Note: this is done at every index; if `s` contains a surrogate pair, converting at the *second* (low-surrogate) index raises an error.
- Writes the result to `RESULT_ARRAY`:
  - `RESULT:0 = len(s)`
  - For `0 <= i < len(s)`: `RESULT:(i+1) = code[i]`
- Does not clear any `RESULT:*` slots beyond `RESULT:len(s)`.

**Errors & validation**
- Runtime error if `len(s) > length(RESULT_ARRAY) - 1`.
- Runtime error if the UTF-16 conversion fails at any index (e.g. low surrogate, invalid surrogate pair).

**Examples**
```erabasic
ENCODETOUNI ABC
; RESULT:0 = 3
; RESULT:1 = 65
; RESULT:2 = 66
; RESULT:3 = 67
```

**Progress state**
- complete
