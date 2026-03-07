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
- If the file does not exist, no-op (does not stop any currently playing BGM).
- Otherwise, starts playback on the BGM channel and repeats indefinitely.
  - Starting a new BGM replaces the previous BGM.

**Errors & validation**
- Runtime error if the file exists but cannot be decoded/played by the audio backend.

**Examples**
- `PLAYBGM "bgm\\theme.flac"`

**Progress state**
- complete
