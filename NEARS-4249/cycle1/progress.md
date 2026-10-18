# NEARS-4249 delta re-QA (fix_cycle 1) on 4959bd1b0 - backend only, HTTP/JSON
Backend: /Users/Apple/Projects/nears-NEARS-4249-pack-size-popular-category @ 4959bd1b0 (port 8917, DB multi_food_db_qaF_nears4249, proven by cache-table growth clone 54->58, shared 899 unchanged)
Base: /Users/Apple/Projects/nears @ 4f9e8f570 (app code == 28ab7b118, git diff --stat empty over Admin/app,routes,config,database), port 8918, array cache
- D1 PASS popular flagged keys == base (no pack_size/diet); pack_size=500_ml&diet=veg ignored (applied [], ids equal unfiltered, total 200); omitted scope (cap 1 and total-1=199): same keys as base, 0 pack_size queries. Scope has 5 pairs (1kg,250g,6pcs,1l,500ml) and veg 0/1.
- D2 PASS category z2 pack_size offered 250_g:1 1_kg:2 6_pcs:1; pack_size=1_kg 43->2; cap 42 hides pack_size, 0 pack_size queries; chosen 1_kg stays selected:true count:null.
- D3 PASS unflagged popular/category byte-identical to base (normalised *_full_url); other lists identical.
- D4 PASS phpunit 115 tests / 1486 assertions OK.
