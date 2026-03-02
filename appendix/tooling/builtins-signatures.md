# Built-in Commands and Functions (Signatures)

This file contains extracted `erbapi` signature blocks for built-in commands/functions. It is intended for quick lookup and offline use.

## `ABS`

- Source (fact-check): `emuera.em.doc/docs/Reference/ABS.en.md`
- Source language: `en`

```erb
	int ABS int
	int SIGN int
```

## `ADDCHARA`

- Source (fact-check): `emuera.em.doc/docs/Reference/ADDCHARA.en.md`
- Source language: `en`

```erb
	ADDCHARA charaNo(, charaNo,...)
```

## `ADDCOPYCHARA`

- Source (fact-check): `emuera.em.doc/docs/Reference/ADDCOPYCHARA.en.md`
- Source language: `en`

```erb
	ADDCOPYCHARA charaID
```

## `ADDDEFCHARA`

- Source (fact-check): `emuera.em.doc/docs/Reference/ADDDEFCHARA.en.md`
- Source language: `en`

```erb
	ADDDEFCHARA
```

## `ADDVOIDCHARA`

- Source (fact-check): `emuera.em.doc/docs/Reference/ADDVOIDCHARA.en.md`
- Source language: `en`

```erb
	ADDVOIDCHARA
```

## `ALIGNMENT`

- Source (fact-check): `emuera.em.doc/docs/Reference/ALIGNMENT.en.md`
- Source language: `en`

```erb
	ALIGNMENT keyword
	string CURRENTALIGN
```

## `ARRAYCOPY`

- Source (fact-check): `emuera.em.doc/docs/Reference/ARRAYCOPY.en.md`
- Source language: `en`

```erb
	ARRAYCOPY variableName, variableName
```

## `ARRAYMSORT`

- Source (fact-check): `emuera.em.doc/docs/Reference/ARRAYMSORT.en.md`
- Source language: `en`

```erb
	ARRAYMSORT variableName1(, variableName2,...)
```

## `ARRAYMSORTEX`

- Source (fact-check): `emuera.em.doc/docs/Reference/ARRAYMSORTEX.en.md`
- Source language: `en`

```erb
1. 1 ARRAYMSORTEX indexName, arrayNameList(, sortAscending, size)
2. 1 ARRAYMSORTEX indexArray, arrayNameList(, sortAscending, size)
```

## `ARRAYREMOVE`

- Source (fact-check): `emuera.em.doc/docs/Reference/ARRAYREMOVE.en.md`
- Source language: `en`

```erb
	ARRAYREMOVE variableName, startIndex, clearCount
```

## `ARRAYSHIFT`

- Source (fact-check): `emuera.em.doc/docs/Reference/ARRAYSHIFT.en.md`
- Source language: `en`

```erb
	ARRAYSHIFT variable, shiftCount, value(, startIndex, targetCount)
```

## `ARRAYSORT`

- Source (fact-check): `emuera.em.doc/docs/Reference/ARRAYSORT.en.md`
- Source language: `en`

```erb
	ARRAYSORT variableName(, FORWARD or BACK, startIndex, targetCount)
```

## `ASSERT`

- Source (fact-check): `emuera.em.doc/docs/Reference/ASSERT.en.md`
- Source language: `en`

```erb
	ASSERT bool
```

## `AWAIT`

- Source (fact-check): `emuera.em.doc/docs/Reference/AWAIT.en.md`
- Source language: `en`

```erb
	AWAIT milliSecond
```

## `BACKGROUND`

- Source (fact-check): `emuera.em.doc/docs/Reference/BACKGROUND.en.md`
- Source language: `en`

```erb
	SETBGIMAGE resourceName(, depth, opacity)
	REMOVEBGIMAGE resourceName
	CLEARBGIMAGE
```

## `BAR`

- Source (fact-check): `emuera.em.doc/docs/Reference/BAR.en.md`
- Source language: `en`

```erb
	BAR value, maxValue, length
```

## `BARSTR`

- Source (fact-check): `emuera.em.doc/docs/Reference/BARSTR.en.md`
- Source language: `en`

```erb
	string BARSTR value, maxValue, length
```

## `BEGIN`

- Source (fact-check): `emuera.em.doc/docs/Reference/BEGIN.en.md`
- Source language: `en`

```erb
	BEGIN identifier
```

## `BINPUT`

- Source (fact-check): `emuera.em.doc/docs/Reference/BINPUT.en.md`
- Source language: `en`

```erb
	BINPUT (defaultValue, AllowClick, CanSkip)
	BINPUTS (defaultValue, AllowClick, CanSkip)
```

## `BITMAP_CACHE_ENABLE`

- Source (fact-check): `emuera.em.doc/docs/Reference/BITMAP_CACHE_ENABLE.en.md`
- Source language: `en`

```erb
	BITMAP_CACHE_ENABLE bool
```

## `BIT_OPERATION`

- Source (fact-check): `emuera.em.doc/docs/Reference/BIT_OPERATION.en.md`
- Source language: `en`

```erb
	int GETBIT targetInt, bit
	SETBIT integerVariable, bit(, bit...)
	CLEARBIT integerVariable, bit(, bit...)
	INVERTBIT integerVariable, bit(, bit...)
```

## `CALL`

- Source (fact-check): `emuera.em.doc/docs/Reference/CALL.en.md`
- Source language: `en`

```erb
	CALL funcName
```

## `CALLEVENT`

- Source (fact-check): `emuera.em.doc/docs/Reference/CALLEVENT.en.md`
- Source language: `en`

```erb
	CALLEVENT eventFunction
```

## `CALLF`

- Source (fact-check): `emuera.em.doc/docs/Reference/CALLF.en.md`
- Source language: `en`

```erb
	CALLF functionName
	CALLFORMF formedString
```

## `CALLSHARP`

- Source (fact-check): `emuera.em.doc/docs/Reference/CALLSHARP.en.md`
- Source language: `en`

```erb
	CALLSHARP funcName
```

## `CALLTRAIN`

- Source (fact-check): `emuera.em.doc/docs/Reference/CALLTRAIN.en.md`
- Source language: `en`

```erb
	CALLTRAIN comCount
```

## `CARRAY`

- Source (fact-check): `emuera.em.doc/docs/Reference/CARRAY.en.md`
- Source language: `en`

```erb
	int SUMCARRAY charaArray(, start, end)
	int CMATCH charaArray, value(, start, end)
	int MAXCARRAY charaArray(, start, end)
	int MINCARRAY charaArray(, start, end)
```

## `CBGCLEAR`

- Source (fact-check): `emuera.em.doc/docs/Reference/CBGCLEAR.en.md`
- Source language: `en`

```erb
	int CBGCLEAR
```

## `CBGCLEARBUTTON`

- Source (fact-check): `emuera.em.doc/docs/Reference/CBGCLEARBUTTON.en.md`
- Source language: `en`

```erb
	int CBGCLEARBUTTON
```

## `CBGREMOVEMAPB`

- Source (fact-check): `emuera.em.doc/docs/Reference/CBGREMOVEMAPB.en.md`
- Source language: `en`

```erb
	int CBGREMOVEMAPB
```

## `CBGREMOVERANGE`

- Source (fact-check): `emuera.em.doc/docs/Reference/CBGREMOVERANGE.en.md`
- Source language: `en`

```erb
	int CBGREMOVERANGE zMin, zMax
```

## `CBGSETBMAPG`

- Source (fact-check): `emuera.em.doc/docs/Reference/CBGSETBMAPG.en.md`
- Source language: `en`

```erb
	int CBGSETBMAPG gID
```

## `CBGSETBUTTONSPRITE`

- Source (fact-check): `emuera.em.doc/docs/Reference/CBGSETBUTTONSPRITE.en.md`
- Source language: `en`

```erb
	int CBGSETBUTTONSPRITE button, spriteName, spriteNameB, x, y, zDepth
	int CBGSETBUTTONSPRITE button, spriteName, spriteNameB, x, y, zDepth, tooltip
```

## `CBGSETG`

- Source (fact-check): `emuera.em.doc/docs/Reference/CBGSETG.en.md`
- Source language: `en`

```erb
	int CBGSETG gID, x, y, zDepth
```

## `CBGSETSPRITE`

- Source (fact-check): `emuera.em.doc/docs/Reference/CBGSETSPRITE.en.md`
- Source language: `en`

```erb
	int CBGSETSPRITE, spriteName, x, y, zDepth
```

## `CHARATU`

- Source (fact-check): `emuera.em.doc/docs/Reference/CHARATU.en.md`
- Source language: `en`

```erb
	string CHARATU string, position
```

## `CHKCHARADATA`

- Source (fact-check): `emuera.em.doc/docs/Reference/CHKCHARADATA.en.md`
- Source language: `en`

```erb
	int CHKCHARADATA filename
```

## `CHKDATA`

- Source (fact-check): `emuera.em.doc/docs/Reference/CHKDATA.en.md`
- Source language: `en`

```erb
	int CHKDATA saveID
```

## `CLEARLINE`

- Source (fact-check): `emuera.em.doc/docs/Reference/CLEARLINE.en.md`
- Source language: `en`

```erb
	CLEARLINE line
```

## `CLEARMEMORY`

- Source (fact-check): `emuera.em.doc/docs/Reference/CLEARMEMORY.en.md`
- Source language: `en`

```erb
	int CLEARMEMORY
```

## `CLEARTEXTBOX`

- Source (fact-check): `emuera.em.doc/docs/Reference/CLEARTEXTBOX.en.md`
- Source language: `en`

```erb
	CLEARTEXTBOX
```

## `CLIENTFIELD`

- Source (fact-check): `emuera.em.doc/docs/Reference/CLIENTFIELD.en.md`
- Source language: `en`

```erb
	int CLIENTWIDTH
	int CLIENTHEIGHT
```

## `COLOR_FROM`

- Source (fact-check): `emuera.em.doc/docs/Reference/COLOR_FROM.en.md`
- Source language: `en`

```erb
	int COLOR_FROMNAME colorName
	string COLOR_FROMRGB R, G, B
```

## `CONTINUE`

- Source (fact-check): `emuera.em.doc/docs/Reference/CONTINUE.en.md`
- Source language: `en`

```erb
	loopInstruction
		CONTINUE
		BREAK
	loopendInstruction
```

## `CONVERT`

- Source (fact-check): `emuera.em.doc/docs/Reference/CONVERT.en.md`
- Source language: `en`

```erb
	
	string CONVERT value, ※
```

## `COPYCHARA`

- Source (fact-check): `emuera.em.doc/docs/Reference/COPYCHARA.en.md`
- Source language: `en`

```erb
	COPYCHARA charaID, charaID
```

## `CSVNAME`

- Source (fact-check): `emuera.em.doc/docs/Reference/CSVNAME.en.md`
- Source language: `en`

```erb
	CSVNAME charaNo
	CSVCALLNAME charaNo
	CSVNICKNAME charaNo
	CSVMASTERNAME charaNo
```

## `CSV_STATUS`

- Source (fact-check): `emuera.em.doc/docs/Reference/CSV_STATUS.en.md`
- Source language: `en`

```erb
	CSVBASE charaNo, index
	CSVCSTR charaNo, index
	CSVABL charaNo, index
	CSVTALENT charaNo, index
	CSVMARK charaNo, index
	CSVEXP charaNo, index
	CSVRELATION charaNo, index
	CSVJUEL charaNo, index
	CSVEQUIP charaNo, index
	CSVCFLAG charaNo, index
```

## `CUPCHECK`

- Source (fact-check): `emuera.em.doc/docs/Reference/CUPCHECK.en.md`
- Source language: `en`

```erb
CUPCHECK charaID
```

## `CUSTOMDRAWLINE`

- Source (fact-check): `emuera.em.doc/docs/Reference/CUSTOMDRAWLINE.en.md`
- Source language: `en`

```erb
	CUSTOMDRAWLINE string
	DRAWLINEFORM formedString
```

## `CVARSET`

- Source (fact-check): `emuera.em.doc/docs/Reference/CVARSET.en.md`
- Source language: `en`

```erb
	CVARSET characterVariable, index, value, startID, endID
```

## `DEBUGPRINT`

- Source (fact-check): `emuera.em.doc/docs/Reference/DEBUGPRINT.en.md`
- Source language: `en`

```erb
	DEBUGPRINT string
	DEBUGPRINTL string
	DEBUGPRINTFORM formedString
	DEBUGPRINTFORML formedString
```

## `DELALLCHARA`

- Source (fact-check): `emuera.em.doc/docs/Reference/DELALLCHARA.en.md`
- Source language: `en`

```erb
	DELALLCHARA
```

## `DELCHARA`

- Source (fact-check): `emuera.em.doc/docs/Reference/DELCHARA.en.md`
- Source language: `en`

```erb
	DELCHARA charaID(, charaID,...)
```

## `DELDATA`

- Source (fact-check): `emuera.em.doc/docs/Reference/DELDATA.en.md`
- Source language: `en`

```erb
	DELDATA saveID
```

## `DO`

- Source (fact-check): `emuera.em.doc/docs/Reference/DO.en.md`
- Source language: `en`

```erb
	DO
	LOOP bool
```

## `DOTRAIN`

- Source (fact-check): `emuera.em.doc/docs/Reference/DOTRAIN.en.md`
- Source language: `en`

```erb
	DOTRAIN trainNo
```

## `DRAWLINE`

- Source (fact-check): `emuera.em.doc/docs/Reference/DRAWLINE.en.md`
- Source language: `en`

```erb
	DRAWLINE
```

## `DT_CELL`

- Source (fact-check): `emuera.em.doc/docs/Reference/DT_CELL.en.md`
- Source language: `en`

```erb
int DT_CELL_GET dataTableName, row, columnName(, asId)
string DT_CELL_GETS dataTableName, row, columnName(, asId)
int DT_CELL_ISNULL dataTableName, row, columnName(, asId)
int DT_CELL_SET dataTableName, row, columnName(, value, asId)
```

## `DT_COLUMN`

- Source (fact-check): `emuera.em.doc/docs/Reference/DT_COLUMN.en.md`
- Source language: `en`

```erb
int DT_COLUMN_ADD dataTableName, columnName(, type, nullable)
int DT_COLUMN_EXIST dataTableName, columnName
int DT_COLUMN_REMOVE dataTableName, columnName
int DT_COLUMN_LENGTH dataTableName
int DT_COLUMN_OPTIONS dataTableName, columnName, option, optionValue([, option, optionValue] ...)
int DT_COLUMN_NAMES dataTableName(, outputArray)
```

## `DT_MANAGE`

- Source (fact-check): `emuera.em.doc/docs/Reference/DT_MANAGE.en.md`
- Source language: `en`

```erb
int DT_CREATE dataTableName
int DT_EXIST dataTableName
1 DT_RELEASE dataTableName
int DT_CLEAR dataTableName
int DT_NOCASE dataTableName, ignoreCase
```

## `DT_ROW`

- Source (fact-check): `emuera.em.doc/docs/Reference/DT_ROW.en.md`
- Source language: `en`

```erb
a. int DT_ROW_ADD dataTableName(, columnName, columnValue) ...
b. int DT_ROW_ADD dataTableName, columnNames, columnValues, count

a. int DT_ROW_SET dataTableName, idValue(, columnName, columnValue) ...
b. int DT_ROW_SET dataTableName, idValue, columnNames, columnValues, count

a. int DT_ROW_REMOVE dataTableName, idValue
b. int DT_ROW_REMOVE dataTableName, idValues, count

int DT_ROW_LENGTH dataTableName
```

## `DT_SELECT`

- Source (fact-check): `emuera.em.doc/docs/Reference/DT_SELECT.en.md`
- Source language: `en`

```erb
int DT_SELECT dataTableName(, filterExpression, sortRule, output)
```

## `DT_SERIALIZATION`

- Source (fact-check): `emuera.em.doc/docs/Reference/DT_SERIALIZATION.en.md`
- Source language: `en`

```erb
1. string DT_TOXML dataTableName(, schemaOutput)
2. int DT_FROMXML dataTableName, schemaXml, dataXml
```

## `ENUMFILES`

- Source (fact-check): `emuera.em.doc/docs/Reference/ENUMFILES.en.md`
- Source language: `en`

```erb
int ENUMFILES dir, pattern, option
```

## `ENUMFUNC`

- Source (fact-check): `emuera.em.doc/docs/Reference/ENUMFUNC.en.md`
- Source language: `en`

```erb
int ENUMFUNCBEGINSWITH keyword
int ENUMFUNCENDSWITH keyword
int ENUMFUNCWITH keyword
```

## `ENUMMACRO`

- Source (fact-check): `emuera.em.doc/docs/Reference/ENUMMACRO.en.md`
- Source language: `en`

```erb
int ENUMMACROBEGINSWITH keyword
int ENUMMACROENDSWITH keyword
int ENUMMACROWITH keyword
```

## `ENUMVAR`

- Source (fact-check): `emuera.em.doc/docs/Reference/ENUMVAR.en.md`
- Source language: `en`

```erb
int ENUMVARBEGINSWITH keyword
int ENUMVARENDSWITH keyword
int ENUMVARWITH keyword
```

## `ERDNAME`

- Source (fact-check): `emuera.em.doc/docs/Reference/ERDNAME.en.md`
- Source language: `en`

```erb
	string ERDNAME variableName, index(, dimension)
```

## `ESCAPE`

- Source (fact-check): `emuera.em.doc/docs/Reference/ESCAPE.en.md`
- Source language: `en`

```erb
	string ESCAPE string
```

## `EXISTCSV`

- Source (fact-check): `emuera.em.doc/docs/Reference/EXISTCSV.en.md`
- Source language: `en`

```erb
	int EXISTCSV charaNO
```

## `EXISTFILE`

- Source (fact-check): `emuera.em.doc/docs/Reference/EXISTFILE.en.md`
- Source language: `en`

```erb
	int EXISTFILE relativePath
```

## `EXISTFUNCTION`

- Source (fact-check): `emuera.em.doc/docs/Reference/EXISTFUNCTION.en.md`
- Source language: `en`

```erb
	int EXISTFUNCTION funcName
```

## `EXISTMETH`

- Source (fact-check): `emuera.em.doc/docs/Reference/EXISTMETH.en.md`
- Source language: `en`

```erb
	int EXISTMETH functionName
```

## `EXISTSOUND`

- Source (fact-check): `emuera.em.doc/docs/Reference/EXISTSOUND.en.md`
- Source language: `en`

```erb
	EXISTSOUND MediaFile
```

## `EXISTVAR`

- Source (fact-check): `emuera.em.doc/docs/Reference/EXISTVAR.en.md`
- Source language: `en`

```erb
int EXISTVAR varName
```

## `FINDCHARA`

- Source (fact-check): `emuera.em.doc/docs/Reference/FINDCHARA.en.md`
- Source language: `en`

```erb
	int FINDCHARA charaVariable, value(, startID, endID)
	int FINDLASTCHARA charaVariable, value(, startID, endID)
```

## `FINDELEMENT`

- Source (fact-check): `emuera.em.doc/docs/Reference/FINDELEMENT.en.md`
- Source language: `en`

```erb
	FINDELEMENT variableName, value(, startIndex, endIndex, completeMatch)
	FINDLASTELEMENT variableName, value(, startIndex, endIndex, completeMatch)
```

## `FIND_CHARADATA`

- Source (fact-check): `emuera.em.doc/docs/Reference/FIND_CHARADATA.en.md`
- Source language: `en`

```erb
	int FIND_CHARADATA filename
```

## `FLOWINPUT`

- Source (fact-check): `emuera.em.doc/docs/Reference/FLOWINPUT.en.md`
- Source language: `en`

```erb
	FLOWINPUT default(, AllowLeftClick, AllowSkip, ForceSkip)
	FLOWINPUTS toggle(, default)
```

## `FONT_OPERATION`

- Source (fact-check): `emuera.em.doc/docs/Reference/FONT_OPERATION.en.md`
- Source language: `en`

```erb
	FONTBOLD
	FONTITALIC
	FONTSTYLE
	FONTREGULAR bitStyle
	int GETSTYLE
```

## `FOR`

- Source (fact-check): `emuera.em.doc/docs/Reference/FOR.en.md`
- Source language: `en`

```erb
	FOR integerVariable, startNum, endNum(, value)
```

## `FORCEKANA`

- Source (fact-check): `emuera.em.doc/docs/Reference/FORCEKANA.en.md`
- Source language: `en`

```erb
	FORCEKANA int
```

## `FORCEWAIT`

- Source (fact-check): `emuera.em.doc/docs/Reference/FORCEWAIT.en.md`
- Source language: `en`

```erb
	FORCEWAIT
```

## `FORCE_BEGIN`

- Source (fact-check): `emuera.em.doc/docs/Reference/FORCE_BEGIN.en.md`
- Source language: `en`

```erb
	FORCE_BEGIN SystemFuncName
```

## `FORCE_QUIT`

- Source (fact-check): `emuera.em.doc/docs/Reference/FORCE_QUIT.en.md`
- Source language: `en`

```erb
	FORCE_QUIT
```

## `FORCE_QUIT_AND_RESTART`

- Source (fact-check): `emuera.em.doc/docs/Reference/FORCE_QUIT_AND_RESTART.en.md`
- Source language: `en`

```erb
	FORCE_QUIT_AND_RESTART
```

## `FORM`

- Source (fact-check): `emuera.em.doc/docs/Reference/FORM.en.md`
- Source language: `en`

```erb
	CALLFORM functionName(, argument...)
	JUMPFORM functionName(, argument...)
	GOTOFORM labelName
```

## `GCLEAR`

- Source (fact-check): `emuera.em.doc/docs/Reference/GCLEAR.en.md`
- Source language: `en`

```erb
	int GCLEAR gID, cARGB
```

## `GCREATE`

- Source (fact-check): `emuera.em.doc/docs/Reference/GCREATE.en.md`
- Source language: `en`

```erb
	int GCREATE gID, width, height
```

## `GCREATED`

- Source (fact-check): `emuera.em.doc/docs/Reference/GCREATED.en.md`
- Source language: `en`

```erb
	int GCREATED gID
```

## `GCREATEFROMFILE`

- Source (fact-check): `emuera.em.doc/docs/Reference/GCREATEFROMFILE.en.md`
- Source language: `en`

```erb
	int GCREATEFROMFILE gID, filePath
```

## `GDASHSTYLE`

- Source (fact-check): `emuera.em.doc/docs/Reference/GDASHSTYLE.en.md`
- Source language: `en`

```erb
	int GDASHSTYLE gID, DashStyle, DashCap
```

## `GDISPOSE`

- Source (fact-check): `emuera.em.doc/docs/Reference/GDISPOSE.en.md`
- Source language: `en`

```erb
	int GDISPOSE gID
```

## `GDRAWG`

- Source (fact-check): `emuera.em.doc/docs/Reference/GDRAWG.en.md`
- Source language: `en`

```erb
	int GDRAWG destID, srcID, destX, destY, destWidth, destHeight, srcX, srcY, srcWidth, srcHeight
	int GDRAWG destID, srcID, destX, destY, destWidth, destHeight, srcX, srcY, srcWidth, srcHeight, colorMatrix
```

## `GDRAWGWITHMASK`

- Source (fact-check): `emuera.em.doc/docs/Reference/GDRAWGWITHMASK.en.md`
- Source language: `en`

```erb
	GDRAWGWITHMASK destID, srcID, maskID, destX, destY
```

## `GDRAWGWITHROTATE`

- Source (fact-check): `emuera.em.doc/docs/Reference/GDRAWGWITHROTATE.en.md`
- Source language: `en`

```erb
	int GDRAWGWITHROTATE gID, destID, Angle(, x, y)
```

## `GDRAWLINE`

- Source (fact-check): `emuera.em.doc/docs/Reference/GDRAWLINE.en.md`
- Source language: `en`

```erb
	int GDRAWLINE gID, fromX, fromY, forX, forY
```

## `GDRAWSPRITE`

- Source (fact-check): `emuera.em.doc/docs/Reference/GDRAWSPRITE.en.md`
- Source language: `en`

```erb
	int GDRAWSPRITE gID, spriteName
	int GDRAWSPRITE gID, spriteName, destX, destY
	int GDRAWSPRITE gID, spriteName, destX, destY, destWidth, destHeight
	int GDRAWSPRITE gID, spriteName, destX, destY, destWidth, destHeight, colorMatrix
```

## `GDRAWTEXT`

- Source (fact-check): `emuera.em.doc/docs/Reference/GDRAWTEXT.en.md`
- Source language: `en`

```erb
	int GDRAWTEXT gID, text(, x, y)
```

## `GETCHARA`

- Source (fact-check): `emuera.em.doc/docs/Reference/GETCHARA.en.md`
- Source language: `en`

```erb
	int GETCHARA charaNO
```

## `GETCOLOR`

- Source (fact-check): `emuera.em.doc/docs/Reference/GETCOLOR.en.md`
- Source language: `en`

```erb
	int GETCOLOR
	int GETBGCOLOR
	int GETDEFCOLOR
	int GETDEFBGCOLOR
	int GETFOCUSCOLOR
```

## `GETCONFIG`

- Source (fact-check): `emuera.em.doc/docs/Reference/GETCONFIG.en.md`
- Source language: `en`

```erb
	int GETCONFIG configWord
	string GETCONFIGS configWord
```

## `GETDISPLAYLINE`

- Source (fact-check): `emuera.em.doc/docs/Reference/GETDISPLAYLINE.en.md`
- Source language: `en`

```erb
	string GETDISPLAYLINE lineNumber
```

## `GETKEY`

- Source (fact-check): `emuera.em.doc/docs/Reference/GETKEY.en.md`
- Source language: `en`

```erb
	GETKEY keyCode
	GETKEYTRIGGERED keyCode
```

## `GETLINESTR`

- Source (fact-check): `emuera.em.doc/docs/Reference/GETLINESTR.en.md`
- Source language: `en`

```erb
	string GETLINESTR pattern
```

## `GETMEMORYUSAGE`

- Source (fact-check): `emuera.em.doc/docs/Reference/GETMEMORYUSAGE.en.md`
- Source language: `en`

```erb
	int GETMEMORYUSAGE
```

## `GETMETH`

- Source (fact-check): `emuera.em.doc/docs/Reference/GETMETH.en.md`
- Source language: `en`

```erb
	int GETMETH functionName(, defaultValue, argument...)
	string GETMETHS functionName(, defaultValue, argument...)
```

## `GETMILLISECOND`

- Source (fact-check): `emuera.em.doc/docs/Reference/GETMILLISECOND.en.md`
- Source language: `en`

```erb
	int GETMILLISECOND
```

## `GETNUM`

- Source (fact-check): `emuera.em.doc/docs/Reference/GETNUM.en.md`
- Source language: `en`

```erb
	GETNUM variableName, indexName
```

## `GETPALAMLV`

- Source (fact-check): `emuera.em.doc/docs/Reference/GETPALAMLV.en.md`
- Source language: `en`

```erb
	GETPALAMLV int, maxLV
	GETEXPLV int, maxLV
```

## `GETSECOND`

- Source (fact-check): `emuera.em.doc/docs/Reference/GETSECOND.en.md`
- Source language: `en`

```erb
	int GETTIME
```

## `GETSETVAR`

- Source (fact-check): `emuera.em.doc/docs/Reference/GETSETVAR.en.md`
- Source language: `en`

```erb
int GETVAR varName
string GETVARS varName
1 SETVAR varName, value
```

## `GETTIME`

- Source (fact-check): `emuera.em.doc/docs/Reference/GETTIME.en.md`
- Source language: `en`

```erb
	GETTIME
	int GETTIME
	string GETTIMES
```

## `GFILLRECTANGLE`

- Source (fact-check): `emuera.em.doc/docs/Reference/GFILLRECTANGLE.en.md`
- Source language: `en`

```erb
	int GFILLRECTANGLE gID, x, y, width, height
```

## `GGETBRUSH`

- Source (fact-check): `emuera.em.doc/docs/Reference/GGETBRUSH.en.md`
- Source language: `en`

```erb
	int GGETBRUSH gID
```

## `GGETCOLOR`

- Source (fact-check): `emuera.em.doc/docs/Reference/GGETCOLOR.en.md`
- Source language: `en`

```erb
	int GGETCOLOR gID, x, y
```

## `GGETFONT`

- Source (fact-check): `emuera.em.doc/docs/Reference/GGETFONT.en.md`
- Source language: `en`

```erb
	string GGETFONT gID
```

## `GGETFONTSIZE`

- Source (fact-check): `emuera.em.doc/docs/Reference/GGETFONTSIZE.en.md`
- Source language: `en`

```erb
	int GGETFONTSIZE gID
```

## `GGETFONTSTYLE`

- Source (fact-check): `emuera.em.doc/docs/Reference/GGETFONTSTYLE.en.md`
- Source language: `en`

```erb
	int GGETFONTSTYLE gID
```

## `GGETPEN`

- Source (fact-check): `emuera.em.doc/docs/Reference/GGETPEN.en.md`
- Source language: `en`

```erb
	int GGETPEN gID
```

## `GGETPENWIDTH`

- Source (fact-check): `emuera.em.doc/docs/Reference/GGETPENWIDTH.en.md`
- Source language: `en`

```erb
	int GGETPENWIDTH gID
```

## `GGETTEXTSIZE`

- Source (fact-check): `emuera.em.doc/docs/Reference/GGETTEXTSIZE.en.md`
- Source language: `en`

```erb
	int GGETTEXTSIZE text, fontName, fontSize(, fontStyle)
```

## `GOTO`

- Source (fact-check): `emuera.em.doc/docs/Reference/GOTO.en.md`
- Source language: `en`

```erb
	GOTO labelName
	$labelName
```

## `GROUPCHECK`

- Source (fact-check): `emuera.em.doc/docs/Reference/GROUPCHECK.en.md`
- Source language: `en`

```erb
	int GROUPMATCH key, value...
	int NOSAMES value, value...
	int ALLSAMES value, value...
```

## `GSAVELOAD`

- Source (fact-check): `emuera.em.doc/docs/Reference/GSAVELOAD.en.md`
- Source language: `en`

```erb
	int GSAVE gID, fileNo
	int GLOAD gID, fileNo
```

## `GSETBRUSH`

- Source (fact-check): `emuera.em.doc/docs/Reference/GSETBRUSH.en.md`
- Source language: `en`

```erb
	int GSETBRUSH gID, cARGB
```

## `GSETCOLOR`

- Source (fact-check): `emuera.em.doc/docs/Reference/GSETCOLOR.en.md`
- Source language: `en`

```erb
	int GSETCOLOR gID, cARGB, x, y
```

## `GSETFONT`

- Source (fact-check): `emuera.em.doc/docs/Reference/GSETFONT.en.md`
- Source language: `en`

```erb
	int GSETFONT gID, fontName, fontSize(, fontStyle)
```

## `GSETPEN`

- Source (fact-check): `emuera.em.doc/docs/Reference/GSETPEN.en.md`
- Source language: `en`

```erb
	int GSETPEN gID, cARGB, penWidth
```

## `GWIDTHHEIGHT`

- Source (fact-check): `emuera.em.doc/docs/Reference/GWIDTHHEIGHT.en.md`
- Source language: `en`

```erb
	int GWIDTH gID
	int GHEIGHT gID
```

## `HTML_ESCAPE`

- Source (fact-check): `emuera.em.doc/docs/Reference/HTML_ESCAPE.en.md`
- Source language: `en`

```erb
	str HTML_ESCAPE, htmlString  
```

## `HTML_GETPRINTEDSTR`

- Source (fact-check): `emuera.em.doc/docs/Reference/HTML_GETPRINTEDSTR.en.md`
- Source language: `en`

```erb
	str HTML_GETPRINTEDSTR, lineNo  
```

## `HTML_POPPRINTINGSTR`

- Source (fact-check): `emuera.em.doc/docs/Reference/HTML_POPPRINTINGSTR.en.md`
- Source language: `en`

```erb
	string HTML_POPPRINTINGSTR
```

## `HTML_PRINT`

- Source (fact-check): `emuera.em.doc/docs/Reference/HTML_PRINT.en.md`
- Source language: `en`

```erb
	HTML_PRINT htmlStyleString
```

## `HTML_PRINT_ISLAND`

- Source (fact-check): `emuera.em.doc/docs/Reference/HTML_PRINT_ISLAND.en.md`
- Source language: `en`

```erb
	HTML_PRINT_ISLAND htmlStyleString
```

## `HTML_STRINGLEN`

- Source (fact-check): `emuera.em.doc/docs/Reference/HTML_STRINGLEN.en.md`
- Source language: `en`

```erb
int HTML_STRINGLEN html(, returnPixel)
```

## `HTML_STRINGLINES`

- Source (fact-check): `emuera.em.doc/docs/Reference/HTML_STRINGLINES.en.md`
- Source language: `en`

```erb
int HTML_STRINGLINES html, width
```

## `HTML_SUBSTRING`

- Source (fact-check): `emuera.em.doc/docs/Reference/HTML_SUBSTRING.en.md`
- Source language: `en`

```erb
int HTML_SUBSTRING html, width
```

## `HTML_TAGSPLIT`

- Source (fact-check): `emuera.em.doc/docs/Reference/HTML_TAGSPLIT.en.md`
- Source language: `en`

```erb
	HTML_TAGSPLIT string(, integerVariable, stringVariable)
```

## `HTML_TOPLAINTEXT`

- Source (fact-check): `emuera.em.doc/docs/Reference/HTML_TOPLAINTEXT.en.md`
- Source language: `en`

```erb
	str HTML_TOPLAINTEXT, string  
```

## `IF`

- Source (fact-check): `emuera.em.doc/docs/Reference/IF.en.md`
- Source language: `en`

```erb
	IF operand(int)
	ELSEIF operand(int)
	ELSE
	ENDIF
	SIF operand(int)
```

## `INPUT`

- Source (fact-check): `emuera.em.doc/docs/Reference/INPUT.en.md`
- Source language: `en`

```erb
	INPUT (defaultValue, canClick, allowSkip)
	INPUTS (defaultValue, canClick, allowSkip)
```

## `INPUTANY`

- Source (fact-check): `emuera.em.doc/docs/Reference/INPUTANY.en.md`
- Source language: `en`

```erb
	INPUTANY
```

## `INPUTMOUSEKEY`

- Source (fact-check): `emuera.em.doc/docs/Reference/INPUTMOUSEKEY.en.md`
- Source language: `en`

```erb
	INPUTMOUSEKEY timeLimit
```

## `INRANGEARRAY`

- Source (fact-check): `emuera.em.doc/docs/Reference/INRANGEARRAY.en.md`
- Source language: `en`

```erb
	int INRANGEARRAY integerArray, minValue, maxValue(, start, end)
	int INRANGECARRAY charaArray, minValue, maxValue(, start, end)
```

## `ISACTIVE`

- Source (fact-check): `emuera.em.doc/docs/Reference/ISACTIVE.en.md`
- Source language: `en`

```erb
	ISACTIVE
```

## `ISDEFINED`

- Source (fact-check): `emuera.em.doc/docs/Reference/ISDEFINED.en.md`
- Source language: `en`

```erb
int ISDEFINED macroName
```

## `JUMP`

- Source (fact-check): `emuera.em.doc/docs/Reference/JUMP.en.md`
- Source language: `en`

```erb
	JUMP functionName
```

## `LINEISEMPTY`

- Source (fact-check): `emuera.em.doc/docs/Reference/LINEISEMPTY.en.md`
- Source language: `en`

```erb
	int LINEISEMPTY
```

## `LOADCHARA`

- Source (fact-check): `emuera.em.doc/docs/Reference/LOADCHARA.en.md`
- Source language: `en`

```erb
	LOADCHARA filename
```

## `LOADDATA`

- Source (fact-check): `emuera.em.doc/docs/Reference/LOADDATA.en.md`
- Source language: `en`

```erb
	LOADDATA saveID
```

## `LOADGLOBAL`

- Source (fact-check): `emuera.em.doc/docs/Reference/LOADGLOBAL.en.md`
- Source language: `en`

```erb
	LOADGLOBAL
```

## `LOADTEXT`

- Source (fact-check): `emuera.em.doc/docs/Reference/LOADTEXT.en.md`
- Source language: `en`

```erb
	LOADTEXT fileNo{, force_savdir, int force_UTF8}
```

## `MAP_GETKEYS`

- Source (fact-check): `emuera.em.doc/docs/Reference/MAP_GETKEYS.en.md`
- Source language: `en`

```erb
1. string MAP_GETKEYS mapName
2. string MAP_GETKEYS mapName, doOutput
3. string MAP_GETKEYS mapName, ref outputArray, doOutput
```

## `MAP_MANAGE`

- Source (fact-check): `emuera.em.doc/docs/Reference/MAP_MANAGE.en.md`
- Source language: `en`

```erb
int MAP_CREATE mapName
int MAP_EXIST mapName
1 MAP_RELEASE mapName
```

## `MAP_OPERATION`

- Source (fact-check): `emuera.em.doc/docs/Reference/MAP_OPERATION.en.md`
- Source language: `en`

```erb
string MAP_GET mapName, key
int MAP_HAS mapName, key
int MAP_SET mapName, key, value
int MAP_REMOVE mapName, key
int MAP_SIZE mapName
int MAP_CLEAR mapName
```

## `MAP_SERIALIZATION`

- Source (fact-check): `emuera.em.doc/docs/Reference/MAP_SERIALIZATION.en.md`
- Source language: `en`

```erb
1. string MAP_TOXML mapName
2. int MAP_FROMXML mapName, xmlMap
```

## `MATCH`

- Source (fact-check): `emuera.em.doc/docs/Reference/MATCH.en.md`
- Source language: `en`

```erb
	int MATCH array, value(, start, end)
```

## `MATH_EXTENSION`

- Source (fact-check): `emuera.em.doc/docs/Reference/MATH_EXTENSION.en.md`
- Source language: `en`

```erb
	int CBRT value
	int LOG value
	int LOG10 value
	int EXPONENT value
```

## `MAX`

- Source (fact-check): `emuera.em.doc/docs/Reference/MAX.en.md`
- Source language: `en`

```erb
	int MAX int(, int...)
	int MIN int(, int...)
	int LIMIT int, minValue, maxValue
	int INRANGE int, minValue, maxValue
```

## `MAXMINARRAY`

- Source (fact-check): `emuera.em.doc/docs/Reference/MAXMINARRAY.en.md`
- Source language: `en`

```erb
	int MAXARRAY integerArray(, start, end)
	int MINARRAY integerArray(, start, end)
```

## `MONEYSTR`

- Source (fact-check): `emuera.em.doc/docs/Reference/MONEYSTR.en.md`
- Source language: `en`

```erb
	string MONEYSTR
```

## `MOUSEB`

- Source (fact-check): `emuera.em.doc/docs/Reference/MOUSEB.en.md`
- Source language: `en`

```erb
	string MOUSEB
```

## `MOUSEXY`

- Source (fact-check): `emuera.em.doc/docs/Reference/MOUSEXY.en.md`
- Source language: `en`

```erb
	MOUSEX
	MOUSEY
```

## `ONEINPUT`

- Source (fact-check): `emuera.em.doc/docs/Reference/ONEINPUT.en.md`
- Source language: `en`

```erb
	ONEINPUT defaultValue
	ONEINPUTS defaultValue
```

## `OUTPUTLOG`

- Source (fact-check): `emuera.em.doc/docs/Reference/OUTPUTLOG.en.md`
- Source language: `en`

```erb
	OUTPUTLOG (filePath)
```

## `PICKUPCHARA`

- Source (fact-check): `emuera.em.doc/docs/Reference/PICKUPCHARA.en.md`
- Source language: `en`

```erb
	PICKUPCHARA charaID(, charaID...)
```

## `PLAYBGM`

- Source (fact-check): `emuera.em.doc/docs/Reference/PLAYBGM.en.md`
- Source language: `en`

```erb
	PLAYBGM MediaFile
```

## `PLAYSOUND`

- Source (fact-check): `emuera.em.doc/docs/Reference/PLAYSOUND.en.md`
- Source language: `en`

```erb
	PLAYSOUND MediaFile
```

## `POWER`

- Source (fact-check): `emuera.em.doc/docs/Reference/POWER.en.md`
- Source language: `en`

```erb
	POWER integerVariable, int, int
	int POWER int, int
```

## `PRINT`

- Source (fact-check): `emuera.em.doc/docs/Reference/PRINT.en.md`
- Source language: `en`

```erb
PRINTV(|K|D)(|L|W|N) integerVariable
PRINTS(|K|D)(|L|W|N) stringVariable
PRINTFORM(|K|D)(|L|W|N) formedString
PRINTFORMS(|K|D)(|L|W|N) string
```

## `PRINTBUTTON`

- Source (fact-check): `emuera.em.doc/docs/Reference/PRINTBUTTON.en.md`
- Source language: `en`

```erb
PRINTBUTTON(|C|LC) string, buttonValue
```

## `PRINTC`

- Source (fact-check): `emuera.em.doc/docs/Reference/PRINTC.en.md`
- Source language: `en`

```erb
PRINT(C|L)(|K|D) string
PRINTFORM(C|L)(|K|D)(|L|W) formedString
```

## `PRINTCLENGTH`

- Source (fact-check): `emuera.em.doc/docs/Reference/PRINTCLENGTH.en.md`
- Source language: `en`

```erb
	int PRINTCLENGTH
```

## `PRINTCPERLINE`

- Source (fact-check): `emuera.em.doc/docs/Reference/PRINTCPERLINE.en.md`
- Source language: `en`

```erb
	int PRINTCPERLINE
```

## `PRINTDATA`

- Source (fact-check): `emuera.em.doc/docs/Reference/PRINTDATA.en.md`
- Source language: `en`

```erb
PRINTDATA(|K|D)(|L|W)
	DATA string
	DATAFORM formedString
	DATALIST
	ENDLIST
ENDDATA
```

## `PRINTN`

- Source (fact-check): `emuera.em.doc/docs/Reference/PRINTN.en.md`
- Source language: `en`

```erb
	PRINTN string
    PRINTVN integerVariable
    PRINTSN stringVariable
    PRINTFORMN formedString
    PRINTFORMSN string
```

## `PRINTPLAIN`

- Source (fact-check): `emuera.em.doc/docs/Reference/PRINTPLAIN.en.md`
- Source language: `en`

```erb
PRINTPLAIN(|FORM) string
```

## `PRINTSINGLE`

- Source (fact-check): `emuera.em.doc/docs/Reference/PRINTSINGLE.en.md`
- Source language: `en`

```erb
PRINTSINGLEV(|K|D) integerVariable
PRINTSINGLES(|K|D) stringVariable
PRINTSINGLEFORM(|K|D) formedString
PRINTSINGLEFORMS(|K|D) string
```

## `PRINT_IMG`

- Source (fact-check): `emuera.em.doc/docs/Reference/PRINT_IMG.en.md`
- Source language: `en`

```erb
	PRINT_IMG spriteName
	PRINT_IMG spriteName, width, height, ypos
	PRINT_IMG spriteName, spriteNameBack, width, height, ypos
	PRINT_IMG spriteName, spriteNameBack, colorMatrix, width, height, ypos
```

## `PRINT_RECT`

- Source (fact-check): `emuera.em.doc/docs/Reference/PRINT_RECT.en.md`
- Source language: `en`

```erb
	PRINT_RECT width
	PRINT_RECT xPos, yPos, width, height
```

## `PRINT_SPACE`

- Source (fact-check): `emuera.em.doc/docs/Reference/PRINT_SPACE.en.md`
- Source language: `en`

```erb
	PRINT_SPACE width
```

## `PRINT_STATUS`

- Source (fact-check): `emuera.em.doc/docs/Reference/PRINT_STATUS.en.md`
- Source language: `en`

```erb
	PRINT_ABL charaID
	PRINT_TALENT charaID
	PRINT_MARK charaID
	PRINT_EXP charaID
	PRINT_PALAM charaID
	PRINT_ITEM
	PRINT_SHOPITEM
```

## `PUTFORM`

- Source (fact-check): `emuera.em.doc/docs/Reference/PUTFORM.en.md`
- Source language: `en`

```erb
	PUTFORM saveInfo
```

## `QUIT`

- Source (fact-check): `emuera.em.doc/docs/Reference/QUIT.en.md`
- Source language: `en`

```erb
	QUIT
```

## `QUIT_AND_RESTART`

- Source (fact-check): `emuera.em.doc/docs/Reference/QUIT_AND_RESTART.en.md`
- Source language: `en`

```erb
	QUIT_AND_RESTART
```

## `RAND`

- Source (fact-check): `emuera.em.doc/docs/Reference/RAND.en.md`
- Source language: `en`

```erb
	int RAND min(, max)
```

## `RANDOMIZE`

- Source (fact-check): `emuera.em.doc/docs/Reference/RANDOMIZE.en.md`
- Source language: `en`

```erb
	RANDOMIZE int
	DUMPRAND
	INITRAND
```

## `REDRAW`

- Source (fact-check): `emuera.em.doc/docs/Reference/REDRAW.en.md`
- Source language: `en`

```erb
	REDRAW int
	int CURRENTREDRAW
```

## `REGEXPMATCH`

- Source (fact-check): `emuera.em.doc/docs/Reference/REGEXPMATCH.en.md`
- Source language: `en`

```erb
1. int REGEXPMATCH str, pattern(, output)
2. int REGEXPMATCH str, pattern, ref groupCount, ref matches
```

## `REPEAT`

- Source (fact-check): `emuera.em.doc/docs/Reference/REPEAT.en.md`
- Source language: `en`

```erb
	REPEAT loopCount
	REND
```

## `REPLACE`

- Source (fact-check): `emuera.em.doc/docs/Reference/REPLACE.en.md`
- Source language: `en`

```erb
	string REPLACE string, searchWord, replaceWord
```

## `RESETDATA`

- Source (fact-check): `emuera.em.doc/docs/Reference/RESETDATA.en.md`
- Source language: `en`

```erb
	RESETDATA
```

## `RESETGLOBAL`

- Source (fact-check): `emuera.em.doc/docs/Reference/RESETGLOBAL.en.md`
- Source language: `en`

```erb
	RESETGLOBAL
```

## `RESET_STAIN`

- Source (fact-check): `emuera.em.doc/docs/Reference/RESET_STAIN.en.md`
- Source language: `en`

```erb
	RESET_STAIN charaID
```

## `RESTART`

- Source (fact-check): `emuera.em.doc/docs/Reference/RESTART.en.md`
- Source language: `en`

```erb
	RESTART
```

## `RETURN`

- Source (fact-check): `emuera.em.doc/docs/Reference/RETURN.en.md`
- Source language: `en`

```erb
	RETURN result:0(, result:1,...)
	RETURNFORM formedString(, formedString,...)
```

## `REUSELASTLINE`

- Source (fact-check): `emuera.em.doc/docs/Reference/REUSELASTLINE.en.md`
- Source language: `en`

```erb
	REUSELASTLINE string
```

## `SAVECHARA`

- Source (fact-check): `emuera.em.doc/docs/Reference/SAVECHARA.en.md`
- Source language: `en`

```erb
	SAVECHARA filename, memo, charaNO{,charaNO2...}
```

## `SAVEDATA`

- Source (fact-check): `emuera.em.doc/docs/Reference/SAVEDATA.en.md`
- Source language: `en`

```erb
	SAVEDATA saveID, saveInfo
```

## `SAVEGAME`

- Source (fact-check): `emuera.em.doc/docs/Reference/SAVEGAME.en.md`
- Source language: `en`

```erb
	SAVEGAME
	LOADGAME
```

## `SAVEGLOBAL`

- Source (fact-check): `emuera.em.doc/docs/Reference/SAVEGLOBAL.en.md`
- Source language: `en`

```erb
	SAVEGLOBAL
```

## `SAVENOS`

- Source (fact-check): `emuera.em.doc/docs/Reference/SAVENOS.en.md`
- Source language: `en`

```erb
	int SAVENOS variable
```

## `SAVETEXT`

- Source (fact-check): `emuera.em.doc/docs/Reference/SAVETEXT.en.md`
- Source language: `en`

```erb
	int SAVETEXT text, fileNo(, forceSavdir, forceUTF8)
```

## `SELECTCASE`

- Source (fact-check): `emuera.em.doc/docs/Reference/SELECTCASE.en.md`
- Source language: `en`

```erb
	SELECTCASE anyValue
	CASE anyValue(, anyValue...)
	CASEELSE
	ENDSELECT
```

## `SETANIMETIMER`

- Source (fact-check): `emuera.em.doc/docs/Reference/SETANIMETIMER.en.md`
- Source language: `en`

```erb
	SETANIMETIMER time
```

## `SETBGCOLOR`

- Source (fact-check): `emuera.em.doc/docs/Reference/SETBGCOLOR.en.md`
- Source language: `en`

```erb
	SETBGCOLOR R, G, B
	SETBGCOLOR hexaDecimal
	RESETBGCOLOR
```

## `SETBGMVOLUME`

- Source (fact-check): `emuera.em.doc/docs/Reference/SETBGMVOLUME.en.md`
- Source language: `en`

```erb
	SETBGMVOLUME int(0 to 100)
```

## `SETCOLOR`

- Source (fact-check): `emuera.em.doc/docs/Reference/SETCOLOR.en.md`
- Source language: `en`

```erb
	SETCOLOR R, G, B
	SETCOLOR hexaDecimal
	RESETCOLOR
```

## `SETCOLORBYNAME`

- Source (fact-check): `emuera.em.doc/docs/Reference/SETCOLORBYNAME.en.md`
- Source language: `en`

```erb
	SETCOLORBYNAME colorName
	SETBGCOLORBYNAME colorName
```

## `SETFONT`

- Source (fact-check): `emuera.em.doc/docs/Reference/SETFONT.en.md`
- Source language: `en`

```erb
	int CHKFONT fontName
	SETFONT fontName
	string GETFONT
```

## `SETSOUNDVOLUME`

- Source (fact-check): `emuera.em.doc/docs/Reference/SETSOUNDVOLUME.en.md`
- Source language: `en`

```erb
	SETSOUNDVOLUME int(0 to 100)
```

## `SKIPLOG`

- Source (fact-check): `emuera.em.doc/docs/Reference/SKIPLOG.en.md`
- Source language: `en`

```erb
	SKIPLOG bool
```

## `SKIP_RELATE`

- Source (fact-check): `emuera.em.doc/docs/Reference/SKIP_RELATE.en.md`
- Source language: `en`

```erb
	SKIPDISP bool
	NOSKIP
	ENDNOSKIP
	int ISSKIP
	int MOUSESKIP
	int MESSKIP
```

## `SORTCHARA`

- Source (fact-check): `emuera.em.doc/docs/Reference/SORTCHARA.en.md`
- Source language: `en`

```erb
	SORTCHARA charaVariable, FORWARDorBACK
```

## `SPLIT`

- Source (fact-check): `emuera.em.doc/docs/Reference/SPLIT.en.md`
- Source language: `en`

```erb
	SPLIT string, sepalateWord, stringArray
	string STRJOIN stringArray(, sepalateWord, startIndex, joinCount)
```

## `SPRITEANIMEADDFRAME`

- Source (fact-check): `emuera.em.doc/docs/Reference/SPRITEANIMEADDFRAME.en.md`
- Source language: `en`

```erb
	int SPRITEANIMEADDFRAME spriteName, gID, x, y, width, height, offsetx, offsety, delay
```

## `SPRITEANIMECREATE`

- Source (fact-check): `emuera.em.doc/docs/Reference/SPRITEANIMECREATE.en.md`
- Source language: `en`

```erb
	int SPRITEANIMECREATE spriteName, width, height
```

## `SPRITECREATE`

- Source (fact-check): `emuera.em.doc/docs/Reference/SPRITECREATE.en.md`
- Source language: `en`

```erb
	int SPRITECREATE spriteName, gID
	int SPRITECREATE spriteName, gID, x, y, width, height
```

## `SPRITECREATED`

- Source (fact-check): `emuera.em.doc/docs/Reference/SPRITECREATED.en.md`
- Source language: `en`

```erb
	int SPRITECREATED spriteName
```

## `SPRITEDISPOSE`

- Source (fact-check): `emuera.em.doc/docs/Reference/SPRITEDISPOSE.en.md`
- Source language: `en`

```erb
	int SPRITDISPOSE spriteName
```

## `SPRITEDISPOSEALL`

- Source (fact-check): `emuera.em.doc/docs/Reference/SPRITEDISPOSEALL.en.md`
- Source language: `en`

```erb
	int SPRITEDISPOSEALL, containCsvSprite
```

## `SPRITEGETCOLOR`

- Source (fact-check): `emuera.em.doc/docs/Reference/SPRITEGETCOLOR.en.md`
- Source language: `en`

```erb
	int SPRITEGETCOLOR spriteName, x, y
```

## `SPRITEMOVE`

- Source (fact-check): `emuera.em.doc/docs/Reference/SPRITEMOVE.en.md`
- Source language: `en`

```erb
	int SPRITEMOVE spriteName, movex, movey
```

## `SPRITEPOSXY`

- Source (fact-check): `emuera.em.doc/docs/Reference/SPRITEPOSXY.en.md`
- Source language: `en`

```erb
	int SPRITEPOSX spriteName
	int SPRITEPOSY spriteName
```

## `SPRITESETPOS`

- Source (fact-check): `emuera.em.doc/docs/Reference/SPRITESETPOS.en.md`
- Source language: `en`

```erb
	int SPRITESETPOS spriteName, posX, posY
```

## `SPRITEWIDTHHEIGHT`

- Source (fact-check): `emuera.em.doc/docs/Reference/SPRITEWIDTHHEIGHT.en.md`
- Source language: `en`

```erb
	int SPRITEWIDTH spriteName
	int SPRITEHEIGHT spriteName
```

## `SQRT`

- Source (fact-check): `emuera.em.doc/docs/Reference/SQRT.en.md`
- Source language: `en`

```erb
	int SQRT int
```

## `STOPBGM`

- Source (fact-check): `emuera.em.doc/docs/Reference/STOPBGM.en.md`
- Source language: `en`

```erb
	STOPBGM
```

## `STOPCALLTRAIN`

- Source (fact-check): `emuera.em.doc/docs/Reference/STOPCALLTRAIN.en.md`
- Source language: `en`

```erb
	STOPCALLTRAIN
```

## `STOPSOUND`

- Source (fact-check): `emuera.em.doc/docs/Reference/STOPSOUND.en.md`
- Source language: `en`

```erb
	STOPSOUND
```

## `STRCOUNT`

- Source (fact-check): `emuera.em.doc/docs/Reference/STRCOUNT.en.md`
- Source language: `en`

```erb
	int STRCOUNT string, searchWord
```

## `STRDATA`

- Source (fact-check): `emuera.em.doc/docs/Reference/STRDATA.en.md`
- Source language: `en`

```erb
	STRDATA stringVariable
		DATA
		DATAFORM
		DATALIST
		ENDLIST
	ENDDATA
```

## `STRFIND`

- Source (fact-check): `emuera.em.doc/docs/Reference/STRFIND.en.md`
- Source language: `en`

```erb
	int STRFIND string, searchWord(, startPosition)
	int STRFINDU string, searchWord(, startPosition)
```

## `STRFORM`

- Source (fact-check): `emuera.em.doc/docs/Reference/STRFORM.en.md`
- Source language: `en`

```erb
	string STRFORM formedString
```

## `STRLEN`

- Source (fact-check): `emuera.em.doc/docs/Reference/STRLEN.en.md`
- Source language: `en`

```erb
	STRLEN string
	int STRLENS string
	STRLENFORM formedString
	STRLENU string
	int STRLENSU string
	STRLENFORMU formedString
```

## `SUBSTRING`

- Source (fact-check): `emuera.em.doc/docs/Reference/SUBSTRING.en.md`
- Source language: `en`

```erb
	string SUBSTRING string, startPosition, characterCount
	string SUBSTRINGU string, startPosition, characterCount
```

## `SUMARRAY`

- Source (fact-check): `emuera.em.doc/docs/Reference/SUMARRAY.en.md`
- Source language: `en`

```erb
	int SUMARRAY integerArray(, startIndex, endIndex)
```

## `SWAP`

- Source (fact-check): `emuera.em.doc/docs/Reference/SWAP.en.md`
- Source language: `en`

```erb
	SWAP variable, variable
```

## `SWAPCHARA`

- Source (fact-check): `emuera.em.doc/docs/Reference/SWAPCHARA.en.md`
- Source language: `en`

```erb
	SWAPCHARA charaID, charaID
```

## `TEXTBOX`

- Source (fact-check): `emuera.em.doc/docs/Reference/TEXTBOX.en.md`
- Source language: `en`

```erb
1 SETTEXTBOX text
string GETTEXTBOX
1 MOVETEXTBOX xPos, yPos, width
1 RESUMETEXTBOX
```

## `THROW`

- Source (fact-check): `emuera.em.doc/docs/Reference/THROW.en.md`
- Source language: `en`

```erb
	THROW formedString
```

## `TIMES`

- Source (fact-check): `emuera.em.doc/docs/Reference/TIMES.en.md`
- Source language: `en`

```erb
	TIMES integerVariable, float
```

## `TINPUT`

- Source (fact-check): `emuera.em.doc/docs/Reference/TINPUT.en.md`
- Source language: `en`

```erb
	TINPUT timeLimit, defaultValue(, displayTimeRemain, timeOverMessage, allowClick)
	TINPUTS timeLimit, defaultValue(, displayTimeRemain, timeOverMessage, allowClick)
```

## `TOINT`

- Source (fact-check): `emuera.em.doc/docs/Reference/TOINT.en.md`
- Source language: `en`

```erb
	int TOINT string
	int ISNUMERIC string
```

## `TONEINPUT`

- Source (fact-check): `emuera.em.doc/docs/Reference/TONEINPUT.en.md`
- Source language: `en`

```erb
	TONEINPUT timeLimit, defaultValue(, displayTimeRemain, timeOverMessage, allowClick)
	TONEINPUTS timeLimit, defaultValue(, displayTimeRemain, timeOverMessage, allowClick)
```

## `TOOLTIP_EXTENSION`

- Source (fact-check): `emuera.em.doc/docs/Reference/TOOLTIP_EXTENSION.en.md`
- Source language: `en`

```erb
	TOOLTIP_CUSTOM bool
    TOOLTIP_SETFONT fontName
    TOOLTIP_SETFONTSIZE fontSize
    TOOLTIP_FORMAT formatFlags
```

## `TOOLTIP_SET`

- Source (fact-check): `emuera.em.doc/docs/Reference/TOOLTIP_SET.en.md`
- Source language: `en`

```erb
	TOOLTIP_SETDELAY milliSecond
	TOOLTIP_SETDURATION milliSecond
```

## `TOOLTIP_SETCOLOR`

- Source (fact-check): `emuera.em.doc/docs/Reference/TOOLTIP_SETCOLOR.en.md`
- Source language: `en`

```erb
	TOOLTIP_SETCOLOR colorCode, colorCode
```

## `TOSTR`

- Source (fact-check): `emuera.em.doc/docs/Reference/TOSTR.en.md`
- Source language: `en`

```erb
	string TOSTR int, option
```

## `TOUPPER`

- Source (fact-check): `emuera.em.doc/docs/Reference/TOUPPER.en.md`
- Source language: `en`

```erb
	string TOUPPER string
	string TOLOWER string
	string TOHALF string
	string TOFULL string
```

## `TRY`

- Source (fact-check): `emuera.em.doc/docs/Reference/TRY.en.md`
- Source language: `en`

```erb
	TRYCALL functionName(, `argument`...)
	TRYJUMP functionName(, `argument`...)
	TRYGOTO labelName
```

## `TRYC`

- Source (fact-check): `emuera.em.doc/docs/Reference/TRYC.en.md`
- Source language: `en`

```erb
	TRYCCALL functionName(, argument...)
	TRYCJUMP functionName(, argument...)
	TRYCJUMP labelName
	TRYCCALLFORM formedString(, argument...)
	TRYCJUMPFORM formedString(, argument...)
	TRYCGOTOFORM formedString
	CATCH
	ENDCATCH
```

## `TRYCALLF`

- Source (fact-check): `emuera.em.doc/docs/Reference/TRYCALLF.en.md`
- Source language: `en`

```erb
	TRYCALLF funcName
```

## `TRYCALLFORMF`

- Source (fact-check): `emuera.em.doc/docs/Reference/TRYCALLFORMF.en.md`
- Source language: `en`

```erb
	TRYCALLFORMF funcName
```

## `TRYFORM`

- Source (fact-check): `emuera.em.doc/docs/Reference/TRYFORM.en.md`
- Source language: `en`

```erb
	TRYCALLFORM formedString(, argument...)
	TRYJUMPFORM formedString(, argument...)
	TRYGOTOFORM formedString
```

## `TRYLIST`

- Source (fact-check): `emuera.em.doc/docs/Reference/TRYLIST.en.md`
- Source language: `en`

```erb
	TRYCALLLIST
	TRYJUMPLIST
	TRYGOTOLIST
	FUNC functionName(, argument...)
	ENDFUNC
```

## `TWAIT`

- Source (fact-check): `emuera.em.doc/docs/Reference/TWAIT.en.md`
- Source language: `en`

```erb
	TWAIT timeLimit, forceWait
```

## `UNICODE`

- Source (fact-check): `emuera.em.doc/docs/Reference/UNICODE.en.md`
- Source language: `en`

```erb
	string UNICODE characterCode
	int ENCODETOUNI string(, position)
```

## `UPCHECK`

- Source (fact-check): `emuera.em.doc/docs/Reference/UPCHECK.en.md`
- Source language: `en`

```erb
	UPCHECK
```

## `UPDATECHECK`

- Source (fact-check): `emuera.em.doc/docs/Reference/UPDATECHECK.en.md`
- Source language: `en`

```erb
	UPDATECHECK
```

## `VAR`

- Source (fact-check): `emuera.em.doc/docs/Reference/VAR.en.md`
- Source language: `en`

```erb
	VARI variableName = intValue
	VARS variableName = strValue
	VARI variableName(, arraySize)
	VARS variableName(, arraySize)
```

## `VARSET`

- Source (fact-check): `emuera.em.doc/docs/Reference/VARSET.en.md`
- Source language: `en`

```erb
	VARSET variableName(, value, startIndex, endIndex)
```

## `VARSETEX`

- Source (fact-check): `emuera.em.doc/docs/Reference/VARSETEX.en.md`
- Source language: `en`

```erb
1 VARSETEX varName, value(, setAllDim, from, to)
```

## `VARSIZE`

- Source (fact-check): `emuera.em.doc/docs/Reference/VARSIZE.en.md`
- Source language: `en`

```erb
	VARSIZE variableName
	VARSIZE(variableName(, dimension))
```

## `WAIT`

- Source (fact-check): `emuera.em.doc/docs/Reference/WAIT.en.md`
- Source language: `en`

```erb
	WAIT
```

## `WAITANYKEY`

- Source (fact-check): `emuera.em.doc/docs/Reference/WAITANYKEY.en.md`
- Source language: `en`

```erb
	WAITANYKEY
```

## `WHILE`

- Source (fact-check): `emuera.em.doc/docs/Reference/WHILE.en.md`
- Source language: `en`

```erb
	WHILE bool
	WEND
```

## `XML_ADDATTRIBUTE`

- Source (fact-check): `emuera.em.doc/docs/Reference/XML_ADDATTRIBUTE.en.md`
- Source language: `en`

```erb
1. int XML_ADDATTRIBUTE xmlId, xpath, attrName(, attrValue, methodType, doSetAll)
2. int XML_ADDATTRIBUTE ref xml, xpath, attrName(, attrValue, methodType, doSetAll)
3. int XML_ADDATTRIBUTE_BYNAME xmlName, xpath, attrName(, attrValue, methodType, doSetAll)
```

## `XML_ADDNODE`

- Source (fact-check): `emuera.em.doc/docs/Reference/XML_ADDNODE.en.md`
- Source language: `en`

```erb
1. int XML_ADDNODE xmlId, xpath, nodeXml(, methodType, doSetAll)
2. int XML_ADDNODE ref xml, xpath, nodeXml(, methodType, doSetAll)
3. int XML_ADDNODE_BYNAME xmlName, xpath, nodeXml(, methodType, doSetAll)
```

## `XML_GET`

- Source (fact-check): `emuera.em.doc/docs/Reference/XML_GET.en.md`
- Source language: `en`

```erb
1. int XML_GET xml, xpath(, doOutput, outputType)
2. int XML_GET xml, xpath, ref outputArray(, outputType)
3. int XML_GET_BYNAME xmlName, xpath(, doOutput, outputType)
4. int XML_GET_BYNAME xmlName, xpath, ref outputArray(, outputType)
```

## `XML_MANAGE`

- Source (fact-check): `emuera.em.doc/docs/Reference/XML_MANAGE.en.md`
- Source language: `en`

```erb
int XML_DOCUMENT xmlId, xmlContent
1 XML_RELEASE xmlId
int XML_EXIST xmlId
```

## `XML_REMOVEATTRIBUTE`

- Source (fact-check): `emuera.em.doc/docs/Reference/XML_REMOVEATTRIBUTE.en.md`
- Source language: `en`

```erb
1. int XML_REMOVEATTRIBUTE xmlId, xpath(, doSetAll)
2. int XML_REMOVEATTRIBUTE ref xml, xpath(, doSetAll)
3. int XML_REMOVEATTRIBUTE_BYNAME xmlName, xpath(, doSetAll)
```

## `XML_REMOVENODE`

- Source (fact-check): `emuera.em.doc/docs/Reference/XML_REMOVENODE.en.md`
- Source language: `en`

```erb
1. int XML_REMOVENODE xmlId, xpath(, doSetAll)
2. int XML_REMOVENODE ref xml, xpath(, doSetAll)
3. int XML_REMOVENODE_BYNAME xmlName, xpath(, doSetAll)
```

## `XML_REPLACE`

- Source (fact-check): `emuera.em.doc/docs/Reference/XML_REPLACE.en.md`
- Source language: `en`

```erb
1. int XML_REPLACE xmlId, newXml
2. int XML_REPLACE xmlId, xpath, newXml(, doSetAll)
3. int XML_REPLACE ref xml, xpath, newXml(, doSetAll)
4. int XML_REPLACE_BYNAME xmlName, xpath, newXml(, doSetAll)
```

## `XML_SET`

- Source (fact-check): `emuera.em.doc/docs/Reference/XML_SET.en.md`
- Source language: `en`

```erb
1. int XML_SET xmlId, xpath, value(, doSetAll, outputType)
2. int XML_SET ref xml, xpath, value(, doSetAll, outputType)
3. int XML_SET_BYNAME xmlName, xpath, value(, doSetAll, outputType)
```

## `XML_TOSTR`

- Source (fact-check): `emuera.em.doc/docs/Reference/XML_TOSTR.en.md`
- Source language: `en`

```erb
string XML_TOSTR xmlId
```

