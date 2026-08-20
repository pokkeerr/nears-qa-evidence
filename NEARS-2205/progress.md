# NEARS-2205 QA progress

- AC1: PASS — SELECT COUNT(*) ... rating_count > review_count = 0 (verified via mysql client)
- AC2: PASS — SELECT COUNT(*) ... rating IS NOT NULL = 60 (verified via mysql client); item 22 enumerated with expected values
- AC3: PASS — item 22 "Margherita Pizza" (Pizza Heaven, store 5) item-detail screen live-demoed on emulator-5556 (Dhaka zone/zone_id=1), shows 4.0 rating / (1) review, matches DB. Screenshot: ac3-item22-margherita-pizza-detail.png
- Regression sweep: Pizza Heaven store list (5 items, all rating_count=1) match DB exactly; Spice Route Kitchen/Grill House Pizza-category search (5 items) match DB exactly; Sushi World search shows reviewed items with correct rating badges AND reviewless item (Tuna Nigiri, rating_count=0) shows NO stale rating badge, clean.
- Automated backstop: vendor/bin/phpunit — 1421 tests, 13232 assertions, 1 error (pre-existing NEARS-2242 ZoneContainsSqlInjectionTest, unrelated), 1 deprecation, 1 skipped. No new failures.
- ui_errors: clean throughout (0 matches).
