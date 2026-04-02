**Summary**
- Like `GOTOFORM`, but if the evaluated `$label` name does not exist the instruction **does not error** and simply falls through.

**Tags**
- calls

**Syntax**
- `TRYGOTOFORM <formString>`

**Arguments**
- Same as `GOTOFORM`.

**Semantics**
- If the `$label` exists: behaves like `GOTOFORM`.
- If not: does nothing (continues at the next line after `TRYGOTOFORM`).

**Errors & validation**
- Still errors if the label exists but is invalid.

**Examples**
- `TRYGOTOFORM LABEL_{RESULT}`

**Progress state**
- complete
