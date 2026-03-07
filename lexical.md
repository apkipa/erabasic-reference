# Lexical Structure (tokens, comments, literals)

## Lines and whitespace

EraBasic is line-oriented. Most statements end at end-of-line.

Whitespace handling is partly fixed and partly config-controlled: half-width space/tab are always whitespace, while full-width space depends on `SystemAllowFullSpace`.

### Whitespace characters

- Half-width space and tab act as whitespace separators.
- Full-width space (`U+3000`) is treated as whitespace only when `SystemAllowFullSpace=YES`.

Important engine behavior when `SystemAllowFullSpace=NO`:

- During ordinary expression tokenization, encountering a full-width space is a **parse error** (“unexpected full-width space”).
- In some “skip whitespace/comments” helpers used by the line reader, a full-width space is simply *not consumed* (so it can prevent a line from being recognized as empty, or prevent `{` / `[` detection if it appears before them).

## Comments

### Full-line comments

- Any line that starts with `;` is a comment line in classic EraBasic.

### End-of-line comments

You can insert a comment after code by using `;`:

    A = B ; assign B to A

Exception: for some commands that treat their argument as a raw/simple string (for example, some `PRINT` forms), `;` can be part of the printed string rather than starting a comment.

### Special “not-a-comment” prefixes (engine extensions)

The engine can treat certain `;`-prefixed lines as executable by stripping the prefix:

- `;!;` — executed in Emuera, but still a comment in eramaker.
- `;#;` — executed only in *debug mode*; otherwise treated as a comment line.
- `;^;` — executed in this engine (historically an EMEE extension; other engines may treat it as a comment line).

See:

- `;!;` and `;#;` are Emuera-specific extensions.
- `;^;` originated as an EMEE extension, but it is recognized unconditionally in this codebase.

## Line concatenation (“row concatenation”)

Emuera supports a pre-parse line concatenation block:

    {
        #DIM CONST HOGE =
            1,2,3,4
    }

This is treated like a single logical line:

    #DIM CONST HOGE = 1,2,3,4

Rules:

- The `{` line is recognized only when `{` is the first non-whitespace character and the entire trimmed line equals `{`. Otherwise it is an error.
- The `}` line ends the block only when `}` is the first non-whitespace character and the entire trimmed line equals `}`. Otherwise it is an error.
- Nested continuation blocks are rejected: encountering a line whose trimmed-start equals `{` inside a continuation block is an error.
- The block is concatenated by appending each inner raw line (including its whitespace) plus a **joiner string** after it.

Joiner string:

- The joiner is the config value `ReplaceContinuationBR` with all `"` characters removed.
- It is appended after **every** inner line, including the last inner line before `}`.

Important phase note:

- Concatenation occurs at line-reading time, before any later stage applies end-of-line comment rules.
  - In expression-parsed contexts, a `;` can therefore comment-out text that originated from later physical lines in the continuation block.
  - In raw-string / FORM-scanned argument contexts, `;` may be treated as literal instead. See `argument-parsing-modes.md`.

Preprocessor interaction:

- When ERB loading is in a “disabled” preprocessor state (skipped branches), the line reader does **not** treat `{` / `}` as continuation markers (see `preprocessor-and-macros.md`).

This is an Emuera extension used to make long logical lines readable.

## Identifiers

Identifiers are used for function labels, variables, macro names, etc. Practical guidelines:

- User-defined function/variable names should not begin with a digit.
- For `#DIM/#DIMS`-declared variables, the recommended/expected symbol character is `_` (underscore).

### Identifier scanning rules (engine-accurate)

The core identifier reader reads the longest possible substring until it reaches a delimiter character. It does not validate “allowed character classes” beyond delimiter exclusion: practically, most Unicode letters are accepted as long as they don’t include delimiter symbols.

Delimiter characters include (not exhaustive in natural language; this list is the engine’s actual delimiter set):

- whitespace: half-width space, tab, full-width space
- punctuation/operators: `.` `+` `-` `*` `/` `%` `=` `!` `<` `>` `|` `&` `^` `~` `?` `#`
- brackets/separators: `(` `)` `{` `}` `[` `]` `,` `:` `@` `;`
- string/escape related: `\\` `'` `"`
- misc: `$`

Consequences:

- Identifiers cannot contain `-` or `.` in this engine (both are delimiters).
- The reader does not skip whitespace automatically; callers that allow whitespace must skip it explicitly.

Fact-check cross-ref (optional): `emuera.em/Emuera/Runtime/Script/Parser/LexicalAnalyzer.cs`.

## Numeric literals

Supported constant notations include:

- Decimal: `32`
- Binary: `0b100000`
- Hex: `0x20`
- Power-of-two form: `1p5` means `1 * 2^5`
- Scientific: `13e3` means `13 * 10^3`

Octal is intentionally not supported for compatibility reasons; `012` is treated as decimal `12` (not octal `10`).

### Exact integer parsing rules (engine-accurate)

The integer reader (`ReadInt64`) accepts:

- optional leading `+` or `-`
- base prefixes:
  - `0x` / `0X` for base-16 digits
  - `0b` / `0B` for base-2 digits (digits must be `0` or `1`)
- optional exponent suffix:
  - `p` / `P` → exponent base 2
  - `e` / `E` → exponent base 10

Important quirk: the exponent digits are parsed using the **same digit base as the significand** (decimal/hex/binary), and then applied as a normal integer exponent.

Range behavior:

- If the computed value is outside `Int64` range, the engine throws an error.

These notations come from the engine’s documented constant rules.

## String literals and escapes

### String literals

String literals use double quotes:

    "hello"

Some contexts also allow a formatted-string literal form `@"..."` (see “FORM in string expressions” in `expressions.md`).

String literals must be closed on the same physical line. An unterminated `"` string is a parse error.

### Escape sequences

Within strings, `\` escapes the next character. Implemented escapes include:

- `\s` → half-width space
- `\S` → full-width space
- `\t` → tab
- `\n` → newline
- `\\` → literal backslash

An escape followed by a newline is treated as a line-continuation (no character is added).

Note: this escape set is engine-specific; it is not “C-style” escaping.

Additional engine-accurate error rule:

- A trailing `\` at end of line (escape with no following character) is an error (“missing character after escape”).

## Operators and special tokens (engine-accurate)

### Expression operators

The lexer recognizes these operator tokens in expressions (see `expression-grammar.md` for precedence):

- arithmetic: `+ - * / %`
- comparisons: `== != < > <= >=`
- bitwise: `& | ^ ~ << >>`
- logical (integer truthiness): `&& || ^^ !& !|`
- unary: `!` (logical NOT), plus unary `+` / `-`
- ternary: `?` and `#` (the engine uses `#` as the `:` separator)
- increment/decrement: `++ --` (prefix/postfix, with restrictions)

### Assignment operators (statement parsing)

When parsing assignments, the engine scans for these assignment operators:

- `=` (numeric or string, depending on LHS variable type and context)
- `'+= -= *= /= %= <<= >>= &= |= ^=` (compound assignments)
- `'=` (string-only assignment operator token; see `expressions.md` for how string assignment is parsed)
- `++` / `--` are also recognized in assignment/operator scan contexts

### FORM tokens in expressions

In expression tokenization, two additional string tokens exist:

- `@"..."` is not a normal string literal; it is a **formatted-string literal** parsed by the FORM scanner.
- `\@...\@` is a **string-ternary literal** (also a FORM-derived scanner token).

Both are specified precisely in `formatted-strings.md`.

### `[[...]]` after rename processing

If a line still contains a substring matching `[[...]]` at tokenization time, the lexer raises an error (“cannot rename key”).
This is how the engine enforces that rename replacements must already have been applied by the line reader.
