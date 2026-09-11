# NEARS-357 QA progress

Backend-only, no device. Backend booted from worktree `nears-NEARS-357-account-enum-password-reset` (`php artisan serve --host=127.0.0.1 --port=8357`), HEAD 5c5a1c6c6.

## AC1 — unregistered identifier -> 200 generic body (not 404)
- customer `/api/v1/auth/forgot-password` (phone +971500000999, unregistered): HTTP 200 `{"message":"If an account matching that identifier exists, an OTP has been sent."}` PASS
- DM `/api/v1/auth/delivery-man/forgot-password` (phone +971500000998, unregistered): HTTP 200 same body PASS
- vendor `/api/v1/auth/vendor/forgot-password` (email totally-not-registered-xyz@nowhere.test, unregistered): HTTP 200 same body PASS

## AC2 — registered identifier -> same 200 body
- customer (customer@nears.com): HTTP 200 same body PASS
- DM (+971565656656 / ali.hassan@demo.com): HTTP 200 same body PASS
- vendor (ahmed.khan@demo.com): HTTP 200 same body PASS

## AC3 — functional dispatch unchanged
- vendor: fresh password_resets row written (token 193809, created_at 2026-09-11 23:47:28) + mail dispatch attempted (logged [FAIL] password_reset.otp_dispatch, mail not configured in dev -- pre-existing dev-env limitation, not a regression). DB write + dispatch-attempt confirmed PASS
- customer/DM: firebase_otp_verification business_setting = 1 in this DB -> both short-circuit before DB write (pre-existing behavior, unchanged by this fix). Confirmed via business_settings read.
- Fix-cycle-1 throttle/dispatch-failure branches (unreachable live here because firebase_otp_verification=1 short-circuits before that code) -- confirmed via automated backstop: Nears357PasswordResetEnumerationTest, 8/8 green, explicitly flips firebase_otp_verification=0 inside the test transaction to exercise those branches.

## AC4 — no hardcoded "Email not found!" literal
- `grep -rn "Email not found!" Admin/app/Http/Controllers/Api/V1/` -> zero hits. PASS

## AC5 (regression) — NEARS-26 rate limiter still active
- 4th rapid POST to customer forgot-password with same identifier within window -> HTTP 429 "Too Many Requests". PASS (limiter not weakened)

## Automated backstop
- `vendor/bin/phpunit --filter Nears357PasswordResetEnumerationTest`: 8/8 PASS
- `vendor/bin/phpunit --filter "OtpSendThrottleTest|VendorResetOtpTest|MasterOtpAndResetBindingTest|CustomerResetOtpBruteForceTest"`: 18/18 PASS
- Full suite: running in background, pid 52830.
