# Behringer X32 Show Files

These are files that I use to run sound on a Behringer X32.
Each show is in its own branch, so there isn't much in the master branch.

This program does several things:
1. It generates snippets (files named `*.snp`) for each scene, unmuting the appropriate mics.
1. It assigns mics to DCAs, scene by scene.
1. It manages the scribble strip for the DCAs, adjusting it for each scene.
1. It updates the show file (`*.shw`), inserting a cue for each scene. The cues reference the snippets.

## Instructions

1. Pick a name for your show, e.g., "theplay"
1. Using Behringer's X32 Edit, export the show and copy `theplay.shw` to the same directory as `X32Snippets.py`
1. Create an OpenOffice or LibreOffice spreadsheet file of your DCA assignments, e.g., `theplay_dca_assignments.ods`. I use Google Sheets and select File -> Download as -> OpenDocument format (*.ods).
1. Edit the constants near the top of `X32Snippets.py` as necessary to match your spreadsheet.
1. Generate snippets and cues by running `python X32Snippets.py SPREADSHEETFILE SHOWNAME`, e.g., `python X32Snippets.py theplay_dca_assignments.ods theplay`

Repeat the last step every time you edit the spreadsheet file. It will generate a full set of snippets and update the show file.

You can copy the show and snippet files to X32 Edit or to a thumb drive for loading into your Behringer X32 mixer.

## Author

Art Zemon <art@zemon.name>
https://cheerfulcurmudgeon.com

based on the original X32 Snippets by Simon Eves
