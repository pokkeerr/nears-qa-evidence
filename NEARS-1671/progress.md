# NEARS-1671 — QA [8] live evidence

Device `emulator-5560` (woken first; uiautomator bridge HEALTHY — contradicts the profile's NEARS-1727
"broken bridge" exclusion). Disk 2816MB free. `emulator-5554` measured 587MB free = below the 800MB
floor, unusable (matches the brief). `emulator-5556` held by a LIVE `flutter attach` for NEARS-1719.
APK md5 `c613bf12342690679af32d27d309eb08` · Flutter `/Users/Apple/Tools/flutter` 3.41.9
Build: worktree `nears-NEARS-1671-errorretry-inflight`, branch `feat/NEARS-1671-errorretry-inflight`
Backend `127.0.0.1:8000` behind a purpose-built QA fault proxy on `10.0.2.2:8671`
(`--dart-define=API_HOST`), giving regex path rules + per-endpoint DELAY + a per-request wire log.

## Method notes that changed the verdict
- **Build freshness proven behaviourally, not by md5:** every app request arrives at the proxy port,
  which only this build's dart-define produces. md5 was the pre-filter only.
- **Discriminator (essential).** "Retry label absent" ALONE cannot tell a latched CTA from an error
  card that was swapped out for a shimmer. Every latch claim below is qualified by the error-card
  title still being mounted (`Retry=0 AND Title=1`). Two sites that first looked latched
  (staples, category grid) are in fact shimmer swaps.
- **Timing labels must be measured.** Each `ui_list` costs 1.5-3.5s, so nominal `sleep`-based
  t-labels ran far ahead of wall clock and produced one false "released early" reading on wallet.
  All timings below come from measured elapsed timestamps.
- Device clock is 31s BEHIND the host; proxy ts (UTC) vs logcat (device local) reconciled by measurement.
- **Theme: the app was in DARK for the first pass.** All functional results are theme-independent
  (request counts, latch timing, a11y labels). The visual checks were REDONE in light and only the
  light measurements are reported as the gate.

## AC1 — double-tap fires onRetry exactly once
| Site | Kind | Predicted | Measured (wire / app-side) |
|---|---|---|---|
| wallet_screen `_retryLoad` | converted, 3 reqs | 3, never 6 | **3 / 3** |
| loyalty_screen `_reload` | converted, 2 reqs | 2, never 4 | **2** |
| update_profile `_retryLoad` | converted, 1 req | 1, never 2 | **1** |
| item_bottom_sheet `_loadDetails` | converted, 1 req | 1, never 2 | **1** |
| wallet_history_widget | INHERITED, zero code edit | 1, never 2 | **1 / 1** |

## AC2 — busy affordance for the duration, normal after (all discriminated)
| Site | Slowest leg | Busy held | Released |
|---|---|---|---|
| wallet `_retryLoad` | 15s | Retry=0,Title=1 at t=2.2/6.2/9.7/13.0s | between 13.0s and 17.5s -> **the SLOWEST, not the first** |
| loyalty `_reload` | 12s | Retry=0,Title=1 at t=3.7/7.3/11.6s | between 11.6s and 15.5s |
| update_profile | 10s | Retry=0,Title=1 at t=2.6/6.4/11.2s | between 11.2s and 15.9s |
| item_bottom_sheet | 6s | Retry=0, `Server error`=1, `Dismiss`=1 at t=2s | back at t=9s |
| RTL Arabic (update_profile) | 9s | RetryAR=0, TitleAR=1 at t=3.9/7.4s | back at t=11.9s |

Wallet's 3 legs landed staggered on the wire (info 09:49:39.5, bonuses 09:49:40.0,
transactions 09:49:53.5) and the CTA stayed busy across the two fast landings — this is the
"slowest, not first" proof.

## Dead-CTA regression (highest-value check) — retry, let it FAIL, retry again
| Site | 2nd attempt |
|---|---|
| wallet `_retryLoad` | +3 requests, CTA alive |
| loyalty | +2 |
| update_profile | +1 |
| wallet_history (inherited) | +1 |
| staples (inherited) | +1 |
No site was left inert or spinning. Recovery path: faults cleared, one tap -> wallet content renders,
no stuck busy state.

## The view_item harm (the concrete damage motivating the ticket)
Error state via items/details 500, then the retry made to SUCCEED but slowly (pass-through + 5s delay)
so a base build would double-fire. Double-tap ->
- wire requests to `/api/v1/items/details/` = **1**
- `view_item` analytics events = **1**:
  `view_item {item_id: 145, item_category: 9, price: 12.43, value: 12.43}` (IDs only, PII-safe)
Native Firebase Analytics is DISABLED in this worktree ("Missing google_app_id" — the gitignored
google-services.json does not follow a worktree), so DebugView/FA-SVC was unavailable. Counted from the
in-app AnalyticsService debug mirror (`_mirror` -> debugPrint -> logcat), which is the app-side emission
itself. Stated, not faked.

## Unlatched void sites — must NOT spin (confirmed unchanged)
- **category grid** (`retryLastGridLoad`, `void`): during the retry `Retry=0 AND Title=0` -> the whole
  error card is replaced by the grid shimmer, i.e. the pre-1671 self-guarding behaviour, NO CTA spinner.
- **staples** behaves the same way (shimmer swap), so it is NOT a latch demonstration despite its
  request counts looking identical.
- `global_search c.retry` and `chat _retryThread` are block-bodied `void` -> cannot latch. Code-verified,
  NOT live-demonstrated (same class as the category grid, which was demonstrated).

## Visual (light mode only; dark deferred) — measured, not eyeballed
Density 420 => 48dp = 126px.
| Shot | Pill bbox | Height | Interior fill | Glyph |
|---|---|---|---|---|
| busy, light, Arabic RTL | (54,1389)-(1026,1514) | 126px = **48.0dp** | **(0,255,153)** pure mint, 99.4% | spinner 253px |
| idle, light, Arabic RTL | (54,1389)-(1026,1514) | 126px = 48.0dp | (0,255,153), 98.4% | label 740px |
| busy, light, English LTR | (54,1384)-(1026,1509) | 126px = **48.0dp** | **(0,255,153)** pure mint, 99.4% | spinner 224px |
| idle, light, English LTR | (54,1384)-(1026,1509) | 126px = 48.0dp | (0,255,153), 98.8% | label 616px |
Pill bbox is IDENTICAL busy vs idle in both directions: the mint pill holds its exact shape and the fill
is the pure mint token with no transparency (the `disabledBackgroundColor` fix works). The navy spinner
sits inside the pill; its centroid offset is the indeterminate arc's sweep phase, not mis-centring.

## NEmptyState no-regression
- Default (`isActionBusy:false`) pill renders identically to the busy pill's geometry (rows above).
- Independent consumers unchanged: wallet "No transactions yet / Your wallet transactions will appear
  here.", search "No data found".

## Logs (per-AC, scoped)
Every injected failure produced a paired `[FAIL]` line with the endpoint + status, e.g.
`[FAIL] endpoint=/api/v1/customer/info http_status=500 type=ApiFailure msg="api request failed"` and
`[FAIL] endpoint=/api/v1/customer/info http_status=null type=ApiFailure msg="profile load failed"`.
No unexpected `[ERR]`, no unhandled exceptions, no RenderFlex overflow during any AC.

## Not demonstrated (stated, not inferred)
- **module_view `getModules`** (Future<bool>): its error branch is gated on `!hasModules`, and the
  cached module list always wins, so the state is unreachable without clearing app data (which would
  wipe the login this run depended on). NOT demonstrated. `Future<bool>` is a subtype of `Future<void>`,
  so it should latch, but that is reasoning, not an observation.
- Notification list, flash-sale details, html viewer, store reviews, favourites, coupons, cross-store
  and global search, refer-and-earn, splash config retry, chat thread: not individually exercised.
  Coupon's error state was unreachable (list already cached from startup).
  Two inherited sites WERE exercised (wallet_history, staples).

## Unrelated (regression candidate, NOT caused by this change)
Basket fires `GET /api/v1/stores/details/2` TWICE and both return 403, with NO paired `[FAIL]` line —
only `[NET] ... http_status=403`. Duplicate request + a 403 + a silent failure path. See
`bug-storedetails-403.log`. Not an NErrorRetry surface; does not affect this verdict.

## Automated backstop
`packages/nears_dls` full suite on the pinned 3.41.9: **+1102, All tests passed** (goldens NOT regenerated).
