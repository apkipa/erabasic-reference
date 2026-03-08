**Summary**
- Looks up a config-like item by name and returns its value in integer form.

**Tags**
- config

**Syntax**
- `GETCONFIG(key)`

**Signatures / argument rules**
- `GETCONFIG(key)` → `long`

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
- `GETCONFIG` succeeds only when the resolved item materializes as an integer-like value.
- Integer materialization rules include:
  - booleans → `1` / `0`,
  - colors → `0xRRGGBB`,
  - ordinary integer/long values → that integer,
  - textual values equal to `YES` / `NO` → `1` / `0`,
  - other textual values that parse as decimal integers → that integer.
- If the resolved item materializes as a string-like value, use `GETCONFIGS` instead.

**Errors & validation**
- Runtime error if `key == ""`.
- Runtime error if no matching config/replace/debug item exists.
- Runtime error if the matched item is not available in integer form; the engine tells the caller to use `GETCONFIGS`.

**Examples**
- `size = GETCONFIG("FONTSIZE")`

**Progress state**
- complete
