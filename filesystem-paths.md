# Filesystem Path Handling Families (Emuera EvilMask)

This document summarizes the **script-visible path-handling families** used by common file/resource built-ins.

The engine does **not** use one uniform path policy for every built-in.
For compatibility work, it is more accurate to group them into recurring implementation families and then map each built-in to one of them.

## 1) Base directories and terms

This document uses these path bases:

- `ExeDir`: the engine's executable/game root directory.
- `ContentDir`: `ExeDir/resources/`.
- `SoundDir`: `ExeDir/sound/`.
- `SavDir`: the configured save directory (`ExeDir/` or `ExeDir/sav/` depending on config).
- `ForceSavDir`: always `ExeDir/sav/`.
- current working directory:
  - the host process working directory,
  - often equal to `ExeDir` in ordinary launches, but not treated as the same contractually.

## 2) Family matrix

| Surface | Non-rooted base | Rooted/absolute handling | Slash rewrite | Parent-segment handling | Canonicalization | Extra path rules |
| --- | --- | --- | --- | --- | --- | --- |
| `EXISTFILE` | `ExeDir` | rejected | `/` -> `\` | strips `..\` after slash rewrite | no separate `GetFullPath` step | file-only existence check |
| `ENUMFILES` | `ExeDir` | rejected | `/` -> `\` | strips `..\` after slash rewrite | no separate `GetFullPath` step on input | outputs relative paths via `Path.GetRelativePath(ExeDir, file)` |
| `SAVETEXT` explicit-path mode | `ExeDir` | rejected | `/` -> `\` | strips `..\` after slash rewrite | no separate `GetFullPath` step | extension missing/not allow-listed -> rewritten to `.txt` |
| `LOADTEXT` explicit-path mode | `ExeDir` | rejected | `/` -> `\` | strips `..\` after slash rewrite | no separate `GetFullPath` step | extension must already be allow-listed |
| `OUTPUTLOG` | raw `ExeDir + filename` text with textual guards | not parsed as a separate absolute-path mode | none | rejects literal `../` only; does not specially filter `..\` | none before write | raw string-prefix check against `ExeDir` |
| `GCREATEFROMFILE` with `isRelative == 0` | `ContentDir` | rooted path used as-is | none | not stripped; passed through to host file APIs | no explicit `GetFullPath` in engine code | relative path can escape `resources/` via `..` |
| `GCREATEFROMFILE` with `isRelative != 0` | current working directory (host-relative) | rooted path used as-is | none | not stripped; passed through to host file APIs | no explicit `GetFullPath` in engine code | non-rooted input is used unchanged |
| `PLAYSOUND` / `PLAYBGM` | `SoundDir` | not treated as a separate rooted-path mode; input is appended as suffix text | none | not stripped; survives into full-path resolution | `Path.GetFullPath(SoundDir + filename)` | final path is based from `sound/` but not sandboxed inside it |
| `EXISTSOUND` | current working directory's `./sound/` | not treated as a separate rooted-path mode; input is appended as suffix text | none | not stripped; survives into full-path resolution | `Path.GetFullPath("./sound/" + mediaFile)` | does not use runtime `Program.SoundDir` |
| `GSAVE` / `GLOAD` / numeric-slot text save helpers / normal save files | fixed engine-chosen directories | not applicable | not applicable | not applicable | engine builds final filename itself | no user-supplied path text |

## 3) Family A: safe relative-to-`ExeDir` normalization

Used by:

- `EXISTFILE`
- `ENUMFILES`
- `SAVETEXT` explicit-path mode
- `LOADTEXT` explicit-path mode

Implementation shape:

1. Convert `/` to `\`.
2. Remove every literal `..\` substring.
3. Reject rooted / absolute paths.
4. Concatenate the remaining relative text under `ExeDir`.

Observable consequences:

- `..` is **not** a hard validation error here.
- Instead, parent-directory segments are silently stripped from the path text before resolution.
- Because slash conversion happens first, both `../` and `..\` end up following the same stripping rule.

## 4) Family B: `ExeDir`-prefixed path text with textual guards

Used by:

- `OUTPUTLOG`

Implementation shape:

1. If the filename is empty, use `ExeDir/emuera.log`.
2. Otherwise build the path as raw string concatenation: `ExeDir + filename`.
3. Reject only when the resulting text contains literal `../`.
4. Apply a raw string-prefix check against `ExeDir`.
5. Hand the resulting string to the file-writing API.

Observable consequences:

- This is **not** the same as Family A safe normalization.
- Backslash parent-directory text such as `..\` is not specially stripped or rejected here.
- The guard is textual, not canonicalized-path-based.

## 5) Family C: direct image loading

Used by:

- `GCREATEFROMFILE`

Implementation shape:

- Rooted / absolute paths are used as-is.
- Non-rooted `isRelative == 0` paths are prefixed with `ContentDir`.
- Non-rooted `isRelative != 0` paths are used unchanged.
- Then normal file/image loading is attempted on that string.

Observable consequences:

- No safe normalization is applied.
- Parent-directory segments such as `..` are passed through unchanged.
- In `isRelative == 0` mode, `..` can escape from `resources/` after host path resolution.
- In `isRelative != 0` mode, the base is the host current working directory, not forcibly `ContentDir`.

## 6) Family D: `SoundDir` plus `GetFullPath`

Used by:

- `PLAYSOUND`
- `PLAYBGM`

Implementation shape:

1. Build `SoundDir + filename`.
2. Canonicalize with `Path.GetFullPath(...)`.
3. Use the canonicalized path for existence check and playback.

Observable consequences:

- No parent-directory stripping is applied.
- Parent-directory segments such as `..` survive into full-path resolution.
- So these built-ins are based from `ExeDir/sound/`, but they are not sandboxed inside it.

## 7) Family E: `./sound/` plus `GetFullPath`

Used by:

- `EXISTSOUND`

Implementation shape:

1. Build `./sound/ + mediaFile`.
2. Canonicalize with `Path.GetFullPath(...)`.
3. Use the canonicalized path for existence check.

Observable consequences:

- No parent-directory stripping is applied.
- Parent-directory segments such as `..` survive into full-path resolution.
- The base is the host current working directory's `sound/`, not runtime `Program.SoundDir`.

## 8) Family F: fixed engine-chosen filenames

Used by:

- `GSAVE`
- `GLOAD`
- `SAVETEXT` / `LOADTEXT` numeric-slot mode
- normal save/global-save files

Implementation shape:

- The engine chooses the final filename from slot numbers and configured directories such as `SavDir` / `ForceSavDir`.

Observable consequence:

- There is no script-provided path text in this family, so path parsing questions such as slash normalization or `..` handling are not part of the script-visible contract.
