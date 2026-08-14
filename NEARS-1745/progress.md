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

## Final (all items closed)
| item | result |
|---|---|
| A.2 TalkBack plain row | PASS on toggle+node contract; utterance string not logged by this build |
| A.3 rich labelChild | name + separate focus stop PASS; link-vs-toggle clause UNVERIFIABLE (no interactive fixture in the repo) |
| A.4 focus ring | PASS on navy: #001F63 == mint @ 0.12 over #00005A |
| A.5 disabled | render PASS (label #98969B, box #7EFCC8); press-ripple not exercised |
| A.6 error contrast | light 6.17:1 PASS; **navy 2.48:1 FAIL** -> regression R2 |
| A.7 sizes | md 44.0dp live; sm/lg pinned by n_checkbox_test.dart:342 (green) |
| B.1 Reset\|Apply | PASS, both 199.0x52.0dp |
| B.2 press-scale | PASS, 395x43 -> 385x42 px, symmetric |
| Q12 isLoading colour | PASS #A8A8C4 (textOnNavyDim), not #9A9AA6 |
| Q13 AC7 | PASS (email 200, phone+picker 200, autodetect both ways, remember-me persists) |
| Q14 desktop arm | DEFERRED (>=1300dp unreachable on the pool) |
| automated | UserApp 3774p/2s/4f (all 4 pre-existing); DLS 1180/1180 |
| VERDICT | **FAIL** — task-bug B1 (EN ellipsis @360dp) breaks AC4 |

## Delta re-QA, fix-cycle 1 (HEAD ac0c1886) — BLOCKED on the device pool

Device-free work COMPLETE:
- Diff scope verified independently: only manual_login_widget.dart + its widget
  test changed 9d097a27..ac0c1886; packages/nears_dls untouched.
- Fix present in the tree: OverflowBar at :174, `Flexible(` count 0,
  committed blob md5 == on-disk md5 == cd6b5e5699890a21efda51e42f24a3c2.
- AC4 static: `TextButton(` = 0, positive control `NButton(` = 6.
- AC5 (carried) static re-check: bare `Checkbox(` = 0 under the discriminating
  predicate.
- Ticket widget test: 20/20 pass, incl. the stacking pin AND its positive
  control ("while the pair fits they stay on ONE line").
- APK rebuilt from the stable source (see the mid-edit note below).

MID-EDIT READ (real, recorded): a first read of the widget file returned the NEW
OverflowBar comment above the OLD `Row`+2x`Flexible` body (OverflowBar=0,
Flexible=2). The file mtime is 16:53:10 and my first APK build finished 16:53 —
the build may have snapshotted a half-written file. Three reads 2s apart now
agree on md5 cd6b5e56..., and the APK was rebuilt after that. Anyone building in
this shared worktree should re-verify the source md5 after the build, not before.

BLOCKED: all 5 Android emulators held; 9x60s poll found none free.
