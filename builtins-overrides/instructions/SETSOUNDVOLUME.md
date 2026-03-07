**Summary**
- Sets the volume for sound effects (`PLAYSOUND`) across all sound effect slots.

**Tags**
- io

**Syntax**
- `SETSOUNDVOLUME <volume>`

**Arguments**
- `<volume>` (int): volume level, clamped to `0 <= volume <= 100`.

**Semantics**
- Applies the volume to all 10 sound effect slots (`0 <= slot <= 9`).
- If a slot is currently playing, the change takes effect immediately.

**Errors & validation**
- (none)

**Examples**
- `SETSOUNDVOLUME 30`

**Progress state**
- complete
