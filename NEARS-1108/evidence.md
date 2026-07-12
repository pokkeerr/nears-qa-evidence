# NEARS-1108 — LIVE QA evidence (throttle bucket keying)

Verdict: **PASS** (all ACs demonstrated live, pre-fix/post-fix pair captured)

## Harness
| | |
|---|---|
| FIXED server | `:8111` ← worktree `nears-NEARS-1108-throttle` @ `1619fe95` |
| PRE-FIX server | `:8222` ← throwaway worktree @ `feat/human-review 7ad92889` |
| vendor/ | **copied (`cp -R`), NOT symlinked** — verified real dir, 91 entries, own `autoload.php` |
| Provider identity proof | `:8111` → `V1_BLANKET_THROTTLE = throttle:v1-blanket`, `V1_TOTAL = throttle:v1-total`; `:8222` → `throttle:300,1`, **no** V1_TOTAL. Each `ReflectionClass` resolved to its OWN tree's `RouteServiceProvider.php`. |
| Limiter state | `CACHE_DRIVER=database` → `php artisan cache:clear` + `SELECT COUNT(*) FROM cache` = **0 verified before EVERY run** |

Two harness facts, disclosed:
1. **OpenTelemetry disabled on BOTH servers** (`OTEL_SDK_DISABLED=true`) for the load phase. It adds **~1.1s to every request** (`ttfb=0.096s` vs `total=1.22s` — export blocks on `localhost:5080`, not running). That is **NEARS-1089**, pre-existing, unrelated to this ticket. With OTel on, 500 requests take >3 min and can never land inside the limiter's 60s decay window. Throttle behaviour verified **identical** with OTel on and off (newsletter: pre-fix 429@3 / fixed 429@6 both ways).
2. Both servers share the one host `cache` table, so every run is preceded by a cache clear.

## Group A — the 5 stacked sites (double-decrement)
Cap served in full post-fix; only half pre-fix.

| Route | Cap | PRE-FIX | FIXED | Result |
|---|---|---|---|---|
| `POST api/v1/configurations/store` | 5 | req1 `Remaining: 3` → **429 @ #3** | req1 `Remaining: 4` → **429 @ #6** | PASS |
| `POST api/v1/newsletter/subscribe` | 5 | req1 `Remaining: 3` → **429 @ #3** | req1 `Remaining: 4` → **429 @ #6** | PASS |
| `GET api/v1/search/trending` | 60 | req1 `Remaining: 58` → **429 @ #31** | req1 `Remaining: 59` → **429 @ #61** | PASS |
| `POST api/v1/customer/wallet/transfer-mart-from-drivemond` | 5 | req1 `Remaining: 3` → **429 @ #3** | req1 `Remaining: 4` → **429 @ #6** | PASS |
| `GET api/v1/get-combined-data` | 100 | req1 `Remaining: 98` → **429 @ #51** | req1 `Remaining: 99` → **429 @ #101** | PASS |

Every pre-fix/post-fix number matched the predicted value exactly.

## Group B — bucket collision (sites 6 & 7, NOT stacked)
Instrument = cross-route contamination from one IP (the double-decrement instrument would have falsely passed these).

| Scenario | PRE-FIX | FIXED | Result |
|---|---|---|---|
| 60× `GET /api/v1/module` → `POST /api/v2/ls-lib-update` | **429** `Limit:60 Remaining:0` (clean-bucket control: **200**) | **200** `Limit:60 Remaining:59` | PASS |
| 20× `GET /api/v1/module` → `POST /subscribeToTopic` | **429** `Limit:20 Remaining:0` (clean-bucket control: **302**) | **302** `Limit:20 Remaining:19` | PASS |

The clean-bucket control proves the pre-fix 429 came from *contamination by unrelated v1 traffic*, not the route's own budget.
Note: `subscribeToTopic` is a `web` route — CSRF (419) short-circuits **before** the throttle, so a bare POST never reaches the limiter. A real session cookie + `X-XSRF-TOKEN` was used to reach it.

## Group C — the combined v1 ceiling (the ~720/min hole)
500 v1 requests from one guest IP, mixed 250 `items/item-or-store-search` (blanket-detached) + 250 `module`, all inside the 60s window (sent in 32-33s).

| | PRE-FIX | FIXED |
|---|---|---|
| 501st `GET /api/v1/module` | **200 OK** `Limit:300 Remaining:49` | **429** `X-RateLimit-Limit: 500` `Remaining: 0` |
| 502nd `GET items/item-or-store-search` | **403** (not throttled) `Limit:360 Remaining:109` | **429** `X-RateLimit-Limit: 500` `Remaining: 0` |

Pre-fix: 500 requests served and still not throttled — the search surface (420) and the rest of v1 (300) are separate buckets. **Hole captured.** The `Remaining` values (49 = 300−251, 109 = 360−251) match the exact hit counts, so this is not a decay artifact.
Fixed: the ceiling binds at 501 on **both** a non-search and a search route.

## Group D — regressions that must not move

| Check | PRE-FIX | FIXED | Result |
|---|---|---|---|
| typeahead tier 360 (`items/item-or-store-search`) | 429 @ **#361** | 429 @ **#361** | PASS (unmoved) |
| `search-results` tier 210 (`search/global`) | 429 @ **#211** | 429 @ **#211** | PASS (unmoved) |
| 210 tier **shared** global+unified (105+105) | — | 211th → **429** `Limit:210` | PASS |
| backstop 420 (360 typeahead + 60 global) | 421st → **429** `Limit:420` | 421st → **429** `Limit:420` | PASS — `v1-total` (500) does **NOT** pre-empt the backstop |
| `v1-total` on search routes | — | `global` YES · `unified` YES · `items/item-or-store-search` YES (blanket detached on all 3, as designed) | PASS |
| 2 authed customers, ONE IP | A 429 @ #301 `Limit:300`; B 1st = **200** `Remaining:299` | A 429 @ #301 `Limit:300`; B 1st = **200** `Remaining:299` | PASS — independent counters preserved |

### D4 — LIVE on-device (UserApp, emulator-5560, guest, zone 2)
Built from the worktree with `--dart-define=API_HOST=10.0.2.2:8111` (no product-code edit) and pointed at the **fixed** backend; traffic confirmed arriving (limiter buckets populated on my server).

- Cold start from a **verified-empty** limiter → **7 v1 requests**, landing only in `v1-total` + `v1-blanket`. **No 429.** Critically, the small named buckets (`newsletter` 5, `config-update` 5, `wallet-handshake` 5) were **never touched** — pre-fix those same 7 cold-start calls would have gone into the single shared unnamed bucket and already blown the 5-caps.
- Global search, fast typing → debounce collapsed ~30 keystrokes into ~2-4 search calls; query `chicken` returned live results (Boneless Chicken, Chicken Burger, Chicken Tender Vegan, Chicken Wings).
- **No HTTP 429, no `nears_error_retry`, no `[FAIL]`/`[ERR]`** in the app log. All buckets peaked at 8 — orders of magnitude below the 500 ceiling.

## Automated backstop
`vendor/bin/phpunit --configuration phpunit.xml` → **Tests: 884, Assertions: 9902, OK** (no failures/errors; 1 deprecation, 3 PHPUnit deprecations). Matches the expected 884 (baseline 871 + this ticket's new tests).

## Screenshots
**0** — deliberate. No AC on this ticket carries the `[ui]` verify-tag (backend/API only), so per the NEARS-565/567 bounded-evidence model the visual channel is not opened. Evidence is the request → status → `X-RateLimit-*` → 429-index transcript above.
