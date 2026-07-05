# NEARS-524 Buy It Again — QA progress (fix_cycle 0, full scope)

Device: emulator-5554 (locked). Backend: worktree Admin @ :8000 (up). Build: UserApp from worktree.

## PRECONDITION (option-B gate) — FAILED as documented
- Live `GET /api/v1/module` (zoneId=[2]) → grocery module_id=1 `active_stores_count=15`, `single_store_id=None`.
- => For customer@nears.com on zone-2 grocery home, `singleStoreId` is NULL → rail correctly HIDES (multi-store option-B). Cannot demo populated AC1 there.
- Data-checker claim "store 35 is the only ACTIVE grocery store in zone 2" is WRONG (Store::active() scope = status=1 + commission/sub, ignores the `active` toggle; 15 qualify).
- Alternative single-store context search: the ONLY single-store module in the DB is zone 3 / grocery / store 59 (active_stores_count=1). Store 59 has ZERO delivered history for ANY user (incl. user 6). User 6 history stores = 1,8,9,35 all in multi-store zones.
- => NO reachable single-store context with user-6 (or any) purchase history. Populated-rail UI (AC1/AC2/AC4-populated) BLOCKED on Data DoR gap. Read-only: cannot seed.

## API-layer proof (backend booted from worktree)
- AC1 data: `GET /customer/order/buy-it-again?store_id=35` (Bearer customer@nears.com, zoneId=[2], moduleId=1) → total_size=3, products=[332 Low Fat Milk 1L, 96 Fresh Organic Tomato, 95 Broccoli] recency-desc. MATCHES expected [332,96,95]. All store_id=35, module_id=1, status=1. -> data correct.
- AC5 leak: user6 also purchased 52/58 (store 9 inactive), 145 (store 8 inactive), 99 Mango (store 1 zone1). NONE appear in store-35 response. -> leak-excluded at API. PASS(api).

## Live UI (demonstrated on emulator-5554)
- [DONE] logged-in customer@nears.com multi-store grocery home: NO rail + NO /buy-it-again call (home rails all fired, zero [ERR]/[FAIL]). shot 01.
- [DONE] guest (logged out) multi-store grocery home: NO rail + NO /buy-it-again call (home rails fired, no errors). shot 02.
- [BLOCKED] single-store positive gate (zone 3/store 59): zone 3 returns "service not available in your location" in-app -> unreachable. Cannot demo gate-open + fetch-fires live.
- [DONE regression] store-details forShop:true recommended rail: renders clean, no errors/overflow. shot 03.
- AC4 Arabic: string buy_it_again = "اشترِ مجدداً" present; shimmer+loaded both use 'buy_it_again'.tr (no title flip) — code/arb verified. Populated-RTL render BLOCKED (no populated rail reachable).
- App boot: CLEAN, no [ERR]/[FAIL] throughout the session.

## Automated backstop
- Flutter unit: test/features/item/buy_it_again_controller_test.dart -> 7/7 PASS (null-shimmer, populated, empty->[], failed-fetch->[], store-switch drop, CR-1 stale-race, clearBuyItAgain). Covers AC1/AC2/AC3 state logic unreachable in UI.
- Backend: phpunit --filter BuyItAgain -> 8/8 PASS, 36 assertions (2 non-blocking deprecations).

## VERDICT: BLOCKED
- Feature code correct + fully unit/phpunit-tested; backend live-proven; gating hidden-paths live-proven. No task_bug (no defect).
- AC1 populated rail UI / AC2 taps / AC4 populated-RTL NOT live-demonstrable = Data DoR gap (no reachable single-store-with-history context). Conductor must seed: give user 6 delivered history at a SERVICEABLE single-store zone (e.g. seed store 59 history AND make zone 3 serviceable, OR make a zone-1/2 grocery single-store), then re-QA the populated path.
