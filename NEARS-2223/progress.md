# NEARS-2223 QA progress log

- AC1 (no/invalid nonce -> 401, no mutation): PASS. Live curl, isolated backend (port 8090,
  DB copy multi_food_db_qa_nears2223). No-nonce -> 401, store_business_model unchanged
  ('none' -> 'none'). Invalid/garbage nonce -> 401, unchanged. Confirmed via DB SELECT.
- AC2 (valid nonce grants once, replay rejected): PASS ONLY in a narrow non-default
  config variant (both business models enabled, no business_plan/package_id sent at
  register() time). FAILS under the real/default config (subscription_business_model=0)
  — the nonce is dead on arrival due to a pre-existing, unrelated cache:clear side
  effect on Store::save(). See bug-nonce-wiped-by-store-saved-observer.log.
- AC3 (exactly one structured log line, no PII): FAILS on the granted path — LOG_LEVEL=warning
  (real config, both worktree and primary .env) silently drops the Log::info() grant line.
  Denied path (Log::warning) is fine. See bug-log-info-level-swallowed.log.
- AC4 (rate limit, 6th request -> 429): PASS. Live curl, 5x 401 then 429 on the 6th.
- Cross-store scoping: code logic PROVEN correct via isolated tinker test (mint for
  store X, consume attempt with wrong store Y -> false, cache preserved; consume with
  correct store X -> true). Live HTTP cross-store test (stores 91115/91116) was
  CONFOUNDED by the same cache-wipe defect (a later registration wiped store A's nonce
  before the cross-store attempt), so the HTTP-level cross-store test result on its own
  is not trustworthy in isolation — the tinker-isolated proof stands in for it.
- TTL expiry: PASS. Forged well-signed nonce with past expiresAt (correct HMAC via
  config('app.key')) -> 401 live via curl.
- F1 regression (drive real UserApp registration -> business_plan): reproduced the
  headline defect LIVE end-to-end on emulator-5558 — register() 200, business_plan()
  401 (nonce already dead), UserApp then silently routes to the customer home screen
  with NO error dialog shown to the user. Screenshots: bug-nonce-wiped-choose-plan.png,
  bug-nonce-wiped-silent-401-home.png.
- Regression spot-check (authenticated-bearer branch, cancelSubscription, checkProductLimits):
  static diff confirms zero changes to those code paths; live check confirms their
  validators fire before authorizeStore is ever reached (403 on missing required
  params), consistent with pre-existing, unmodified behavior.
- Automated backstop: RegistrationNonceTest 9/9 green, SubscriptionStoreAuthTest 11/11
  green — both green BECAUSE phpunit.xml forces CACHE_DRIVER=array (not the shared
  'database' driver) and the tests never round-trip through register()'s real
  Store::save() chain, and the log test uses Log::spy() which bypasses real
  LOG_LEVEL filtering. Confirmed as a real environment/test gap, not a false alarm.
- UserApp flutter test: test/features/business/subscription_retry_route_test.dart
  15/15 pass, including the NEARS-2223-F1 (base64 "+" URL corruption) pinned tests —
  the CLIENT-side URL-encoding fix from fix-cycle-1 is correctly pinned and holds.
