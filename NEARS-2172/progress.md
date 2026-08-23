# NEARS-2172 QA progress

## Pre-flight (done)
- Diff reviewed: `UserApp/lib/features/store/domain/services/store_service.dart` (filterRestaurantLinkUrl, `useReactWebsite=false` branch) — module null now drops `module=` segment cleanly instead of force-unwrapping; `useReactWebsite=true` branch also patched but unreachable (flag hardcoded false), consistent with QA Test Scope note.
- Diff reviewed: `UserApp/lib/features/store/widgets/store_description_view_widget.dart` — both location-tap sites (desktop ~L240, mobile/IntrinsicHeight ~L308) changed `Get.find<ModuleController>().module!.moduleType!` -> `Get.find<ModuleController>().module?.moduleType`. Confirmed `ModuleController.getModuleConfig(String? moduleType)` (lib/features/splash/controllers/module_controller.dart:555) already accepts nullable moduleType and always returns a non-null `Module` with `newVariation` set to a bool — so the remaining `.newVariation!` downstream stays safe even when `module` is null. No further force-unwrap risk introduced.
- baseUrl confirmed pointed at local dev backend (10.0.2.2:8000 Android / 127.0.0.1:8000 iOS), not a demo server. Backend confirmed up: `curl 127.0.0.1:8000/api/v1/config` -> 200.
- Automated backstop independently re-run: `flutter test test/features/store/store_module_nullguard_test.dart` -> 7/7 PASSED (matches conductor's report).

## Device pool status
- Pool per profile: emulator-5554/5556/5558 (5560 documented broken bridge, excluded). Also physically attached: emulator-5564 (undocumented 4th device).
- `qa_lock_check` probed on ALL FOUR attached emulators (5554, 5556, 5558, 5564): all four report `verdict=occupied` with live foreign host drivers (flutter dartvm + adb logcat pids), i.e. genuinely in-use by other sessions right now, not stale/reclaimable locks (no lock dirs exist at all — bare `flutter run` sessions).
- Polled 4 rounds over ~4 minutes (16:21:29 -> 16:25:18 local); identical foreign pids each round (5554: 47197/47312, 5556: 99533/99663, 5558: 97315, 5564: 45263/45325) confirming stable live occupancy, not lock-check flicker.
- No device acquired; no lock written; nothing to release.

## Verdict: BLOCKED (device pool saturated)
Live AC1/AC2/AC3 device demonstrations NOT performed — every attached Android device is actively driven by another live session. Code review + independent automated-backstop re-run both clean, but per QA hard rules a FAIL/BLOCKED is required when the live demonstration cannot be run — "couldn't run it" is never a PASS on green tests alone.

## Retry (same commit 1fcd9d9c, conductor-2172 message)
- Independently ran `qa_lock_acquire emulator-5558 NEARS-2172` (disk precheck passed: 2.5GB free). FAILED — genuinely held by a live same-session-but-different-lane lock (holder_key=NEARS-2199, worktree WT:NEARS, pid alive). Did NOT override — not my lock to take.
- Rechecked emulator-5554 (occupied, new foreign pids), emulator-5556 (dropped from adb pool entirely), emulator-5564 (occupied, same foreign pids as before) — twice, ~90s apart, stable.
- Verdict unchanged: BLOCKED. No device acquired, nothing to release.
