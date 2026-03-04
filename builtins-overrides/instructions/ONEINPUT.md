**Summary**
- Like `INPUT`, but requests a “one input” integer entry (UI-side restriction).

**Tags**
- io

**Syntax**
- `ONEINPUT`
- `ONEINPUT <default>`
- `ONEINPUT <default>, <mouse>, <canSkip> [, <extra>]`

**Arguments**
- Same as `INPUT`.

- Omitted arguments / defaults:
  - Same as `INPUT`.

**Semantics**
- Like `INPUT` (including `MesSkip` behavior and mouse side channels), but sets `OneInput = true` on the input request.
- Implementation-oriented notes:
  - In the UI input handler, `OneInput` truncates the entered text to at most one character in many cases, so it typically behaves like “read a single digit/character then parse”.
  - Depending on configuration, mouse-provided input may bypass this truncation.

**Errors & validation**
- Same as `INPUT`.

**Examples**
- `ONEINPUT`
- `ONEINPUT 0`

**Progress state**
- complete
