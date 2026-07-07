# NEARS-1023 QA progress — closed-store 403 pre-gate + typed extractor

Device: emulator-5556 (locked) · worktree `/Users/Apple/Projects/nears-NEARS-1023-closed-store-403` (uncommitted) · backend primary :8000 (Admin delta vs f19208a0 = EMPTY, verified) · user customer@nears.com (id 6) · light mode.

| AC | Verdict | Evidence |
|---|---|---|
| AC1 grid `+` quick-add, store 8 | PASS | Clean scripted flow: gate blocks, NO POST (logcat empty between tap and check, 2 items: Pretzels 13:37, Spinach 13:31), snackbar "Store is closed now", no cart row (no View Cart bar). Shots: ac1-*.png. Stepper fresh-add branch: UI-unreachable by design (`optimisticStep` index==-1 defensive path, "shouldn't happen from the stepper UI"); verified via ClosedStoreGate unit tests + identical code path. Stale-StoreController fail-open observed and root-caused → followup log (designed fail-open, AC3 mechanism covers it). |
| AC2 card tap → bottom sheet | PASS | NEARS-421 notice "Store closed · opens at ‪08:00‬ · advance ordering unavailable" + blocked "Store is closed" CTA + Dismiss; no POST, logs clean. ac2-bottomsheet-blocked-cta.png |
| AC3 mid-session flip → mapped 403 | PASS | Store 12 flipped active=0 via Store-panel "Temporarily Closed" toggle (restored after: status=1, active=1, schedule_order=0 verified + post-restore add 200). Stale pre-gate passed → POST 403 → snackbar "Store is closed now" (mapped, NOT generic), [FAIL] w/ correlation_id 464a9c64. BE-log grep: no backend line (guard responds w/o logging — pre-existing 463 design, followup). ac3-stale-403-mapped-message.png |
| AC4 open-store adds | PASS | Simple add 200 (Popcorn); variation (Rubiks 86) → sheet → add 200; OOS (61534, zone-1 store 2) → "Out of Stock" toast, no POST; rapid-tap ×4 → ONE cart/update POST → 200, qty 1→5 converged, single-notify (no toast spam); cross-store reset dialog both Yes (DELETE+add 200) and No (intact). ac4-*.png |
| AC5 CLOSED badge in rails | PASS | Store 8 card "CLOSED" in Recommended-For-You rail (EN) + "مغلق" (AR). ac5-*.png |
| Edge schedule_order=1 (store 9) | PASS | Quick-add NOT gated → POST → 200, cart row created. edge-schedule-store9-add-succeeds.png |
| Edge ar/RTL | PASS | "المتجر مغلق · يفتح في ‪08:00‬ · الطلب المسبق غير متاح" — localized, RTL layout mirrored, clock digits LTR-pinned (bidi wraps), no POST. edge-ar-quickadd-blocked-rtl.png |

Regression sweep: cart add→cart screen→quantity ± (update 200 both ways) · reorder (bool API, DELETE+add 200, dialog as before) · staples Buy-It-Again (dialog → No → intact) — all PASS, zero runtime errors (Dart MCP + ui_errors clean).
Automated: `flutter test` in worktree = 1974 passed, exit 0.
Store 4116 zone-1 rail presence: NOT surfaced (module-6 store; zone-1 rails only carry module 1/2/3) — best-effort, noted.
