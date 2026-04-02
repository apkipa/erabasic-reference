**Summary**
- Checks a remote “update check” URL and reports whether a newer version is available.

**Tags**
- system

**Syntax**
- `UPDATECHECK`

**Arguments**
- None.

**Semantics**
- Writes a status code into `RESULT`:
  - `0`: remote version string equals the current version string (no update).
  - `1`: remote version differs; user chose “No” in the confirmation dialog.
  - `2`: remote version differs; user chose “Yes” and the engine attempted to open the provided link in the OS.
  - `3`: update check failed (URL missing/invalid response/network/IO error).
  - `4`: update check is forbidden by config (config item `ForbidUpdateCheck`).
  - `5`: no network is available.
- The update check source is `UpdateCheckURL` from the game base metadata.
  - If it is missing/empty, sets `RESULT = 3`.
- If network is available and the URL is present:
  - Fetches the URL and reads the first two lines:
    - line 1: remote version string
    - line 2: link URL
  - If either line is missing/empty, sets `RESULT = 3`.
  - If the remote version string differs from the current version string:
    - Shows a confirmation dialog containing the version and link.
    - If the user accepts, sets `RESULT = 2` and opens the link via the OS.
    - Otherwise sets `RESULT = 1`.

**Errors & validation**
- No runtime errors; failures are reported via `RESULT`.

**Examples**
- `UPDATECHECK`
- `PRINTFORML updatecheck={RESULT}`

**Progress state**
- complete
