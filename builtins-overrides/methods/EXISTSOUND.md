**Summary**
- Tests whether a file exists under the runtime's `sound` path prefix.

**Tags**
- files
- audio

**Syntax**
- `EXISTSOUND(mediaFile)`

**Signatures / argument rules**
- `EXISTSOUND(mediaFile)` → `long`

**Arguments**
- `mediaFile` (string): path suffix appended to the `sound` directory prefix.

**Semantics**
- Resolves the path as `./sound/<mediaFile>` under the host's current working directory, then canonicalizes it with the platform's full-path resolver.
- Returns `1` if that resolved path exists as a file.
- Returns `0` otherwise.
- No safe-path normalization is applied here:
  - subdirectories are allowed,
  - parent-directory segments such as `..` are not stripped before full-path resolution.

**Errors & validation**
- None.

**Examples**
- `EXISTSOUND("bgm/theme.ogg")`

**Progress state**
- complete
