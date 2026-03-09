**Summary**
- Starts looping background music (BGM) from the sound directory.

**Tags**
- io

**Syntax**
- `PLAYBGM <filename>`

**Arguments**
- `<filename>` (string): file name or relative path under the sound directory.

**Semantics**
- Resolves the path by concatenating the engine’s sound directory with `<filename>`, then normalizing to an absolute path.
- Parent-directory segments such as `..` are not stripped before that full-path resolution, so the final target is based from `sound/` but not sandboxed inside it.
- If the file does not exist, no-op (does not stop any currently playing BGM).
- Format handling:
  - `.wav` uses the wave-file loader.
  - `.ogg` uses the Vorbis loader.
  - other extensions are delegated to the host media backend and are therefore not a stable portability guarantee.
- Otherwise, starts playback on the BGM channel and repeats indefinitely.
  - Starting a new BGM replaces the previous BGM.
- Path-handling family: see `filesystem-paths.md` Family D.

**Errors & validation**
- Runtime error if the file exists but cannot be decoded/played by the audio backend.

**Examples**
- `PLAYBGM "bgm\\theme.ogg"`

**Progress state**
- complete
