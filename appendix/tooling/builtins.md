# Built-in Commands and Functions (Index)

This appendix is self-contained: it lists built-in instruction/function names and their API signatures as used by the engine documentation in this workspace.

Notes:
- The index does **not** try to fully explain the behavior of every built-in; it is meant as a searchable catalog.
- Fact-check sources (optional) point into `emuera.em.doc/docs/Reference/`.

Entries: 278 (preferred language order: `.en.md` → `.md` → `.zh.md`).

## Quick Index

| Name | API (first line) | Source (fact-check) |
|---|---|---|
| `ABS` | `int ABS int` | `emuera.em.doc/docs/Reference/ABS.en.md` |
| `ADDCHARA` | `ADDCHARA charaNo(, charaNo,...)` | `emuera.em.doc/docs/Reference/ADDCHARA.en.md` |
| `ADDCOPYCHARA` | `ADDCOPYCHARA charaID` | `emuera.em.doc/docs/Reference/ADDCOPYCHARA.en.md` |
| `ADDDEFCHARA` | `ADDDEFCHARA` | `emuera.em.doc/docs/Reference/ADDDEFCHARA.en.md` |
| `ADDVOIDCHARA` | `ADDVOIDCHARA` | `emuera.em.doc/docs/Reference/ADDVOIDCHARA.en.md` |
| `ALIGNMENT` | `ALIGNMENT keyword` | `emuera.em.doc/docs/Reference/ALIGNMENT.en.md` |
| `ARRAYCOPY` | `ARRAYCOPY variableName, variableName` | `emuera.em.doc/docs/Reference/ARRAYCOPY.en.md` |
| `ARRAYMSORT` | `ARRAYMSORT variableName1(, variableName2,...)` | `emuera.em.doc/docs/Reference/ARRAYMSORT.en.md` |
| `ARRAYMSORTEX` | `1. 1 ARRAYMSORTEX indexName, arrayNameList(, sortAscending, size)` | `emuera.em.doc/docs/Reference/ARRAYMSORTEX.en.md` |
| `ARRAYREMOVE` | `ARRAYREMOVE variableName, startIndex, clearCount` | `emuera.em.doc/docs/Reference/ARRAYREMOVE.en.md` |
| `ARRAYSHIFT` | `ARRAYSHIFT variable, shiftCount, value(, startIndex, targetCount)` | `emuera.em.doc/docs/Reference/ARRAYSHIFT.en.md` |
| `ARRAYSORT` | `ARRAYSORT variableName(, FORWARD or BACK, startIndex, targetCount)` | `emuera.em.doc/docs/Reference/ARRAYSORT.en.md` |
| `ASSERT` | `ASSERT bool` | `emuera.em.doc/docs/Reference/ASSERT.en.md` |
| `AWAIT` | `AWAIT milliSecond` | `emuera.em.doc/docs/Reference/AWAIT.en.md` |
| `BACKGROUND` | `SETBGIMAGE resourceName(, depth, opacity)` | `emuera.em.doc/docs/Reference/BACKGROUND.en.md` |
| `BAR` | `BAR value, maxValue, length` | `emuera.em.doc/docs/Reference/BAR.en.md` |
| `BARSTR` | `string BARSTR value, maxValue, length` | `emuera.em.doc/docs/Reference/BARSTR.en.md` |
| `BEGIN` | `BEGIN identifier` | `emuera.em.doc/docs/Reference/BEGIN.en.md` |
| `BINPUT` | `BINPUT (defaultValue, AllowClick, CanSkip)` | `emuera.em.doc/docs/Reference/BINPUT.en.md` |
| `BITMAP_CACHE_ENABLE` | `BITMAP_CACHE_ENABLE bool` | `emuera.em.doc/docs/Reference/BITMAP_CACHE_ENABLE.en.md` |
| `BIT_OPERATION` | `int GETBIT targetInt, bit` | `emuera.em.doc/docs/Reference/BIT_OPERATION.en.md` |
| `CALL` | `CALL funcName` | `emuera.em.doc/docs/Reference/CALL.en.md` |
| `CALLEVENT` | `CALLEVENT eventFunction` | `emuera.em.doc/docs/Reference/CALLEVENT.en.md` |
| `CALLF` | `CALLF functionName` | `emuera.em.doc/docs/Reference/CALLF.en.md` |
| `CALLSHARP` | `CALLSHARP funcName` | `emuera.em.doc/docs/Reference/CALLSHARP.en.md` |
| `CALLTRAIN` | `CALLTRAIN comCount` | `emuera.em.doc/docs/Reference/CALLTRAIN.en.md` |
| `CARRAY` | `int SUMCARRAY charaArray(, start, end)` | `emuera.em.doc/docs/Reference/CARRAY.en.md` |
| `CBGCLEAR` | `int CBGCLEAR` | `emuera.em.doc/docs/Reference/CBGCLEAR.en.md` |
| `CBGCLEARBUTTON` | `int CBGCLEARBUTTON` | `emuera.em.doc/docs/Reference/CBGCLEARBUTTON.en.md` |
| `CBGREMOVEMAPB` | `int CBGREMOVEMAPB` | `emuera.em.doc/docs/Reference/CBGREMOVEMAPB.en.md` |
| `CBGREMOVERANGE` | `int CBGREMOVERANGE zMin, zMax` | `emuera.em.doc/docs/Reference/CBGREMOVERANGE.en.md` |
| `CBGSETBMAPG` | `int CBGSETBMAPG gID` | `emuera.em.doc/docs/Reference/CBGSETBMAPG.en.md` |
| `CBGSETBUTTONSPRITE` | `int CBGSETBUTTONSPRITE button, spriteName, spriteNameB, x, y, zDepth` | `emuera.em.doc/docs/Reference/CBGSETBUTTONSPRITE.en.md` |
| `CBGSETG` | `int CBGSETG gID, x, y, zDepth` | `emuera.em.doc/docs/Reference/CBGSETG.en.md` |
| `CBGSETSPRITE` | `int CBGSETSPRITE, spriteName, x, y, zDepth` | `emuera.em.doc/docs/Reference/CBGSETSPRITE.en.md` |
| `CHARATU` | `string CHARATU string, position` | `emuera.em.doc/docs/Reference/CHARATU.en.md` |
| `CHKCHARADATA` | `int CHKCHARADATA filename` | `emuera.em.doc/docs/Reference/CHKCHARADATA.en.md` |
| `CHKDATA` | `int CHKDATA saveID` | `emuera.em.doc/docs/Reference/CHKDATA.en.md` |
| `CLEARLINE` | `CLEARLINE line` | `emuera.em.doc/docs/Reference/CLEARLINE.en.md` |
| `CLEARMEMORY` | `int CLEARMEMORY` | `emuera.em.doc/docs/Reference/CLEARMEMORY.en.md` |
| `CLEARTEXTBOX` | `CLEARTEXTBOX` | `emuera.em.doc/docs/Reference/CLEARTEXTBOX.en.md` |
| `CLIENTFIELD` | `int CLIENTWIDTH` | `emuera.em.doc/docs/Reference/CLIENTFIELD.en.md` |
| `COLOR_FROM` | `int COLOR_FROMNAME colorName` | `emuera.em.doc/docs/Reference/COLOR_FROM.en.md` |
| `CONTINUE` | `loopInstruction` | `emuera.em.doc/docs/Reference/CONTINUE.en.md` |
| `CONVERT` | `` | `emuera.em.doc/docs/Reference/CONVERT.en.md` |
| `COPYCHARA` | `COPYCHARA charaID, charaID` | `emuera.em.doc/docs/Reference/COPYCHARA.en.md` |
| `CSVNAME` | `CSVNAME charaNo` | `emuera.em.doc/docs/Reference/CSVNAME.en.md` |
| `CSV_STATUS` | `CSVBASE charaNo, index` | `emuera.em.doc/docs/Reference/CSV_STATUS.en.md` |
| `CUPCHECK` | `CUPCHECK charaID` | `emuera.em.doc/docs/Reference/CUPCHECK.en.md` |
| `CUSTOMDRAWLINE` | `CUSTOMDRAWLINE string` | `emuera.em.doc/docs/Reference/CUSTOMDRAWLINE.en.md` |
| `CVARSET` | `CVARSET characterVariable, index, value, startID, endID` | `emuera.em.doc/docs/Reference/CVARSET.en.md` |
| `DEBUGPRINT` | `DEBUGPRINT string` | `emuera.em.doc/docs/Reference/DEBUGPRINT.en.md` |
| `DELALLCHARA` | `DELALLCHARA` | `emuera.em.doc/docs/Reference/DELALLCHARA.en.md` |
| `DELCHARA` | `DELCHARA charaID(, charaID,...)` | `emuera.em.doc/docs/Reference/DELCHARA.en.md` |
| `DELDATA` | `DELDATA saveID` | `emuera.em.doc/docs/Reference/DELDATA.en.md` |
| `DO` | `DO` | `emuera.em.doc/docs/Reference/DO.en.md` |
| `DOTRAIN` | `DOTRAIN trainNo` | `emuera.em.doc/docs/Reference/DOTRAIN.en.md` |
| `DRAWLINE` | `DRAWLINE` | `emuera.em.doc/docs/Reference/DRAWLINE.en.md` |
| `DT_CELL` | `int DT_CELL_GET dataTableName, row, columnName(, asId)` | `emuera.em.doc/docs/Reference/DT_CELL.en.md` |
| `DT_COLUMN` | `int DT_COLUMN_ADD dataTableName, columnName(, type, nullable)` | `emuera.em.doc/docs/Reference/DT_COLUMN.en.md` |
| `DT_MANAGE` | `int DT_CREATE dataTableName` | `emuera.em.doc/docs/Reference/DT_MANAGE.en.md` |
| `DT_ROW` | `a. int DT_ROW_ADD dataTableName(, columnName, columnValue) ...` | `emuera.em.doc/docs/Reference/DT_ROW.en.md` |
| `DT_SELECT` | `int DT_SELECT dataTableName(, filterExpression, sortRule, output)` | `emuera.em.doc/docs/Reference/DT_SELECT.en.md` |
| `DT_SERIALIZATION` | `1. string DT_TOXML dataTableName(, schemaOutput)` | `emuera.em.doc/docs/Reference/DT_SERIALIZATION.en.md` |
| `ENUMFILES` | `int ENUMFILES dir, pattern, option` | `emuera.em.doc/docs/Reference/ENUMFILES.en.md` |
| `ENUMFUNC` | `int ENUMFUNCBEGINSWITH keyword` | `emuera.em.doc/docs/Reference/ENUMFUNC.en.md` |
| `ENUMMACRO` | `int ENUMMACROBEGINSWITH keyword` | `emuera.em.doc/docs/Reference/ENUMMACRO.en.md` |
| `ENUMVAR` | `int ENUMVARBEGINSWITH keyword` | `emuera.em.doc/docs/Reference/ENUMVAR.en.md` |
| `ERDNAME` | `string ERDNAME variableName, index(, dimension)` | `emuera.em.doc/docs/Reference/ERDNAME.en.md` |
| `ESCAPE` | `string ESCAPE string` | `emuera.em.doc/docs/Reference/ESCAPE.en.md` |
| `EXISTCSV` | `int EXISTCSV charaNO` | `emuera.em.doc/docs/Reference/EXISTCSV.en.md` |
| `EXISTFILE` | `int EXISTFILE relativePath` | `emuera.em.doc/docs/Reference/EXISTFILE.en.md` |
| `EXISTFUNCTION` | `int EXISTFUNCTION funcName` | `emuera.em.doc/docs/Reference/EXISTFUNCTION.en.md` |
| `EXISTMETH` | `int EXISTMETH functionName` | `emuera.em.doc/docs/Reference/EXISTMETH.en.md` |
| `EXISTSOUND` | `EXISTSOUND MediaFile` | `emuera.em.doc/docs/Reference/EXISTSOUND.en.md` |
| `EXISTVAR` | `int EXISTVAR varName` | `emuera.em.doc/docs/Reference/EXISTVAR.en.md` |
| `FINDCHARA` | `int FINDCHARA charaVariable, value(, startID, endID)` | `emuera.em.doc/docs/Reference/FINDCHARA.en.md` |
| `FINDELEMENT` | `FINDELEMENT variableName, value(, startIndex, endIndex, completeMatch)` | `emuera.em.doc/docs/Reference/FINDELEMENT.en.md` |
| `FIND_CHARADATA` | `int FIND_CHARADATA filename` | `emuera.em.doc/docs/Reference/FIND_CHARADATA.en.md` |
| `FLOWINPUT` | `FLOWINPUT default(, AllowLeftClick, AllowSkip, ForceSkip)` | `emuera.em.doc/docs/Reference/FLOWINPUT.en.md` |
| `FONT_OPERATION` | `FONTBOLD` | `emuera.em.doc/docs/Reference/FONT_OPERATION.en.md` |
| `FOR` | `FOR integerVariable, startNum, endNum(, value)` | `emuera.em.doc/docs/Reference/FOR.en.md` |
| `FORCEKANA` | `FORCEKANA int` | `emuera.em.doc/docs/Reference/FORCEKANA.en.md` |
| `FORCEWAIT` | `FORCEWAIT` | `emuera.em.doc/docs/Reference/FORCEWAIT.en.md` |
| `FORCE_BEGIN` | `FORCE_BEGIN SystemFuncName` | `emuera.em.doc/docs/Reference/FORCE_BEGIN.en.md` |
| `FORCE_QUIT` | `FORCE_QUIT` | `emuera.em.doc/docs/Reference/FORCE_QUIT.en.md` |
| `FORCE_QUIT_AND_RESTART` | `FORCE_QUIT_AND_RESTART` | `emuera.em.doc/docs/Reference/FORCE_QUIT_AND_RESTART.en.md` |
| `FORM` | `CALLFORM functionName(, argument...)` | `emuera.em.doc/docs/Reference/FORM.en.md` |
| `GCLEAR` | `int GCLEAR gID, cARGB` | `emuera.em.doc/docs/Reference/GCLEAR.en.md` |
| `GCREATE` | `int GCREATE gID, width, height` | `emuera.em.doc/docs/Reference/GCREATE.en.md` |
| `GCREATED` | `int GCREATED gID` | `emuera.em.doc/docs/Reference/GCREATED.en.md` |
| `GCREATEFROMFILE` | `int GCREATEFROMFILE gID, filePath` | `emuera.em.doc/docs/Reference/GCREATEFROMFILE.en.md` |
| `GDASHSTYLE` | `int GDASHSTYLE gID, DashStyle, DashCap` | `emuera.em.doc/docs/Reference/GDASHSTYLE.en.md` |
| `GDISPOSE` | `int GDISPOSE gID` | `emuera.em.doc/docs/Reference/GDISPOSE.en.md` |
| `GDRAWG` | `int GDRAWG destID, srcID, destX, destY, destWidth, destHeight, srcX, srcY, srcWidth, srcHeight` | `emuera.em.doc/docs/Reference/GDRAWG.en.md` |
| `GDRAWGWITHMASK` | `GDRAWGWITHMASK destID, srcID, maskID, destX, destY` | `emuera.em.doc/docs/Reference/GDRAWGWITHMASK.en.md` |
| `GDRAWGWITHROTATE` | `int GDRAWGWITHROTATE gID, destID, Angle(, x, y)` | `emuera.em.doc/docs/Reference/GDRAWGWITHROTATE.en.md` |
| `GDRAWLINE` | `int GDRAWLINE gID, fromX, fromY, forX, forY` | `emuera.em.doc/docs/Reference/GDRAWLINE.en.md` |
| `GDRAWSPRITE` | `int GDRAWSPRITE gID, spriteName` | `emuera.em.doc/docs/Reference/GDRAWSPRITE.en.md` |
| `GDRAWTEXT` | `int GDRAWTEXT gID, text(, x, y)` | `emuera.em.doc/docs/Reference/GDRAWTEXT.en.md` |
| `GETCHARA` | `int GETCHARA charaNO` | `emuera.em.doc/docs/Reference/GETCHARA.en.md` |
| `GETCOLOR` | `int GETCOLOR` | `emuera.em.doc/docs/Reference/GETCOLOR.en.md` |
| `GETCONFIG` | `int GETCONFIG configWord` | `emuera.em.doc/docs/Reference/GETCONFIG.en.md` |
| `GETDISPLAYLINE` | `string GETDISPLAYLINE lineNumber` | `emuera.em.doc/docs/Reference/GETDISPLAYLINE.en.md` |
| `GETKEY` | `GETKEY keyCode` | `emuera.em.doc/docs/Reference/GETKEY.en.md` |
| `GETLINESTR` | `string GETLINESTR pattern` | `emuera.em.doc/docs/Reference/GETLINESTR.en.md` |
| `GETMEMORYUSAGE` | `int GETMEMORYUSAGE` | `emuera.em.doc/docs/Reference/GETMEMORYUSAGE.en.md` |
| `GETMETH` | `int GETMETH functionName(, defaultValue, argument...)` | `emuera.em.doc/docs/Reference/GETMETH.en.md` |
| `GETMILLISECOND` | `int GETMILLISECOND` | `emuera.em.doc/docs/Reference/GETMILLISECOND.en.md` |
| `GETNUM` | `GETNUM variableName, indexName` | `emuera.em.doc/docs/Reference/GETNUM.en.md` |
| `GETPALAMLV` | `GETPALAMLV int, maxLV` | `emuera.em.doc/docs/Reference/GETPALAMLV.en.md` |
| `GETSECOND` | `int GETTIME` | `emuera.em.doc/docs/Reference/GETSECOND.en.md` |
| `GETSETVAR` | `int GETVAR varName` | `emuera.em.doc/docs/Reference/GETSETVAR.en.md` |
| `GETTIME` | `GETTIME` | `emuera.em.doc/docs/Reference/GETTIME.en.md` |
| `GFILLRECTANGLE` | `int GFILLRECTANGLE gID, x, y, width, height` | `emuera.em.doc/docs/Reference/GFILLRECTANGLE.en.md` |
| `GGETBRUSH` | `int GGETBRUSH gID` | `emuera.em.doc/docs/Reference/GGETBRUSH.en.md` |
| `GGETCOLOR` | `int GGETCOLOR gID, x, y` | `emuera.em.doc/docs/Reference/GGETCOLOR.en.md` |
| `GGETFONT` | `string GGETFONT gID` | `emuera.em.doc/docs/Reference/GGETFONT.en.md` |
| `GGETFONTSIZE` | `int GGETFONTSIZE gID` | `emuera.em.doc/docs/Reference/GGETFONTSIZE.en.md` |
| `GGETFONTSTYLE` | `int GGETFONTSTYLE gID` | `emuera.em.doc/docs/Reference/GGETFONTSTYLE.en.md` |
| `GGETPEN` | `int GGETPEN gID` | `emuera.em.doc/docs/Reference/GGETPEN.en.md` |
| `GGETPENWIDTH` | `int GGETPENWIDTH gID` | `emuera.em.doc/docs/Reference/GGETPENWIDTH.en.md` |
| `GGETTEXTSIZE` | `int GGETTEXTSIZE text, fontName, fontSize(, fontStyle)` | `emuera.em.doc/docs/Reference/GGETTEXTSIZE.en.md` |
| `GOTO` | `GOTO labelName` | `emuera.em.doc/docs/Reference/GOTO.en.md` |
| `GROUPCHECK` | `int GROUPMATCH key, value...` | `emuera.em.doc/docs/Reference/GROUPCHECK.en.md` |
| `GSAVELOAD` | `int GSAVE gID, fileNo` | `emuera.em.doc/docs/Reference/GSAVELOAD.en.md` |
| `GSETBRUSH` | `int GSETBRUSH gID, cARGB` | `emuera.em.doc/docs/Reference/GSETBRUSH.en.md` |
| `GSETCOLOR` | `int GSETCOLOR gID, cARGB, x, y` | `emuera.em.doc/docs/Reference/GSETCOLOR.en.md` |
| `GSETFONT` | `int GSETFONT gID, fontName, fontSize(, fontStyle)` | `emuera.em.doc/docs/Reference/GSETFONT.en.md` |
| `GSETPEN` | `int GSETPEN gID, cARGB, penWidth` | `emuera.em.doc/docs/Reference/GSETPEN.en.md` |
| `GWIDTHHEIGHT` | `int GWIDTH gID` | `emuera.em.doc/docs/Reference/GWIDTHHEIGHT.en.md` |
| `HTML_ESCAPE` | `str HTML_ESCAPE, htmlString` | `emuera.em.doc/docs/Reference/HTML_ESCAPE.en.md` |
| `HTML_GETPRINTEDSTR` | `str HTML_GETPRINTEDSTR, lineNo` | `emuera.em.doc/docs/Reference/HTML_GETPRINTEDSTR.en.md` |
| `HTML_POPPRINTINGSTR` | `string HTML_POPPRINTINGSTR` | `emuera.em.doc/docs/Reference/HTML_POPPRINTINGSTR.en.md` |
| `HTML_PRINT` | `HTML_PRINT htmlStyleString` | `emuera.em.doc/docs/Reference/HTML_PRINT.en.md` |
| `HTML_PRINT_ISLAND` | `HTML_PRINT_ISLAND htmlStyleString` | `emuera.em.doc/docs/Reference/HTML_PRINT_ISLAND.en.md` |
| `HTML_STRINGLEN` | `int HTML_STRINGLEN html(, returnPixel)` | `emuera.em.doc/docs/Reference/HTML_STRINGLEN.en.md` |
| `HTML_STRINGLINES` | `int HTML_STRINGLINES html, width` | `emuera.em.doc/docs/Reference/HTML_STRINGLINES.en.md` |
| `HTML_SUBSTRING` | `int HTML_SUBSTRING html, width` | `emuera.em.doc/docs/Reference/HTML_SUBSTRING.en.md` |
| `HTML_TAGSPLIT` | `HTML_TAGSPLIT string(, integerVariable, stringVariable)` | `emuera.em.doc/docs/Reference/HTML_TAGSPLIT.en.md` |
| `HTML_TOPLAINTEXT` | `str HTML_TOPLAINTEXT, string` | `emuera.em.doc/docs/Reference/HTML_TOPLAINTEXT.en.md` |
| `IF` | `IF operand(int)` | `emuera.em.doc/docs/Reference/IF.en.md` |
| `INPUT` | `INPUT (defaultValue, canClick, allowSkip)` | `emuera.em.doc/docs/Reference/INPUT.en.md` |
| `INPUTANY` | `INPUTANY` | `emuera.em.doc/docs/Reference/INPUTANY.en.md` |
| `INPUTMOUSEKEY` | `INPUTMOUSEKEY timeLimit` | `emuera.em.doc/docs/Reference/INPUTMOUSEKEY.en.md` |
| `INRANGEARRAY` | `int INRANGEARRAY integerArray, minValue, maxValue(, start, end)` | `emuera.em.doc/docs/Reference/INRANGEARRAY.en.md` |
| `ISACTIVE` | `ISACTIVE` | `emuera.em.doc/docs/Reference/ISACTIVE.en.md` |
| `ISDEFINED` | `int ISDEFINED macroName` | `emuera.em.doc/docs/Reference/ISDEFINED.en.md` |
| `JUMP` | `JUMP functionName` | `emuera.em.doc/docs/Reference/JUMP.en.md` |
| `LINEISEMPTY` | `int LINEISEMPTY` | `emuera.em.doc/docs/Reference/LINEISEMPTY.en.md` |
| `LOADCHARA` | `LOADCHARA filename` | `emuera.em.doc/docs/Reference/LOADCHARA.en.md` |
| `LOADDATA` | `LOADDATA saveID` | `emuera.em.doc/docs/Reference/LOADDATA.en.md` |
| `LOADGLOBAL` | `LOADGLOBAL` | `emuera.em.doc/docs/Reference/LOADGLOBAL.en.md` |
| `LOADTEXT` | `LOADTEXT fileNo{, force_savdir, int force_UTF8}` | `emuera.em.doc/docs/Reference/LOADTEXT.en.md` |
| `MAP_GETKEYS` | `1. string MAP_GETKEYS mapName` | `emuera.em.doc/docs/Reference/MAP_GETKEYS.en.md` |
| `MAP_MANAGE` | `int MAP_CREATE mapName` | `emuera.em.doc/docs/Reference/MAP_MANAGE.en.md` |
| `MAP_OPERATION` | `string MAP_GET mapName, key` | `emuera.em.doc/docs/Reference/MAP_OPERATION.en.md` |
| `MAP_SERIALIZATION` | `1. string MAP_TOXML mapName` | `emuera.em.doc/docs/Reference/MAP_SERIALIZATION.en.md` |
| `MATCH` | `int MATCH array, value(, start, end)` | `emuera.em.doc/docs/Reference/MATCH.en.md` |
| `MATH_EXTENSION` | `int CBRT value` | `emuera.em.doc/docs/Reference/MATH_EXTENSION.en.md` |
| `MAX` | `int MAX int(, int...)` | `emuera.em.doc/docs/Reference/MAX.en.md` |
| `MAXMINARRAY` | `int MAXARRAY integerArray(, start, end)` | `emuera.em.doc/docs/Reference/MAXMINARRAY.en.md` |
| `MONEYSTR` | `string MONEYSTR` | `emuera.em.doc/docs/Reference/MONEYSTR.en.md` |
| `MOUSEB` | `string MOUSEB` | `emuera.em.doc/docs/Reference/MOUSEB.en.md` |
| `MOUSEXY` | `MOUSEX` | `emuera.em.doc/docs/Reference/MOUSEXY.en.md` |
| `ONEINPUT` | `ONEINPUT defaultValue` | `emuera.em.doc/docs/Reference/ONEINPUT.en.md` |
| `OUTPUTLOG` | `OUTPUTLOG (filePath)` | `emuera.em.doc/docs/Reference/OUTPUTLOG.en.md` |
| `PICKUPCHARA` | `PICKUPCHARA charaID(, charaID...)` | `emuera.em.doc/docs/Reference/PICKUPCHARA.en.md` |
| `PLAYBGM` | `PLAYBGM MediaFile` | `emuera.em.doc/docs/Reference/PLAYBGM.en.md` |
| `PLAYSOUND` | `PLAYSOUND MediaFile` | `emuera.em.doc/docs/Reference/PLAYSOUND.en.md` |
| `POWER` | `POWER integerVariable, int, int` | `emuera.em.doc/docs/Reference/POWER.en.md` |
| `PRINT` | `PRINTV(\|K\|D)(\|L\|W\|N) integerVariable` | `emuera.em.doc/docs/Reference/PRINT.en.md` |
| `PRINTBUTTON` | `PRINTBUTTON(\|C\|LC) string, buttonValue` | `emuera.em.doc/docs/Reference/PRINTBUTTON.en.md` |
| `PRINTC` | `PRINT(C\|L)(\|K\|D) string` | `emuera.em.doc/docs/Reference/PRINTC.en.md` |
| `PRINTCLENGTH` | `int PRINTCLENGTH` | `emuera.em.doc/docs/Reference/PRINTCLENGTH.en.md` |
| `PRINTCPERLINE` | `int PRINTCPERLINE` | `emuera.em.doc/docs/Reference/PRINTCPERLINE.en.md` |
| `PRINTDATA` | `PRINTDATA(\|K\|D)(\|L\|W)` | `emuera.em.doc/docs/Reference/PRINTDATA.en.md` |
| `PRINTN` | `PRINTN string` | `emuera.em.doc/docs/Reference/PRINTN.en.md` |
| `PRINTPLAIN` | `PRINTPLAIN(\|FORM) string` | `emuera.em.doc/docs/Reference/PRINTPLAIN.en.md` |
| `PRINTSINGLE` | `PRINTSINGLEV(\|K\|D) integerVariable` | `emuera.em.doc/docs/Reference/PRINTSINGLE.en.md` |
| `PRINT_IMG` | `PRINT_IMG spriteName` | `emuera.em.doc/docs/Reference/PRINT_IMG.en.md` |
| `PRINT_RECT` | `PRINT_RECT width` | `emuera.em.doc/docs/Reference/PRINT_RECT.en.md` |
| `PRINT_SPACE` | `PRINT_SPACE width` | `emuera.em.doc/docs/Reference/PRINT_SPACE.en.md` |
| `PRINT_STATUS` | `PRINT_ABL charaID` | `emuera.em.doc/docs/Reference/PRINT_STATUS.en.md` |
| `PUTFORM` | `PUTFORM saveInfo` | `emuera.em.doc/docs/Reference/PUTFORM.en.md` |
| `QUIT` | `QUIT` | `emuera.em.doc/docs/Reference/QUIT.en.md` |
| `QUIT_AND_RESTART` | `QUIT_AND_RESTART` | `emuera.em.doc/docs/Reference/QUIT_AND_RESTART.en.md` |
| `RAND` | `int RAND min(, max)` | `emuera.em.doc/docs/Reference/RAND.en.md` |
| `RANDOMIZE` | `RANDOMIZE int` | `emuera.em.doc/docs/Reference/RANDOMIZE.en.md` |
| `REDRAW` | `REDRAW int` | `emuera.em.doc/docs/Reference/REDRAW.en.md` |
| `REGEXPMATCH` | `1. int REGEXPMATCH str, pattern(, output)` | `emuera.em.doc/docs/Reference/REGEXPMATCH.en.md` |
| `REPEAT` | `REPEAT loopCount` | `emuera.em.doc/docs/Reference/REPEAT.en.md` |
| `REPLACE` | `string REPLACE string, searchWord, replaceWord` | `emuera.em.doc/docs/Reference/REPLACE.en.md` |
| `RESETDATA` | `RESETDATA` | `emuera.em.doc/docs/Reference/RESETDATA.en.md` |
| `RESETGLOBAL` | `RESETGLOBAL` | `emuera.em.doc/docs/Reference/RESETGLOBAL.en.md` |
| `RESET_STAIN` | `RESET_STAIN charaID` | `emuera.em.doc/docs/Reference/RESET_STAIN.en.md` |
| `RESTART` | `RESTART` | `emuera.em.doc/docs/Reference/RESTART.en.md` |
| `RETURN` | `RETURN result:0(, result:1,...)` | `emuera.em.doc/docs/Reference/RETURN.en.md` |
| `REUSELASTLINE` | `REUSELASTLINE string` | `emuera.em.doc/docs/Reference/REUSELASTLINE.en.md` |
| `SAVECHARA` | `SAVECHARA filename, memo, charaNO{,charaNO2...}` | `emuera.em.doc/docs/Reference/SAVECHARA.en.md` |
| `SAVEDATA` | `SAVEDATA saveID, saveInfo` | `emuera.em.doc/docs/Reference/SAVEDATA.en.md` |
| `SAVEGAME` | `SAVEGAME` | `emuera.em.doc/docs/Reference/SAVEGAME.en.md` |
| `SAVEGLOBAL` | `SAVEGLOBAL` | `emuera.em.doc/docs/Reference/SAVEGLOBAL.en.md` |
| `SAVENOS` | `int SAVENOS variable` | `emuera.em.doc/docs/Reference/SAVENOS.en.md` |
| `SAVETEXT` | `int SAVETEXT text, fileNo(, forceSavdir, forceUTF8)` | `emuera.em.doc/docs/Reference/SAVETEXT.en.md` |
| `SELECTCASE` | `SELECTCASE anyValue` | `emuera.em.doc/docs/Reference/SELECTCASE.en.md` |
| `SETANIMETIMER` | `SETANIMETIMER time` | `emuera.em.doc/docs/Reference/SETANIMETIMER.en.md` |
| `SETBGCOLOR` | `SETBGCOLOR R, G, B` | `emuera.em.doc/docs/Reference/SETBGCOLOR.en.md` |
| `SETBGMVOLUME` | `SETBGMVOLUME int(0 to 100)` | `emuera.em.doc/docs/Reference/SETBGMVOLUME.en.md` |
| `SETCOLOR` | `SETCOLOR R, G, B` | `emuera.em.doc/docs/Reference/SETCOLOR.en.md` |
| `SETCOLORBYNAME` | `SETCOLORBYNAME colorName` | `emuera.em.doc/docs/Reference/SETCOLORBYNAME.en.md` |
| `SETFONT` | `int CHKFONT fontName` | `emuera.em.doc/docs/Reference/SETFONT.en.md` |
| `SETSOUNDVOLUME` | `SETSOUNDVOLUME int(0 to 100)` | `emuera.em.doc/docs/Reference/SETSOUNDVOLUME.en.md` |
| `SKIPLOG` | `SKIPLOG bool` | `emuera.em.doc/docs/Reference/SKIPLOG.en.md` |
| `SKIP_RELATE` | `SKIPDISP bool` | `emuera.em.doc/docs/Reference/SKIP_RELATE.en.md` |
| `SORTCHARA` | `SORTCHARA charaVariable, FORWARDorBACK` | `emuera.em.doc/docs/Reference/SORTCHARA.en.md` |
| `SPLIT` | `SPLIT string, sepalateWord, stringArray` | `emuera.em.doc/docs/Reference/SPLIT.en.md` |
| `SPRITEANIMEADDFRAME` | `int SPRITEANIMEADDFRAME spriteName, gID, x, y, width, height, offsetx, offsety, delay` | `emuera.em.doc/docs/Reference/SPRITEANIMEADDFRAME.en.md` |
| `SPRITEANIMECREATE` | `int SPRITEANIMECREATE spriteName, width, height` | `emuera.em.doc/docs/Reference/SPRITEANIMECREATE.en.md` |
| `SPRITECREATE` | `int SPRITECREATE spriteName, gID` | `emuera.em.doc/docs/Reference/SPRITECREATE.en.md` |
| `SPRITECREATED` | `int SPRITECREATED spriteName` | `emuera.em.doc/docs/Reference/SPRITECREATED.en.md` |
| `SPRITEDISPOSE` | `int SPRITDISPOSE spriteName` | `emuera.em.doc/docs/Reference/SPRITEDISPOSE.en.md` |
| `SPRITEDISPOSEALL` | `int SPRITEDISPOSEALL, containCsvSprite` | `emuera.em.doc/docs/Reference/SPRITEDISPOSEALL.en.md` |
| `SPRITEGETCOLOR` | `int SPRITEGETCOLOR spriteName, x, y` | `emuera.em.doc/docs/Reference/SPRITEGETCOLOR.en.md` |
| `SPRITEMOVE` | `int SPRITEMOVE spriteName, movex, movey` | `emuera.em.doc/docs/Reference/SPRITEMOVE.en.md` |
| `SPRITEPOSXY` | `int SPRITEPOSX spriteName` | `emuera.em.doc/docs/Reference/SPRITEPOSXY.en.md` |
| `SPRITESETPOS` | `int SPRITESETPOS spriteName, posX, posY` | `emuera.em.doc/docs/Reference/SPRITESETPOS.en.md` |
| `SPRITEWIDTHHEIGHT` | `int SPRITEWIDTH spriteName` | `emuera.em.doc/docs/Reference/SPRITEWIDTHHEIGHT.en.md` |
| `SQRT` | `int SQRT int` | `emuera.em.doc/docs/Reference/SQRT.en.md` |
| `STOPBGM` | `STOPBGM` | `emuera.em.doc/docs/Reference/STOPBGM.en.md` |
| `STOPCALLTRAIN` | `STOPCALLTRAIN` | `emuera.em.doc/docs/Reference/STOPCALLTRAIN.en.md` |
| `STOPSOUND` | `STOPSOUND` | `emuera.em.doc/docs/Reference/STOPSOUND.en.md` |
| `STRCOUNT` | `int STRCOUNT string, searchWord` | `emuera.em.doc/docs/Reference/STRCOUNT.en.md` |
| `STRDATA` | `STRDATA stringVariable` | `emuera.em.doc/docs/Reference/STRDATA.en.md` |
| `STRFIND` | `int STRFIND string, searchWord(, startPosition)` | `emuera.em.doc/docs/Reference/STRFIND.en.md` |
| `STRFORM` | `string STRFORM formedString` | `emuera.em.doc/docs/Reference/STRFORM.en.md` |
| `STRLEN` | `STRLEN string` | `emuera.em.doc/docs/Reference/STRLEN.en.md` |
| `SUBSTRING` | `string SUBSTRING string, startPosition, characterCount` | `emuera.em.doc/docs/Reference/SUBSTRING.en.md` |
| `SUMARRAY` | `int SUMARRAY integerArray(, startIndex, endIndex)` | `emuera.em.doc/docs/Reference/SUMARRAY.en.md` |
| `SWAP` | `SWAP variable, variable` | `emuera.em.doc/docs/Reference/SWAP.en.md` |
| `SWAPCHARA` | `SWAPCHARA charaID, charaID` | `emuera.em.doc/docs/Reference/SWAPCHARA.en.md` |
| `TEXTBOX` | `1 SETTEXTBOX text` | `emuera.em.doc/docs/Reference/TEXTBOX.en.md` |
| `THROW` | `THROW formedString` | `emuera.em.doc/docs/Reference/THROW.en.md` |
| `TIMES` | `TIMES integerVariable, float` | `emuera.em.doc/docs/Reference/TIMES.en.md` |
| `TINPUT` | `TINPUT timeLimit, defaultValue(, displayTimeRemain, timeOverMessage, allowClick)` | `emuera.em.doc/docs/Reference/TINPUT.en.md` |
| `TOINT` | `int TOINT string` | `emuera.em.doc/docs/Reference/TOINT.en.md` |
| `TONEINPUT` | `TONEINPUT timeLimit, defaultValue(, displayTimeRemain, timeOverMessage, allowClick)` | `emuera.em.doc/docs/Reference/TONEINPUT.en.md` |
| `TOOLTIP_EXTENSION` | `TOOLTIP_CUSTOM bool` | `emuera.em.doc/docs/Reference/TOOLTIP_EXTENSION.en.md` |
| `TOOLTIP_SET` | `TOOLTIP_SETDELAY milliSecond` | `emuera.em.doc/docs/Reference/TOOLTIP_SET.en.md` |
| `TOOLTIP_SETCOLOR` | `TOOLTIP_SETCOLOR colorCode, colorCode` | `emuera.em.doc/docs/Reference/TOOLTIP_SETCOLOR.en.md` |
| `TOSTR` | `string TOSTR int, option` | `emuera.em.doc/docs/Reference/TOSTR.en.md` |
| `TOUPPER` | `string TOUPPER string` | `emuera.em.doc/docs/Reference/TOUPPER.en.md` |
| `TRY` | `TRYCALL functionName(, `argument`...)` | `emuera.em.doc/docs/Reference/TRY.en.md` |
| `TRYC` | `TRYCCALL functionName(, argument...)` | `emuera.em.doc/docs/Reference/TRYC.en.md` |
| `TRYCALLF` | `TRYCALLF funcName` | `emuera.em.doc/docs/Reference/TRYCALLF.en.md` |
| `TRYCALLFORMF` | `TRYCALLFORMF funcName` | `emuera.em.doc/docs/Reference/TRYCALLFORMF.en.md` |
| `TRYFORM` | `TRYCALLFORM formedString(, argument...)` | `emuera.em.doc/docs/Reference/TRYFORM.en.md` |
| `TRYLIST` | `TRYCALLLIST` | `emuera.em.doc/docs/Reference/TRYLIST.en.md` |
| `TWAIT` | `TWAIT timeLimit, forceWait` | `emuera.em.doc/docs/Reference/TWAIT.en.md` |
| `UNICODE` | `string UNICODE characterCode` | `emuera.em.doc/docs/Reference/UNICODE.en.md` |
| `UPCHECK` | `UPCHECK` | `emuera.em.doc/docs/Reference/UPCHECK.en.md` |
| `UPDATECHECK` | `UPDATECHECK` | `emuera.em.doc/docs/Reference/UPDATECHECK.en.md` |
| `VAR` | `VARI variableName = intValue` | `emuera.em.doc/docs/Reference/VAR.en.md` |
| `VARSET` | `VARSET variableName(, value, startIndex, endIndex)` | `emuera.em.doc/docs/Reference/VARSET.en.md` |
| `VARSETEX` | `1 VARSETEX varName, value(, setAllDim, from, to)` | `emuera.em.doc/docs/Reference/VARSETEX.en.md` |
| `VARSIZE` | `VARSIZE variableName` | `emuera.em.doc/docs/Reference/VARSIZE.en.md` |
| `WAIT` | `WAIT` | `emuera.em.doc/docs/Reference/WAIT.en.md` |
| `WAITANYKEY` | `WAITANYKEY` | `emuera.em.doc/docs/Reference/WAITANYKEY.en.md` |
| `WHILE` | `WHILE bool` | `emuera.em.doc/docs/Reference/WHILE.en.md` |
| `XML_ADDATTRIBUTE` | `1. int XML_ADDATTRIBUTE xmlId, xpath, attrName(, attrValue, methodType, doSetAll)` | `emuera.em.doc/docs/Reference/XML_ADDATTRIBUTE.en.md` |
| `XML_ADDNODE` | `1. int XML_ADDNODE xmlId, xpath, nodeXml(, methodType, doSetAll)` | `emuera.em.doc/docs/Reference/XML_ADDNODE.en.md` |
| `XML_GET` | `1. int XML_GET xml, xpath(, doOutput, outputType)` | `emuera.em.doc/docs/Reference/XML_GET.en.md` |
| `XML_MANAGE` | `int XML_DOCUMENT xmlId, xmlContent` | `emuera.em.doc/docs/Reference/XML_MANAGE.en.md` |
| `XML_REMOVEATTRIBUTE` | `1. int XML_REMOVEATTRIBUTE xmlId, xpath(, doSetAll)` | `emuera.em.doc/docs/Reference/XML_REMOVEATTRIBUTE.en.md` |
| `XML_REMOVENODE` | `1. int XML_REMOVENODE xmlId, xpath(, doSetAll)` | `emuera.em.doc/docs/Reference/XML_REMOVENODE.en.md` |
| `XML_REPLACE` | `1. int XML_REPLACE xmlId, newXml` | `emuera.em.doc/docs/Reference/XML_REPLACE.en.md` |
| `XML_SET` | `1. int XML_SET xmlId, xpath, value(, doSetAll, outputType)` | `emuera.em.doc/docs/Reference/XML_SET.en.md` |
| `XML_TOSTR` | `string XML_TOSTR xmlId` | `emuera.em.doc/docs/Reference/XML_TOSTR.en.md` |

## Full Signatures

See `builtins-signatures.md` for the full extracted signature blocks (doc-derived).
