# NEARS-4220 QA progress (checkpoint)
Backend: own server :8420 (php artisan serve --no-reload, DB_DATABASE=multi_food_db_qa4220), worktree @574e0a15e
- AC1 PASS: z2 has 12 (not 49); z364 has 49 (not 12/13/144): api-categories-z*.json
- AC2 PASS: z364 parent 9/6/102 present via child only; Juices(10) (child 62 empty) absent; childes pruned
- AC3 PASS: ac3-variants.txt (inactive item, unapproved item, inactive stores, stores out of zone, 1-of-3 control)
- AC4 PASS: module 2/3 never list module-1 ids; cache keys per module (ac4-cache-keys-clone.txt)
- AC5 PASS: ac5-consistency-loop.txt z2 27ids, z364 14ids, z1 28ids all total_size>0
- AC6 PASS: ac6-ttl-measurement.txt (stale to +57s, visible +61s), ac6-cache-writes.txt
- AC10 PASS live: ac10-failopen.txt
Clone restored (items 47541/56226/58386 status/approved=1; stores 3183/3762/3906 status=1 zone 364; cache rows cleared)
- AC7 PASS: rail==API in EN zone [2,412] (29), EN zone [364] (13), AR zone [364] (13), AR zone [2] (27); tile loops z2-ar 27/27, z364-en 13/13, none showed the empty state; strip Beverages z[2,412] = Juices/Soft Drinks/Seafood/Fresh Fish; Dairy z364 strip = All/Cheese (Milk pruned); detector positive control seen live
- AC8 PASS (observable outcome): z2 last/non-surviving category selected -> switched to saved 364 address -> first valid category, grid loads, no red screen; mounted-screen reconcile branch not drivable (tab rebuilds) -> unit tests
- AC9 PASS: phpunit 62 tests/561 assertions OK; flutter test test/features/category 175 passed
- regression_bug: setState during build on zone change (StoreFilterHub._resetSessions) bug-setstate-during-build-zone-switch.log
