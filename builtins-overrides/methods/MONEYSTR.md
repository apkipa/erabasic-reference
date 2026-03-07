**Summary**
- Formats an integer as a currency string using the engine’s configured currency label and placement.

**Tags**
- formatting

**Syntax**
- `MONEYSTR(money [, format])`

**Signatures / argument rules**
- `MONEYSTR(money)` → `string`
- `MONEYSTR(money, format)` → `string`

**Arguments**
- `money` (int)
- `format` (optional, string; default `""`): numeric format string passed to `Int64.ToString(format)`.

**Semantics**
- Formats `money`:
  - if `format` is omitted or `""`: uses default numeric formatting (`money.ToString()`)
  - otherwise: uses `money.ToString(format)`
- Then attaches the currency label (`MoneyLabel`) either as a prefix or suffix depending on `MoneyFirst`:
  - `MoneyFirst = true`: `MoneyLabel + formatted`
  - `MoneyFirst = false`: `formatted + MoneyLabel`

**Errors & validation**
- Runtime error if `format` is not a valid `Int64.ToString` format string.

**Examples**
- `MONEYSTR(123)` → `"$123"` if `MoneyLabel="$"` and `MoneyFirst=true`.
- `MONEYSTR(123, "D6")` → `"$000123"` under the same config.

**Progress state**
- complete

