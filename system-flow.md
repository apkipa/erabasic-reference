# System Phases and Host Flow

This engine defines a host-driven **system phase** state machine (TITLE/SHOP/TRAIN/ABLUP/…), in addition to the script-level language rules.

This document specifies the **observable compatibility contract** for that state machine: which script entry points are called, how phase transitions happen, and what initialization/reset side effects occur.

Config keys are referenced by their `config-items.md` names (e.g. `SaveDataNos`, `MaxShopItem`, `ComAbleDefault`).

## 1) Concepts

### 1.1 System phases vs script execution

At runtime, the engine alternates between:

- executing script lines inside a call stack (entered via `CALL`, `JUMP`, event calls, and system entry points), and
- running host-side “system flow” steps when the script call stack reaches its system-defined boundary.

When a system hook finishes (e.g. `@SYSTEM_TITLE`), if the engine has no further script to execute, it continues system flow. Some hooks **must** perform a phase transition (typically via `BEGIN`) or the engine errors (see §2).

### 1.2 Phase transitions (`BEGIN`)

`BEGIN <keyword>` requests a transition into a system phase (see `builtins-reference.md` → `BEGIN`).

Key compatibility rule:

- A `BEGIN` request is not entered immediately as a normal call; instead, it ends the current function and is applied after unwinding to the top-level boundary, then system flow continues in the requested phase.

This is why certain system hooks are required to execute `BEGIN`: otherwise, the hook returns, the script stack ends, and there is no next phase to enter.

### 1.3 “Temporary line” and system prompts

Some system flows interpret the presence of a trailing **temporary line** (see `REUSELASTLINE`) as “re-prompt without restarting the whole screen”.

This is observable in SHOP/TRAIN/ABLUP flows: after a user handler returns, the engine may either:

- re-open the immediate input prompt (same screen), or
- restart the phase’s top-level loop (re-render via `@SHOW_*`).

## 2) Required `BEGIN` contracts (runtime errors)

The engine treats “script ends while in the normal/non-system state” as an error.

In practice, this means the following system hooks must execute a phase transition (usually `BEGIN`) before returning normally:

- `@SYSTEM_TITLE` (TITLE custom entry), unless it performs `LOADDATA`/`QUIT`/etc.
- `@EVENTFIRST` (FIRST)
- `@EVENTEND` (AFTERTRAIN)
- `@EVENTTURNEND` (TURNEND)

Post-load hooks have a defined fallback (see §7), so they do not have the same “must BEGIN or error” requirement.

## 3) Phase catalog and legal transitions (high level)

System phases covered here:

- TITLE (including the default title menu and optional `@SYSTEM_TITLE`)
- FIRST
- SHOP
- TRAIN
- ABLUP
- AFTERTRAIN
- TURNEND
- LOADDATAEND (post-load hook sequence after `LOADDATA`/`LOADGAME`)
- SAVEGAME/LOADGAME (interactive save/load UIs)

Legal transitions are driven primarily by `BEGIN <keyword>`:

- `BEGIN TITLE` → TITLE
- `BEGIN FIRST` → FIRST
- `BEGIN SHOP` → SHOP
- `BEGIN TRAIN` → TRAIN
- `BEGIN ABLUP` → ABLUP
- `BEGIN AFTERTRAIN` → AFTERTRAIN
- `BEGIN TURNEND` → TURNEND

If a phase does not call `BEGIN` anywhere, it normally does not exit that phase (e.g. SHOP/TRAIN/ABLUP loops are “infinite” until a script issues `BEGIN`).

## 4) TITLE phase

### 4.1 Entry points

On entering TITLE, the engine does one of the following:

1) If `@SYSTEM_TITLE` exists: call it (event-style calling rules apply). No default title UI is shown.
2) Otherwise: show the default title menu UI (see §4.2).

### 4.2 Default title menu behavior

The default title menu:

- prints a title header (script title/version/author metadata), then
- prints two menu items:
  - `[0] <TitleMenuString0>` (“start new game”)
  - `[1] <TitleMenuString1>` (“load and start”)
- requests an integer input.

If the selected value is:

- `0`:
  - reset non-global variables to defaults (same reset as `RESETDATA`),
  - add character(s) for a new game (at least character CSV #0; an additional default character may also be added depending on `GAMEBASE.CSV`),
  - then enter FIRST (equivalent to `BEGIN FIRST`).
- `1`:
  - if `@TITLE_LOADGAME` exists: call it, then return to TITLE afterwards,
  - otherwise: enter the opening load UI (a `LOADGAME`-like flow tied to the title menu; see §8).
- otherwise:
  - show an “invalid value” message and re-prompt.

### 4.3 `@SYSTEM_TITLE` requirements

If `@SYSTEM_TITLE` exists, it is responsible for deciding what happens next.

Compatibility requirement:

- If `@SYSTEM_TITLE` returns normally without executing a phase transition (typically `BEGIN`, or a successful `LOADDATA`, or `QUIT`), the engine errors.

## 5) FIRST phase

Entry:

- FIRST is entered after starting a new game from TITLE (`BEGIN FIRST`).

Behavior:

- The engine calls `@EVENTFIRST` (event function).

Compatibility requirement:

- If `@EVENTFIRST` returns normally without executing a phase transition (`BEGIN ...`), the engine errors.

## 6) SHOP phase

There are two distinct entry variants.

### 6.1 Entry variant A: `BEGIN SHOP` (normal SHOP entry)

On `BEGIN SHOP`, the engine:

1) calls `@EVENTSHOP` if it exists (if it does not exist, it is skipped),
2) may perform an autosave if autosave is enabled (see §6.3),
3) calls `@SHOW_SHOP`,
4) requests an integer input and processes it (see §6.4).

### 6.2 Entry variant B: post-load fallback (implicit SHOP loop)

After a successful load (`LOADDATA`/`LOADGAME`), if the post-load hooks finish without executing `BEGIN`, the engine enters SHOP’s main loop **without** calling `@EVENTSHOP` and **without** autosave (see §7.3).

### 6.3 Autosave on SHOP entry

If autosave is enabled, the engine performs an autosave at the beginning of the SHOP loop (after `@EVENTSHOP` and before the first `@SHOW_SHOP`).

Autosave details:

- The autosave slot index is `99`.
- The description text starts with the current timestamp in `yyyy/MM/dd HH:mm:ss ` format, and `@SAVEINFO` may append to it.
- If `@SYSTEM_AUTOSAVE` exists, the engine delegates autosave to it instead of performing the default autosave write.

### 6.4 SHOP main loop: `@SHOW_SHOP` → input → action

After `@SHOW_SHOP`, the engine requests an integer input (system prompt). Let the received integer be `x`.

If `0 <= x < MaxShopItem`:

- Treat `x` as an item index.
- If the item is not for sale (`ITEMSALES[x] == 0`): show an “out of stock” message and re-prompt.
- Else if the purchase fails (e.g. not enough money): show a “not enough money” message and re-prompt.
- Else (purchase succeeds):
  - update purchase state (sets `BOUGHT`, increments `ITEM:BOUGHT`, decrements money accordingly),
  - call `@EVENTBUY` if it exists,
  - then continue the SHOP loop.

If `x` is outside the buy range:

- set `RESULT = x`,
- call `@USERSHOP`,
- then continue the SHOP loop.

Re-prompt vs restart behavior after `@USERSHOP` / `@EVENTBUY`:

- If the last output line is a **temporary line**, the engine re-opens the input prompt without calling `@SHOW_SHOP` again.
- Otherwise, the engine restarts from `@SHOW_SHOP`.

## 7) LOADDATAEND (post-load hook sequence)

After a successful `LOADDATA <slot>` or a successful selection in the `LOADGAME` UI, the engine:

1) calls `@SYSTEM_LOADEND` if it exists,
2) then calls `@EVENTLOAD` if it exists.

If a hook executes `BEGIN`, the engine transitions to that phase.

If `@EVENTLOAD` returns normally without executing `BEGIN`:

- the engine proceeds to SHOP’s main loop as a fallback (equivalent to “enter SHOP and start at `@SHOW_SHOP`”), without calling `@EVENTSHOP` and without autosave.

## 8) LOADGAME / SAVEGAME (interactive UIs)

These UIs are host-driven flows that save/restore the previous execution context when canceled or completed.

### 8.1 Slot list and navigation

The UI shows save slots:

- Normal slots: `0 <= slot < SaveDataNos`
- Autosave slot: `99` (shown in load UI; not shown in save UI)
- Back/cancel: `100`

Slots are shown in pages of 20.

If the user enters a valid slot number that belongs to a different page, the UI switches to that page and redraws the list.

### 8.2 SAVEGAME flow

When entering SAVEGAME:

- the UI shows the slot list and requests an integer input.

If the user selects:

- `100`: cancel; restore the previous system state and return.
- a normal slot `s`:
  - if the slot already contains data: prompt for overwrite confirmation (0 = yes, 1 = no).
  - if confirmed (or if the slot was empty):
    - initialize `SAVEDATA_TEXT` with the current timestamp in `yyyy/MM/dd HH:mm:ss ` format,
    - call `@SAVEINFO` if it exists (it can append to `SAVEDATA_TEXT`, commonly via `PUTFORM`),
    - write the save file for slot `s`,
    - restore the previous system state and return.
- any other value: show an “invalid value” message and re-prompt.

### 8.3 LOADGAME flow

When entering LOADGAME:

- the UI shows the slot list and requests an integer input.

If the user selects:

- `100`: cancel; restore the previous system state and return.
- a normal slot `s` (or autosave slot `99`):
  - if there is no data in the slot: show a “no data” message and re-open the load prompt.
  - otherwise:
    - load the slot’s save state,
    - clear the previous execution context,
    - enter the LOADDATAEND hook sequence (§7).
- any other value: show an “invalid value” message and re-prompt.

## 9) TRAIN phase

### 9.1 Entry behavior (`BEGIN TRAIN`)

On entering TRAIN, the engine performs a phase-entry reset (affects compatibility and save data):

- Sets `ASSIPLAY = 0`, `PREVCOM = -1`, `NEXTCOM = -1`.
- Clears `TFLAG[*]` to `0`.
- Clears `TSTR[*]` to `""`.
- For every character in the current character list, clears these arrays to `0`:
  - `GOTJUEL[*]`, `TEQUIP[*]`, `EX[*]`, `PALAM[*]`, `SOURCE[*]`, `TCVAR[*]`
- For every character, resets `STAIN[*]` to the configured default stain values.

Then the engine calls `@EVENTTRAIN` if it exists, and enters the main TRAIN loop.

`NEXTCOM` shortcut (compatibility behavior):

- After `@EVENTTRAIN` returns, if `NEXTCOM >= 0`, the engine skips the normal command-list UI and immediately treats that value as the selected command:
  - sets `SELECTCOM = NEXTCOM`,
  - then sets `NEXTCOM = 0` (not `-1`),
  - then proceeds to command execution as in §9.5.

### 9.2 Main TRAIN loop outline

At a high level, the TRAIN loop is:

1) `@SHOW_STATUS`
2) Enumerate executable commands (via `@COM_ABLEnn` and/or config defaults) and display the command list.
3) `@SHOW_USERCOM`
4) Reset pre-input deltas (`UP/DOWN/LOSEBASE`, etc.)
5) Prompt for integer input.
6) If the input selects an executable command:
   - run `@EVENTCOM` (if present), then `@COMnn`,
   - if the command reports success, run `@SOURCE_CHECK` and then `@EVENTCOMEND`,
   - then loop back to step (1).
7) Otherwise:
   - set `RESULT = <input>`,
   - call `@USERCOM`,
   - then loop back to step (1).

### 9.3 Command enumeration (`@COM_ABLEnn`)

Let `TRAINNAME[]` be the configured list of training command names (from data files).

For each index `i` where `TRAINNAME[i]` exists:

- Call `@COM_ABLE{i}` if it exists.
  - If it returns `0`, the command is not shown as executable.
  - If it returns non-zero, the command is shown as executable.
- If `@COM_ABLE{i}` does not exist, the default behavior is controlled by config:
  - If `ComAbleDefault == 0`, the command is treated as not executable.
  - Otherwise, it is treated as executable.

The engine caches this executability decision for the current list rendering (it does not re-call `@COM_ABLE{i}` during the subsequent input check).

### 9.4 Per-prompt resets before input

After `@SHOW_USERCOM` returns (and before the input prompt), the engine resets:

- Global arrays: `UP[*] = 0`, `DOWN[*] = 0`, `LOSEBASE[*] = 0`
- Per-character arrays: `DOWNBASE[*] = 0`, `CUP[*] = 0`, `CDOWN[*] = 0`

### 9.5 Executing a command

When an executable command `n` is selected:

- Set `SELECTCOM = n`.
- Reset `NOWEX[*] = 0` for all characters.
- Call `@EVENTCOM` if it exists, then call `@COM{n}`.

Command result:

- If `RESULT == 0` after `@COM{n}` returns: the command is treated as “failed” and TRAIN proceeds to the post-command stage without running `@SOURCE_CHECK`.
- Otherwise:
  - call `@SOURCE_CHECK`,
  - then clear `SOURCE[*] = 0` for all characters,
  - then call `@EVENTCOMEND` if it exists.

After the post-command stage, the engine returns to `@SHOW_STATUS`.

WAIT injection:

- If `@EVENTCOMEND` does not exist, or if it exists but does not execute a wait instruction, the engine performs a wait (equivalent to `WAIT`) before returning to `@SHOW_STATUS`.

### 9.6 USERCOM path

If the input does not select an executable command:

- Set `RESULT = <input>`.
- Call `@USERCOM`.

After `@USERCOM` returns, the engine may re-prompt without restarting the whole screen:

- If the last output line is a **temporary line**: re-open the input prompt.
- Otherwise: continue the TRAIN loop from `@SHOW_STATUS`.

## 10) ABLUP phase

Entry and loop:

1) Call `@SHOW_JUEL`.
2) Call `@SHOW_ABLUP_SELECT`.
3) Prompt for integer input. Let the received integer be `x`.

If `0 <= x < 100`:

- Attempt to call `@ABLUP{x}`.
- If `@ABLUP{x}` does not exist: show an “invalid value” message and re-prompt (it does **not** fall back to `@USERABLUP` for this case).

Otherwise (`x < 0` or `x >= 100`):

- Set `RESULT = x`.
- Call `@USERABLUP`.

After the handler returns:

- If the last output line is a **temporary line**, re-open the input prompt without re-calling `@SHOW_JUEL`.
- Otherwise, restart from `@SHOW_JUEL`.

## 11) AFTERTRAIN phase (`BEGIN AFTERTRAIN`)

On entering AFTERTRAIN:

- The engine calls `@EVENTEND` (event function).

Compatibility requirement:

- If `@EVENTEND` returns normally without executing `BEGIN`, the engine errors.

## 12) TURNEND phase (`BEGIN TURNEND`)

On entering TURNEND:

- The engine calls `@EVENTTURNEND` (event function).

Compatibility requirement:

- If `@EVENTTURNEND` returns normally without executing `BEGIN`, the engine errors.
