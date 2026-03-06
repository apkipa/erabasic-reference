**Summary**
- Disposes multiple sprites and returns how many were removed.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEDISPOSEALL(<includeCsvSprites>)`

**Signatures / argument rules**
- Signature: `int SPRITEDISPOSEALL(int includeCsvSprites)`.

**Arguments**
- `<includeCsvSprites>` (int): controls whether sprites loaded from content/resource CSVs are also disposed.
  - `0`: keep CSV/resource sprites.
  - non-zero: dispose all sprites, including CSV/resource sprites.

**Semantics**
- Disposes sprite entries in bulk.
- If `<includeCsvSprites> == 0`:
  - disposes only non-resource sprites,
  - preserves the sprites that come from the resource/content tables,
  - returns the number of sprites removed by that selective disposal.
- If `<includeCsvSprites> != 0`:
  - disposes all sprites,
  - returns the total number of sprites that were present before clearing.
- Layer boundary:
  - this does not itself print anything or modify the normal output model,
  - but later rendering that depended on disposed sprites may stop drawing them.

**Errors & validation**
- None beyond normal integer-expression evaluation.

**Examples**
```erabasic
R = SPRITEDISPOSEALL(0)
R = SPRITEDISPOSEALL(1)
```

**Progress state**
- complete
