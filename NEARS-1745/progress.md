# NEARS-1745 QA progress (live, emulator-5566, worktree build 9d097a27)

Live-isolate symbol probe: the running isolate's OWN copy of
`manual_login_widget.dart` md5 `cc09bbc1ff5fd1c1be7dd4ea76d09943` == worktree
file at HEAD 9d097a27; base 74470e0a is `9f93ee352ae1b67860eb16c9189960d5`
(differs). `n_checkbox.dart` live md5 `6dbfc5a1817a7511218f4c953b87b63a` ==
worktree, and carries `throw FlutterError` at :97, not the old assert.

| item | result |
|---|---|
| AC4 TextButton -> tertiary | PASS. 0 `TextButton(`; base had 3. |
| AC5 Checkbox -> NCheckbox | PASS *under a corrected predicate* (see finding B1). |
| AC1/AC2 satisfied-elsewhere | PASS. cited paths exist; pin green (29 tests). |
| AC6 tap targets | PASS. remember-me 44.0dp, forgot 44.0dp, create 44.0dp. |
| Q10 navy colours | PASS. forgot+create ink #00FF99; remember-me label #FFFFFF. |
| Q7 label-words tap | PASS. false->true->false tapping the words; box also toggles. |
| Q1 RTL pixel-MSE | PASS. content-free mint-glyph mask A=0.0023 vs B=0.0747 (32.9x); centroid residual 1.0px vs 593.0px under the defect. |
| Q_ar1 Arabic ellipsis | PASS at 360dp. |
| Q9 en ellipsis @360dp | **FAIL** — "Forgot Passwo..." truncated in English. |
| Q11 keyboard-up overflow | PASS. no RenderFlex at 448dp or 360dp. |
