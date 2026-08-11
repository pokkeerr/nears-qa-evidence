# NEARS-1829 — QA progress log (live checkpoints)

Device `emulator-5556` · physical 1344x2992 @ 480dpi, **no override** → **448 x 997 dp** (target geometry).
Insets ROTATION_0: status bar 159px (53.0dp), nav bar 72px (24.0dp).
Worktree `/Users/Apple/Projects/nears-NEARS-1829-lightbox-overflow` @ `a589cf06`, tree clean.
Flutter 3.41.9 (`/Users/Apple/Tools/flutter`). `pubspec.lock` meta = 1.17.0 (unpolluted).
**Light mode only** (default theme; never toggled). Dark deferred for the reskin.

## Step 1a — test-channel positive control (free)
- base (post-fix): `attachment_viewer_dls_test.dart` → **31/31 pass**, incl. the NEARS-1829 pin.
- `git show 87080f8f^:…image_preview_widget.dart >` the file → pin goes **RED**:
  `Expected: null  Actual: FlutterError:<A RenderFlex overflowed by 20 pixels on the bottom.>`
- Predicted 20px from the test host's geometry (411x915, bottomInset 22) **before** running. Matched.
- → test instrument QUALIFIED (it can fail).

## Step 1b — live positive control, pre-fix build
- Predicted **22px** before measuring (997.33dp − 24dp nav = 973.33 constraint; 20+48+927.33 = 995.33).
- Live isolate source sha256 `65e46bfee01775b0` — `MainAxisSize.min` true, `SafeArea(` false → pre-fix RUNNING.
- Installed APK md5 `6f5b0e014871986694ca16ec840d9697`, lastUpdateTime 18:39:06.
- logcat cleared 18:48:52; tapped tile; captured at **18:48:55.388, pid 10933 (mine)**:
  `[FAIL] framework_error library=rendering library type=FlutterError msg="A RenderFlex overflowed by 22 pixels on the bottom."`
  `constraints: BoxConstraints(w=448.0, h=973.3)` · `mainAxisSize: min`
- **Channel A `ui_errors` QUALIFIED** (exit 0, scanned 1, 1 match). **Channel B flutter-run console QUALIFIED.**
- Pre-fix Close button rect `[1200,60][1344,204]` → top 60px (20dp) vs 159px status bar (NEARS-1874 defect visible).

## Step 2 — post-fix measurement
- File restored; `git status --porcelain` empty before build.
- Installed md5 `f076de01f2e3aa8b819a922ef4ee0c0e` (≠ pre-fix), lastUpdateTime 18:55:28, firstInstallTime 14:17:37.
- Live isolate sha256 `5cb6f6cb3e5483ce` — `MainAxisSize.max` true, `.min` false, `NEARS-1829: Expanded` true → post-fix RUNNING.
- **In-session liveness control on the SAME build/process/widget:** `wm size 1344x240` →
  `18:58:43.659 13132 [FAIL] framework_error … "A RenderFlex overflowed by 65 pixels on the bottom."`
  `constraints: BoxConstraints(w=448.0, h=3.0)` (20+48−3 = 65, exact).
- Geometry restored (`wm size reset`), lightbox closed + reopened at 448x997dp **in the same logcat buffer**:
  `ui_errors` exit **0**, scanned 1 of 1690 lines, **1 match = the 65px control only**. Zero at real geometry.
- Positive half from the live render tree: Column `constraints h=920.3` → `size Size(448.0, 920.3)`,
  `offset=Offset(0.0, 53.0)` inside the 973.3 viewer; children 20.0 + 48.0 + Stack `flex=1, fit=FlexFit.tight`
  at offset 68.0, pane `Size(428.0, 852.3)`. **`OVERFLOWING` markers in the whole render tree: 0.**

## Per-AC checkpoints
- **AC1 — zero RenderFlex overflow in the lightbox: PASS** (qualified channel, exit 0, scanned>0, 0 matches
  at real geometry, in a buffer that simultaneously carried a deliberate 65px overflow).
- **AC2a — Close fully visible + tappable: PASS.** Rect `[1200,219][1344,363]` → top 219px = **73.0dp** ≥ 53dp
  status bar; height 144px = 48dp. Tap at (1272, **225**) = 2dp INSIDE the top edge popped back to conversation 47.
- **AC2b — prev/next arrows: NOT TESTED, unreachable by construction.** `messages.id 75` `file` JSON has ONE
  element; gates `_currentIndex > 0` and `_currentIndex < length-1` are both false at index 0/length 1.
  Live render tree: the arrow Row has exactly one child — `SizedBox.shrink ← Expanded ← Spacer`; a11y tree has
  one clickable node (Close); zero `previous`/`next` semantics, zero arrow glyphs.
- **AC2c — page indicator: FAIL-as-written (mis-specified).** `grep` for indicator-ish tokens in
  `image_preview_widget.dart` returns **0 at HEAD and 0 at `87080f8f^`** — no page indicator has ever existed
  in this widget. False about the codebase independently of the diff.

## Third instrument — the banner itself, by pixel (qualified)
Flutter's hazard stripe = (191,191,0) alternating with black. First filter (`r>200`) returned 0 on the
PRE-FIX control too — **mis-calibrated, disqualified, discarded**. Recalibrated:
pre-fix **95,676** stripe px (POSITIVE) vs post-fix **0** and **0**. AC1's visual "banner" clause verified.

## Test gate (own tip a589cf06, clean tree)
`3570 passed, 2 skipped, 4 failed` — `coupon_controller_test` x3, `category_screen_back_button_test` x1.
Composition identical to the documented baseline. Extracted with `grep -E '\[E\]$'` over the complete
12,685-line log (never a tail). The brief's 3447-passed figure is simply older; failures unchanged at 4.
