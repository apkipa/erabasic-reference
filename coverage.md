# Coverage Plan (Reimplementable Typical-Game Spec)

Goal: a reader can reimplement a **fully compatible EraBasic parser + interpreter**, plus the **minimal host/UI contracts and built-ins** needed to run **typical games** for this engine family, *using only* `erabasic-reference/*`.

Scope (current phase): **typical-game compatibility**.

- Included: loading order, preprocessing, lexing, parsing, expression evaluation, variables/scopes, user functions, control flow, runtime model for execution.
- Included (host/runtime contract): the **system phase state machine** (TITLE/SHOP/TRAIN/ABLUP/...) and its script entry points (`@SYSTEM_*`, `@EVENT*`, etc.), to the extent needed to run typical games.
- Included (UI/runtime contract): the **observable console output + input model** that typical games depend on (pending-buffer vs visible-line behavior, buttons/choices, and HTML output used by the UI layer).
- Deferred: niche host features and tooling that are not required by most games (hotkeys, debug tooling, localization/tooling, etc.), tracked explicitly below. The plugin system is already specified separately in `plugins.md`.

This document tracks what is already specified vs what still needs to be written.

Legend:

- ✅ Spec complete (sufficient to implement + test)
- 🟡 Partially specified (needs edge cases / error conditions / exact phase ordering)
- ⛔ Not specified yet
- 🔁 Deferred (out of current phase)

## 1) Source of truth and versioning

- ✅ Engine codebase is `emuera.em` (EvilMask-flavored Emuera; also contains some Emuera.NET/EMEE-compat code paths).
- ✅ Documentation used for fact-checking is `emuera.em.doc` (English pages exist for `docs/Reference` entries).
- 🟡 Target “compatibility” must be pinned to specific commits/tags and to a config profile (many behaviors are config-dependent).

## 2) Input model (files, folders, load order)

- ✅ Folder layout assumptions (csv/ERH/ERB, subfolder loading rules, and filesystem case-sensitivity caveat).
- ✅ Load order and phase boundaries (CSV → rename/replace → ERH macros/vars → ERB).
- ✅ File encodings and newline normalization.
- ✅ `_Rename.csv` missing-file behavior when config item `UseRenameFile` = `YES` (host prints an error and continues with an empty rename map).
- ✅ `_Replace.csv` replaceable-item set and its main script-visible effects (it targets a fixed replace-item table, including some runtime defaults, not arbitrary config keys).
- 🟡 Error/warning behavior on duplicate definitions and missing references.

Where described today:

- `program-structure.md`
- `pipeline.md`
- `data-files.md`

## 3) Preprocessing

### 3.1 Line concatenation blocks (`{` … `}`)

- ✅ Syntax and basic rules.
- ✅ Interaction with comments and preprocessing (phase ordering in `lexical.md` and `preprocessor-and-macros.md`).
- ✅ Error conditions: invalid brace lines, nesting rejection, EOF handling.

Where described today:

- `lexical.md`

### 3.2 Comment processing

- ✅ `;` full-line and end-of-line comment concept.
- ✅ Special executable prefixes: `;!;`, `;#;`, `;^;`.
- ✅ Core rule for “why `;` is sometimes literal”: it depends on the instruction’s argument parsing mode (expression lexing vs FORM scanning vs raw-string slice).
- 🟡 Still missing: a complete per-built-in mapping table (which instructions use which argument parsing mode).

Where described today:

- `lexical.md`

### 3.3 Macro system (`#DEFINE`) and conditional blocks

- ✅ Macro expansion model: token-based, where expansion applies, recursion limit.
- ✅ Boundary against line-level structure: `#DEFINE` expansion does not change whether an ERB line is classified as `@` / `$` / `#` / `[`-started structure vs ordinary statement; `[[...]]` rename replacement can, because it runs earlier during line reading.
- ✅ Conditional inclusion blocks: `[IF]...[ENDIF]`, `[IF_DEBUG]`, `[IF_NDEBUG]`, and their interaction with line reading.
- ✅ `[SKIPSTART]...[SKIPEND]` handling (skip-forces-disabled, but directives still parsed).

Where described today:

- `preprocessor-and-macros.md` (engine-accurate)

## 4) Lexical rules (tokenization)

- ✅ Full delimiter set; exact identifier scanning rules.
- ✅ Whitespace rules, including full-width spaces and config gating.
- ✅ Numeric literal grammar (binary/hex/p/e forms, overflow behavior).
- ✅ String literal grammar, escapes, and unterminated literal errors.
- ✅ Operator scanning (including assignment operators like `'+='`, `'=`).

Where described today:

- `lexical.md` (user-facing behavior)
- `expressions.md` (operators summary)

## 5) Grammar: program and statement parsing

### 5.1 Function labels (`@...`)

- ✅ Label grammar (allowed chars, begin-with-digit rules, case-sensitivity).
- ✅ Duplicate labels, multi-definition ordering, and event grouping rules.
- ✅ Interaction with “event function” categories and attributes: event-name set, grouped dispatch order, return-driven control flow, and config item `CompatiCallEvent` compatibility behavior are specified across `labels.md` and `runtime-model.md`.

Where described today:

- `program-structure.md`
- `labels.md`

### 5.2 `#` directives under labels

- ✅ Full directive set and constraints (where allowed, conflicts, precedence).
- ✅ Attribute semantics: `#ONLY`, `#FUNCTION/#FUNCTIONS`, `#PRI/#LATER/#SINGLE`, and `#LOCALSIZE/#LOCALSSIZE` (including engine quirks).

### 5.3 Statement list and block structures

- ✅ Canonical statement grammar for:
  - `IF/ELSEIF/ELSE/ENDIF`, `SIF`
  - `SELECTCASE/CASE/CASEELSE/ENDSELECT` (including `IS ...` and `a TO b` case conditions)
  - loops: `REPEAT/REND`, `FOR/NEXT`, `WHILE/WEND`, `DO/LOOP`
  - `BREAK/CONTINUE`
  - `CALL/JUMP/RETURN/RETURNFORM/RETURNF` interactions with `RESULT/RESULTS`
- ✅ Line-start dispatch special cases (e.g. `;!;`, `{...}` concatenation blocks, `@/$/#` label/directive lines, and prefix `++/--` parsing).
- 🟡 Error behavior on malformed blocks, cross-block jumps, and direct-entry via `GOTO/JUMP` into blocks.
  - ✅ Unstructured entry via `GOTO $label` (allowed) and the “advance-first” marker-skipping implications are specified (see `runtime-model.md` and `control-flow.md`).
  - 🟡 Still missing: a fully enumerated matrix of which malformed-nest situations become “error lines” vs warnings, and which ones can still run.

Where described today:

- `control-flow.md` (behavioral summary for main blocks)
- `functions.md` (CALL/RETURN family overview)
- `line-start-special-cases.md` (engine-accurate dispatch edge cases)

## 6) Expression language (core)

### 6.1 Types, coercions, and type errors

- ✅ Exact typing rules: int vs string; required-type contexts across core constructs.
- ✅ Conversion rules and config-controlled behaviors (notably user-function arg binding).

### 6.2 Operator semantics

- ✅ Full operator list and precedence/associativity as implemented.
- ✅ Short-circuit semantics (`&&`, `||`, `!&`, `!|`, ternary; `^^` does not short-circuit).
- ✅ Ternary operators (numeric `? #` and string `\@ ? # \@`), including parse rules and nesting.
- ✅ Increment/decrement (`++/--`) as statement and expression operators (variable-only, const rejection, prefix vs postfix result value).
- ✅ String comparison semantics in expressions: equality/inequality are case-sensitive content comparisons, ordering is ordinal, and config item `IgnoreCase` does not apply.
- ✅ Numeric edge cases and exception behavior:
  - division/modulo by zero
  - negative division/modulo semantics
  - shift-count handling (large/negative shift counts)
  - integer overflow behavior in runtime arithmetic (including the exceptional `long.MinValue / -1` family)

### 6.3 String expressions and FORM syntax

- ✅ Formal definition of “string expression” vs “raw string argument” at the language/tooling boundary.
- ✅ `%...%` and `{...}` interpolation grammar, compilation, and evaluation semantics.
- ✅ `@"..."` rules (FORM-in-string-expression literal) and `\@...\@` string-ternary literal form.
- ✅ Escape rules inside FORM literal segments.
- 🟡 Where FORM is accepted vs treated as literal text (command-category-dependent).
- ✅ Load-time expression normalization/optimization that can affect observable evaluation (constant folding and “restructuring”).

Where described today:

- `expressions.md` (high level)
- `formatted-strings.md` (engine-accurate)

## 7) Variables and storage model

### 7.1 Built-in variables (core semantics)

- ✅ `RESULT/RESULTS/COUNT` core behavior across calls/loops (RETURN/implicit return, REPEAT counter, null-string reads).
- ✅ Array indexing syntax with `:`; multi-dimensional indexing and omission/inference rules.
- ✅ Batch assignment (`A:i = v1,v2,...` / `A:i:j = ...`) including which elements are written and out-of-range behavior.
- ✅ Bounds checking and prohibited-variable errors (no config knobs observed for relaxing bounds checks).
- ✅ CSV-name indexing resolution rules and ambiguity rules.
- ✅ Built-in variable catalog + lifecycle beyond `RESULT/RESULTS/COUNT`: selector variables (`MASTER/TARGET/ASSI/PLAYER`), `CHARANUM`, character-list mutation boundaries, reset-sensitive command arrays, and global-reset survivors are specified.

### 7.2 User-defined variables

- ✅ `#DIM/#DIMS` declaration grammar (keywords, dimensions, initializers) and timing (ERH batch + ERB sharp lines).
- ✅ `DYNAMIC` lifetime and recursion behavior.
- ✅ `CONST` write-protection and interaction constraints.
- ✅ `REF` reference binding rules and mutation behavior (for user-function ref parameters).

### 7.3 Global scope (ERH variables)

- ✅ `SAVEDATA/GLOBAL/CHARADATA` storage partitioning and reset/load boundaries (engine-accurate).
- ✅ Save/load built-in semantics (see `builtins-reference.md`).
- ✅ On-disk save file formats (field/byte-level spec): `save-files.md`.

Where described today:

- `variables.md` (core rules + inference)
- `string-key-indexing.md` (engine-accurate mapping + runtime resolution)
- `control-flow.md` and `runtime-model.md` (`COUNT` + `RESULT` return semantics)

## 8) Function call model

- ✅ Call stack model and `RESULT/RESULTS` assignment boundaries.
- ✅ Argument binding (`ARG/ARGS`) including defaults and omitted args (including implicit defaults for some formals).
- ✅ Empty-slot parsing is specified for both expression calls and instruction-style comma lists, including the engine quirk that `F(a,,c)` creates a `null` middle slot but trailing `F(a,)` / `CALL X, a,` do **not** create an extra final omitted slot.
- ✅ Pass-by-reference via `REF` formal parameters.
- ✅ Expression functions (`#FUNCTION/#FUNCTIONS`): call sites, statement-form boundaries, method-safe restriction model, side-effect caveats, and the main disallowed instruction families are specified.
- ✅ Error behavior on missing functions and labels (including `TRY*`, `TRYC*`, `TRY*LIST`, `CALLF`, and `TRYCALLF`), calling event functions, and `CompatiCallEvent` / config item `FunctionNotFoundWarning` effects is specified.
- 🟡 Execution modes that affect call/IO behavior (e.g. output skipping `SKIPDISP` / script-runner skip-print mode, and message-skip `MesSkip`) are documented at the shared-rule level; a tighter exhaustive inventory of print-like built-ins is still desirable.

Where described today:

- `functions.md` (call resolution, TRY families, method restrictions, and execution-mode boundaries)
- `input-flow.md` (`MesSkip` wait behavior)
- `output-flow.md` (shared output-skip model)

## 9) Error/warning model (core)

- ✅ Taxonomy of parse-time vs load-time vs runtime errors.
- 🟡 Warning vs error behavior for every individual diagnostic family is still incomplete, but the core warning/error model and error-line mechanics are specified.
- ✅ Line/position reporting and how concatenated lines map to file locations.

Where described today:

- `errors-and-warnings.md` (core mechanics)
- `source-position-mapping.md` (engine-accurate file/line mapping rules)

## 10) System phases and host flow

This engine family is not “just an interpreter”: it also defines a host-driven **system phase** state machine (TITLE/FIRST/SHOP/TRAIN/ABLUP/AFTERTRAIN/TURNEND/LOADDATAEND, plus save/load flows).

This matters for compatibility because:

- It defines which script entry points are called (e.g. `@SYSTEM_TITLE`, `@EVENTTRAIN`, `@SHOW_SHOP`) and in what order.
- Some phases require a `BEGIN` to be executed by the end of a system hook (otherwise the engine errors), which is an observable runtime contract.
- Entering certain phases performs variable initialization/reset that affects save data and gameplay logic (not just UI).

Coverage target (core-compat requirements):

- ✅ Enumerate phases and legal transitions.
- ✅ Specify which labels are called in each phase (including required/optional labels and default fallbacks when labels are missing).
- ✅ Specify mandatory “must execute `BEGIN`” contracts (and error behavior when violated), including `@SYSTEM_TITLE`, `@EVENTFIRST`, `@EVENTEND`, `@EVENTTURNEND`, and the distinct post-load fallback path.
- ✅ Specify the key variable initialization/reset performed when entering phases (including TRAIN pre-initialization and the post-load SHOP fallback that skips `@EVENTSHOP`).
- 🟡 Specify which parts are configurable via `_replace.csv` / config (including a tighter inventory of host message texts/ranges that are data-driven vs fixed).
- ✅ Specify the minimal host I/O contract that system flow depends on:
  - system input request behavior (integer parsing, defaults, and retry behavior on invalid input)
  - console output buffering concepts referenced by system flow (e.g. “temporary line” affecting re-prompt vs full redraw)

Where described today:

- ✅ `system-flow.md` (system phases, entry points, required transitions, save/load UI flow, and phase-entry resets)

## 11) Built-in commands/functions

- ✅ Signature catalog for lookup: `appendix/tooling/builtins.md` and `appendix/tooling/builtins-signatures.md`.
- ✅ RNG contract for `RAND` / `RANDOMIZE` / `INITRAND` / `DUMPRAND`: legacy SFMT(MT19937) path, `RANDDATA` snapshot layout, legacy modulo-based range reduction, and the `UseNewRandom` switch to host `.NET System.Random`.

Typical-game compatibility requires a subset of “UI-ish” built-ins to be specified as **observable contracts**.

### 11.1 Output model (console)

- ✅ Shared output-state model:
  - pending print buffer vs visible display-line array vs logical-line grouping
  - separate HTML-island layer outside the normal output/log model
  - temporary trailing line as a distinct visible state rather than just buffered text
- ✅ Shared console layout primitives:
  - the common width-measurement / row-formation / splitting / alignment backend used by plain-text and HTML output is documented
  - HTML `<div>` subdivision width feeds that same backend rather than using a separate row builder
- 🟡 Remaining output-edge details:
  - the shared pending-buffer/materialization model is documented
  - remaining gaps are now mostly a smaller set of producer-specific “buffer vs temporary line vs system line” notes and other isolated producer/readback quirks
- ✅ Output skipping baseline:
  - `SKIPDISP` suppresses output producers at the producer side rather than merely hiding already-produced output
  - reaching input while `SKIPDISP`-driven skipping is active is an error boundary, not a hidden auto-input path
  - default “skipped means no evaluation / no side effects” rule is centralized in `agents.md`; document only built-in exceptions
- ✅ Buttons as output objects:
  - button regions are part of visible output before later waits consume them
  - HTML history export preserves button vs nonbutton regions
- ✅ Buttons and choice presentation baseline:
  - button labels vs accepted values are separated explicitly
  - duplicated accepted values are observable as value-based typed acceptance, while mouse clicks still identify the clicked region
  - older visible buttons can remain rendered after they stop being selectable because the active generation advanced
- ✅ Output history / buffer-introspection layer split:
  - display-row getter vs logical-line getter vs pending-buffer export are now separated explicitly
  - `GETDISPLAYLINE` / `HTML_GETPRINTEDSTR` / `HTML_POPPRINTINGSTR` now share one cross-document model
- ✅ Output history / buffer-introspection built-ins:
  - `GETDISPLAYLINE` vs `HTML_GETPRINTEDSTR` vs `HTML_POPPRINTINGSTR` layer split is specified
  - retained-row/logical-line boundaries and excluded layers are specified
- ✅ `DRAWLINE` helper string expansion:
  - `GETLINESTR` returns the width-fitted line string for an arbitrary pattern using the same host-width rule as runtime `DRAWLINE` expansion
- ✅ HTML-island model and redraw coupling:
  - `HTML_PRINT_ISLAND*` accumulation / clear / exclusion from normal getters and counters are specified
  - `REDRAW` / `CURRENTREDRAW` are tied to repaint scheduling rather than stored output state

Where described today:

- ✅ `output-flow.md` (shared output-state model, temporary lines, button generations, island model, redraw/readback boundaries)
- ✅ `console-layout.md` (shared width measurement, wrapping/splitting, alignment, and plain-text/HTML convergence point)
- ✅ `html-output.md` (logical line vs display lines for HTML rendering)
- ✅ `builtins-reference.md` (individual producer/readback entries for the shared output/readback surface)
- ✅ `system-flow.md` (temporary-line-dependent reprompt paths)

### 11.2 Input model (console)

- ✅ Shared input-request lifecycle, submission paths, segment draining/discard rules, one-input segment semantics, and `MesSkip` auto-advance model: `input-flow.md`.
- ✅ Choice/input-request entry conditions and shared submission paths:
  - how waits become active (explicit input instructions vs selectable buttons already present)
  - button-click submission vs textbox submission, including the boundary against `CBG` hit-maps
- ✅ Integer input parsing / rejection contract:
  - shared trimming/sign/rejection behavior is documented
  - per-family default/retry rules are documented for the `INPUT*` / `BINPUT*` / `TINPUT*` families
  - rejection-side host UX (textbox clearing, no separate warning/system line) is documented
- ✅ Time-limited input and request-kind differences beyond the shared model:
  - `TINPUT*`, `TWAIT`, and `INPUTMOUSEKEY` timeout/result contracts are documented
  - primitive waits explicitly document that this host exposes no separate cancel event beyond ordinary key/mouse events plus timeout
- ✅ Blocking input instructions and their observable effects on output:
  - the shared wait/submission flow is documented
  - visibility-before-wait / flush behavior is documented for `WAIT` / `WAITANYKEY` / `FORCEWAIT` / `TWAIT` / `BINPUT*`, with the shared materialization rule centralized in `output-flow.md`
- ✅ Keyboard/mouse state built-ins and their interaction with the input loop:
  - `GETKEY`, `GETKEYTRIGGERED`, `MOUSEX`, `MOUSEY`, `MOUSEB`, `MOUSESKIP` (coordinate system, polling vs event semantics, and when values update)
- ✅ Mouse input “mapping color” side channel for `<img srcm='...'>`:
  - how the mapping sprite is selected and sampled
  - which `RESULT:*` indices it is written to (depends on input wait type)

### 11.3 HTML output and HTML-string helpers

- ✅ HTML parser/renderer contract for `HTML_PRINT*`:
  - supported tags/attributes set (including which tags are treated as formatting vs structural)
  - nesting rules and error recovery (invalid/mismatched tags)
  - entity/escape handling and how raw text is treated
- ✅ “HTML island” buffering:
  - `HTML_PRINT_ISLAND*` buffer separation rules and retrieval (`HTML_GETPRINTEDSTR`, `HTML_POPPRINTINGSTR`)
- ✅ HTML-string helpers (`HTML_ESCAPE`, `HTML_TOPLAINTEXT`, `HTML_TAGSPLIT`, `HTML_STRINGLEN/SUBSTRING/STRINGLINES`):
  - exact output for edge cases (empty input, invalid markup, unsupported tags)

### 11.4 Images and sound (commonly used resource built-ins)

- ✅ Resource lookup and path resolution:
  - sprite names vs direct file-based image/audio paths are now separated explicitly
  - `GCREATEFROMFILE`, `PLAYSOUND` / `PLAYBGM`, and `EXISTSOUND` path-base differences are now documented
- ✅ Sprite lookup contract used by `<img src='...'>` / `PRINT_IMG` / sprite built-ins:
  - sprite names are defined by `resources/**/*.csv` and resolved case-insensitively
  - missing sprites fall back to literal-tag text in HTML output
- ✅ Console background image stack:
  - `SETBGIMAGE` / `REMOVEBGIMAGE` / `CLEARBGIMAGE` (sprite requirements, depth ordering, opacity handling, and removal key matching)
- ✅ Supported formats (as an observable contract):
  - image loading uses the host bitmap loader plus explicit `.webp` support via the bundled native WebP path
  - `.wav` / `.ogg` are the stable audio formats this reference treats as portable; other audio extensions are backend-dependent and intentionally not promised
- ✅ Failure behavior:
  - missing/decode/size-limit paths are now summarized for sprite CSV loading, `GCREATEFROMFILE`, `PLAYSOUND` / `PLAYBGM`, and `EXISTSOUND`

### 11.5 Save/load UI behaviors beyond on-disk formats

- ✅ Save/load phase hooks and default fallback behavior when optional hooks are missing.
- ✅ Save-slot “sidecar” files written/read by built-ins (often used by games for save/load UIs):
  - image: `SavDir/img{index:0000}.png` (via `GSAVE/GLOAD`)
  - text: `SavDir/txt{index:00}.txt` or `ForceSavDir/txt{index:00}.txt` (via `SAVETEXT/LOADTEXT` numeric-slot mode)
  - these sidecars are now called out centrally in `save-files.md`

### 11.6 File-IO helper built-ins used by games

- ✅ Common filesystem-touching helpers relied on by games are now documented:
  - `EXISTFILE`, `ENUMFILES`, `SAVETEXT`, `LOADTEXT`, `OUTPUTLOG`, `GCREATEFROMFILE`, `EXISTSOUND`, `GSAVE`, and `GLOAD`
  - path rules, encoding/newline behavior, and return/error contracts are covered across `builtins-reference.md`, `filesystem-paths.md`, `save-files.md`, `resources-and-sprites.md`, and `output-flow.md`

## 12) Host/UI tooling and extensions (deferred)

These items are **observable engine features** but are deferred because they are not required for typical-game compatibility.

- 🔁 Command-line invocation contract (flags and positional args), including `--ExeDir`, `-Debug`, and `-GenLang`.
- 🔁 Localization/language pack system under `ExeDir/lang/` (including `-GenLang` template generation and selection/fallback rules).
  - Files/patterns: `lang/emuera.*.xml` (load), `lang/emuera-default-lang.xml` (generated template).
- ✅ Keyboard macro system: `ExeDir/macro.txt` + config item `UseKeyMacro` (load/save timing, file format, localization-sensitive parsing, and input-loop behavior) are specified in `host-aux-files.md`.
- 🔁 In-game debug command mode: config item `UseDebugCommand` and the console rule “input beginning with `@` is treated as a debug command” (supported syntax subset + restrictions).
- 🔁 Hotkey scripting extension: `ExeDir/HOTKEY.ERB` + Ctrl+D toggle + its limited grammar, and how it interacts with `HOTKEY_STATE*`.
  - Optional developer dump file: `ExeDir/HOTKEY.ERB.bytecode.txt`.
- ✅ Plugin system: discovery/load timing, `Plugins/*.dll` admission, `pluginsAware.txt` gating, public plugin contract types, `CALLSHARP` interop, and the public `PluginManager` / `PluginAPICharContext` helper surface are specified in `plugins.md`.
- ✅ Debug UI aux files under `ExeDir/debug/`: `debug/debug.config`, `debug/watchlist.csv`, and `debug/console.log` are specified in `host-aux-files.md` together with their path/encoding behavior.
- 🔁 Rikaichan integration files: config item `RikaiFilename` (dictionary path) and its sidecar index file `RikaiFilename.ind`.
- 🟡 Misc host diagnostics/aux files:
  - `ExeDir/time.log` is now specified in `host-aux-files.md`.
  - Still deferred: `ExeDir/patch_versions/*.txt`, `ExeDir/emuera.log`, `ExeDir/Analysis.log`, and `img_err.log`.
- 🔁 Native OS interop dependencies (host implementation detail): `user32.dll`, `winmm.dll`, `kernel32.dll`.

## Next concrete deliverables (to reach “reimplementable typical-game”)

1) ✅ Write a **phase-ordered pipeline spec**: `pipeline.md`.
2) ✅ Document **config + CSV formats** that affect parsing/runtime: `data-files.md`.
   - ✅ Catalog config keys, types, defaults, and shared config-adjacent derived runtime values: `config-items.md`.
3) 🟡 Write a **formal-ish grammar** for statements and expressions (EBNF + edge-case rules).
 - ✅ Statement-level grammar + block matching: `grammar.md`.
 - ✅ Expression grammar (EBNF + precedence): `expression-grammar.md`.
 - ✅ FORM/formatted-string subgrammar: `formatted-strings.md`.
4) ✅ Finish the **runtime model** for variables, call stack, and control-flow constructs.
   - ✅ The runtime-execution core is now covered across `runtime-model.md` (stack / events / scopes / method execution), `control-flow.md` (block and loop runtime behavior), `variables.md` (storage classes / reset boundaries), and `save-files.md` (save/load partitions that affect runtime-visible state).
   - ✅ Remaining partial items nearby are tracked under their own sections (for example malformed-block diagnostic matrices in §5.3), not as a missing runtime-model core.
5) 🟡 Specify the **system phase state machine** (host flow) as a reimplementable contract (TITLE/SHOP/TRAIN/...).
   - ✅ Core phase/state-machine contract is now documented in `system-flow.md`; remaining gaps are mainly narrower config/data-driven detail.
6) 🟡 Specify **typical-game UI contracts** for output/input/HTML and the commonly used UI built-ins.
   - 🟡 Shared output/input/HTML models and the common resource/file helper surfaces are mostly documented; remaining gaps are concentrated in some per-built-in input edge contracts and output layout/width details.
7) ⛔ Add a **conformance test suite plan** (golden tests) that validates parsing + typical-game execution, plus a minimal host-flow harness.
