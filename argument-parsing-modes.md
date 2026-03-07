# Argument Parsing Modes (raw vs expression vs FORM)

Many “syntax questions” in EraBasic are not decided by the core expression grammar, but by **how each instruction parses its argument region**.

This document defines Emuera’s argument parsing modes in an engine-accurate, self-contained way.

## 1) Instruction lines pass a raw argument *slice*

For an instruction statement, the loader:

1) reads the instruction name token (e.g. `PRINTFORM`)
2) checks the single character immediately after the name
3) if that character is a valid separator, it consumes **exactly one** separator character and stores the rest of the line as the instruction’s `argprimitive` (`CharStream`)

Valid separators are:

- end-of-line (no arguments)
- `;` (comment start; arguments become empty)
- whitespace (` `, `\t`, and optionally full-width space U+3000 when `SystemAllowFullSpace=YES`)

Important implication:

- If you write more than one space after the instruction name, only the first is consumed. Any remaining spaces become part of the raw argument slice and may or may not matter depending on the argument parsing mode.

### 1.1 Omitted argument slots are instruction-family specific

For built-in instructions and methods, there is **no single universal rule** saying that an omitted later argument always becomes `0` or `""`.
Instead, each instruction family defines its own omission behavior.

Practical reading rule:

- some optional arguments are replaced immediately with their documented default during argument parsing,
- some remain absent until the instruction's own semantics inspect them,
- some cannot be omitted at all,
- and an explicit value such as `0` or `""` is still different from omission unless that entry explicitly states they are treated the same.

This is why built-in reference entries should distinguish:

- **optional / omitted**,
- **required but allowed to be empty**,
- and **explicit sentinel values** such as `0`.

## 2) The meaning of `;` depends on the parsing mode

The engine does **not** strip inline comments before argument parsing. Instead, `;` is handled by whichever parser is used for that instruction:

- **Ordinary expression lexing** treats `;` as “end-of-line comment” and stops tokenization.
  - Exceptions: `;!;` is a special “force executable line” prefix, `;#;` is a debug-only prefix, and this codebase also recognizes `;^;` as an executable prefix (historically an EMEE extension). These are handled in the lexer’s whitespace/comment skipper.
- **FORM scanning** does **not** treat `;` as a comment delimiter. In FORM contexts, `;` is literal text unless it is inside a `%...%`/`{...}` placeholder where other rules apply.
- **Raw-string arguments** (the `STR` argument builder) do **not** treat `;` as a comment delimiter. The argument is the raw remaining substring to end-of-line.

Practical rule:

- If an instruction uses an **expression** argument builder, `X ; comment` works as an inline comment.
- If an instruction uses a **FORM** or **raw string** argument builder, `;` is literal (so inline comments are not available in the usual way).

## 3) The three core parsing families

From a compatibility perspective, most built-in instructions fall into one of these families:

### 3.0 Identifier-only arguments (no expression parsing)

Some instructions accept a single **identifier token** as their entire argument (for example, a variable name), and do not parse the rest of the line as expressions.

Behavior:

- The parser reads one identifier token (letters/digits/underscore; same identifier rules as normal keywords).
- Any remaining characters after that identifier are not tokenized or reduced as expressions.
  - The engine may emit a warning about extra trailing characters, but the tail is not evaluated and has no side effects.
- This mode is distinct from “compatibility tails” such as `GOTO label, ...` where the tail is still lexed as expressions (syntactically) even if not evaluated.

### 3.1 Expression-argument builders (tokenized, `;` comments out remainder)

These builders lex the argument slice into tokens and then reduce an expression / argument list:

- `INT_EXPRESSION`, `INT_EXPRESSION_NULLABLE`
- `STR_EXPRESSION`, `STR_EXPRESSION_NULLABLE`
- `EXPRESSION`, `EXPRESSION_NULLABLE`
- most multi-arg builders built on `popTerms(...)` / `popWords(...)` (comma-separated expression lists)

Behavior:

- whitespace is skipped by the lexer
- `;` ends the argument region (comment)
- string literals `"..."` and formatted-string literals `@"..."` are recognized by the lexer

### 3.2 FORM-argument builders (formatted-string scanner, `;` is literal)

These builders scan a formatted string and then compile it to a string expression term:

- `FORM_STR`, `FORM_STR_NULLABLE`
- `FORM_STR_ANY` (comma-separated list of FORM segments, each scanned independently)

Behavior:

- `;` is not a comment delimiter
- the FORM scanner implements `%...%`, `{...}`, triple-symbol expansion, and `\@...\@` per `formatted-strings.md`

### 3.3 Raw-string builders (`STR`, `STR_NULLABLE`) (no lexing, `;` is literal)

These builders treat the argument as the raw remaining substring:

- no tokenization
- no comment stripping
- no escape processing
- no FORM expansion

This mode is used by some “raw text” instructions (notably some `PRINT...` variants).

## 4) String assignment is special (`=` vs `'=`)

String variable assignment has two distinct RHS parsers:

- `STR = ...` uses **FORM scanning** for the RHS (FORM rules, `;` is literal).
- `STR '= ...` uses **string-expression parsing** for the RHS (expression rules, `;` starts a comment).

This is why the engine has two assignment operators for string variables.

## 5) How to classify a built-in instruction

You do not need full per-instruction semantics to classify its argument parsing mode.

Engine-accurate procedure:

1) Determine the instruction’s `ArgumentBuilder` (or the `ArgBuilder` set by its `AInstruction` constructor).
2) Map it to one of the families in §3.

Common high-impact examples (as implemented by this codebase):

- `PRINT` uses a raw-string builder (`STR_NULLABLE`) → `;` is literal.
- `PRINTFORM` uses a FORM builder (`FORM_STR_NULLABLE`) → `;` is literal.
- `PRINTS` uses a string-expression builder (`STR_EXPRESSION`) → `;` starts a comment.

## Appendix A) Built-ins whose argument mode treats `;` as literal (raw string)

These built-ins use `STR` / `STR_NULLABLE` as their primary argument parsing mode (so `;` is not an inline-comment delimiter in their arguments):

- `ALIGNMENT`
- `BEGIN`, `FORCE_BEGIN`
- `CALLEVENT`
- `DATA` (inside `PRINTDATA` / `STRDATA` syntax blocks)
- `DEBUGPRINT`, `DEBUGPRINTL`
- `PRINT*` variants that are not `...FORM...` / `...S...` / `...FORMS...` / `...V...` (e.g. `PRINT`, `PRINTL`, `PRINTW`, `PRINTC`, `PRINTSINGLE`, and K/D/N variants)
- `PRINTPLAIN`
- `SETCOLORBYNAME`, `SETBGCOLORBYNAME`
- `STRLEN`, `STRLENU`

Notes:

- `PRINTS`, `PRINTFORMS`, and `PRINTV` are **not** in this list because they use expression parsing (so `;` starts a comment there).
- This list is about argument parsing mode only; it does not imply anything about runtime behavior.

## Appendix B) Built-ins whose argument mode treats `;` as literal (FORM string)

These built-ins use `FORM_STR*` parsing for their primary argument parsing mode (so `;` is literal):

- `DATAFORM` (inside `PRINTDATA` / `STRDATA` syntax blocks)
- `DEBUGPRINTFORM`, `DEBUGPRINTFORML`
- `DRAWLINEFORM`
- `ENCODETOUNI`
- `PRINTFORM*` variants (including `PRINTFORM`, `PRINTFORMW`, `PRINTSINGLEFORM`, and K/D/N variants)
- `PRINTPLAINFORM`
- `PUTFORM`
- `RETURNFORM`
- `REUSELASTLINE`
- `STRLENFORM`, `STRLENFORMU`
- `THROW`

Note: `STRLEN*` illustrates that the engine offers both raw-string and FORM-scanned variants; they differ only in argument parsing mode.

## Fact-check cross-refs (optional)

- Instruction line parsing and “consume exactly one separator char”: `emuera.em/Emuera/Runtime/Script/Parser/LogicalLineParser.cs` (`ParseLine`)
- Expression lexing and `;` comment handling: `emuera.em/Emuera/Runtime/Script/Parser/LexicalAnalyzer.cs` (`Analyse`)
- FORM scanning: `emuera.em/Emuera/Runtime/Script/Parser/LexicalAnalyzer.cs` (`AnalyseFormattedString`)
- Core argument builders (`STR`, `FORM_STR`, `STR_EXPRESSION`, etc.): `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs`
- `PRINT*` parsing mode selection: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs` (`PRINT_Instruction`)
