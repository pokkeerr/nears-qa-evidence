# NEARS-2142 QA progress

- AC1 [ui]: FAIL — name-squeeze at 320dp/1.3x on item_that_you_love_view.dart (h<=8.2 LTR/4.2 RTL) and store_screen.dart grid (h<=12.2/8.2). Zero RenderFlex overflow LOG (that sub-clause passes) but visual match-to-frame fails hard (illegible text). frequently_bought_together_widget.dart unreachable (dead code, no call sites).
- AC2 [behav]: PASS — 100% scale/std width provably byte-identical to pre-fix code path; visually clean in screenshot.
- Regression: category_screen.dart pre-existing squeeze (h<=3.0) CONFIRMED live, non-blocking, filed regression_bugs. One unrelated animated_flip_counter overflow noted, not filed.
- Automated: item_widget_textscale_overflow_test.dart 28/28; other 4 item_widget_*.dart files 18/18.
- Evidence gallery: https://github.com/pokkeerr/nears-qa-evidence/tree/main/NEARS-2142
- QA comment posted: yes (Jira NEARS-2142)
- Device: emulator-5556, lock released, app left running.
