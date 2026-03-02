**Summary**
- Copies elements from one array variable to another array variable of the same element type and dimension.

**Syntax**
- `ARRAYCOPY <srcVarNameExpr>, <dstVarNameExpr>`

**Arguments**
- `<srcVarNameExpr>`: string expression whose value is a variable name.
- `<dstVarNameExpr>`: string expression whose value is a variable name.

**Defaults / optional arguments**
- None.

**Semantics**
- Resolves both variable names to variable tokens (early when literal, otherwise at runtime).
- Requires both to be arrays (1D/2D/3D), non-character-data; destination must be non-const.
- Copies element-wise; behavior is defined by the engine helper and may clamp to destination sizes per dimension.

**Errors & validation**
- Errors if a name does not resolve to a variable, if either is not an array, if either is character-data, if destination is const, or if dimension/type mismatch.

**Examples**
- `ARRAYCOPY "ABL", "ABL_BAK"`
- `ARRAYCOPY "ITEM", SAVETO`
