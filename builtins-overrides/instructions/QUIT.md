**Summary**
- Ends the current run by requesting the console to quit.

**Syntax**
- `QUIT`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Calls `Console.Quit()`, which sets the console state to `Quit`.
- Script execution stops because `Console.IsRunning` becomes false.
- UI shutdown is handled by the console’s event loop (implementation detail).

**Errors & validation**
- None.

**Examples**
- `QUIT`

**Progress state**
- complete

