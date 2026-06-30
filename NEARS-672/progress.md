# NEARS-672 QA progress — NewOnShimmerView RTL mirror — VERDICT: PASS

Device: emulator-5554 (locked, ANDROID_SERIAL pinned). Sibling NEARS-632 live on emulator-5556 — untouched.
Worktree: /Users/Apple/Projects/nears-NEARS-672-shimmer-rtl @ 2e506bda · branch feat/NEARS-672-shimmer-rtl
Build: fresh assembleDebug installed 02:11:28 (matches APK mtime) — running app IS the fix.
Backend: php on :8000 (shared, read-only).

## AC results
- [PASS] AC1 RTL mirror — widget test t3 (avatar left-edge rtl>ltr) green AND live: store-list
  NewOnShimmerView caught in RTL (Pharmacy module, AR) — avatar 65x65 + text indent on the
  RIGHT (start) edge, heart top-right. Evidence: ac1-newonshimmer-rtl-mirrored.png.
- [PASS] AC2 LTR unchanged — widget test t2 (builds w/o exception RTL+LTR) green; directional
  start resolves to left in LTR (same physical position; geometry confirmed by t3 ltr baseline).
- [PASS] AC3 analyze — flutter analyze lib/common/widgets/item_view.dart -> No issues found (0 new).
- Authoritative test: new_on_shimmer_rtl_test.dart 3/3 green (widget-test-output.log).

## Regression smoke
- LTR Pharmacy (non-food/grocery) module home: rails + store cards + categories loaded clean.
- RTL Pharmacy module home: rendered mirrored, no crash, rails loaded.
- Logs (ui_errors + run log): CLEAN all session — no exception/[FAIL]/[ERR]/overflow.

## Code trace
- Fix converts the 2 physical-LEFT offsets only: padding left:95->start:95 (line 157),
  Positioned left:15->PositionedDirectional start:15 (line 210). LTR identical, RTL mirrors.
- Remaining Positioned(right:15) heart = CONSISTENT with loaded card popular_store_view.dart:97-98
  (also physical right). Not a bug.

## SEPARATE FINDING (followup, NOT a NEARS-672 fail) — out of scope, pre-existing
- WebNewOnShimmerView (web_new_on_view_widget.dart:194 left:95 + :247-248 Positioned(top:60,left:15))
  is the SAME pre-fix RTL bug in a SIBLING widget. It is rendered ON MOBILE for the "new on <App>"
  horizontal rail shimmer via new_on_mart_view.dart:124. Live: avatar stays on physical LEFT in
  RTL (Arabic) while the location row auto-mirrors -> mixed/wrong layout.
  Evidence: followup-webnewonshimmer-rtl-avatar-left.png. Same one-line directional swap fixes it.
