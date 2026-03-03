**Summary**
- Ends an `IF ... ENDIF` block.

**Syntax**
- `ENDIF`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Marker-only instruction (no runtime effect). The loader uses it to close the `IF` nesting and to set jump targets for `IF`/`ELSEIF`/`ELSE`.

**Errors & validation**
- `ENDIF` without a matching open `IF` is a load-time error (the line is marked as error).

**Examples**
- `ENDIF`

**Progress state**
- complete
