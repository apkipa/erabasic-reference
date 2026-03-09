**Summary**
- Writes the current retained normal output log to a UTF-8-with-BOM text file using an `ExeDir`-prefixed path.

**Tags**
- io
- files

**Syntax**
- `OUTPUTLOG()`
- `OUTPUTLOG(<filename>)`
- `OUTPUTLOG(<filename>, <hideInfo>)`

**Signatures / argument rules**
- Signature: `int OUTPUTLOG(string filename = "", int hideInfo = 0)`.
- `<hideInfo>` is treated as “hide headers” only when it is exactly `1`.

**Arguments**
- `<filename>` (optional, string; default `""`): output path text.
  - If omitted or `""`, the file name is `emuera.log` in the executable-root directory.
  - Otherwise the engine prepends the executable-root directory to the given text as a raw relative-path string.
- `<hideInfo>` (optional, int; default `0`): whether to suppress the environment/title header block.
  - `1`: hide the header block.
  - any other value: include the header block.

**Semantics**
- Exports the current retained **normal output** to a text file encoded as UTF-8 with BOM.
- Log source boundary:
  - it reads only the currently retained normal display-line log,
  - pending buffered output is **not** flushed first and is therefore not included,
  - the separate `HTML_PRINT_ISLAND` layer is not included,
  - debug-output-buffer content is not included.
- Output text is plain text:
  - HTML/button markup is stripped,
  - one retained display row becomes one output file line.
- If `<hideInfo> != 1`, the file begins with environment/title/log header text before the retained output lines.
- Path handling is text-based, not `EXISTFILE`-style safe normalization:
  - if `<filename>` is omitted or `""`, the path is `ExeDir/emuera.log`,
  - otherwise the engine builds the path by raw string concatenation: `ExeDir + <filename>`,
  - if that resulting path text contains literal `../`, the call is rejected,
  - the host also applies a raw string-prefix check against `ExeDir`; this is not a canonicalized path-safety check.
- On successful file creation while the window exists, the host appends a normal **system line** announcing the created log file.
  - That announcement happens **after** the file has already been written, so the just-written file does not contain its own success message.
  - Because that success path uses the normal system-line path, any pending print buffer may become visible on screen at that point even though it was not included in the file.
- Return value:
  - returns `1` after the method call completes,
  - this return value does **not** distinguish success from failure.
  - Failure is instead signaled by host dialog/error UI and by the absence of the success system line.

**Errors & validation**
- Textually rejected path strings are rejected by host error UI.
- File-write failures are rejected by host error UI.
- No exception-style success/failure code is exposed through the return value.

**Examples**
```erabasic
R = OUTPUTLOG()
R = OUTPUTLOG("logs\\scene.txt", 1)
```

**Progress state**
- complete
