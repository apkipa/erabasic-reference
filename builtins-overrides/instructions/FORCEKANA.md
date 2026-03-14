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
- The state is stored as three internal flags:
  - mode `0`: all flags off
  - mode `1`: katakana conversion on
  - mode `2`: hiragana conversion on
  - mode `3`: hiragana conversion on, plus half-width-to-full-width widening before the hiragana conversion
- The mode remains in effect until another `FORCEKANA` changes it.
- It does not retroactively modify text that has already been buffered or printed.
- When an affected output path converts text, it calls Visual Basic `.NET` `Strings.StrConv(...)` using a fixed Japanese locale ID `0x0411`:
  - mode `1`: `StrConv(str, Katakana, 0x0411)`
  - mode `2`: `StrConv(str, Hiragana, 0x0411)`
  - mode `3`: `StrConv(str, Hiragana | Wide, 0x0411)`
- This path does **not** use config item `useLanguage`; the locale used for kana conversion is fixed rather than derived from config.
- Therefore, `FORCEKANA` is a separate conversion mechanism from `TOHALF` / `TOFULL`, even though both ultimately call Visual Basic `.NET` `StrConv`.

**Errors & validation**
- Runtime error if `<mode>` is outside `0 <= mode <= 3`.

**Examples**
- `FORCEKANA 1`
- `FORCEKANA 0`

**Progress state**
- complete
