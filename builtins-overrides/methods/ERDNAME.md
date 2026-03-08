**Summary**
- Reverse-maps an integer value back to an ERD key name for a user-defined variable.

**Tags**
- erd
- string-key

**Syntax**
- `ERDNAME(varTerm, value [, dimension])`

**Signatures / argument rules**
- `ERDNAME(varTerm, value)` → `string`
- `ERDNAME(varTerm, value, dimension)` → `string`

**Arguments**
- `varTerm` (variable term): selects the declared variable name whose ERD dictionary should be queried.
  - This function uses only the identifier name.
  - Any written `:` subscripts do not participate in the reverse lookup itself.
- `value` (int): integer value to reverse-map.
- `dimension` (optional, int): ERD dimension selector.
  - Omitted: uses the base ERD dictionary `name`.
  - Supplied `n`: uses the ERD dictionary `name@n`.

**Semantics**
- Performs reverse lookup against ERD dictionaries only.
- Built-in CSV-name / alias tables are not consulted.
- Returns the matching key string if the selected ERD dictionary contains an entry whose value equals `value`.
- Returns `""` if:
  - `value < 0`,
  - no matching ERD dictionary exists,
  - or no key in that dictionary maps to `value`.
- If multiple ERD keys share the same integer value, scripts should not rely on a stable public choice among them.

**Errors & validation**
- Parse/type error if `varTerm` is not a variable term.
- Otherwise, missing ERD data is not an error; it returns `""`.

**Examples**
```erabasic
S = ERDNAME(HOGE3D, 0, 1)
S = ERDNAME(HOGE3D, 1, 2)
```

**Progress state**
- complete
