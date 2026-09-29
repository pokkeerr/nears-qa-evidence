# NEARS-3857 QA progress (phase [8], fix-cycle 0)

Build: debug UserApp from worktree `feat/NEARS-3857-userapp-logging-gaps` @ 9e3e34126, package `com.izzes.nears.nears_nears_3857_userapp_logging_gaps`, `--dart-define API_HOST=10.0.2.2:8157`.
Device: emulator-5586 (AVD NEARS_2414_QA, spare booted for this run). Backend: own `php artisan serve --no-reload` on :8157 from the worktree, `DB_DATABASE=nears3857_qa` (private copy of multi_food_db; the copy is proven by a flag flip that `/api/v1/config` reflected while shared id=228 stayed 0).
Account: customer@nears.com (user 6), zone 400 (Abu Dhabi).

| AC | Status | Proof | Evidence (see live-lines.log / ac-log-keys.log) |
|---|---|---|---|
| 1 site 1 skip | PASS | live + unit | flag OFF, fresh install, pick-map save: 1 x `[WARN] cart getCartDataOnline: fetch skipped reason=no_module config_loaded=true` (23:28:05). Control flag ON (copy), same caller after pm clear: cart/list fetched, 0 skip lines. |
| 1b splash (i) | PASS | live + unit | logged in, no cached module, cold start: `[INFO] splash: cart fetch skipped reason=no_cached_module`, 0 cart/list calls. |
| 1b splash (ii) | PASS | live + unit | logged in (remember-me), user-scoped cached module Pharmacy, cold start: cart/list at splash, 0 skip lines. |
| 1b splash (iii) | PASS | live + unit | pm clear (no token, no guest id), cold start: 0 skip lines, 0 cart/list calls. The same result on the first fresh install. |
| 2a initCall miss | PASS | live + widget | module null + cache null, cart row module 3, module 3 status=0 in copy: `[WARN] cart initCall: module match miss module_id=3 store_id=57 modules=3`; basket renders. |
| 2b prepareCheckout miss | PASS | live + unit | same cart, Proceed to Checkout: `[WARN] cart prepareCheckout: module match miss module_id=3 store_id=57 modules=3`; checkout still opens. |
| 3 module_mismatch | PASS | live (both) | Reorder 91401 (active pharmacy); Reorder OTC 91160 (active food). |
| 3 order_lines_fetch_failed | PASS | live (both) | airplane mode: Reorder 91404, Reorder OTC 91160. |
| 3 no_addable_lines | PASS | live (both) | Reorder 91117 (all lines have variations, active food); Reorder OTC 91160 (copy fixture: all lines Rx). |
| 3 no_order_id / no_store_id / no_order_lines | PASS (unit only) | unit | reorder_module_block_test.dart: all 3 tokens pass through BOTH reorder() and reorderOtc() (22/22 in file). |
| 4 nothing added | PASS | live + unit | store 58 active=0 in copy: `rejected=1 skipped=0 rx_skipped=0` before the unchanged toast. Flag ON 91160 Reorder Items: `rejected=2 skipped=0 rx_skipped=1`. |
| 5 cleanup timeout | PASS | live (VM-seeded) + unit | seeded `_abandonedInFlight` with a never-resolving id through the VM service, called the gate: `timed out leftover=1 polls=20`, returned false. Negative control: returned true, no WARN. Checkout-refusal adjacency proven by unit only (FIX-CYCLE-3). |
| 6 read-through | PASS | diff | `git diff 36beebbe2..HEAD -- UserApp/lib`: 0 new toasts, 0 new AppLogger.failure; only warn/info added. |
| AC-LOG | PASS | live | 16 observed lines, every key set equals its closed list, and values are ids, counts, bools or tokens only. |
