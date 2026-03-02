# Built-ins (Engine Metadata Appendix)

This appendix augments `builtins-engine.md` by attaching **engine-extracted metadata** to built-ins.

This is intended for reimplementations that need to match:

- which statement keywords exist (instruction identifiers)
- how arguments are parsed (by `FunctionArgType` / `ArgumentBuilder` selection)
- which instructions are marked `METHOD_SAFE`, `FLOW_CONTROL`, `PARTIAL`, etc.
- which instructions participate in block matching (`funcMatch` / `funcParent`)

Important scope note:

- This table covers **explicitly registered statement keywords** from `FunctionIdentifier`’s registration (`addFunction(...)`, `addPrintFunction(...)`, etc.), plus the parser-internal pseudo instruction `SET`.
- Separately, this engine also inserts many **expression-function (method)** names into the same identifier table as “callable as statement” stubs when no instruction keyword with the same name exists. That “method-as-instruction” behavior is not yet tabulated here.

Limitations (important):

- For instructions registered with a custom `AInstruction` instance, the `Flags` cell is a best-effort extraction of the instruction class’s own `flag = ...` assignment (from `Instraction.Child.cs`) combined with any extra flags passed in registration.
  Note that some instruction classes further mutate `flag` later (e.g. `flag |= ...`), sometimes conditionally; this appendix currently only captures the initial `flag = ...` assignment.
  Some instruction classes are defined outside `Instraction.Child.cs`; those may appear as “unknown”.
- This table does **not** describe runtime semantics of each built-in; it only describes registration/shape metadata.

Row count: 303 (includes parser-internal `SET`).

## Instructions and statement keywords

| Name | Kind | Arg Spec | Flags | Match End | Parent | Notes |
|---|---|---|---|---|---|---|
<!-- ROWS START -->
| `ADDCHARA` | instruction | AInstruction: ADDCHARA_Instruction | METHOD_SAFE |  |  |  |
| `ADDCOPYCHARA` | instruction | AInstruction: ADDCOPYCHARA_Instruction | METHOD_SAFE |  |  |  |
| `ADDDEFCHARA` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `ADDSPCHARA` | instruction | AInstruction: ADDCHARA_Instruction | METHOD_SAFE |  |  |  |
| `ADDVOIDCHARA` | instruction | AInstruction: ADDVOIDCHARA_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `ALIGNMENT` | instruction | FunctionArgType.STR (STR_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `ARRAYCOPY` | instruction | FunctionArgType.SP_COPY_ARRAY (SP_COPY_ARRAY_Arguments) | EXTENDED \| METHOD_SAFE |  |  |  |
| `ARRAYREMOVE` | instruction | FunctionArgType.SP_CONTROL_ARRAY (SP_CONTROL_ARRAY_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `ARRAYSHIFT` | instruction | FunctionArgType.SP_SHIFT_ARRAY (SP_SHIFT_ARRAY_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `ARRAYSORT` | instruction | FunctionArgType.SP_SORTARRAY (SP_SORT_ARRAY_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `ASSERT` | instruction | FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder) | EXTENDED \| METHOD_SAFE \| DEBUG_FUNC |  |  |  |
| `AWAIT` | instruction | AInstruction: AWAIT_Instruction | EXTENDED |  |  |  |
| `BAR` | instruction | AInstruction: BAR_Instruction | EXTENDED \| METHOD_SAFE \| IS_PRINT |  |  |  |
| `BARL` | instruction | AInstruction: BAR_Instruction | EXTENDED \| METHOD_SAFE \| IS_PRINT |  |  |  |
| `BEGIN` | instruction | AInstruction: BEGIN_Instruction | FLOW_CONTROL |  |  |  |
| `BINPUT` | instruction | AInstruction: BINPUT_Instruction | IS_PRINT \| IS_INPUT |  |  |  |
| `BINPUTS` | instruction | AInstruction: BINPUTS_Instruction | IS_PRINT \| IS_INPUT |  |  |  |
| `BREAK` | instruction | AInstruction: BREAK_Instruction | FLOW_CONTROL \| METHOD_SAFE |  |  |  |
| `CALL` | instruction | AInstruction: CALL_Instruction | FLOW_CONTROL \| FORCE_SETARG |  |  |  |
| `CALLEVENT` | instruction | AInstruction: CALLEVENT_Instruction | FLOW_CONTROL \| EXTENDED |  |  |  |
| `CALLF` | instruction | AInstruction: CALLF_Instruction | EXTENDED \| METHOD_SAFE \| FORCE_SETARG |  |  |  |
| `CALLFORM` | instruction | AInstruction: CALL_Instruction | FLOW_CONTROL \| EXTENDED \| FORCE_SETARG |  |  |  |
| `CALLFORMF` | instruction | AInstruction: CALLF_Instruction | EXTENDED \| METHOD_SAFE \| FORCE_SETARG |  |  |  |
| `CALLSHARP` | instruction | AInstruction: CALLSHARP_Instruction | EXTENDED \| METHOD_SAFE \| FORCE_SETARG |  |  |  |
| `CALLTRAIN` | instruction | FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder) | FLOW_CONTROL \| EXTENDED |  |  |  |
| `CASE` | instruction | AInstruction: ELSEIF_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| PARTIAL \| FORCE_SETARG |  |  |  |
| `CASEELSE` | instruction | AInstruction: ELSEIF_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| PARTIAL \| FORCE_SETARG |  |  |  |
| `CATCH` | instruction | AInstruction: CATCH_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| PARTIAL | `ENDCATCH` |  |  |
| `CLEARBGIMAGE` | instruction | AInstruction: CLEARBGIMAGE_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `CLEARBIT` | instruction | AInstruction: SETBIT_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `CLEARLINE` | instruction | AInstruction: CLEARLINE_Instruction | EXTENDED \| METHOD_SAFE \| IS_PRINT |  |  |  |
| `CLEARTEXTBOX` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `CONTINUE` | instruction | AInstruction: CONTINUE_Instruction | FLOW_CONTROL \| METHOD_SAFE |  |  |  |
| `COPYCHARA` | instruction | AInstruction: COPYCHARA_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `CUPCHECK` | instruction | FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `CUSTOMDRAWLINE` | instruction | AInstruction: CUSTOMDRAWLINE_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `CVARSET` | instruction | AInstruction: CVARSET_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `DATA` | instruction | FunctionArgType.STR_NULLABLE (STR_ArgumentBuilder) | EXTENDED \| METHOD_SAFE \| PARTIAL |  |  |  |
| `DATAFORM` | instruction | FunctionArgType.FORM_STR_NULLABLE (FORM_STR_ArgumentBuilder) | EXTENDED \| METHOD_SAFE \| PARTIAL |  |  |  |
| `DATALIST` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | EXTENDED \| METHOD_SAFE \| PARTIAL | `ENDLIST` |  |  |
| `DEBUGCLEAR` | instruction | AInstruction: DEBUGCLEAR_Instruction | EXTENDED \| METHOD_SAFE \| DEBUG_FUNC |  |  |  |
| `DEBUGPRINT` | instruction | AInstruction: DEBUGPRINT_Instruction | EXTENDED \| METHOD_SAFE \| DEBUG_FUNC |  |  |  |
| `DEBUGPRINTFORM` | instruction | AInstruction: DEBUGPRINT_Instruction | EXTENDED \| METHOD_SAFE \| DEBUG_FUNC |  |  |  |
| `DEBUGPRINTFORML` | instruction | AInstruction: DEBUGPRINT_Instruction | EXTENDED \| METHOD_SAFE \| DEBUG_FUNC |  |  |  |
| `DEBUGPRINTL` | instruction | AInstruction: DEBUGPRINT_Instruction | EXTENDED \| METHOD_SAFE \| DEBUG_FUNC |  |  |  |
| `DELALLCHARA` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `DELCHARA` | instruction | AInstruction: ADDCHARA_Instruction | METHOD_SAFE |  |  |  |
| `DELDATA` | instruction | AInstruction: DELDATA_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `DO` | instruction | AInstruction: ENDIF_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| PARTIAL \| FORCE_SETARG | `LOOP` |  |  |
| `DOTRAIN` | instruction | FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder) | FLOW_CONTROL \| EXTENDED |  |  |  |
| `DRAWLINE` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | METHOD_SAFE |  |  |  |
| `DRAWLINEFORM` | instruction | FunctionArgType.FORM_STR (FORM_STR_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `DT_COLUMN_OPTIONS` | instruction | AInstruction: DT_COLUMN_OPTIONS_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `DUMPRAND` | instruction | AInstruction: DUMPRAND_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `ELSE` | instruction | AInstruction: ELSEIF_Instruction | FLOW_CONTROL \| METHOD_SAFE \| PARTIAL \| FORCE_SETARG |  |  |  |
| `ELSEIF` | instruction | AInstruction: ELSEIF_Instruction | FLOW_CONTROL \| METHOD_SAFE \| PARTIAL \| FORCE_SETARG |  |  |  |
| `ENCODETOUNI` | instruction | FunctionArgType.FORM_STR_NULLABLE (FORM_STR_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `ENDCATCH` | instruction | AInstruction: ENDIF_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| PARTIAL \| FORCE_SETARG |  |  |  |
| `ENDDATA` | instruction | AInstruction: DO_NOTHING_Instruction | EXTENDED \| METHOD_SAFE \| PARTIAL |  |  |  |
| `ENDFUNC` | instruction | AInstruction: ENDIF_Instruction | FLOW_CONTROL \| EXTENDED \| PARTIAL \| FORCE_SETARG |  |  |  |
| `ENDIF` | instruction | AInstruction: ENDIF_Instruction | FLOW_CONTROL \| METHOD_SAFE \| PARTIAL \| FORCE_SETARG |  |  |  |
| `ENDLIST` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | EXTENDED \| METHOD_SAFE \| PARTIAL |  |  |  |
| `ENDNOSKIP` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | EXTENDED \| METHOD_SAFE \| PARTIAL |  |  |  |
| `ENDSELECT` | instruction | AInstruction: ENDIF_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| PARTIAL \| FORCE_SETARG |  |  |  |
| `FONTBOLD` | instruction | AInstruction: FONTBOLD_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `FONTITALIC` | instruction | AInstruction: FONTITALIC_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `FONTREGULAR` | instruction | AInstruction: FONTREGULAR_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `FONTSTYLE` | instruction | FunctionArgType.INT_EXPRESSION_NULLABLE (INT_EXPRESSION_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `FOR` | instruction | AInstruction: REPEAT_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| PARTIAL | `NEXT` |  |  |
| `FORCEKANA` | instruction | FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `FORCEWAIT` | instruction | AInstruction: WAIT_Instruction | IS_PRINT |  |  |  |
| `FORCE_BEGIN` | instruction | AInstruction: FORCE_BEGIN_Instruction | FLOW_CONTROL |  |  |  |
| `FORCE_QUIT` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) |  |  |  |  |
| `FORCE_QUIT_AND_RESTART` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) |  |  |  |  |
| `FUNC` | instruction | FunctionArgType.SP_CALLFORM (SP_CALL_ArgumentBuilder) | FLOW_CONTROL \| EXTENDED \| PARTIAL \| FORCE_SETARG |  |  |  |
| `GETTIME` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `GOTO` | instruction | AInstruction: GOTO_Instruction | FLOW_CONTROL \| METHOD_SAFE \| FORCE_SETARG |  |  |  |
| `GOTOFORM` | instruction | AInstruction: GOTO_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| FORCE_SETARG |  |  |  |
| `HTML_PRINT` | instruction | AInstruction: HTML_PRINT_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `HTML_PRINT_ISLAND` | instruction | AInstruction: HTML_PRINT_ISLAND_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `HTML_PRINT_ISLAND_CLEAR` | instruction | AInstruction: HTML_PRINT_ISLAND_CLEAR_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `HTML_TAGSPLIT` | instruction | AInstruction: HTML_TAGSPLIT_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `IF` | instruction | AInstruction: IF_Instruction | FLOW_CONTROL \| METHOD_SAFE \| PARTIAL \| FORCE_SETARG | `ENDIF` |  |  |
| `INITRAND` | instruction | AInstruction: INITRAND_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `INPUT` | instruction | AInstruction: INPUT_Instruction | IS_PRINT \| IS_INPUT |  |  |  |
| `INPUTANY` | instruction | AInstruction: INPUTANY_Instruction | EXTENDED |  |  |  |
| `INPUTMOUSEKEY` | instruction | AInstruction: INPUTMOUSEKEY_Instruction | EXTENDED |  |  |  |
| `INPUTS` | instruction | AInstruction: INPUTS_Instruction | IS_PRINT \| IS_INPUT |  |  |  |
| `INVERTBIT` | instruction | AInstruction: SETBIT_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `JUMP` | instruction | AInstruction: CALL_Instruction | FLOW_CONTROL \| FORCE_SETARG |  |  |  |
| `JUMPFORM` | instruction | AInstruction: CALL_Instruction | FLOW_CONTROL \| EXTENDED \| FORCE_SETARG |  |  |  |
| `LOADCHARA` | instruction | AInstruction: LOADCHARA_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `LOADDATA` | instruction | FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder) | FLOW_CONTROL \| EXTENDED |  |  |  |
| `LOADGAME` | instruction | AInstruction: SAVELOADGAME_Instruction | FLOW_CONTROL |  |  |  |
| `LOADGLOBAL` | instruction | AInstruction: LOADGLOBAL_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `LOADVAR` | instruction | AInstruction: LOADVAR_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `LOOP` | instruction | AInstruction: LOOP_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| PARTIAL \| FORCE_SETARG |  | `DO` |  |
| `NEXT` | instruction | AInstruction: REND_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| PARTIAL |  | `FOR` |  |
| `NOSKIP` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | EXTENDED \| METHOD_SAFE \| PARTIAL | `ENDNOSKIP` |  |  |
| `ONEBINPUT` | instruction | AInstruction: ONEBINPUT_Instruction | IS_PRINT \| IS_INPUT |  |  |  |
| `ONEBINPUTS` | instruction | AInstruction: ONEBINPUTS_Instruction | IS_PRINT \| IS_INPUT |  |  |  |
| `ONEINPUT` | instruction | AInstruction: ONEINPUT_Instruction | EXTENDED \| IS_PRINT \| IS_INPUT |  |  |  |
| `ONEINPUTS` | instruction | AInstruction: ONEINPUTS_Instruction | EXTENDED \| IS_PRINT \| IS_INPUT |  |  |  |
| `PICKUPCHARA` | instruction | FunctionArgType.INT_ANY (INT_ANY_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `PLAYBGM` | instruction | AInstruction: PLAYBGM_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `PLAYSOUND` | instruction | AInstruction: PLAYSOUND_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `POWER` | instruction | FunctionArgType.SP_POWER (SP_POWER_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `PRINT` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTBUTTON` | instruction | FunctionArgType.SP_BUTTON (SP_BUTTON_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `PRINTBUTTONC` | instruction | FunctionArgType.SP_BUTTON (SP_BUTTON_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `PRINTBUTTONLC` | instruction | FunctionArgType.SP_BUTTON (SP_BUTTON_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `PRINTC` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTCD` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTCK` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTCPERLINE` | instruction | FunctionArgType.SP_GETINT (SP_GETINT_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `PRINTD` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTDATA` | instruction | AInstruction: PRINT_DATA_Instruction | EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA | `ENDDATA` |  |  |
| `PRINTDATAD` | instruction | AInstruction: PRINT_DATA_Instruction | EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA | `ENDDATA` |  |  |
| `PRINTDATADL` | instruction | AInstruction: PRINT_DATA_Instruction | EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA | `ENDDATA` |  |  |
| `PRINTDATADW` | instruction | AInstruction: PRINT_DATA_Instruction | EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA | `ENDDATA` |  |  |
| `PRINTDATAK` | instruction | AInstruction: PRINT_DATA_Instruction | EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA | `ENDDATA` |  |  |
| `PRINTDATAKL` | instruction | AInstruction: PRINT_DATA_Instruction | EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA | `ENDDATA` |  |  |
| `PRINTDATAKW` | instruction | AInstruction: PRINT_DATA_Instruction | EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA | `ENDDATA` |  |  |
| `PRINTDATAL` | instruction | AInstruction: PRINT_DATA_Instruction | EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA | `ENDDATA` |  |  |
| `PRINTDATAW` | instruction | AInstruction: PRINT_DATA_Instruction | EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA | `ENDDATA` |  |  |
| `PRINTDL` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTDW` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORM` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMC` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMCD` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMCK` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMD` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMDL` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMDW` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMK` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMKL` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMKW` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORML` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMLC` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMLCD` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMLCK` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMN` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMS` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMSD` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMSDL` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMSDW` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMSK` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMSKL` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMSKW` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMSL` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMSN` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMSW` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTFORMW` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTK` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTKL` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTKW` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTL` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTLC` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTLCD` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTLCK` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTN` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTPLAIN` | instruction | FunctionArgType.STR_NULLABLE (STR_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `PRINTPLAINFORM` | instruction | FunctionArgType.FORM_STR_NULLABLE (FORM_STR_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `PRINTS` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSD` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSDL` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSDW` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSINGLE` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSINGLED` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSINGLEFORM` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSINGLEFORMD` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSINGLEFORMK` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSINGLEFORMS` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSINGLEFORMSD` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSINGLEFORMSK` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSINGLEK` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSINGLES` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSINGLESD` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSINGLESK` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSINGLEV` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSINGLEVD` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSINGLEVK` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSK` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSKL` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSKW` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSL` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSN` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTSW` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTV` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTVD` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTVDL` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTVDW` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTVK` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTVKL` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTVKW` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTVL` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTVN` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTVW` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINTW` | instruction | AInstruction: PRINT_Instruction | IS_PRINT |  |  |  |
| `PRINT_ABL` | instruction | FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder) | METHOD_SAFE |  |  |  |
| `PRINT_EXP` | instruction | FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder) | METHOD_SAFE |  |  |  |
| `PRINT_IMG` | instruction | AInstruction: PRINT_IMG_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `PRINT_ITEM` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | METHOD_SAFE |  |  |  |
| `PRINT_MARK` | instruction | FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder) | METHOD_SAFE |  |  |  |
| `PRINT_PALAM` | instruction | FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder) | METHOD_SAFE |  |  |  |
| `PRINT_RECT` | instruction | AInstruction: PRINT_RECT_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `PRINT_SHOPITEM` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | METHOD_SAFE |  |  |  |
| `PRINT_SPACE` | instruction | AInstruction: PRINT_SPACE_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `PRINT_TALENT` | instruction | FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder) | METHOD_SAFE |  |  |  |
| `PUTFORM` | instruction | FunctionArgType.FORM_STR_NULLABLE (FORM_STR_ArgumentBuilder) | METHOD_SAFE |  |  |  |
| `QUIT` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) |  |  |  |  |
| `QUIT_AND_RESTART` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) |  |  |  |  |
| `RANDOMIZE` | instruction | AInstruction: RANDOMIZE_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `REDRAW` | instruction | FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `REF` | instruction | AInstruction: REF_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `REFBYNAME` | instruction | AInstruction: REF_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `REMOVEBGIMAGE` | instruction | AInstruction: REMOVEBGIMAGE_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `REND` | instruction | AInstruction: REND_Instruction | FLOW_CONTROL \| METHOD_SAFE \| PARTIAL |  | `REPEAT` |  |
| `REPEAT` | instruction | AInstruction: REPEAT_Instruction | FLOW_CONTROL \| METHOD_SAFE \| PARTIAL | `REND` |  |  |
| `RESETBGCOLOR` | instruction | AInstruction: RESETBGCOLOR_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `RESETCOLOR` | instruction | AInstruction: RESETCOLOR_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `RESETDATA` | instruction | AInstruction: RESETDATA_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `RESETGLOBAL` | instruction | AInstruction: RESETGLOBAL_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `RESET_STAIN` | instruction | FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `RESTART` | instruction | AInstruction: RESTART_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE |  |  |  |
| `RETURN` | instruction | AInstruction: RETURN_Instruction | FLOW_CONTROL |  |  |  |
| `RETURNF` | instruction | AInstruction: RETURNF_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE |  |  |  |
| `RETURNFORM` | instruction | AInstruction: RETURNFORM_Instruction | FLOW_CONTROL \| EXTENDED |  |  |  |
| `REUSELASTLINE` | instruction | AInstruction: REUSELASTLINE_Instruction | EXTENDED \| METHOD_SAFE \| IS_PRINT |  |  |  |
| `SAVECHARA` | instruction | AInstruction: SAVECHARA_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `SAVEDATA` | instruction | FunctionArgType.SP_SAVEDATA (SP_SAVEDATA_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `SAVEGAME` | instruction | AInstruction: SAVELOADGAME_Instruction | FLOW_CONTROL |  |  |  |
| `SAVEGLOBAL` | instruction | AInstruction: SAVEGLOBAL_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `SAVENOS` | instruction | FunctionArgType.SP_GETINT (SP_GETINT_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `SAVEVAR` | instruction | AInstruction: SAVEVAR_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `SELECTCASE` | instruction | AInstruction: SELECTCASE_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| PARTIAL \| FORCE_SETARG | `ENDSELECT` |  |  |
| `SETBGCOLOR` | instruction | FunctionArgType.SP_COLOR (SP_COLOR_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `SETBGCOLORBYNAME` | instruction | FunctionArgType.STR (STR_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `SETBGIMAGE` | instruction | AInstruction: SETBGIMAGE_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `SETBGMVOLUME` | instruction | AInstruction: SETBGMVOLUME_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `SETBIT` | instruction | AInstruction: SETBIT_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `SETCOLOR` | instruction | FunctionArgType.SP_COLOR (SP_COLOR_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `SETCOLORBYNAME` | instruction | FunctionArgType.STR (STR_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `SETFONT` | instruction | FunctionArgType.STR_EXPRESSION_NULLABLE (STR_EXPRESSION_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `SETSOUNDVOLUME` | instruction | AInstruction: SETSOUNDVOLUME_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `SIF` | instruction | AInstruction: SIF_Instruction | FLOW_CONTROL \| METHOD_SAFE \| PARTIAL \| FORCE_SETARG |  |  |  |
| `SKIPDISP` | instruction | FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `SKIPLOG` | instruction | FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `SORTCHARA` | instruction | AInstruction: SORTCHARA_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `SPLIT` | instruction | FunctionArgType.SP_SPLIT (SP_SPLIT_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `STOPBGM` | instruction | AInstruction: STOPBGM_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `STOPCALLTRAIN` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | FLOW_CONTROL \| EXTENDED |  |  |  |
| `STOPSOUND` | instruction | AInstruction: STOPSOUND_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `STRDATA` | instruction | FunctionArgType.VAR_STR (VAR_STR_ArgumentBuilder) | EXTENDED \| METHOD_SAFE \| PARTIAL | `ENDDATA` |  |  |
| `STRLEN` | instruction | AInstruction: STRLEN_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `STRLENFORM` | instruction | AInstruction: STRLEN_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `STRLENFORMU` | instruction | AInstruction: STRLEN_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `STRLENU` | instruction | AInstruction: STRLEN_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `SWAP` | instruction | FunctionArgType.SP_SWAPVAR (SP_SWAPVAR_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `SWAPCHARA` | instruction | AInstruction: SWAPCHARA_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `THROW` | instruction | FunctionArgType.FORM_STR_NULLABLE (FORM_STR_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `TIMES` | instruction | AInstruction: TIMES_Instruction | METHOD_SAFE |  |  |  |
| `TINPUT` | instruction | AInstruction: TINPUT_Instruction | EXTENDED \| IS_PRINT \| IS_INPUT |  |  |  |
| `TINPUTS` | instruction | AInstruction: TINPUTS_Instruction | EXTENDED \| IS_PRINT \| IS_INPUT |  |  |  |
| `TONEINPUT` | instruction | AInstruction: TINPUT_Instruction | EXTENDED \| IS_PRINT \| IS_INPUT |  |  |  |
| `TONEINPUTS` | instruction | AInstruction: TINPUTS_Instruction | EXTENDED \| IS_PRINT \| IS_INPUT |  |  |  |
| `TOOLTIP_CUSTOM` | instruction | AInstruction: TOOLTIP_CUSTOM_Instruction | EXTENDED |  |  |  |
| `TOOLTIP_FORMAT` | instruction | AInstruction: TOOLTIP_FORMAT_Instruction | EXTENDED |  |  |  |
| `TOOLTIP_IMG` | instruction | AInstruction: TOOLTIP_IMG_Instruction | EXTENDED |  |  |  |
| `TOOLTIP_SETCOLOR` | instruction | AInstruction: TOOLTIP_SETCOLOR_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `TOOLTIP_SETDELAY` | instruction | AInstruction: TOOLTIP_SETDELAY_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `TOOLTIP_SETDURATION` | instruction | AInstruction: TOOLTIP_SETDURATION_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `TOOLTIP_SETFONT` | instruction | AInstruction: TOOLTIP_SETFONT_Instruction | EXTENDED |  |  |  |
| `TOOLTIP_SETFONTSIZE` | instruction | AInstruction: TOOLTIP_SETFONTSIZE_Instruction | EXTENDED |  |  |  |
| `TRYCALL` | instruction | AInstruction: CALL_Instruction | FLOW_CONTROL \| EXTENDED \| FORCE_SETARG |  |  |  |
| `TRYCALLF` | instruction | AInstruction: TRYCALLF_Instruction | EXTENDED \| METHOD_SAFE \| FORCE_SETARG |  |  |  |
| `TRYCALLFORM` | instruction | AInstruction: CALL_Instruction | FLOW_CONTROL \| EXTENDED \| FORCE_SETARG |  |  |  |
| `TRYCALLFORMF` | instruction | AInstruction: TRYCALLF_Instruction | EXTENDED \| METHOD_SAFE \| FORCE_SETARG |  |  |  |
| `TRYCALLLIST` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | FLOW_CONTROL \| EXTENDED \| PARTIAL \| IS_TRY | `ENDFUNC` |  |  |
| `TRYCCALL` | instruction | AInstruction: CALL_Instruction | FLOW_CONTROL \| EXTENDED \| FORCE_SETARG | `CATCH` |  |  |
| `TRYCCALLFORM` | instruction | AInstruction: CALL_Instruction | FLOW_CONTROL \| EXTENDED \| FORCE_SETARG | `CATCH` |  |  |
| `TRYCGOTO` | instruction | AInstruction: GOTO_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| FORCE_SETARG | `CATCH` |  |  |
| `TRYCGOTOFORM` | instruction | AInstruction: GOTO_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| FORCE_SETARG | `CATCH` |  |  |
| `TRYCJUMP` | instruction | AInstruction: CALL_Instruction | FLOW_CONTROL \| EXTENDED \| FORCE_SETARG | `CATCH` |  |  |
| `TRYCJUMPFORM` | instruction | AInstruction: CALL_Instruction | FLOW_CONTROL \| EXTENDED \| FORCE_SETARG | `CATCH` |  |  |
| `TRYGOTO` | instruction | AInstruction: GOTO_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| FORCE_SETARG |  |  |  |
| `TRYGOTOFORM` | instruction | AInstruction: GOTO_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| FORCE_SETARG |  |  |  |
| `TRYGOTOLIST` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | FLOW_CONTROL \| EXTENDED \| PARTIAL \| IS_TRY | `ENDFUNC` |  |  |
| `TRYJUMP` | instruction | AInstruction: CALL_Instruction | FLOW_CONTROL \| EXTENDED \| FORCE_SETARG |  |  |  |
| `TRYJUMPFORM` | instruction | AInstruction: CALL_Instruction | FLOW_CONTROL \| EXTENDED \| FORCE_SETARG |  |  |  |
| `TRYJUMPLIST` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | FLOW_CONTROL \| EXTENDED \| PARTIAL \| IS_JUMP \| IS_TRY | `ENDFUNC` |  |  |
| `TWAIT` | instruction | AInstruction: TWAIT_Instruction | EXTENDED \| IS_PRINT |  |  |  |
| `UPCHECK` | instruction | FunctionArgType.VOID (VOID_ArgumentBuilder) | METHOD_SAFE |  |  |  |
| `UPDATECHECK` | instruction | AInstruction: UPDATECHECK_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `VARI` | instruction | AInstruction: VARI_Instruction |  |  |  | Only registered when JSONConfig.Data.UseScopedVariableInstruction is true. |
| `VARS` | instruction | AInstruction: VARS_Instruction |  |  |  | Only registered when JSONConfig.Data.UseScopedVariableInstruction is true. |
| `VARSET` | instruction | AInstruction: VARSET_Instruction | EXTENDED \| METHOD_SAFE |  |  |  |
| `VARSIZE` | instruction | FunctionArgType.SP_VAR (SP_VAR_ArgumentBuilder) | EXTENDED \| METHOD_SAFE |  |  |  |
| `WAIT` | instruction | AInstruction: WAIT_Instruction | IS_PRINT |  |  |  |
| `WAITANYKEY` | instruction | AInstruction: WAITANYKEY_Instruction | IS_PRINT |  |  |  |
| `WEND` | instruction | AInstruction: WEND_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| PARTIAL |  | `WHILE` |  |
| `WHILE` | instruction | AInstruction: WHILE_Instruction | FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| PARTIAL | `WEND` |  |  |
| `SET` | pseudo-instruction | AInstruction: SET_Instruction | METHOD_SAFE |  |  | Internal pseudo instruction used for assignment statements; not a normal statement keyword. |
<!-- ROWS END -->

## Engine sources (fact-check)

- Instruction registration + flags + block pairing tables: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- ArgumentBuilder mapping for `FunctionArgType`: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs`
- Many instruction-class internal flags: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`
