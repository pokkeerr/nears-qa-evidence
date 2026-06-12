# NEARS-26 — SEC-E: otp-send rate limiter — LIVE QA VERDICT

**VERDICT: PASS** (7/7 AC met, regression clean, phpunit 205 green)

- **Build/env:** branch `feat/NEARS-26-rate-limit-otp-send` (in-tree, uncommitted), primary tree `/Users/Apple/Projects/nears`
- **Backend:** dedicated `php artisan serve` on `127.0.0.1:8011` serving the branch code (shared :8000 left untouched)
- **Cache:** `CACHE_DRIVER=database` (persistent across separate curl invocations — limiter state survives, 429 fires)
- **Limiter:** `RateLimiter::for('otp-send')` = 3 req / 10 min, keyed `ip|identifier` (email ?: phone ?: email_or_phone ?: ip)
- **Middleware confirmed on all 3 routes** (via router introspection): `...,throttle:auth,throttle:otp-send`

| AC | Result | Evidence |
|----|--------|----------|
| 1. otp-send fires (customer 4×, 4th=429+Retry-After) | PASS | ac1: req1-3 = 404 (non-429), req4 = 429 `Retry-After: 600`, `X-RateLimit-Limit: 3`, remaining 2→1→0 |
| 2. all three routes 429 on 4th | PASS | ac2: DM 4th=429 Retry-After:600; vendor 4th=429 Retry-After:599 |
| 3. empty-email isolation (fix-cycle-1) | PASS | ac3: phoneA exhausted (4th=429), phoneB (same blank email, same IP) = 404 remaining:2 — fresh bucket, key did NOT collapse on `ip\|''` |
| 4. login NOT throttled by otp-send | PASS | ac4: 4× same identifier login all 403, `X-RateLimit-Limit: 5` (auth limiter only), no 429 |
| 5. happy path intact (real seeded user) | PASS | ac5: real customer +971565811199 → HTTP 200 "Otp sent successfull", remaining:2 |
| 6. phpunit green | PASS | 205 tests / 4292 assertions green; OtpSendThrottleTest 6/6 incl. empty-email + login-exemption |
| 7. persistence across separate procs | PASS | ac7: 4 independent curl OS-procs → 4th=429; 2 otp-send buckets (~10min TTL) present in `cache` DB table |

**Regression sweep (clean):**
- v2 group still throttled: `POST /api/v2/ls-lib-update` → `X-RateLimit-Limit: 60` (throttle:60,1 intact)
- Normal customer login (customer@nears.com / field_type=email) → HTTP 200 + token

**Notes:**
- Throwaway phones return 404 "User not found" on req 1-3 — the limiter counts the hit regardless of user existence (expected; the cap is pre-controller middleware).
- `QUEUE_CONNECTION=sync` so OTP send runs inline; happy-path 200 confirms no queue:work needed for this AC.
- `route:list -v` has a pre-existing unrelated crash (`AnalyticsController` reflection) — NOT caused by this change; middleware verified via `app('router')->getRoutes()` instead.
