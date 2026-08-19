# NEARS-2310 QA — BLOCKED (device pool exhausted)

## Verdict: BLOCKED — no available device/simulator to demonstrate AC1/AC2 live.

## What WAS demonstrated (device-independent)
- AC3 sibling-shape sweep: `grep -n "final List<String>" UserApp/lib --include='*.dart' | grep -i controller`
  confirmed the search_controller.dart eager-`.tr` field is the only true instance;
  all other `final List<String>` controller fields (order_controller, deliveryman_registration_controller,
  store_registration_controller, cross_store_search_controller, global_search_controller,
  item_controller._sortOptions, item_controller._filter) hold raw i18n KEYS with no eager `.tr` call —
  none replicate the trap. Re-confirmed unchanged from engineer/TL's prior finding.
- Automated backstop: `flutter test test/features/search/search_sort_labels_locale_switch_test.dart`
  -> 4/4 pass (V0 fixture-validity probe + W1 controller-getter locale-follow + W2 already-open-sheet
  reactive-flip). `flutter test test/features/search/` (full folder, 147 tests) -> all pass, no
  regression signal in the search feature area.

## What could NOT be demonstrated: AC1 [ui], AC2 [behav]
Both require a live device/simulator with the app booted and the search filter sheet driven by hand
(open sheet in EN, then switch locale live without closing it). Device acquisition was exhausted:

### Android pool (emulator-5554 / 5556 / 5558) — all 3 unavailable
- emulator-5554: `qa_lock_check` verdict=self-driven — 2 driver processes (flutter run + adb logcat)
  match this session's anchor but were NOT started by this QA lane; per the same-session caveat in
  the workflow profile, treated as occupied by a sibling lane, not claimed.
- emulator-5556: verdict=occupied — a foreign `flutter run` (pids 32172/32294) is driving it with no
  lock file (bare `flutter run` bypass, documented residual gap).
- emulator-5558: PHANTOM HOLD — lock held by a live session (pid 10132, key NEARS-2130) but the
  device is not currently attached (adb devices does not list it). Per protocol this lock is left in
  place (the holder may be mid-reboot/reattach); not cleared.
- Bounded queue-wait performed TWICE (~8 min + ~4 min, ~13 min total, exceeding the documented
  "poll ~60s up to 10 min" ceiling) — no device freed either time.

### iOS fallback attempted (UserApp fix is platform-agnostic Dart)
- Acquired lock on iPhone 17 Pro simulator (53F3807C-3BF6-46ED-8487-DEC957036BAA) via `--no-probe`
  (this guard's device probe is `adb devices`-only; it does not enumerate `simctl`).
- `flutter run -d 53F3807C...` failed at `pod install`: CocoaPods specs repo out of date
  (CDN `trunk`). Ran `pod repo update` (benign, non-code, no product-file change) and retried —
  second failure was a deeper FirebaseAnalytics pod version conflict, an environment/toolchain issue
  unrelated to this ticket's diff. Did not attempt further host-level pod/gem surgery (out of QA's
  read-only-on-infra remit; risks affecting other worktrees sharing the same CocoaPods cache).
- Released the iOS lock and shut the simulator down on abandoning that path.

## Conclusion
No FAIL — nothing was observed to be broken. No PASS — AC1/AC2 were never demonstrated live, which
is a hard gate ("couldn't run it" is FAIL/BLOCKED, never a PASS on green unit tests alone). Returning
BLOCKED{queue: ...}. Re-run QA once a device frees (or NEARS-2130's session finishes with
emulator-5558) — AC3 + automated backstop do not need to be re-run; only AC1/AC2 remain.
