# NEARS-2284 QA progress

- AC1 (automated backstop): PASS. `flutter test test/features/auth/deliveryman_registration_zone_sentinel_test.dart` -> 3/3 green (positive control + -1 sentinel + null sentinel). Static confirmation: NSelect.onChange (packages/nears_dls/lib/components/select/n_select.dart:340-345) always fires with `widget.items[index].value` from a tapped rendered item, and both call sites (delivery_man_registration_screen.dart:892, :1742) pass that value straight into setZoneIndex — so the -1/null path is confirmed unreachable from the live UI. Backstop-only per ticket note.
- Diff scope: `git diff 855cb3a6 e4668881 --stat` -> only deliveryman_registration_controller.dart (+3/-2) and its own new test file. store_registration_controller.dart untouched (empty diff) -> regression-sweep scope confirmation satisfied statically.
- Device pool status: emulator-5554 (Vendor+Delivery live, foreign), emulator-5556 (UserApp live, foreign), emulator-5558 (locked NEARS-2223, live anchor pid 10132) -- all 3 pool devices occupied by other live sessions at QA start (09:2x). Polled ~2min then ~7min (background) with qa_lock_acquire retries every 20-30s; see poll logs.

## Final result
- Device pool exhausted for the full poll window (~9 min total: ~2min initial + 6:40 background poll, `qa_lock_acquire` retried every 20-30s against emulator-5554/5556/5558). All 3 returned `verdict=occupied` (foreign live `flutter run` processes + active app procs) at every check, including the final one:
  - emulator-5554: host drivers pids 2047,2185,84234,84296 (foreign); device procs com.izzes.nearsvendor, com.izzes.nearsdelivery
  - emulator-5556: host drivers pids 77026,77135 (foreign); device procs com.izzes.nears
  - emulator-5558: locked by NEARS-2223, owner.json pid 10132 (anchor, live, `ps -p 10132` confirms alive)
- Never acquired a device lock -> nothing to release.
- AC2 (live zone-dropdown regression check) could not be demonstrated -> UNVERIFIABLE/BLOCKED, not a code defect. Static coverage in lieu: full `flutter test test/features/auth/` (280/280 green, includes deliveryman_registration_controller_test.dart AND store_registration_controller_test.dart in full) + `flutter analyze` clean on both the controller and the screen file + diff-scope confirmation (git diff 855cb3a6..e4668881 touches ONLY the controller + its own new test, valid-index code path is byte-identical to pre-fix — the guard only adds an early-return for -1/null, so behavior for valid indices cannot have changed).

## Fix-cycle 2 (delta re-QA, AC2 only)
- Confirmed emulator-5556 free (no `flutter_tools.snapshot run -d emulator-5556` process, no lock dir) -> `qa_lock_acquire emulator-5556 NEARS-2284` succeeded (anchor pid 5228, reclaimed nothing, disk 1285488KB free, well above 800MB floor).
- Backend up on :8000 (200 on `/api/v1/config`), UserApp `baseUrl` resolves to real local dev host (`10.0.2.2:8000`), not a demo/placeholder server.
- Booted UserApp on emulator-5556 (`scripts/qa-run.sh`), logged in as Customer Nears, home loaded clean (all `[NET]` calls 200, no `[FAIL]`/`[ERR]`).
- Navigated: sector-landing has no bottom-nav in the a11y tree (documented NEARS-520/587 gap) -> entered a module (`Grocery & Food`) first, then `ui_tap "Profile" --exact` resolved normally -> scrolled to EARNINGS card -> `Join as a Delivery Partner` -> filled General Info (name/phone/email/password+confirm, meeting all 5 password-strength checks incl. special char, profile image via SAF picker) -> `Next` -> landed on Additional Info tab, which is exactly where the AC's `delivery_man_registration_screen.dart:1742` zone dropdown (mobile arm) renders.
- Tapped `Select Zone` -> full zone list opened (Abu Dhabi Zone, 13 Baqala zones, Main Service Zone, Single Store QA Zone). Picked `Main Service Zone` (valid index >= 0):
  - logcat: `[NET] GET endpoint=/api/v1/module` -> `[NET] endpoint=/api/v1/module http_status=200` fired immediately (the pre-existing `getModules` call, gated by the new NEARS-2284 early-return guard which is a no-op here since index >= 0).
  - No `[FAIL]`/`[ERR]`/exception in the app log; `adb logcat -d -s AndroidRuntime:E flutter:E` empty (no fatal/red-screen).
  - `Select Zone` trigger label updated to `Main Service Zone` (single value, not duplicated).
- Repeated the pick a second time with a DIFFERENT valid zone (`Abu Dhabi Zone`) to rule out a stale/duplicated update on re-selection: a second clean `[NET] GET endpoint=/api/v1/module` -> `200` fired, and the trigger label updated to `Abu Dhabi Zone` only (no duplicate rows, no dropped update, no crash).
- **AC2: PASS, live-demonstrated on emulator-5556.** Screenshot: `docs/qa-evidence/NEARS-2284/ac2-zone-dropdown-populated.png` (Additional Info tab, zone = Abu Dhabi Zone, no error state).
- `qa_lock_release emulator-5556` on exit.
