# NEARS-3515 QA progress checkpoint

Worktree: /Users/Apple/Projects/nears-NEARS-3515-toctou-state-integrity
Branch: feat/NEARS-3515-toctou-state-integrity
HEAD: 9af34e5bbdd02150456434ff98f1411cd1daa8af
Backend: php -S 127.0.0.1:8010 (own worktree), DB copy multi_food_db_qa_nears3515 (isolated clone of multi_food_db)

## AC1 (2933) input shape guards — PASS
- payment_token[]=x&payment_token[]=y -> 403 payment-auth (clean, no 500)
- callback[]=... array -> 403 payment-auth (clean, no 500)
- legit scalar bogus token -> 403 payment-auth (baseline, consistent)
- legit scalar VALID token (order 91230, minted via PaymentToken::mint) -> passes verify+order-state gate,
  fails later at unrelated "Payment not found" (missing payment_method param) - proves no false-positive rejection.

## AC2 (2945) payment-confirmation state gate — PASS
- payment-mobile GET on canceled order 91229 -> 403 order-state (log confirmed reason=order-state)
- payment-mobile GET on already-paid order 91226 -> 403 order-state
- walletPayment HTTP route blocked by a PRE-EXISTING (not this ticket) missing auth:api middleware bug
  -> verified gate logic directly via controller invocation with Auth::shouldUse('api') set (mirrors what
  Passport::actingAs does in the automated tests):
    - canceled order 91229 -> 403 order-002, no mutation
    - already-paid order 91226 -> 200 early-return, NO double debit (wallet_balance unchanged, no 2nd wallet_transactions row)
    - normal pending order 91230 -> 200 success, wallet debited exactly once (15.84 -> 1.82), order -> confirmed/paid/wallet
- order_place_confirm() helper: canceled -> null no-op; first confirm applies; REPLAY -> null no-op (confirmed_at timestamp unchanged)

## AC3 (2947) vendor withdraw TOCTOU — PASS
- Two concurrent request-withdraw calls (amount=250=full balance) for vendor_id=2:
  call1 200 success, call2 403 insufficient_balance. pending_withdraw += 250 exactly once. Only 1 withdraw_requests row.

## AC4 (2948) wallet adjustment lock — PASS
- Two concurrent make-wallet-adjustment calls: call1 200 applied, call2 201 "Already Adjusted".
  total_withdrawn incremented exactly once (+200), exactly one adjustment row.

## AC5 (2949) admin withdraw-status re-approval guard — PASS
- Vendor: approved withdraw id=3 via real browser click-through (eye icon -> Approve -> note -> Complete).
  Replayed POST (re-approve + deny-after-approve) via in-page fetch -> no mutation (transaction_note/approved/
  total_withdrawn/pending_withdraw/updated_at all unchanged after replay).
- DeliveryMan: same pattern, withdraw id=5, delivery_man_id=1. Approved once (total_withdrawn +50 once), replay
  re-approve + deny-after-approve -> no further mutation.

## AC6 (2954) CSRF GET->POST hardening — PASS
- All 10 routes confirmed POST-only via route:list; bare GET -> 405 for all 10 (curl-verified).
- Live browser click-through (3 of 10): language delete (Swal-equivalent Bootstrap modal confirm preserved,
  final action = POST, ar removed from business_settings.language), zone digital-payment toggle (SweetAlert2
  confirm preserved, POST captured via network listener, DB flipped), category priority reorder (plain
  form POST, no confirm needed - correct, matches original no-confirm trigger).
- Remaining 7 callers code-reviewed: all use nearsPostRoute()/$.ajax POST + CSRF header, existing Swal
  confirms preserved (order edit/update/cancel), no confirm was ever present for mail-send-test /
  add-delivery-man (correct - those were plain unconfirmed AJAX GETs before too).

## AC7 (2971) atomic is_paid flip — PASS
- Simulated the exact atomic conditional-update block (identical across Stripe/Paypal/Bkash/RazorPay/SslCommerz
  controllers) for Stripe-shaped and Paypal-shaped payment_requests rows against real pending orders (91111, 91112):
  call1 updated=1, hook fires once (order -> confirmed/paid). REPLAY call2 updated=0, hook does NOT fire again
  (confirmed_at timestamp stable). Code-reviewed Bkash/RazorPay/SslCommerz - byte-identical pattern.

## Regression sweep
- Orders list, categories, zone list, language settings, mail settings pages: load clean (200, no console JS errors).
- Advertisement list: loads 200, ONE console error = 404 on a missing STATIC asset
  (public/assets/admin/img/advertisement.png) - pre-existing, never in git history, unrelated to this diff.
  Flagged as regression_bugs (Low, non-blocking).
- walletPayment() route missing ->middleware('auth:api') - PRE-EXISTING bug (predates this diff), makes
  $request->user() resolve null for legitimately authenticated bearer-token callers -> every real wallet-payment
  HTTP call from a genuine customer 401s. Automated PHPUnit tests mask this because Passport::actingAs() calls
  Auth::shouldUse() which a raw bearer request through apiGuestCheck never does. Flagged regression_bugs (High).

## Automated backstop
- vendor/bin/phpunit --testsuite Unit,Feature (own worktree, own DB copy multi_food_db_test_nears_nears_3515_toctou_state_integrity)
- IN PROGRESS at checkpoint time.
