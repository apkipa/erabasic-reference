**Summary**
- Plays a one-shot sound effect file from the sound directory.

**Tags**
- io

**Syntax**
- `PLAYSOUND <filename> [, <repeat>]`

**Arguments**
- `<filename>` (string): file name or relative path under the sound directory.
- `<repeat>` (optional, int; default `1`): number of times to repeat the sound.
  - Values `< 1` are clamped to `1`.

**Semantics**
- Resolves the path by concatenating the engine’s sound directory with `<filename>`, then normalizing to an absolute path.
- Parent-directory segments such as `..` are not stripped before that full-path resolution, so the final target is based from `sound/` but not sandboxed inside it.
- If the file does not exist, no-op.
- Format handling:
  - `.wav` uses the wave-file loader.
  - `.ogg` uses the Vorbis loader.
  - other extensions are delegated to the host media backend and are therefore not a stable portability guarantee.
- Otherwise, starts playback on a “sound effect slot”:
  - There are 10 slots (`0 <= slot <= 9`).
  - The engine prefers the first non-playing slot; if all are playing, it reuses slot `0`.
- Playback is independent from BGM (`PLAYBGM`).
- Path-handling family: see `filesystem-paths.md` Family D.

**Errors & validation**
- Runtime error if the file exists but cannot be decoded/played by the audio backend.

**Examples**
- `PLAYSOUND "click.wav"`
- `PLAYSOUND "se\\hit.ogg", 3`

**Progress state**
- complete
