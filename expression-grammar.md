# EraBasic Expression Grammar (EBNF, Emuera)

This document specifies EraBasic’s **expression syntax** as implemented by this Emuera codebase.

It is **self-contained**: it defines the accepted tokens, operator set, precedence, and the main parser quirks needed to reimplement a compatible expression parser.

For formatted strings (FORM) details, see `formatted-strings.md` (this document treats formatted strings as a token form that produces a string expression node).

## 1) Value model and types

Emuera expressions are dynamically typed at runtime but have a small static type set:

- **Integer**: `Int64` (`long`)
- **String**: `string`
- There is **no array value type**. Arrays exist as variable storage; expressions can read/write **array elements** via `VAR:...` terms, but cannot produce or pass “array values” (no array literals, no array return values).

Many parsing rules depend on the expected type context (e.g., instruction argument builders may require integer expressions).

Implementation note (runtime arithmetic):

- Integer operations use `Int64` (`long`) arithmetic and follow .NET default behavior as detailed below:
  - overflow wraps around (unchecked)
  - `/` and `%` throw on divide-by-zero
  - `<<` / `>>` cast the shift count to `int` before shifting (so behavior matches C# shift semantics)

## 2) Tokenization model (what the expression parser sees)

Expressions are not parsed from raw characters directly: Emuera first lexes a character stream into a token sequence containing:

- integer literals
- string literals `"..."`, with C-like escape sequences handled by the string reader
- identifiers
- operators, including multi-character operators like `>=`, `&&`, `!|`
- symbols such as `(` `)` `,` `:` `@` `]`
- formatted-string tokens, produced by:
  - `@"...FORM..."` (formatted-string literal), and
  - `\@ ... ? ... # ... \@` (string-ternary literal form; see §6.4)

### 2.1 Macro expansion happens at the token level

After lexing, the lexer may expand `#DEFINE` macros inside that token sequence:

- Macro expansion is **token-based** (not raw-text).
- Function-like macros are supported by the lexer (they use `(...)`), but **ERH `#DEFINE` in this engine rejects function-like macros** (encountering them is an error).
- Macro expansion is bounded (there is a maximum expansion count; exceeding it is an error).

Expression parsing in this document assumes it receives the post-expansion token sequence.

## 3) Operator set and precedence (source of truth)

The lexer recognizes exactly these operator tokens for expressions:

- Unary: `+` `-` `!` `~` `++` `--`
- Postfix unary: `++` `--`
- Arithmetic: `+` `-` `*` `/` `%`
- Comparisons: `==` `!=` `<` `<=` `>` `>=`
- Bitwise: `&` `^` `|`
- Logical: `&&` `||` `^^` `!&` `!|`
- Shifts: `<<` `>>`
- Ternary: `?` and `#` (the separator is `#`, not `:`)

Precedence is implemented by integer priority values plus a dedicated postfix-unary reduction step. The effective precedence order is (high → low):

1) postfix unary: `++ --`
2) prefix unary: `+ - ! ~` (and the prefix forms of `++ --` when allowed)
3) multiplicative: `* / %`
4) additive: `+ -`
5) shifts: `<< >>`
6) comparisons: `< > <= >=`
7) equality: `== !=`
8) bitwise: `& ^ |` (all three share one precedence level in this engine)
9) logical: `&& || ^^ !& !|` (all five share one precedence level in this engine)
10) ternary: `? ... # ...` (lowest)

Associativity: operators with the same precedence behave as **left-associative** in this parser. Postfix `++/--` bind before any pending prefix unary, so `-X++` parses as `-(X++)`.

## 3.1 Evaluation semantics (engine-accurate)

### Boolean results are `0/1`

All comparisons and logical operators return:

- `1` for “true”
- `0` for “false”

This includes `== != < <= > >=`, `!`, `&&`, `||`, `^^`, `!&`, `!|`.

### Short-circuiting operators

The engine evaluates operands left-to-right.

Short-circuiting behavior is implemented in the operator methods:

- `&&` and `||` short-circuit (the right operand may not be evaluated).
- `!&` (logical NAND) and `!|` (logical NOR) short-circuit (the right operand may not be evaluated).
- `^^` (logical XOR) does **not** short-circuit (both operands are evaluated).
- ternary `? ... # ...` short-circuits: only the chosen branch is evaluated.

### Overflow / corner cases

- Integer arithmetic uses `long` and follows the host's plain `Int64` operator behavior. There is no explicit overflow check for `+`, binary `-`, `*`, bitwise operators, or shifts, so overflow wraps in two's-complement style.
- Unary minus has one special case: when the operand is `long.MinValue`, the engine prints a system warning line and returns `long.MinValue` (because `-long.MinValue` overflows back to itself).
- Division and modulo use the host `long / long` and `long % long` operators:
  - divisor `0` throws the engine's divide-by-zero runtime error,
  - otherwise division truncates toward zero,
  - the remainder keeps the sign of the left operand,
  - exceptional host-overflow cases such as `long.MinValue / -1` and `long.MinValue % -1` propagate as overflow failures rather than being rewritten into divide-by-zero.
- Shift operators first evaluate the right operand as `long`, then cast it to `int`, then apply the host `long << int` / `long >> int` semantics:
  - the effective shift count is the low 6 bits of that `int` value (so counts behave modulo `64`),
  - negative counts therefore wrap through the same rule (`-1` behaves like `63`, `-64` behaves like `0`),
  - `>>` is an arithmetic right shift (sign-extending) because the operand type is signed `long`.

Examples:

- `-7 / 3 == -2`
- `-7 % 3 == -1`
- `7 % -3 == 1`
- `1 << 64 == 1`
- `1 << -1 == 1 << 63`

### Restructure (constant folding) affects when errors happen

Many engine paths call `Restructure(exm)` on expression trees during load/parse (especially instruction argument parsing and assignment parsing).

Consequences:

- Constant subexpressions are folded into constant expression nodes.
- Errors inside constant-only subexpressions (e.g. division by zero; invalid string repetition count) can occur at load time rather than runtime.

## 4) Expression grammar (EBNF)

This EBNF describes the shape of expressions the parser accepts. It is organized by precedence.

### 4.1 Primary terms

```ebnf
primary
  ::= int_lit
   | str_lit
   | formatted_str
   | variable_term
   | func_call
   | "(" expr ")"
  ;
```

Where:

- `int_lit` is an `Int64` literal.
- `str_lit` is a double-quoted string literal.
- `formatted_str` is a formatted-string literal token (`@"..."`) or a `\@...\@` token that produces a string term.
- `func_call` is a built-in or user-defined expression function call by name.

### 4.2 Unary

```ebnf
unary
  ::= [ unary_op ] postfix
  ;

unary_op ::= "+" | "-" | "!" | "~" | "++" | "--" ;
```

Notes:

- `+` as unary on an integer is a no-op.
- Unary operators apply only to integer operands. Applying them to strings is an error.
- The parser accepts **at most one** prefix unary operator. Chains such as `!!X`, `-~X`, or `++--X` are rejected.
- Prefix `++/--` require a non-const integer variable term and have side effects:
  - `++X` / `--X` yield the **new** value.

### 4.3 Postfix (`++` / `--`)

```ebnf
postfix
  ::= primary [ postfix_op ]
  ;

postfix_op ::= "++" | "--" ;
```

Constraints:

- Postfix `++/--` are only valid on a **non-const variable term** of integer type.
- The parser accepts **at most one** postfix `++/--` on a primary; forms such as `X++++` are rejected.
- The parser also rejects combining prefix and postfix increment/decrement on the same primary (for example `++X++`).
- `X++` / `X--` yield the **old** value.
- The same prefix/postfix `++/--` forms are also accepted as standalone statements; see `grammar.md`.

### 4.4 Binary operator ladder

```ebnf
mul   ::= unary { ("*" | "/" | "%") unary } ;
add   ::= mul   { ("+" | "-") mul } ;
shift ::= add   { ("<<" | ">>") add } ;
rel     ::= shift   { ("<" | "<=" | ">" | ">=") shift } ;
eq      ::= rel     { ("==" | "!=") rel } ;
bitwise ::= eq      { ("&" | "^" | "|") eq } ;
logic   ::= bitwise { ("&&" | "||" | "^^" | "!&" | "!|") bitwise } ;
```

Type rules (as implemented):

- Most binary operators require both operands to be integers.
- For strings:
  - `str + str` is concatenation.
  - `str * int` and `int * str` repeat the string. The repeat count must satisfy `0 <= n < 10000`; values outside that range are errors in this engine.
  - Comparisons `== != < <= > >=` are allowed for `str` vs `str` using ordinal comparisons.
- Any other int/string mixes are errors.

### 4.5 Ternary

```ebnf
expr ::= ternary ;

ternary
  ::= logic [ "?" expr "#" expr ] ;
```

Constraints (as implemented):

- The parser requires `?` to be paired with `#`. Missing `#` is an error; stray `#` without a preceding `?` is an error.
- Type rules:
  - Condition must be integer (`long`).
  - Both branches must be integers or both branches must be strings.

## 5) Identifiers: variable terms vs function calls

When the parser sees an identifier `IDENT`, it decides its meaning by the next token:

1) If followed by `(`, it is a **function call**: `IDENT "(" arglist ")"`.
2) Otherwise it is a **variable term** *if* the identifier resolves to a variable token; if not, the parser tries:
   - function-reference (if the identifier resolves to a referenceable function/method name), or
   - a “named constant key” in the special context of variable `:` arguments, or
   - otherwise it errors (“cannot interpret identifier”).

### 5.1 Function call

```ebnf
func_call ::= IDENT "(" [ arglist ] ")" ;
arglist   ::= expr { "," expr } ;
```

Notes:

- `IDENT "[" ... "]"` function calls are explicitly rejected in this engine.
- Argument lists can contain **empty slots** (e.g. `F(a,,c)` or `F(a,)`):
  - the expression parser represents an empty slot as `null` in the argument list
  - whether `null` is accepted, treated as “omitted”, or rejected is method-specific (validated by the called built-in method or user-defined signature rules)

### 5.2 Variable term

```ebnf
variable_term
  ::= IDENT [ "@" IDENT ] { ":" var_arg } ;

var_arg ::= expr ;
```

Notes and constraints:

- Up to **3** `:` arguments are allowed syntactically; semantic rules then depend on the variable’s dimension and category (see `variables.md` and `runtime-model.md`).
- `@IDENT` is not a general “namespace” feature in this engine:
  - it is accepted only for the local-variable families `LOCAL`, `LOCALS`, `ARG`, and `ARGS`
  - using it with a global variable or a private `#DIM/#DIMS` variable is an error
  - `@` is **not** an expression operator: it is recognized only in this specific spot while parsing a variable identifier.
    - Example: `(A+B)@X` is a parse error (“unexpected symbol `@`”) in expression-parsed contexts.
- Omitted/implicit indices are part of variable-term construction (argument inference):
  - For non-character **1D** arrays, omitting the index makes it `:0`; for `RAND`, this is accepted only when `CompatiRAND=YES`, and otherwise omission errors.
  - For character-data **1D** arrays, a single written index is treated as the element index and the character selector defaults to `TARGET` (when `SystemNoTarget=NO`); selecting a specific character requires writing both indices.
  - For **2D/3D** arrays, omitting required indices can produce a “no-arg variable term” that throws a “missing variable argument” error if evaluated as a value.
- In a `var_arg` position, the parser may accept a **bare identifier** as a string key (e.g. `ABL:Skill`) *only if* that identifier does not resolve to a variable/function name and is a known key for that table/variable.
- Some variables (notably character variables) have **argument auto-completion** behavior that is config-dependent (`SystemNoTarget`).
- `RAND` argument omission/zero behavior is config-dependent (`CompatiRAND`).

## 6) Formatted strings inside expressions

Formatted strings are parsed by a separate formatted-string analyzer and then inserted into expressions as a string-valued term.

Two forms exist at the lexer level:

### 6.1 `@"..."`

`@"...` starts a formatted-string literal; the lexer produces a `StrFormWord` token up to the closing `"`.

### 6.2 `\@...\@` (string-ternary literal form)

The lexer supports a special `\@...\@` construct intended for a string-ternary form:

- it is tokenized as a formatted-string token containing a sub-word that itself parses the inner ternary split by `?` and `#`.

From the expression parser’s perspective, this is just a `formatted_str` primary producing a string.

The full scanner rules (including the fact that the `#` branch can be omitted with a warning) are specified in `formatted-strings.md`.

## 7) Context-sensitive terminators (`=`, `)`, `]`, `,`)

The expression parser is often invoked with an “end-with” set (examples):

- parse up to end-of-line
- parse up to `,`
- parse up to `)` or `]`
- parse up to an assignment `=` (used in function signature parsing)

Notable rule:

- `=` is **not** an operator inside expressions; seeing `=` in a normal expression context is an error.
- When the caller enables “assignment terminator” mode, the expression parser stops before consuming the `=` token.

## 8) Non-normative: Emuera’s expression parsing and evaluation model

This section is **not** part of EraBasic’s expression *syntax*. It is a supplementary engine-model note that helps explain where certain expression work happens (parse time vs runtime).

### 8.1 Parse time: operator-precedence reduction → expression tree

Emuera does **not** parse expressions by directly constructing EBNF productions. Instead, it reads a token stream and incrementally reduces it using a precedence-aware working stack:

- The parser maintains a working stack for operators and partially built subexpressions.
- That working stack holds a mix of:
  - operator markers, and
  - partially built expression nodes.
- When an operator is encountered, the parser compares precedence to the stack top and reduces prior operators first (left-associative behavior for same precedence).
- Reduction creates new expression-tree nodes:
  - unary operator + operand → new expression node
  - binary operator + left/right → new expression node
  - ternary `? ... # ...` reduces into a ternary expression node

Conceptually, this is similar to a shunting-yard / operator-precedence reduction approach. The key point is that this stack is only a **parsing** data structure used to build an expression tree.

### 8.2 Runtime: AST evaluation (host call stack), not a stack-bytecode VM

Once parsed, the engine evaluates expressions primarily by recursively calling virtual methods on the expression tree:

- Numeric evaluation dispatches to the expression tree's numeric-evaluation path.
- String evaluation dispatches to the expression tree's string-evaluation path.

Intermediate results flow through the host language’s call stack and locals; Emuera does **not** run expressions by interpreting a separate “operand stack bytecode” representation.

This matters when comparing execution models:

- a fine-grained stack-bytecode VM must frequently materialize intermediate values into a VM value stack between tiny steps
- Emuera’s AST model computes many intermediate values directly as local temporaries within C# methods
