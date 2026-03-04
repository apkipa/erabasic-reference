**Summary**
- Reorders the engine’s character list (`0 .. CHARANUM-1`) by a key taken from a character-data variable.
- Observable behavior: keeps `MASTER` fixed at its numeric position for this instruction.

**Tags**
- characters

**Syntax**
- `SORTCHARA`
- `SORTCHARA FORWARD | BACK`
- `SORTCHARA <charaVarTerm> [ , FORWARD | BACK ]`

**Arguments**
- `<charaVarTerm>`: a variable term whose identifier is a character-data variable.
- Order: `FORWARD` = ascending, `BACK` = descending.
- If the key variable is an array, the element indices are taken from the variable term’s subscripts after the character selector.

- Omitted arguments / defaults:
  - If no args: uses key `NO` and ascending.

**Semantics**
- Computes a sort key for each character via the engine’s key setter; null strings are treated as empty string.
- Stable sort: ties are broken by original order.
- After sorting, `TARGET`/`ASSI` are updated to keep pointing at the same character objects; `MASTER` is kept at its fixed index.

**Errors & validation**
- Parse-time error if `<charaVarTerm>` is not a character-data variable term.
- Runtime error if selected element indices are out of range for the variable.

**Examples**
- `SORTCHARA NO`
- `SORTCHARA CFLAG:3, BACK`
- `SORTCHARA NAME, FORWARD`

**Progress state**
- complete
