# X32 File Formats

## .shw File

```
#2.6#
show "Nuncrackers" 0 0 0 15 0 0 0 0 0 0 "X32-Edit 3.00"
cue/000 100 "cue list: overtu" 0 -1 9 0 1 0 0
cue/001 110 "cue list: top of" 1 -1 10 0 1 0 0
cue/002 200 "cue list: Virgil" 0 -1 11 0 1 0 0
scene/000 "power on" "" %000000000 1
snippet/000 "" 0 0 0 0 1
snippet/001 "" 0 0 0 0 1
snippet/002 "" 0 0 0 0 1
snippet/003 "" 0 0 0 0 1
snippet/004 "" 0 0 0 0 1
snippet/005 "" 0 0 0 0 1
snippet/006 "" 0 0 0 0 1
snippet/007 "" 0 0 0 0 1
snippet/008 "" 0 0 0 0 1
snippet/009 "Overture" 0 0 0 0 1
snippet/010 "Top Of Show" 0 0 0 0 1
snippet/011 "Virgil She's bac" 0 0 0 0 1
snippet/012 "Stage Mgr enters" 0 0 0 0 1
snippet/013 "The kids exit" 0 0 0 0 1
```

### cue line

`cue` lines appear immediately after the `show` line.

* cue/NNN - NNN = sequential number starting with 000
* ABC - cue number, displayed within X32 as A.B.C. B and C are restricted to single digits.
* Cue List a/k/a name - maximum 16 characters
* Skip - 1 = skip cue. 0 = do not skip cue
* Scene - Scene number or -1 for no scene
* Snippet - Snippet number or -1 for no snippet
* 0 1 0 0 - _unknown_