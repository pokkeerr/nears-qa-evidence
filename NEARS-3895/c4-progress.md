# NEARS-3895 delta re-QA cycle 4 (final): build 985566c47
Fresh debug build `flutter run` from the worktree via `qa-run.sh --root <worktree> --dart-define API_HOST=10.0.2.2:8101`. Package: com.izzes.nears.nears_nears_3895_search_quickadd_guard. Device: emulator-5690 (AVD NEARS_2414_QA).
Backend: `/Users/Apple/Projects/nears-NEARS-3895-search-quickadd-guard @ 985566c47`, port :8100, pid 42950, DB_DATABASE=multi_food_db_qa_bug3895. All traffic went through the logging/fault proxy on :8101. The backend-freshness check PASSED.
Test user: james.wilson (id 1), zone 1. Flag 228 was '0' in both DBs.

Fixtures were re-created on the DB copy only:
- 990001 Zqx Rice and 990008 Zqx Rice Two (module 1, store 1)
- 990002 Zqx Pill and 990009 Zqx Pill Two (module 3, store 7)
- store_schedule for stores 1 and 7 opened 00:00-23:59:59 (backup: scratchpad/c4-backup_store_schedule.sql)

Timing: tap times are on the device clock. The proxy clock is the host clock, which runs about 24.6s ahead of the device.

Raw logs: c4-race-runs.log.

## Results

- **SMOKE / AC-1:** The pharmacy '+' tapped with a grocery basket opens the "Start a new basket?" dialog with zero cart calls. Tapping No sends zero calls. c4-smoke-reset-dialog.png
- **Control C1:** The same tap sequence answered No sends the old cart/add 990008 under module 1 about 500ms after the tap. This proves the old taps register.
- **S1 (old tap before Yes, debounce elapses inside the DELETE): 5 of 5 clean**
  - Runs: R1 add (delay 1.5s), R2 PATCH on saved row 1101 (delay 1.5s), R3 PATCH on row 1103 (natural speed), R4 add (natural speed), R5 add (delay 2.5s).
  - In every run: no old cart/add or cart/update after Yes, exactly one cart/add under module 3, no rowGone.
- **S2 (failure legs): 3 of 3 PASS**
  - Runs: F1 DELETE 500 with a PATCH, F2 DELETE 503 with an add, F3 DELETE 500 with no delay and a PATCH.
  - In every run: the held old sync was sent exactly once after the failure, under module 1. The basket was kept. Logs show `[FAIL] cross-module clear-cart failed` + `[ERR] error snackbar shown`. No add under the new module.
- **S3 (the cycle-3 FAIL shape: stepper '+' on a pending old row after Yes, during the DELETE): 4 of 4 clean**
  - Runs: D1 tap at 0.3s (delay 2.5s), D2 tap at 0.5s (delay 2.5s), D3 tap at 0.2s (natural), D5 tap at 0.4s (natural).
  - No cart/add for 990008 under any module. Exactly one add 990002 under module 3. The DB holds only the module 3/3 row.
  - Positive control S3-CTRL: identical timing with DELETE forced to 500 sent cart/add 990008 qty 2 once. That proves the post-Yes stepper tap registers.
  - Each following reset (DELETE moduleId=3) cleared correctly.
- **S4 (tap after a successful DELETE while the reloads are delayed past 500ms), pending row: 3 of 3 PASS**
  - Runs: A1 (cart/list and get-zone-id delayed 2.5s, tap at 1.2s), A2 (also home/all delayed, 4s, tap at 1.6s), and D4 (natural speed: tap 0.29s after the DELETE succeeded).
  - Each run logged `[WARN] pending add dropped: reason=module_mismatch phase=send item_id=990008 row_module_id=1 active_module_id=3` and sent no POST for 990008.
- **Residual B (stepper '+' on a SAVED old row during the DELETE): no longer reproduces.** RB-1 (0.4s) and RB-2 (0.6s), both with a 2.5s delay: no cart/update, no 404.
- **Residual B, post-success variant: reproduces 2 of 2.**
  - Shape (S4-B1, S4-B2): stepper '+' on a SAVED old row tapped 0.42-0.58s AFTER the DELETE succeeded, with the reloads delayed.
  - Result: POST cart/update for the deleted row id goes out under moduleId=3 and gets 404. The paired `[FAIL] rowGone` is logged. The row is dropped silently by design (NEARS-1991). The DB stays clean and no stray row is created.
  - Guard B covers ADDs only, so this PATCH is not covered.
  - Classified as known residual B (same mechanism and outcome as NEARS-3877 c23153; only the window moved). Not counted as a failure. Evidence: c4-residualB-postsuccess-savedrow-404.log
- **AC-2 / AC-7:** Every run sent exactly one cart/add under the new module. After a hot restart, cart/list moduleId=3 returned rows=[[1144,990002,3]] and the Basket shows only Zqx Pill. c4-ac7-basket-after-hot-restart-only-new-row.png
- **Audit across the whole run:**
  - 48 cart/add calls. None has a header module that differs from the item's module.
  - The DB has zero rows where the cart module differs from the item module (ids > 1097).
- **Sanity with the flag OFF (Guard B must not drop legitimate adds):**
  - Store-page '+' Zqx Pill Two (a non-search add) sent cart/add moduleId=3 (row 1145).
  - A same-module search '+' Zqx Rice Two right after a Yes switch (RESEED runs) sent cart/add moduleId=1 each time (rows 1104, 1111, 1134, 1137, 1140, 1143).
- **Logs:** No unexpected [ERR]/[FAIL] lines. These were present but are pre-existing and not caused by this change:
  - the RenderTable semantics assertion that fires on uiautomator dumps
  - the Firebase init/FCM failures at the hot restart
- **Backstop:** `flutter test test/features/cart test/features/global_search` passed 1066/1066. The 2 ticket test files outside those folders passed 6/6.
