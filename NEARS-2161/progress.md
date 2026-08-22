# NEARS-2161 — LIVE QA evidence (Android, emulator-5558)

Device **emulator-5558** (1344x2992 @ 480dp, pool device — reclaimed from residue, no live
holder). Worktree `/Users/Apple/Projects/nears-NEARS-2161-getx-toast-a11y`, branch
`fix/NEARS-2161-getx-toast-bypass-liveregion`, base `feat/userapp-reskin2`. Package
`com.izzes.nears`, freshly built + installed by `flutter run -d emulator-5558 --debug` from this
worktree (confirmed via `Installing build/app/outputs/flutter-apk/app-debug.apk` in the run log).
Backend: primary tree `Admin/` (`php artisan serve :8000`), real local backend (`app_constants.dart`
`baseUrl` resolves `10.0.2.2:8000` for the Android emulator — not a demo/placeholder host).
Flutter 3.41.9 (`~/Tools/flutter`). Light mode only (dark deferred). All 5 ACs are
[behav]-tagged (a11y announcement mechanism + .tr string resolution) — no Stitch/DLS reference
was supplied, so NEARS-567's `[ui]` gate does not fire; **0 screenshots taken**, verification is
via the live Dart VM-Service semantics tree + app logs, per the ticket's own instrument
requirement ("VM-service `isLiveRegion` flag ... NOT uiautomator XML dump").

## Oracle

Live reads via `ext.flutter.debugDumpSemanticsTreeInTraversalOrder` (VM Service HTTP GET,
`http://127.0.0.1:<port>/<auth>/ext.flutter.debugDumpSemanticsTreeInTraversalOrder?isolateId=<id>`).
Semantics forced on by enabling a real `AccessibilityService`
(`com.android.systemui.accessibility.accessibilitymenu/.AccessibilityMenuService`, via
`adb shell settings put secure enabled_accessibility_services ...` +
`accessibility_enabled 1`) — leaves touch behaviour untouched, same technique as
`docs/qa-evidence/NEARS-1601/progress.md`. Flag of interest: `isLiveRegion` (renders literally as
`flags: isLiveRegion` in the dump), matching `SemanticsFlag.isLiveRegion` / `flagsCollection.isLiveRegion`
in the pinned widget tests.

Wallet screen reached via VM-Service `evaluate` (`Get.toNamed(RouteHelper.getWalletRoute(...))`,
scoped to a library that imports `route_helper.dart` so `Get`/`RouteHelper` resolve) — the exact
production code path the real payment-gateway webview redirect invokes (`getWalletRoute` builds
the same `?payment_status=&token=` query the redirect deep-link carries). This was necessary
because the "Wallet Balance" profile stat-tile is `clickable=false` in the current build (not a
tappable entry point on this screen today — noted as a **followups[] observation**, not a defect
of this ticket).

Chat PDF/generic-file arms reached by tapping the REAL attachment tile in a REAL conversation
(conversation 47, "Ahmed Khan / Vendor", message id 89) with a QA-only response-rewriting proxy
(stdlib `http.server`, port 8899, forwarding to the primary `:8000` backend, rewriting only the
one seeded `.webp` filename's extension to `.pdf`/`.zip` in the `message/details` JSON body —
zero DB writes) in front of it, `--dart-define=API_HOST=10.0.2.2:8899`. `FileTypeHelper.getFileType`
branches purely on the URL string suffix (confirmed by reading `file_type_helper.dart`), so this
reproduces the identical arm a real PDF/zip attachment would. `canLaunchUrl` forced to `false` (a
real, unmocked failure) by disabling the two apps that otherwise resolve `ACTION_VIEW` for those
URLs on this AVD — `com.android.chrome` AND `com.google.android.apps.docs` (Drive/PDF Viewer;
missed on the first pass, confirmed via `pm resolve-activity`), both re-enabled after. This is a
real `canLaunchUrl` → `false` outcome, not a bypassed/eval'd branch.

## AC1 — wallet fund-added / fund-not-added toast (`wallet_screen.dart`)

**fund-added** (`fundStatus=success`, fresh token):
```
SemanticsNode#286  flags: isLiveRegion
                   label: "تمت إضافة الصندوق إلى المحفظة بنجاح"
```
Exactly 1 occurrence of the label string in the whole dump, exactly 1 `isLiveRegion` flag anywhere
in the dump — single announcement, label == message exactly (no `"msg\nmsg"` doubling, the
NEARS-1601 defect class). Matches `ar.json` `fund_successfully_added_to_wallet` verbatim.

**fund-not-added** (`fundStatus=fail`, fresh token):
```
SemanticsNode#332  flags: isLiveRegion
                   label: "لم تتم إضافة الصندوق إلى المحفظة"
```
Same single-node/single-flag result. Matches `ar.json` `fund_not_added_to_wallet` verbatim.
Logs: `[ERR] msg="error snackbar shown"` fired for the FAIL case only (isError=true), none for the
SUCCESS case (isError=false) — exactly the `showCustomSnackBar` `isError && logError` contract.
**AC1 PASS.**

## AC2 — chat "Could not open PDF file" (`image_file_view_widget.dart` PDF branch)
```
SemanticsNode#507  flags: isLiveRegion
                   label: "لا يمكن فتح ملف PDF"
```
1 occurrence, 1 live-region node. Matches `ar.json` `could_not_open_pdf_file` verbatim. Logcat
stack trace confirms the exact call path: `AppLogger.error` ← `showCustomSnackBar` (`custom_snackbar.dart:30`)
← `_ImageFileViewWidgetState._openFile` (`image_file_view_widget.dart:31` — the PDF branch's
`showCustomSnackBar` call). `[ERR] msg="error snackbar shown"` paired, no silent failure.
**AC2 PASS.**

## AC3 — chat "Could not open file" (`image_file_view_widget.dart` generic branch)
```
SemanticsNode#550  flags: isLiveRegion
                   label: "لا يمكن فتح الملف"
```
1 occurrence, 1 live-region node. Matches `ar.json` `could_not_open_file` verbatim. Stack trace:
`_ImageFileViewWidgetState._openFile` (`image_file_view_widget.dart:51` — the generic/`other`
branch). `[ERR] msg="error snackbar shown"` paired. **AC3 PASS.**

## AC4 — both chat strings resolve via `.tr`, Arabic renders (not raw key, not English)

Explicitly demonstrated as a **live locale switch**, not just an observed default: navigated
Profile → Settings → Language, selected **English**, tapped Update (screen re-rendered in English:
"Settings"/"Language"/"Dark Mode" etc., confirmed live) — then switched back **English → Arabic**
via the same real `LanguageCardWidget` picker, tapped Update, confirmed the interface re-rendered
in Arabic. Re-triggered the PDF toast immediately after this explicit switch:
```
SemanticsNode#725  flags: isLiveRegion
                   label: "لا يمكن فتح ملف PDF"
```
Renders the correct Arabic copy (matches `ar.json`), not the raw key `could_not_open_pdf_file` and
not the old hardcoded English literal `"Could not open PDF file"` the pre-fix `Get.snackbar` call
carried. Combined with AC3's independently-observed Arabic string, both chat toasts are confirmed
`.tr`-resolved. **AC4 PASS.**

## AC5 — no `label:` on any Semantics touched by this ticket

```
git diff -- UserApp/lib/features/wallet/screens/wallet_screen.dart \
            UserApp/lib/features/chat/widgets/image_file_view_widget.dart \
            UserApp/lib/common/widgets/custom_snackbar.dart \
  | grep -n "^+" | grep -Fi "label:"
```
Zero matches. `custom_snackbar.dart` (the a11y choke-point both new call sites route through via
`getXSnackBar: true`) is **untouched by this diff** (pre-existing NEARS-1968 wiring, confirmed by
`git status` showing only `wallet_screen.dart` + `image_file_view_widget.dart` + language JSON +
new test files changed) and structurally carries no `label:` argument on its
`Semantics(container: true, liveRegion: true, ...)` wrapper (read at source, `showOverOverlay`).
**AC5 PASS.**

## Regression sweep

- **Wallet fund flow completes normally.** Deep-link-equivalent navigation
  (`Get.toNamed(RouteHelper.getWalletRoute(...))`, the same route a payment-gateway redirect
  builds) for both `success` and `fail` rendered the Wallet screen correctly — balance, transaction
  history list, filter — with only the toast's chrome differing (standard DLS `NToast` pill via the
  `getXSnackBar: true` GetX-overlay branch), matching the TL/UX-reviewed expected change.
- **NEARS-758 dedup intact.** Re-navigated with the SAME token (`qa-eval-tok-fail-1`) already
  persisted by the prior fail-toast show: polled the semantics tree for 6s (covers the 2s delay + 3s
  toast duration) — **zero** `isLiveRegion` node appeared, screen loaded cleanly (transaction list,
  no errors). Confirms both halves of the chain live: the fresh-token persist happened after the
  first show (or the replay could not have deduped), and the dedup guard suppresses a same-token
  replay.
- **Chat attachment flow otherwise unaffected.** With the fixture proxy passthrough (`.webp`),
  tapping the (still unlabelled) image tile opened `ImagePreviewWidget` normally (`Close`/`يغلق`
  button present, no toast, no errors) — the two edited branches are additive, the image/video arms
  are untouched.
- **Existing choke-point spot-check.** Coupon screen "Copy code" (`ينسخ`, an existing
  `showCustomSnackBar` call site unrelated to this ticket) still renders `"تم نسخ الكود!"` — the
  11+ other call sites are structurally unaffected (`custom_snackbar.dart` has zero diff).

## Logs — whole session

`ui_errors` (pid-scoped to the app process across the full session): **3 matches, all
`[ERR] msg="error snackbar shown"`** — exactly the 3 error-toast triggers fired (AC2 PDF, AC3 zip,
AC4 PDF-recheck), each the expected paired breadcrumb. **Zero `[FAIL]`, zero unhandled exceptions,
zero red screens** across wallet navigation (x4), the Language switch (x2), the chat conversation
open + 2 forced-failure taps + 1 normal image open, and the coupon copy spot-check.

## Automated backstop

Per the engineer/conductor: `flutter test test/features/wallet/wallet_fund_status_toast_a11y_test.dart
test/features/chat/image_file_view_toast_a11y_test.dart` — 5/5 pass, `flutter analyze` clean.
Not re-run (per spawn instructions); live device verification above is independent corroboration —
the exact `isLiveRegion` + label-equality instrument the widget tests use was reproduced live.

## Environment / cleanup notes

- **Gotcha (worth keeping for the guide):** on this AVD, disabling `com.android.chrome` alone is
  **not sufficient** to force `canLaunchUrl` false for a `.pdf` URL — `com.google.android.apps.docs`
  (Drive/PDF Viewer) independently resolves `ACTION_VIEW` for `.pdf`. Confirmed via
  `adb shell cmd package resolve-activity --brief -a android.intent.action.VIEW -d <url>` — the
  cheap way to check what will actually catch a forced-fail probe before trusting a "canLaunchUrl
  should return false" assumption. Both apps were re-enabled after this run.
- Proxy + the proxy-pointed `flutter run` were killed at teardown; the device was left on a
  **clean, non-proxied** `flutter run -d emulator-5558 --debug` (real `:8000` backend) for the next
  session, per "leave devices running, don't leave them broken."
- `qa_lock_acquire` reclaimed `emulator-5558` from a `residue` state (a leftover VendorApp process
  with no lane driving it) — noted, not a live-holder conflict.

## followups[] (non-blocking)

- The Profile screen's "Wallet Balance" stat tile is `clickable=false` in the current build — the
  screen-inventory doc (`userapp-screen-inventory.md` §4.6) describes it as a "tappable stat tile";
  live behaviour disagrees. Not this ticket's surface (untouched by the diff) — flagged as a
  regression-candidate for a separate ticket to confirm/fix, not filed as a bug here.
