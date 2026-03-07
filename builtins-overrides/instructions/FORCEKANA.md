**Summary**
- Sets the kana-conversion mode used by output operations that explicitly request kana conversion.

**Tags**
- text

**Syntax**
- `FORCEKANA <mode>`

**Arguments**
- `<mode>` (int): conversion mode.
  - `0`: no conversion
  - `1`: hiragana -> katakana
  - `2`: full-width katakana -> hiragana
  - `3`: katakana -> hiragana, and half-width katakana are widened first

**Semantics**
- Updates the persistent kana-conversion state used by print paths that request kana conversion (the `...K` / `K` output family; see the relevant print built-ins and `output-flow.md`).
- The mode remains in effect until another `FORCEKANA` changes it.
- It does not retroactively modify text that has already been buffered or printed.

**Errors & validation**
- Runtime error if `<mode>` is outside `0 <= mode <= 3`.

**Examples**
- `FORCEKANA 1`
- `FORCEKANA 0`

**Progress state**
- complete
