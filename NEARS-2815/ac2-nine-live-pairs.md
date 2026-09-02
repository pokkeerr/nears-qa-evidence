# AC2 — 9 live request/response pairs (manual/otp/social x merged/no_cart/rejected)

Server: `php artisan serve --port=8215`, private DB clone `multi_food_db_test_qa2815`
(cloned from the `multi_food_db_test` phpunit twin), GUEST_TOKEN_ENFORCEMENT=grace (default).

## manual_login (real HTTP POST /api/v1/auth/login, login_type=manual)
- merged  (guest_id=910000037, real cart + correct token): `cart_merged: true`
- no_cart (guest_id=910000038, correct token, no cart row): `cart_merged: null`
- rejected(guest_id=910000039, real cart, wrong token):     `cart_merged: false`

## otp_login (real HTTP POST /api/v1/auth/login, login_type=otp)
- merged  (guest_id=910000040, real cart + correct token): `cart_merged: true`
- no_cart (guest_id=910000041, correct token, no cart row): `cart_merged: null`
- rejected(guest_id=910000042, real cart, wrong token):     `cart_merged: false`

## social_login (direct method invocation via reflection -- social_login() cannot be
## reached over real HTTP without a live Google/Facebook OAuth handshake; this is the
## same technique the engineering test suite (CartMergedTriStateLoginResponseTest) uses
## for the identical reason. Still real application code execution, not a mock.)
- merged  (real cart + correct token): `cart_merged: true`
- no_cart (correct token, no cart row): `cart_merged: null`
- rejected(real cart, wrong token):     `cart_merged: false`

All 9/9 matched the expected tri-state. Full raw JSON bodies for manual/otp captured
live via curl during the QA session (see terminal transcript in the QA-evidence Jira
comment); social_login raw response bodies decoded via `json_decode($res->getContent())`
in the same tinker session, `cart_merged` key confirmed present in every response.
