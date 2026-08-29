# NEARS-2546 — fix verification, delta re-QA cycle 1

Date: 2026-08-29
Worktree: /Users/Apple/Projects/nears-NEARS-2546-store-reg-back-dialog-reentrancy
HEAD: fb61c83ee (fix(NEARS-2546): guard store registration PopScope against re-entrant onPopInvokedWithResult)
Device: emulator-5554, per-ticket package com.izzes.nears.nears_nears_2546_store_reg_back_dialog_r
Backend: primary tree php artisan serve --port=8000 (reused)

## Fix under test
`store_registration_screen.dart`'s PopScope.onPopInvokedWithResult now has `if (didPop) return;` as its
first line (mirrors wallet_screen.dart NEARS-1526 exactly).

## Method
Exact repro that produced 6/6 crashes pre-fix: navigate to Store Registration pushed on top of an
existing route (Home, via Get.toNamed while a route is beneath — the real production navigation shape),
one real hardware-back-press (or app-bar-back tap), wait for the confirm dialog, one deliberate real tap
on "Yes". No rapid double-tap, no VM-Service/synthetic Navigator call for the repro action itself
(VM-Service evaluate used only for inter-rep navigation reset, exactly as in the original run).

## Results

### Desktop-width branch (ResponsiveHelper.isDesktop, wm density 160 + wm size 1600x1200) — 7/7 clean
| Rep | Entry | Result |
|---|---|---|
| 1 | OS/hardware back | clean — landed on Home |
| 2 | OS/hardware back | clean |
| 3 | OS/hardware back | clean |
| 4 | OS/hardware back | clean |
| 5 | OS/hardware back | clean |
| 6 | OS/hardware back | clean |
| 7 | NAppBar back (app-bar tap) | clean |

0/7 `!_debugLocked` occurrences (pre-fix: 6/6 crashed under this exact precondition).

### Mobile-width branch (default 1080x2400) — 3/3 clean (regression check)
| Rep | Entry | Result |
|---|---|---|
| 1 | OS/hardware back | clean — landed on Dashboard pageIndex:4 |
| 2 | OS/hardware back | clean |
| 3 | OS/hardware back | clean |

Unaffected by the fix, as expected (was already clean pre-fix).

### Guard-does-not-over-block check
The back-confirmation dialog legitimately appeared on **every one of the 10 real back-press/app-bar-tap
attempts above** (both branches) — `if (didPop) return;` only short-circuits the REENTRANT second
invocation (didPop=true, framework already popped), never the original first invocation (didPop=false,
canPop:false blocked it) that must show the dialog. Confirmed live, not just via the engineer's unit test.

## Verdict
**PASS.** The fix eliminates the `!_debugLocked` assertion on the exact precondition/branch that
reproduced it 6/6 pre-fix, does not regress the already-clean mobile branch, and does not over-block the
legitimate confirm-dialog UX.
