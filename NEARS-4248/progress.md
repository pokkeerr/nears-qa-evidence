# NEARS-4248 QA progress (first pass, fix_cycle 0)
Backend: own `artisan serve --no-reload` :9317 from /Users/Apple/Projects/nears-NEARS-4248-cold-facet-build @ bd9b62d64 (freshness-check PASS), clone multi_food_db_qa4248, CACHE_DRIVER=database. Base copy (bef2ee630, git archive + copied vendor/.env/storage-app, file cache) :9318.
- AC1 PASS: popular 1005/1500 false+int; 1515 and 1575 and 1605 true+null (1575 = documented residual); cat9 1011 false+int; cat11 1582 true+null; [417,431]=600 false (base true). Zero-count pruned: min_rating, available_now absent at 1005/1500 (SQL avg_rating>=4 = 0).
- AC2 PASS (spot checks valid at load<2.5): pop1605 all 6 PASS (S 1.89); cat9 1011 all 6 PASS (S 2.5). cat11 1582 extra runs: NO VERDICT (S 11.3) / loaded end 3.3. Doc cells spot-checked against results files: match.
- AC3 PASS: unflagged 141 requests byte-identical vs base (only normalisation: own port in *_full_url); phpunit 822 tests, 3 failures = the 3 known base-red (also red on base copy).
- Flagged byte identity: 115 + 60 edge requests identical cold and warm at scope below old cap.
- Direct SQL parity: popular (8 selections), category grid 9 (7 selections incl. diet), category roll-up; hidden item 100 (status=0) in store 1 moved into zone 417 does not move any count; 13,608 other-zone items do not move counts.
- Crafted payloads ignored; cache rows hold no discounted/available_now.
- Logs: laravel.log clean for the window (0 production.* lines 20:38-20:52).
