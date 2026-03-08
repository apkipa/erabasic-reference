**Summary**
- Searches a string and returns the first match position in UTF-16 code units.

**Tags**
- text

**Syntax**
- `STRFINDU(target, word [, start])`

**Signatures / argument rules**
- `STRFINDU(target, word)` → `long`
- `STRFINDU(target, word, start)` → `long`

**Arguments**
- `target` (string): string to search.
- `word` (string): substring to find.
- `start` (optional, int; default `0`): UTF-16 code-unit start position.

**Semantics**
- Uses ordinal, case-sensitive substring search.
- `start` is interpreted in the same unit as `STRLENSU` (`.NET` `string.Length`).
- If `start < 0` or `start >= target.Length`, returns `-1`.
- Otherwise returns the first matching UTF-16 code-unit index, or `-1` if no match is found.
- If `word == ""`, returns `start` when `0 <= start < target.Length`; otherwise returns `-1`.
- Because indexing is by UTF-16 code unit, a supplementary character occupies two positions and can be split by `start`.

**Errors & validation**
- None.

**Examples**
- `STRFINDU("abcdeabced", "a", 3)` → `5`

**Progress state**
- complete
