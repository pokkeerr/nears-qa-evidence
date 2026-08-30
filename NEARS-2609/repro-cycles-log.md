# NEARS-2609 — independent logout→guest-transition repro attempts (QA phase 8)

Device: emulator-5554, package `com.izzes.nears.nears_nears_2609_splash_guest_hang`, backend `http://127.0.0.1:8000` (worktree-local, primary Admin/ tree).

| # | Entry point | Timing variant | Result | Elapsed |
|---|---|---|---|---|
| 1 | ProfileScreen (top avatar → `profile_screen.dart`) `Logout` → `Yes` | normal tap | Resolved to guest Menu screen | <2s (first poll) |
| 2 | MenuScreen bottom-tab hero-exit door icon (`_confirmHeroSignOut`) → `Yes` → `Continue as Guest` | normal tap, reached via VM-service `Get.toNamed`/`_setPage` workaround (floating nav not a11y-addressable, documented gap) | Resolved to guest Home | <5s |
| 3 | ProfileScreen `Logout` → `Yes` | double-tap unrelated UI (1200,200) immediately after confirm | Resolved, "Logout Successful" toast visible | <2s |
| 4 | ProfileScreen `Logout` → `Yes` | normal tap | Resolved | <2s |
| 5 | ProfileScreen `Logout` → `Yes` | normal tap | Resolved | <2s |
| 6 | ProfileScreen `Logout` → `Yes` | 3s delay between confirm-open and `Yes` tap | Resolved | <2s |
| 7 | ProfileScreen `Logout` → 3x rapid tap on `Yes` (same coords, same second) | rapid multi-tap (re-entrancy stress, attempt 1) | Resolved; logs showed 3x concurrent `cm-firebase-token`+`auth/guest/request`, all 200 | <2s |
| 8 | ProfileScreen `Logout` → 5x rapid tap on `Yes` (same coords) | rapid multi-tap (re-entrancy stress, attempt 2) | Resolved; logs showed 4x concurrent `cm-firebase-token` POSTs, **4x HTTP 401**, each paired with `[FAIL]` AppLogger line + correlation_id + Crashlytics non-fatal print; self-recovered, final state clean guest Home | <2s (UI), ~300ms (network race window) |
| 9 | ProfileScreen `Logout` → `Yes` (pre-cold-restart guest-state setup) | normal tap | Resolved | <2s |

**AC1 verdict:** across 9 independent attempts spanning both documented UI entry points, normal timing, delayed timing, unrelated-UI stress, and rapid multi-tap stress on the confirm dialog itself — **zero hangs observed**. Every cycle resolved to the correct guest surface within single-digit seconds (bounded mostly by `uiautomator dump` overhead, not app latency). No `[FAIL]`/`[ERR]` in the app log for any of these except the deliberately-induced re-entrancy race (cycle 8), which is a **different, already-caught, self-recovering** failure mode (see `bug-logout-dialog-reentrancy.log`). This corroborates the engineer's non-repro conclusion.

**AC3 (cold restart) verdict:**
- Already-logged-in, force-stop + `am start`: reached Home in ~3s, session preserved (`Customer Nears` shown, not `Guest User`). Clean logs.
- Already-guest, force-stop + `am start`: reached Home by ~t+9-13s (dump-call overhead dominated; real resolution likely <9s), well inside normal cold-start budget, nowhere near the reported 60s+. Clean logs.

**Static-analysis corroboration (independently re-checked, not just taken on the engineer's word):**
- `grep -rln "SplashScreen(" UserApp/lib` → only `splash_screen.dart` (class def) and `route_helper.dart` line 577 (the cold-boot `/splash` route). No logout path constructs `SplashScreen` — confirmed unreachable from logout, matching the engineer's claim.
- `UserApp/lib/api/api_checker.dart` 401 auto-logout path already carries a `_isLoggingOut` single-flight guard (lines 49-56) that ignores concurrent/subsequent 401s during an in-flight force-logout navigation — consistent with the engineer's claim that NEARS-2553's `refreshCacheModuleForIdentity()` fix already closed the concurrent-guestLogin race for the ordinary case. Not live-tested with a genuinely expired token (needs one — same caveat the engineer already flagged); this QA pass corroborates it by code-read only, same limitation.

**Automated backstop (also re-run, not just trusted):** `flutter test test/features/profile/profile_screen_logout_spinner_hang_test.dart` — 1/1 passed ("logout from a live ProfileScreen transitions in-place to the guest view, not a permanent spinner"). Plus `menu_controller_pin_test.dart` (17/17), `chat_logout_reset_test.dart` (9/9), `clear_shared_data_logout_refresh_no_reinject_test.dart` (2/2) — all green, all pre-existing (zero diff in this ticket).
