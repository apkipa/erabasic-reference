**Summary**
- Maps a CSV/alias/ERD key name to its integer index for a variable family or user-defined variable.

**Tags**
- string-key
- erd

**Syntax**
- `GETNUM(varTerm, key [, dimension])`

**Signatures / argument rules**
- `GETNUM(varTerm, key)` → `long`
- `GETNUM(varTerm, key, dimension)` → `long`

**Arguments**
- `varTerm` (variable term): selects the variable family or user-defined variable name whose key dictionary should be queried.
  - This function uses the variable identity, not the current cell value.
  - Any written `:` subscripts do not participate in the lookup itself.
- `key` (string): key name to resolve.
- `dimension` (optional, int): ERD dimension selector for user-defined variables.
  - Omitted: ERD fallback uses the base variable name.
  - Supplied `n`: ERD fallback uses the dictionary named `name@n`.

**Semantics**
- First checks the built-in CSV-name / alias dictionary associated with `varTerm`'s variable family.
- If no built-in match is found, it checks ERD data for the selected variable name (or `name@dimension`) when such ERD data exists.
- Returns the mapped integer index on success; otherwise returns `-1`.
- `key = ""` also returns `-1`.
- `dimension` only affects the ERD fallback path; it does not change built-in CSV-name lookup.
- `GETNUM(NAME, key)` / `GETNUM(CALLNAME, key)` are allowed even though those families do not accept string-key syntax in ordinary variable-argument positions.

**Errors & validation**
- Parse/type error if `varTerm` is not a variable term or `key` is not string-typed.
- No runtime error is raised merely because the selected variable family has no key dictionary; that case returns `-1`.

**Examples**
- `n = GETNUM(ABL, "技巧")`
- `charaNo = GETNUM(CALLNAME, "霊夢")`

**Progress state**
- complete
