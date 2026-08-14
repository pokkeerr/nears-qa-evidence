# NEARS-1812 — QA live-gate progress log

Device `emulator-5554` (AVD `nears_qa_delivery`, 448x997dp @480dpi — pool geometry).
Build: `com.izzes.nears` 3.8.0 debug, built from worktree
`/Users/Apple/Projects/nears-NEARS-1812-track-details-unwraps`, SDK 3.41.9.
`firstInstallTime == lastUpdateTime == 2026-08-14 14:38:12` → not a stale APK.
Backend: primary tree `php artisan serve :8000`, app `baseUrl = http://10.0.2.2:8000`.
Light mode only (dark deferred).

| # | Observation | Result |
|---|---|---|
| 1 | Login `customer@nears.com`, switch to saved zone-2 address | ok |
| 2 | Order #158 (delivery, commission store 2 WITH address, no partner) — tracking sheet + Order Summary expanded | renders; subtitle "Delivery Partner"; stepper 5 steps; Trip Route + delivery address; 0 `[FAIL]`/`[ERR]` |
| 3 | Placed order #91119 via normal checkout at store 4117 (NULL address) | order created; **checkout is delivery-only — no take-away option exists** |
| 4 | Order #91119 tracking, Order Summary expanded, held 75 s | renders; 22 `order/track` poll lines (poll alive); **0 `[FAIL]`/`[ERR]`** — correct, the AC3 log is gated on take-away |
| 5 | `[FAIL]` channel positive control (airplane-mode 40 s) | 4 `[FAIL]` lines on the same endpoint → the earlier zero is a real observation, not a dead channel |
| 6 | Chat action on a no-partner delivery order | `Chat` nodes = 0, `Call` nodes = 1 (positive control) → genuinely absent, not disabled-but-tappable |
| 7 | Parcel #154 + delivered #166 (terminal) | details render; **no track FAB on terminal orders** → tracking screen not offered |
| 8 | Arabic / RTL, #91119 expanded | mirrors correctly, no overflow, no crash |
| 9 | PII sweep over the whole run log (8 patterns) + positive controls | all 0; `[FAIL]`=5, `[NET]`=427 |
| 10 | `flutter test test/features/order/` | **125/125 pass, 0 `[E]`** |

## Reachability blocker found

`order_type == 'take_away'` cannot occur:

- `CheckoutController.initCheckoutData()` forces `_orderType = 'delivery'` on every entry
  (NEARS-512 removed the delivery-type picker);
- `setOrderType()` has **zero call sites** in `UserApp/lib/` (positive control: the
  definition itself is found);
- the DB holds **60 delivery + 3 parcel orders and zero take-away orders**.

`_TripRouteSection` gates the store-address slot *and* the new AC3 log on
`showsStoreAddress = takeAway && orderType != 'parcel'`, and `_DriverCard` gates the
"Store" subtitle on the same `takeAway`. So AC3 and the AC2 take-away label are **not
live-demonstrable** — unit-pin only.
