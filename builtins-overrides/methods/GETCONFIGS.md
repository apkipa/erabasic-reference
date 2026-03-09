**Summary**
- Looks up a config-like item by name and returns its value in string form.

**Tags**
- config

**Syntax**
- `GETCONFIGS(key)`

**Signatures / argument rules**
- `GETCONFIGS(key)` → `string`

**Arguments**
- `key` (string): case-insensitive lookup key.

**Semantics**
- Lookup order is fixed:
  - first config items,
  - then replace items,
  - then debug items.
- Matching is case-insensitive.
- Accepted keys:
  - config items: symbolic name, primary display label, or English display label,
  - replace/debug items: symbolic name or primary display label.
- `GETCONFIGS` succeeds only when the resolved item materializes as a string-like value.
- String materialization rules include:
  - ordinary string values → that string,
  - `char` values → a one-character string,
  - config item `TextDrawingMode` values → the enum-name string,
  - other items whose textual form is neither `YES`/`NO` nor a decimal integer → that textual form.
- If the resolved item materializes as an integer-like value, use `GETCONFIG` instead.

**Errors & validation**
- Runtime error if `key == ""`.
- Runtime error if no matching config/replace/debug item exists.
- Runtime error if the matched item is not available in string form; the engine tells the caller to use `GETCONFIG`.

**Examples**
- `font = GETCONFIGS("FONTNAME")`

**Progress state**
- complete
