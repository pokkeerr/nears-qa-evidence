# NEARS-1372 — live QA progress log

Build provenance: UserApp debug APK built **from the worktree**
`/Users/Apple/Projects/nears-NEARS-1372-nbadge-token-unify/UserApp/build/app/outputs/flutter-apk/app-debug.apk`
(built 2026-08-03 01:55, after the lock was taken at 01:54). Branch
`feat/NEARS-1372-nbadge-token-unify`, HEAD `ceb65f9b` + the NBadge change present as
uncommitted worktree edits (`n_badge.dart`, `n_badge.catalog.yaml`, tests, 2 goldens).
`packages/nears_dls` is a path dep of that UserApp, so the token change is in the APK.

Devices: `emulator-5556` (UserApp product app), `emulator-5554` (reclaimed stale lock).
Backend: primary tree `Admin/`, `php artisan serve` :8000, `adb reverse tcp:80 tcp:8000`.

| AC | Result | Evidence |
|---|---|---|
| AC1 OPEN pill = #006D3E | PASS | `ac1-storecard-tile-open-pill.png` — NStoreCard tile, fill sampled `#006D3E`, `#1B9E57` = 0px |
| AC2 OPEN/CLOSED matched pair | PASS | `ac2-badge-gallery-open-closed-pair.png` — open 6.45:1, closed 6.46:1, identical pill geometry |
| AC3 contrast from a real screenshot | PASS | measured off the rendered PNG: `#FFFFFF` on `#006D3E` = **6.45:1** (AA needs 4.5:1) |
| AC4 Arabic / RTL | PARTIAL | `userapp-ar-rtl-store-pills.png` — NBadge status pill mirrors correctly in `ar`; success variant not reachable in-product |
| AC5 non-status + info unchanged | PASS | gallery census: navy/mint/error/successSurface/surface2 all at expected tokens, `#1B9E57` absent, info still `#F0EDEC` |

Blocker recorded: in UserApp the `status:success` store pill only renders in
`NewOnMartView` (food/shop/pharmacy module homes) via
`UserApp/lib/common/widgets/card_design/store_card.dart` -> `NStoreCard(tile).storeStatusLabel`.
That rail is filtered by `StoreController.availableStoresOnly()` (NEARS-481 AC2) to stores
the SERVER reports `open == 1`. At the QA hour (03:xx server time) the only open stores in
the DB are 24h grocery-module stores, and `GroceryHomeScreen` has no `NewOnMartView`.
So the OPEN pill was demonstrated on the same `NStoreCard`/`NBadge` widgets via the
`widgetbook/` DLS storybook built from this worktree, not via the Android product app.
