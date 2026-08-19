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
