**Summary**
- Replaces text in a string using regex mode, literal mode, or sequential array-driven regex replacement.

**Tags**
- text

**Syntax**
- `REPLACE(base, pattern, replaceArg [, mode])`
- `REPLACE(base, pattern, replaceArg, 1)`

**Signatures / argument rules**
- `REPLACE(base, pattern, replacement)` → `string`
- `REPLACE(base, pattern, replacement, mode)` → `string`
- `REPLACE(base, pattern, replacements, 1)` → `string`

**Arguments**
- `base` (string): input string.
- `pattern` (string): regex pattern unless `mode == 2`.
- `replaceArg` (string or non-const 1D string-array variable reference): mode-dependent third argument.
- `mode` (optional, int; default `0`): replacement mode selector.
  - `0`: regex replace using a string third argument
  - `1`: regex replace using successive string-array elements
  - `2`: literal `.NET` `string.Replace`
  - all values other than `1` and `2`: same behavior as `0`

**Semantics**
- Regex modes (`mode` omitted / `0` / all values other than `1` and `2`):
  - Compiles `pattern` as a `.NET` regular expression.
  - Treats `replaceArg` as a string and returns `Regex.Replace(base, pattern, replaceArg)`.
  - The replacement text follows normal `.NET` regex-replacement syntax (for example `$1` for capture groups).
- Sequential array mode (`mode == 1`):
  - Compiles `pattern` as a `.NET` regular expression.
  - Requires `replaceArg` to be a non-const 1D string-array variable reference.
  - For the `k`-th match (0-based), if `k < length(replaceArg)`, the replacement text is `replaceArg[k]`.
  - If `k >= length(replaceArg)`, the replacement text is `""`.
- Literal mode (`mode == 2`):
  - Treats `replaceArg` as a string.
  - Performs plain `.NET` `base.Replace(pattern, replaceArg)`.
  - `pattern` is treated as literal text, not a regex.

**Errors & validation**
- Runtime error if `pattern` is not a valid regular expression in regex modes.
- Runtime error if `mode == 1` but `replaceArg` is not a non-const 1D string-array variable reference.
- In literal mode, an empty `pattern` is rejected by the underlying string-replacement routine.

**Examples**
- `REPLACE("12億3456万7890円", "[^0-9]", "")` → `"1234567890"`
- `REPLACE("A-B-C", "-", ARR, 1)` with `ARR = ["x", "y"]` → `"AxByC"`
- `REPLACE("a.b.c", ".", "-", 2)` → `"a-b-c"`

**Progress state**
- complete
