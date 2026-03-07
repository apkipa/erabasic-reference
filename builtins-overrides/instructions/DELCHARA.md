**Summary**
- Deletes one or more characters from the current character list by character index.

**Tags**
- characters

**Syntax**
- `DELCHARA charaIndex`
- `DELCHARA charaIndex1, charaIndex2, ...`

**Arguments**
- Each `charaIndex` (int): selects an existing character index.

**Semantics**
- Requires at least one argument; multiple arguments are accepted but a parse-time warning is emitted for multi-argument uses.
- Evaluates all `charaIndex` arguments first (left-to-right), storing the integer results in an array.
- Deletion behavior depends on argument count:
  - If exactly one index was provided: deletes that character immediately by index.
  - If multiple indices were provided: deletes all referenced characters as a set.
    - Each index is resolved against the character list as it existed before any removals in this call.
    - The engine rejects duplicate deletions by identity (two indices that resolve to the same character object cause an error).
    - If an error occurs while processing a multi-delete list, some earlier listed characters may already have been deleted (no rollback).
- Deleting characters shifts indices of later characters; after deletion, valid indices are always a dense range `0 <= i < CHARANUM`.
- The engine does not automatically rebind `TARGET`/`MASTER`/`ASSI` after deletion.

**Errors & validation**
- Runtime error if any `charaIndex` is out of range.
- When deleting multiple characters, runtime error if the same character is specified more than once (duplicate deletion).

**Examples**
```erabasic
DELCHARA 2
DELCHARA 1, 3
```

**Progress state**
- complete
