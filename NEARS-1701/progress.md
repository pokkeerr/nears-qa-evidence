# NEARS-1701 — QA progress log (fix cycle 1)

Worktree `/Users/Apple/Projects/nears-NEARS-1701-chat-nullsafe`, branch `feat/NEARS-1701-chat-nullsafe`,
HEAD `df316c3c` (== base; change is UNCOMMITTED in the working tree).
Flutter `/Users/Apple/Tools/flutter/bin/flutter` 3.41.9 (verified). pubspec.lock meta 1.17.0 (clean).

## Device availability (measured 2026-08-10 ~05:05-05:15)
| serial | state | evidence |
|---|---|---|
| emulator-5554 | FREE but LOW DISK — 583,912 KB (~570MB) avail, 91% used, below the 800MB floor | `adb shell df /data` |
| emulator-5556 | HELD live by lane-mate NEARS-1686 (pid 86430 = MY OWN anchor -> guard reads self, exit 0) | owner.json |
| emulator-5558 | HELD live by foreign session NEARS-1626 (pid 40511 alive) | qa_lock_check exit 1 |
| emulator-5560 | HELD live by foreign session NEARS-1673 (pid 39147 alive); also outside the sanctioned pool | qa_lock_check exit 1 |
No lock acquired. No device state mutated.

## Verifications completed
- [x] Diff scope: exactly 2 product files + 1 new test file. No file outside the three named.
- [x] Fence (QA scope 7): last old-side hunk touches L273-274; `adminOrderMessage(` is L282. No hunk in L282-EOF.
- [x] Both compose-gate arms replaced (:432 and :1051) -> `_composeRowEnabled(...)`.
- [x] `flutter analyze lib/features/chat test/features/chat` -> "No issues found!"
- [x] `flutter test test/features/chat/chat_null_field_degrade_test.dart` -> 21/21, `00:01 +21: All tests passed!`
- [x] `flutter test test/features/chat` (all 8 files) -> `00:01 +117: All tests passed!`
- [x] `flutter test` (FULL suite) -> `01:28 +3248 ~2 -6: Some tests failed.` — 6 `[E]` over the COMPLETE
      17,506-line log, composition matched baseline exactly and named:
      coupon_controller_test x3, dls_golden_test x2, category_screen_back_button_test x1.
      **Zero chat failures** (instrument validated: the same pipeline returns 6 for "test/", so the 0 is real).
      No goldens regenerated; `git status` shows no `.png` touched.
- [x] Arm labels: `FooterView` is at L249 inside the FIRST arm, so the FIRST gate is DESKTOP and the
      SECOND is MOBILE — the ticket/solution-doc labels are BACKWARDS. Both arms are fixed either way.

## Per-AC dispositions (ALL TEST-VERIFIED, NONE LIVE-VERIFIED)
- AC1 T1/T1-desktop/T2/T2b/T2c — PASS. T2 is the preserved-behaviour case (status:false + messages -> composer hidden).
- AC2 T3/T4 (both arms) + T3b/T4b (spacer collapse) + T3-rtl + CONTROL — PASS.
- AC3 T5/T5b (the naive-`?.` trap) + T5-rtl + CONTROL — PASS.
- AC4 T6a/T6b/T6c (shape) + T7 (cardinality) + T8 (PII) + T9 (zero on happy path) — PASS.

## LIVE EVIDENCE: NONE. Why, measured not assumed.
All three sanctioned pool devices were held by LIVE sibling sessions for the whole bounded queue-wait
(7 x 60s polls): 5556 = NEARS-1686, 5558 = NEARS-1626, 5560 = NEARS-1673. The only free device,
emulator-5554, sat at 583,896-583,912 KB (~570MB) free / 91% used for the entire window — below the
800MB acquisition floor, and DECLINING rather than recovering. Per protocol I did not `mkdir` a lock,
did not fall through to `flutter run`, and mutated no device state.
=> The fault-proxy demo (a) and the live happy-path sweep (b) were both IMPOSSIBLE, not skipped.
