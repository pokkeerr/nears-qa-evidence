# NEARS-1812 — QA live-gate progress log

Device `emulator-5554` (AVD `nears_qa_delivery`, 448x997dp @480dpi — pool geometry; booted
fresh because all four pool devices were held by foreign lanes).
Build: `com.izzes.nears` 3.8.0 debug from worktree
`/Users/Apple/Projects/nears-NEARS-1812-track-details-unwraps`, Flutter **3.41.9**.
Phase 1 install `firstInstallTime == lastUpdateTime == 2026-08-14 14:38:12` → not a stale APK.
Light mode only (dark deferred).

## Phase 1 — direct against the real backend (`baseUrl = http://10.0.2.2:8000`)

| # | Observation | Result |
|---|---|---|
| 1 | Login `customer@nears.com`, switch to the saved zone-2 address | ok |
| 2 | Order #158 (delivery, commission store 2 WITH address, no partner), sheet expanded | subtitle "Delivery Partner"; 5-step stepper; Trip Route + delivery address; 0 `[FAIL]`/`[ERR]` |
| 3 | Placed order **#91119** via normal checkout at store 4117 (NULL address) | created — and checkout offered **no take-away option** (see reachability note) |
| 4 | #91119 tracking expanded, held 75 s | renders; 22 `order/track` polls; **0 `[FAIL]`** — correct, the AC3 log is take-away-gated |
| 5 | `[FAIL]` channel positive control (device-only airplane mode, 40 s) | 4 genuine `[FAIL]` lines on the same endpoint ⇒ the zeros above are real, not a dead channel |
| 6 | Chat action, no-partner delivery order | `Chat`=0, `Call`=1 (control) ⇒ genuinely absent, not disabled-but-tappable |
| 7 | Terminal orders #166 (delivered) and #154 (parcel) | details render; track FAB correctly not offered |
| 8 | Arabic / RTL, #91119 expanded | mirrors correctly, no overflow, no crash |
| 9 | `flutter test test/features/order/` | **125/125, 0 `[E]`** |

## Reachability note — take-away cannot be produced by the client

`CheckoutController.initCheckoutData()` forces `_orderType = 'delivery'` on every entry
(NEARS-512 removed the picker); `setOrderType()` has **zero call sites** in `UserApp/lib/`
(positive control: its definition *is* found); the DB holds **60 delivery + 3 parcel and
zero take-away orders**. `_TripRouteSection` gates the store-address slot *and* the AC3 log
on `showsStoreAddress = takeAway && orderType != 'parcel'`.

## Phase 2 — documented pass-through proxy (nav guide §"observe a tracking state the seeded DB cannot produce", NEARS-1686 QA). No DB write.

Stdlib proxy on `:8099` → `127.0.0.1:8000`, rewriting **one field on one endpoint**
(`/api/v1/customer/order/track` → `order_type := 'take_away'`); app relaunched with
`--dart-define=API_HOST=10.0.2.2:8099`. Validated before use: `/api/v1/config` bodies
byte-identical through both paths (md5 `beb60fa5…`), track endpoint routes (401 unauth).

| # | Observation | Result |
|---|---|---|
| 10 | Baseline on #91119 in `passthrough` | "Delivery Partner", 0 `[FAIL]` |
| 11 | **Flip to `take_away` on the SAME screen, no re-navigation**, held 80 s | 13 proxy rewrites, 21 poll lines, and **exactly ONE** `[FAIL]` |
| 12 | The line | `[FAIL] endpoint=/api/v1/customer/order/track http_status=null type=ApiFailure msg="order-tracking: store address missing, rendered empty"` |
| 13 | Backend truth, from the proxy's own log | `store_id=4117 store_address=None` ⇒ **`store_data_formatting` substitutes nothing** |
| 14 | AC2 take-away label | subtitle renders **"Store"**; "Delivery Partner" gone; card title = store name |
| 15 | Chat gate, commission store + take-away | **Chat present** (Call = control) ⇒ commission → chat visible, live |
| 16 | Store-address slot with a NULL address | renders **empty** — no crash, no "null", no error widget |
| 17 | **Live negative control** — revert to `passthrough`, same screen | every observable reverts: store name 0, "Delivery Partner" 1, "Direction" 0, "Ready for handover" 0, "Delivery on the way" 1 |
| 18 | **Order #158 as take-away — a NEW order id whose store HAS an address** (9 rewrites) | address `123 Market Street, Downtown` renders verbatim; `[FAIL]` total **still 1** — no spurious log |
| 19 | Total `[FAIL]`/`[ERR]` for the whole phase-2 build | **1** (the single intended AC3 line) |
| 20 | PII sweep, 8 patterns, positive controls in the same command | all 0; controls `[FAIL]`=1, `[NET]`=194 |

## Group-tracking path (`_groupId != null`) — verified, not inferred

`order_tracking_screen.dart` returns `GroupTrackingView(...)` **before** the subtree that
builds `TrackDetailsViewWidget` (its only call site in the app), so `_TripRouteSection` —
and the AC3 log — is never built on the grouped path. The AC1 log site does run there, and
is deduped by the per-State `_loggedNullStore` bool. **No double-log is possible.**

## Device restored

Proxy stopped, app rebuilt and relaunched against the real backend; lock released.
