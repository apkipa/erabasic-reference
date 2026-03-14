**Summary**
- Searches a string and returns the first match position in the engine's length unit based on derived runtime value `LanguageCodePage`.

**Tags**
- text

**Syntax**
- `STRFIND(target, word [, start])`

**Signatures / argument rules**
- `STRFIND(target, word)` → `long`
- `STRFIND(target, word, start)` → `long`

**Arguments**
- `target` (string): string to search.
- `word` (string): substring to find.
- `start` (optional, int; default `0`): search start position in the same unit as `STRLENS`.

**Semantics**
- Uses ordinal, case-sensitive substring search.
- `start` is interpreted in the same length unit based on derived runtime value `LanguageCodePage` returned by `STRLENS`.
- Effective start-position rules:
  - If `start <= 0`, search begins at the start of `target`.
  - If `start` falls inside a multi-byte character, the effective start moves to the following character boundary.
  - If the effective start is at or past the end of `target`, returns `-1`.
- Returns the first match position in the same length unit based on derived runtime value `LanguageCodePage`.
- Returns `-1` if no match is found.
- If `word == ""`, returns the effective start position when that position is still inside the string; otherwise returns `-1`.

**Errors & validation**
- None.

**Examples**
- `STRFIND("abcdeabced", "a", 3)` → `5`

**Progress state**
- complete
