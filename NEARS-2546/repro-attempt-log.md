# NEARS-2546 — Store Registration back-dialog reentrancy repro attempt log

Date: 2026-08-29
Worktree: /Users/Apple/Projects/nears-NEARS-2546-store-reg-back-dialog-reentrancy
Branch: fix/NEARS-2546-store-reg-back-dialog-reentrancy (0 commits ahead of feat/userapp-reskin2)
Backend: primary tree `php artisan serve --host=0.0.0.0 --port=8000` (already running, reused)
Devices: emulator-5556 (mobile arm, 1344x2992@480 default geometry), emulator-5560 (desktop arm,
`wm size 2400x1800` + `wm density 240` = 1600x1200dp, ResponsiveHelper.isDesktop == true)
App package (per-worktree suffix): com.izzes.nears.nears_nears_2546_store_reg_back_dialog_r

## Method
- Real touch/input only for every repro action: `adb shell input tap <x> <y>` (coordinates resolved
  live from a fresh `uiautomator dump` immediately before each action, never hardcoded across reps)
  and `adb shell input keyevent 4` (hardware/gesture back). NEVER a VM-Service/Dart-level Navigator
  call for the repro actions themselves.
- VM-Service `evaluate` (`Get.offAllNamed('/store-registration')`) was used ONLY to reset/navigate to
  a clean StoreRegistrationScreen between reps — the documented NEARS-2518 workaround for the
  currently-broken Profile -> Earnings -> Open Vendor front door (unrelated regression, not this
  ticket). No repro action (tap/back-press) was ever fired via VM-Service.
- `storeStatus` defaults to `0.1` on `initState` (`resetData()` + `storeStatusChange(0.1, isUpdate:
  false)`), so both `PopScope.onPopInvokedWithResult` and `NAppBar.onBack` hit the `else` branch and
  call `_showBackPressedDialogue` immediately on a fresh screen — no form-filling needed to reach the
  dialog.
- Logs scanned after every rep via `adb logcat -d -t 600 | grep -iE
  "_debugLocked|debug_locked|FlutterError|Assertion failed|Navigator.*lock|Exception caught by
  widgets|EXCEPTION CAUGHT"` — logcat buffer cleared (`logcat -b all -c`) immediately before each rep
  so a hit could only be attributed to that specific rep.

## Attempts (46 total, both responsive branches)

### Mobile arm — emulator-5556 (23 attempts)
| Variant | Entry | Reps | Gap | Result |
|---|---|---|---|---|
| 1 — double-tap Yes | NAppBar back | 5 | 150ms | clean |
| 1 — double-tap Yes | OS/gesture back | 3 | 100ms | clean |
| 2 — Yes then 2nd hardware back mid-transition | NAppBar back | 5 | 100ms | clean |
| 3 — rapid repeated OS back, no dialog interaction | OS/gesture back | 5 | 120ms | clean |
| 4 — cross NAppBar-back / OS-back against each other | mixed | 5 | 150ms | clean |

### Desktop arm — emulator-5560 (23 attempts)
| Variant | Entry | Reps | Gap | Result |
|---|---|---|---|---|
| 1 — double-tap Yes (exercises 2nd `Get.back()`) | NAppBar back | 5 | 150ms | clean |
| 1 — double-tap Yes | NAppBar back | 3 | 80ms | clean |
| 2 — Yes then 2nd hardware back mid-transition | NAppBar back | 5 | 100ms | clean |
| 3 — rapid repeated OS back, no dialog interaction | OS/gesture back | 5 | 120ms | clean |
| 4 — cross NAppBar-back / OS-back against each other | mixed | 5 | 150ms | clean |

No `!_debugLocked` / `FlutterError` / `Assertion failed` / Navigator-lock text appeared in any of the
46 attempts, on either responsive branch. Post-sweep `ui_errors` on both devices: 0 matches. Both apps
left in a healthy, non-crashed state (dialog dismissable, screen fully rendered) after the sweep.

## Side observation (not a repro of the ticket's assertion, noted for context only)
During the very first exploratory double-tap (150ms gap, before the disciplined loop script existed),
the second tap landed on the **already-transitioned MenuScreen tab** underneath (Dashboard
`pageIndex: 4`) at the same pixel coordinates as the Store-Registration Yes button, and coincidentally
hit the `join_as_a_delivery_man` Earnings-group row, navigating to `/delivery-man-registration`. This
is a same-coordinate double-tap landing a real second event on the NEW screen once the first
navigation had already fully resolved (well under 150ms) — not a Navigator re-entrancy assertion, no
error logged, no crash. It illustrates why the mobile branch's `Get.back()` + `Get.off()` pair
resolves fast enough that a 100-300ms human-speed double-tap cannot generally catch it mid-flight.
Not filed as a bug; mentioned only as evidence the transition genuinely completes well inside the
tested gap window rather than the app being unresponsive/hung.

## Evidence files
- `mobile-back-dialog.png` — back-confirmation dialog rendered normally on the mobile arm after the
  full sweep (emulator-5556).
- `desktop-back-dialog.png` — back-confirmation dialog rendered normally on the desktop arm after the
  full sweep (emulator-5560, `Submit`/single-page layout visible behind the dialog).
- This file (`repro-attempt-log.md`) — full per-variant attempt table and method.

## Verdict
**NOT REPRODUCIBLE** via real touch/gesture input, on either responsive branch, after 46 attempts
(well above the ~25-attempt good-faith bar) covering all 5 protocol variants. The previously-observed
`!_debugLocked` assertion (NEARS-2517 QA) required a synthetic VM-Service `Get.back()` fired
immediately after another state mutation — a same-tick/same-microtask collision that human-speed
touch input (frames ~16ms apart, taps 80-300ms apart) does not appear able to reproduce, since
`onYesPressed`'s `Get.back()` + `Get.back()`/`Get.off()` pair is a single synchronous handler that
locks and releases the Navigator well within one frame, long before a second real tap's gesture
recognition even begins.
