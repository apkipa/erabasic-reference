**Summary**
- Sets the volume for BGM (`PLAYBGM`).

**Tags**
- io

**Syntax**
- `SETBGMVOLUME <volume>`

**Arguments**
- `<volume>` (int expression): volume level, clamped to `0 .. 100`.

**Semantics**
- Applies the volume to the BGM channel.
- If BGM is currently playing, the change takes effect immediately.

**Errors & validation**
- (none)

**Examples**
- `SETBGMVOLUME 50`

**Progress state**
- complete
