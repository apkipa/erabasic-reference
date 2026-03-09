# EraBasic Grammar (statement-level, Emuera)

This document specifies the **statement-level grammar** of EraBasic as implemented by this Emuera codebase.
It focuses on how ERB/ERH files are parsed into *logical lines*, how blocks are matched, and the concrete syntax of control-flow and definition lines.

This is intended for interpreter reimplementation work; it is therefore biased toward “what the engine accepts/rejects”, including quirks.

## 0) Pipeline context (where grammar starts)

Before any parsing described here, the engine has already performed (see `pipeline.md` and `data-files.md`):

- Config/JSON load (affects whitespace rules and some parsing toggles).
- Optional `[[...]]` rename replacement (line-level, non-recursive).
- Optional `{ ... }` line-continuation joining (line-level).
- ERB-only bracket preprocessor directives (`[IF ...]`, `[SKIPSTART]`, …) which can disable lines.

This document starts from the **enabled logical line** stream after those steps.

## 1) Line classification (ERB)

After leading whitespace is skipped (with config-gated full-width space handling), an enabled ERB line is classified by its first character:

1) Preprocessor directive: `[` *but not* `[[` (handled before parse; not a statement).
2) Function attribute / declaration line: `#...` (only valid in the function's post-label sharp block: zero or more consecutive `#...` lines immediately after an `@...` function label, before the first non-`#` logical line).
3) Label line:
   - `@...` defines a function label.
   - `$...` defines a local “goto label”.
4) Otherwise: a **statement line**, which is either:
   - an **instruction line** (keyword recognized as a built-in instruction), or
   - an **assignment line** (anything else that contains an assignment operator in the correct place).

Comment-only and empty lines are filtered out by the line reader and whitespace skipper rules (see `lexical.md`).

## 2) Lexical placeholders used in this grammar

This file uses the following placeholders:

- `IDENT` — identifier token (see `lexical.md`).
- `WS` — whitespace that is recognized as whitespace by the engine (config item `SystemAllowFullSpace` affects whether U+3000 counts).
- `INT_EXPR` — integer expression (see `expressions.md`).
- `STR_EXPR` — string expression (see `expressions.md`).
- `EXPR` — expression that may be integer or string (engine tracks types).
- `VAR_TERM` — a variable term usable as an lvalue (see `variables.md`).
- `CONST_INT` — integer expression that must reduce to a compile-time constant in the places noted.
- `FORM_STR` — a formatted string token/term as parsed by the engine’s formatted-string analyzer (see `expressions.md`).

Important: instruction keywords and many identifiers are compared using config-controlled comparers. In particular, config item `IgnoreCase` affects much of identifier matching.

## 3) EBNF: file structure (ERB)

The file is parsed line-by-line; blocks are structural and do not use braces.

```ebnf
erb_file        ::= { erb_line } ;

erb_line        ::= pp_directive
                  | sharp_line
                  | func_label_line
                  | goto_label_line
                  | statement_line
                  ;

pp_directive    ::= "[" pp_token [ WS pp_arg ] "]" [ ignored_trailing ] ;
pp_token        ::= "SKIPSTART" | "SKIPEND"
                  | "IF" | "ELSEIF" | "ELSE" | "ENDIF"
                  | "IF_DEBUG" | "IF_NDEBUG"
                  ;
pp_arg          ::= IDENT ;

sharp_line      ::= "#" sharp_directive ;

func_label_line ::= "@" IDENT [ func_signature ] ;
goto_label_line ::= "$" IDENT ;

func_signature  ::= subnames [ arglist_sig ]
                  | arglist_sig
                  ;
subnames        ::= "[" arglist "]" ;
arglist_sig     ::= "(" arglist_define ")"
                  | "," arglist_define
                  ;

statement_line  ::= incdec_stmt
                  | instruction_stmt
                  | assignment_stmt
                  ;
```

Notes:

- `pp_directive` is recognized only when the line begins with `[` and the next character is not `[` (to avoid clashing with `[[...]]` rename syntax).
- `pp_directive` token matching is **case-sensitive** in current code.
- `ignored_trailing` means any trailing characters after `]` exist but are ignored with a warning.
- `goto_label_line` warns if anything follows the label name.
- In this engine, `func_signature` subnames (`@NAME[...]`) are validated at load time but do not affect runtime dispatch; the validated list is then discarded. See `labels.md`.

## 4) `#...` lines inside ERB functions (sharp lines)

In ERB, `#...` lines are accepted only in the function's **post-label sharp block**: zero or more consecutive `#...` lines immediately following an `@...` label, before the first non-`#` logical line of that function. Outside that position, a warning is produced and the line is ignored.

```ebnf
sharp_directive ::=
    event_modifier
  | method_marker
  | localsize_marker
  | private_dim
  ;

event_modifier  ::= ("SINGLE" | "LATER" | "PRI" | "ONLY") ;

method_marker   ::= ("FUNCTION" | "FUNCTIONS") ;

localsize_marker ::= ("LOCALSIZE" | "LOCALSSIZE") WS CONST_INT ;

private_dim     ::= ("DIM" | "DIMS") WS dim_decl ;
```

Notes (behavioral constraints):

- `event_modifier` (`#SINGLE/#LATER/#PRI/#ONLY`) is intended for **event functions** only.
  - If used on a non-event function, the loader warns and ignores it.
  - If used on an expression function (`#FUNCTION/#FUNCTIONS`), the loader warns and ignores it.
  - Duplicate flags (`#SINGLE` twice, etc.) warn and the second one is ignored.
  - `#PRI` and `#LATER` can both be set; this warns (`PriWithLater`) but both flags remain enabled (the label is inserted into both groups).
  - `#ONLY` is a strong override:
    - if `#ONLY` is set, the loader clears `#PRI/#LATER/#SINGLE` on that label (each with its own warning)
    - after `#ONLY`, later `#PRI/#LATER/#SINGLE` directives warn and are ignored
    - if multiple definitions of the same event label name use `#ONLY`, the loader warns but still accepts them
- `method_marker` converts a normal function into an “expression function” (`#FUNCTION` returns `long`, `#FUNCTIONS` returns `string`).
  - Event/system labels cannot become expression functions: attempting to use `#FUNCTION/#FUNCTIONS` there produces a level-2 warning and is treated as a parse failure for that sharp line.
  - If the function is already an expression function, repeating the same marker warns; attempting to change `#FUNCTION` ↔ `#FUNCTIONS` is a level-2 warning and is treated as a parse failure.
  - On success, the loader clears any existing `#PRI/#LATER/#SINGLE/#ONLY` flags on that label (each with a warning).
- `LOCALSIZE/LOCALSSIZE` parse an integer expression which must reduce to a compile-time constant (`SingleLongTerm`).
  - Values must be `>= 1` and `< int.MaxValue`.
  - On event functions, these directives warn and are ignored.
  - If the corresponding local variable family (`LOCAL` or `LOCALS`) is prohibited by configuration/CSV, using the directive is a level-2 warning and is ignored.
- `private_dim` creates a **private variable** scoped to the function; the `dim_decl` syntax is shared with ERH `#DIM/#DIMS` (see `variables.md` and the `UserDefinedVariableData.Create(...)` rules).
  - Duplicate private variable names within the same function are level-2 warnings and the declaration is rejected.
  - Extra characters after a valid declaration warn but do not invalidate the declaration.

### 4.1 `dim_decl` (engine-accurate shape)

This is the declaration “payload” parsed after `#DIM` / `#DIMS` in both ERB (private) and ERH (global).

```ebnf
dim_decl        ::= { dim_kw WS } IDENT dim_sizes? dim_init? ;

dim_kw          ::= "CONST" | "REF" | "DYNAMIC" | "STATIC"
                  | "GLOBAL" | "SAVEDATA" | "CHARADATA" ;

dim_sizes       ::= "," dim_size { "," dim_size } ;
dim_size        ::= CONST_INT ;

dim_init        ::= "=" init_list ;
init_list       ::= CONST_TERM { "," CONST_TERM } ;
```

Notes:

- The engine reads a sequence of identifier tokens and treats them as keywords only if they match one of `dim_kw` under the current `IgnoreCase` mode.
  The first identifier that is not a recognized keyword becomes the variable name.
- `dim_size` and each `CONST_TERM` must reduce to a compile-time constant (integer for `#DIM`, string for `#DIMS`).
- Maximum dimension is 3 (and `CHARADATA` reduces that further; see `variables.md`).
- Initializers are allowed only for non-`REF`, non-`CHARADATA`, 1D variables.
- For ordinary variables, `dim_sizes` does not permit empty size slots once the size list has started. `REF` is the special case: there commas indicate dimension, explicit sizes must be `0`, and empty fields between commas are permitted (see `variables.md`).
- Compatibility quirk: while sharp-directive keyword matching follows `IgnoreCase`, this engine determines “is string?” using a later case-sensitive equality check against `"DIMS"`.

Additional compatibility quirk (case-sensitivity inside some sharp directives):

- The directive name token is matched using `IgnoreCase`, **but** this engine uses case-sensitive checks in some subsequent branches:
  - `#LOCALSIZE` vs `#LOCALSSIZE`: the code chooses which length to set using a case-sensitive equality check against the literal `"LOCALSIZE"`. So `#localsize ...` can be accepted but affect `LOCALS` sizing.
  - `#FUNCTION` vs `#FUNCTIONS`: some “duplicate/already declared” diagnostics use case-sensitive checks and can behave oddly if the marker is written with unexpected casing.

## 5) Function label signatures (`@NAME...`)

After `@NAME`, the engine may parse an optional signature.

### 5.1 Signature delimiters

The signature must start with one of:

- `[` — subname list (parsed and validated, but currently ignored by runtime behavior in this engine)
- `(` — argument list in parentheses
- `,` — argument list without parentheses (comma-list to end-of-line)

Any other token after the label name produces an error/warning (“wrong argument format”).

### 5.2 Argument list for definitions

The definition argument list is parsed as a comma-separated sequence of **parameter specs**.
Each parameter spec is:

```ebnf
arglist_define  ::= param_spec { "," param_spec } ;
param_spec      ::= param_lvalue [ "=" param_default ] ;
```

Constraints enforced by the engine:

- `param_lvalue` must restructure to a non-const `VAR_TERM`.
- For non-`REF` parameters, the variable term must have explicit subscripts (no “bare” variable) and all subscripts must be compile-time constants.
- `param_default` (if present) must be a compile-time constant and type-must-match the parameter.
- Defaults are only allowed for parameters that are `ARG`, `ARGS`, or private variables; other parameter lvalues cannot have defaults.
- If `=` is absent, the engine inserts an implicit default `0` / `""` **only** for `ARG`, `ARGS`, and private-variable parameters; otherwise the parameter has no default.
- Event function labels reject all signature content: any tokens after `@EVENT...` emit a level-2 warning and are ignored for argument-binding purposes.
- If config item `CompatiFuncArgOptional` = `YES` allows an argument to be omitted even when there is no default, then the engine leaves that formal lvalue **unassigned** on entry (it retains its previous value in the underlying storage).

## 6) EBNF: statement forms

### 6.1 Standalone increment / decrement

```ebnf
incdec_stmt     ::= ("++" | "--") VAR_TERM
                  | VAR_TERM ("++" | "--")
                  ;
```

As a standalone statement, the yielded value is discarded; only the variable update is observable.

### 6.2 Instruction statement (generic)

Most non-assignment lines that begin with a recognized built-in instruction name are parsed as instruction statements.

Critical quirk: if an instruction has arguments, the character **immediately after the instruction name** must be one of:

- end-of-line, or
- `;` (comment start), or
- whitespace (` `, `\t`, and optionally full-width space under `SystemAllowFullSpace`)

If the next character is something else (for example `(` or `,`), the line becomes invalid.

```ebnf
instruction_stmt ::= INSTR [ instr_sep instr_args ] ;
instr_sep        ::= WS | ";" ;
instr_args       ::= raw_argument_region ;
```

`INSTR` is a keyword recognized by `IdentifierDictionary.GetFunctionIdentifier(...)`.
`raw_argument_region` is parsed by the instruction’s `ArgumentBuilder`; for many instructions it is a comma-separated `arglist` as defined by the `arglist` production in this grammar.

Note: if `instr_sep` is `;`, the separator begins a comment and `instr_args` is effectively empty (argument builders therefore see “no arguments”).

Special-case instructions (when enabled):

- If `UseScopedVariableInstruction` is enabled, the `VARI` / `VARS` instructions use a dedicated parsing path that does **not** enforce the “separator must be whitespace/`;`/EOL” rule, and uses custom parsing for declarations and initializers.

### 6.3 Assignment statement

If a line is not recognized as an instruction, the engine treats it as an assignment candidate: it locates an assignment operator and then delegates to the `SET` instruction’s argument builder.

Important compatibility detail:

- Assignment syntax is routed through a dedicated assignment-instruction path rather than through a normal user-callable `SET` keyword.
- As a result, writing a line that literally starts with `SET ...` does **not** invoke assignment behavior.
- Assignment statements and standalone increment/decrement lines (`++X`, `--X`, `X++`, `X--`) are still represented as ordinary `InstructionLine`s and are executed by the normal interpreter loop like other instruction lines.

Assignment operators accepted by the lexer in assignment context:

- `=` and (compat) `==` (warns, then treated as `=`)
- `+=`, `-=`, `*=`, `/=`, `%=`
- `<<=`, `>>=`
- `|=`, `&=`, `^=`
- postfix `++`, `--` (recognized by the lexer here, but factored out as `incdec_stmt` in the user-facing statement grammar)
- string assignment operator `'=`

```ebnf
assignment_stmt  ::= VAR_TERM assign_op assign_rhs ;
assign_op        ::= "=" | "==" | "+=" | "-=" | "*=" | "/=" | "%="
                   | "<<=" | ">>=" | "|=" | "&=" | "^="
                   | "'="
                   ;
assign_rhs       ::= assignment_rhs_region ;
```

Notes:

- The exact RHS parsing depends on the LHS variable’s type (integer vs string) and on the operator. Standalone postfix `++/--` are covered by `incdec_stmt`, so `assignment_stmt` itself always has an RHS region.
- For integer variables, multiple comma-separated RHS values can be accepted for array assignment when using `=`.
- For string variables:
  - `=` parses the RHS using the **formatted-string (FORM) scanner**, not the normal expression lexer.
  - `'=` parses the RHS as a normal expression, and each RHS expression must be string-typed.
  - `+=` parses one normal-expression RHS, which must be string-typed.
  - `*=` parses one normal-expression RHS, which must be int-typed.
  - only `'=`, as the operator, supports “batch assignment” (multiple comma-separated RHS values) for string variables.
  - config item `SystemIgnoreStringSet` can prohibit `=` on string variables (while still allowing `'=`, `+=`, `*=`).

Batch assignment semantics (which elements are written, and out-of-range behavior) are specified in `variables.md`.

### 6.4 Comma-separated argument lists (common form)

Many argument builders parse the remaining text as:

```ebnf
arglist          ::= [ arg ] { "," [ arg ] } ;
arg              ::= EXPR ;
```

An empty field between commas denotes an **omitted argument**.

## 7) Core control-flow blocks (structural rules + argument syntax)

This section covers the block-structured core control flow that affects parsing and matching.
The engine validates block pairing while building the function’s instruction list (nesting stack).

### 7.1 `SIF` (single-line IF)

```ebnf
sif_stmt         ::= "SIF" WS INT_EXPR ;
```

Behavioral constraints:

- The statement after `SIF` is conditionally skipped; the loader enforces several constraints:
  - `SIF` must not be the last effective line in a function (missing/EOF next line is an error).
  - The next line must not be a function label (`@...`) or file boundary marker.
  - The next line must not be a local label definition (`$...`).
  - The next line must not be a **partial / structural** instruction line (e.g. `IF`, `SELECTCASE`, loops, `CATCH`-family markers).
  - A non-adjacent next physical source line emits a level-0 warning (but is still allowed).

### 7.2 `IF` / `ELSEIF` / `ELSE` / `ENDIF`

```ebnf
if_block         ::= "IF" WS INT_EXPR
                     { if_body_line }
                     { "ELSEIF" WS INT_EXPR { if_body_line } }
                     [ "ELSE" { if_body_line } ]
                     "ENDIF" ;
```

Notes:

- `ELSE` takes no arguments.
- The engine links `IF/ELSEIF/ELSE` cases to their `ENDIF` during load; unexpected `ENDIF` or `ELSE/ELSEIF` outside an `IF` warns.

### 7.3 `SELECTCASE` / `CASE` / `CASEELSE` / `ENDSELECT`

```ebnf
selectcase_block ::= "SELECTCASE" WS EXPR
                     { case_clause }
                     "ENDSELECT" ;

case_clause      ::= "CASE" WS case_arglist { case_body_line }
                   | "CASEELSE" { case_body_line }
                   ;

case_arglist     ::= case_expr { "," case_expr } ;
case_expr        ::= "IS" WS binary_op WS EXPR
                   | EXPR [ WS "TO" WS EXPR ]
                   ;
```

Notes:

- `SELECTCASE` expression type (int vs string) must match each `CASE` expression’s type; mismatches warn as errors.
- `TO` forms an inclusive range comparison; for strings it uses ordinal comparisons.
- `CASE` after `CASEELSE` warns (still accepted).

### 7.4 Loops: `REPEAT/REND`, `FOR/NEXT`, `WHILE/WEND`, `DO/LOOP`

```ebnf
repeat_block     ::= "REPEAT" WS INT_EXPR { loop_body_line } "REND" ;

for_block        ::= "FOR" WS VAR_TERM "," [ INT_EXPR ] "," INT_EXPR [ "," INT_EXPR ]
                     { loop_body_line }
                     "NEXT" ;

while_block      ::= "WHILE" WS INT_EXPR { loop_body_line } "WEND" ;

do_loop_block    ::= "DO" { loop_body_line } "LOOP" WS INT_EXPR ;
```

Notes:

- `FOR` argument positions are: loop variable, start (may be omitted, defaults to `0`), end, step (optional, defaults to `1`).
- Loop matching is validated during load; missing/extra `REND/NEXT/WEND/LOOP` warn as errors.

### 7.5 `BREAK` / `CONTINUE`

```ebnf
break_stmt       ::= "BREAK" ;
continue_stmt    ::= "CONTINUE" ;
```

These are structurally valid only inside loops; the engine resolves jump targets based on the nearest enclosing loop block.

### 7.6 `TRYC... CATCH ... ENDCATCH` (missing-target catch blocks)

This engine has a “try-catch” *structural* form that only handles “target not found” cases for some jump/call instructions.

```ebnf
tryc_block       ::= tryc_stmt { tryc_body_line } "CATCH" { catch_body_line } "ENDCATCH" ;

tryc_stmt        ::= ("TRYCCALL" | "TRYCJUMP" | "TRYCCALLFORM" | "TRYCJUMPFORM"
                    | "TRYCGOTO" | "TRYCGOTOFORM")
                    WS call_target [ call_tail ] ;
```

Notes (engine-accurate):

- `tryc_stmt` is a normal instruction line (with its own argument builder), but it is also treated as a structural “opener” during block matching.
- `CATCH` must match the nearest preceding `TRYC*` opener; otherwise it is an error.
- `ENDCATCH` must match a preceding `CATCH`; otherwise it is an error.
- When the opener succeeds, the `CATCH` marker line skips the catch body by jumping to `ENDCATCH`.
- When the opener fails because its target is not found, the engine jumps to the `CATCH` marker and executes the catch body.
- This mechanism does not catch arbitrary runtime errors; it only handles the “not found” cases where the underlying resolver returns `null`.

### 7.7 Block matching and error recovery (loader behavior)

While loading ERB, Emuera maintains a nesting stack and performs matching for several “paired” instructions.

Core matching pairs (open → close):

- `IF` → `ENDIF` (with `ELSEIF`/`ELSE` clauses inside)
- `SELECTCASE` → `ENDSELECT` (with `CASE`/`CASEELSE` clauses inside)
- `REPEAT` → `REND`
- `FOR` → `NEXT`
- `WHILE` → `WEND`
- `DO` → `LOOP`
- `TRYC*` (`TRYCCALL`/`TRYCGOTO`/etc.) → `CATCH` → `ENDCATCH`
- `TRY*LIST` (`TRYCALLLIST`/`TRYJUMPLIST`/`TRYGOTOLIST`) → `ENDFUNC` (with `FUNC` clauses inside)

Notable recovery behavior:

- Encountering `CASE`/`CASEELSE`/`ENDSELECT` while the stack top is not `SELECTCASE` triggers warnings and causes the loader to pop intervening unmatched blocks until a `SELECTCASE` is found (preventing cross-block closure).
- Missing closers (e.g. end-of-file reached while `IF` is still open) produce warnings at file end; the resulting jump links may be incomplete.

### 7.8 `TRY...LIST` blocks

```ebnf
trylist_block    ::= trylist_open { trylist_func } "ENDFUNC" ;

trylist_open     ::= ("TRYCALLLIST" | "TRYJUMPLIST" | "TRYGOTOLIST") ;
trylist_func     ::= "FUNC" WS call_target [ call_tail ] ;
```

Notes (engine-accurate):

- `trylist_open` takes no arguments.
- Inside the block, only `FUNC` and `ENDFUNC` are allowed (other instructions are errors).
- These blocks are not nestable.
- `FUNC` uses the same call-target parsing shape as call-like instructions, and in this engine it accepts the same FORM-capable target style as `CALLFORM`.
- For `TRYGOTOLIST`, `FUNC` must not specify subnames or arguments.

## 8) Calls and jumps (statement-level syntax)

The following syntax is relevant for control flow and is parsed by a dedicated argument builder.

```ebnf
call_like        ::= ("CALL" | "CALLF" | "JUMP" | "GOTO" | "TRYCCALL" | "TRYCJUMP" | "TRYCGOTO" | ...)
                     WS call_target [ call_tail ] ;

call_target      ::= call_target_str
                   | call_target_form
                   ;

call_target_str  ::= raw_string_until_delim ;
call_target_form ::= FORM_STR ;  (* when using CALLFORM/CALLFORMF/JUMPFORM/... *)

call_tail        ::= subnames [ "(" arglist ")" ]
                   | "(" arglist ")"
                   | "," arglist
                   ;
```

Notes:

- `call_target_str` is read as raw text up to one of: `(`, `[`, `,`, `;` and then trimmed of half-width spaces/tabs.
- If `;` appears, it starts a comment; the remaining text is ignored.
- The engine also supports “subnames” syntax (`[...]`) at call sites and in label definitions, but in this engine it is effectively **validated then ignored** (it does not affect runtime dispatch). See `functions.md` and `labels.md` for details.

## 9) ERH file grammar (header files)

ERH files are not “normal ERB”: each enabled line must start with `#` after leading whitespace is skipped.

```ebnf
erh_file        ::= { erh_line } ;
erh_line        ::= WS? "#" erh_directive ;

erh_directive   ::= "DEFINE" WS IDENT WS macro_replacement
                 | ("DIM" | "DIMS") WS dim_decl
                 | ("FUNCTION" | "FUNCTIONS") WS ...   (* not implemented in this engine *)
                 ;
```

Key compatibility notes:

- `#DEFINE` in this engine supports **empty macros** (no replacement tokens), but **does not allow function-like macros** (`NAME(arg1,...)`): those are explicitly rejected.
- `#FUNCTION/#FUNCTIONS` in ERH are recognized by the loader, but are currently not implemented and therefore error if encountered.
- `#DIM/#DIMS` are queued and processed later as a batch; they share the same declaration syntax family as ERB `#DIM/#DIMS`.
