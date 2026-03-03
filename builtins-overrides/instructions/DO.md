**Summary**
- Begins a `DO ... LOOP` loop.

**Syntax**
- `DO`
  - `...`
  - `LOOP <int expr>`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Marker-only instruction (no runtime effect).
- The loader links the `DO` marker with its matching `LOOP` condition line.

**Errors & validation**
- `LOOP` without a matching open `DO` is a load-time error (the `LOOP` line is marked as error).

**Examples**
- `DO`
- `  I += 1`
- `LOOP I < 10`

**Progress state**
- complete
