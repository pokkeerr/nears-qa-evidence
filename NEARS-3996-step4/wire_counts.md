# Wire counts per action, base vs tip (scratch-backend access log via QA recording proxy; storage/zone/distance noise filtered; family = /stores/*, home/all, store-open requests; tip zone-switch and store-from-all-store rows are the isolated re-runs P05b/P09b)

| marker | base: family requests | tip: family requests | equal |
|---|---|---|---|
| P01-pharm-chip-Nearest | stores/get-stores/all?store_type=nearest&offset=1&limit=12 | stores/get-stores/all?store_type=nearest&offset=1&limit=12 | EQUAL |
| P01-pharm-chip-Popular | stores/get-stores/all?store_type=popular&offset=1&limit=12 | stores/get-stores/all?store_type=popular&offset=1&limit=12 | EQUAL |
| P01-pharm-chip-Newly | stores/get-stores/all?store_type=newly_joined&offset=1&limit=12 | stores/get-stores/all?store_type=newly_joined&offset=1&limit=12 | EQUAL |
| P01-pharm-chip-All | stores/get-stores/all?store_type=all&offset=1&limit=12 | stores/get-stores/all?store_type=all&offset=1&limit=12 | EQUAL |
| P01-pharm-open-now | 0 requests | 0 requests | EQUAL |
| P01-pharm-scroll-page2 | stores/get-stores/all?store_type=all&offset=2&limit=12 | stores/get-stores/all?store_type=all&offset=2&limit=12 | EQUAL |
| P01-pharm-open-store | stores/details/N<br>items/latest?store_id=N&category_id=0&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price=<br>items/recommended?store_id=N&offset=1&limit=50<br>categories/offers?limit=10&offset=1&store_id=N | stores/details/N<br>items/latest?store_id=N&category_id=0&offset=1&limit=13&type=all&filter=%5B%5D&rating_count=&min_price=&max_price=<br>items/recommended?store_id=N&offset=1&limit=50<br>categories/offers?limit=10&offset=1&store_id=N | EQUAL |
| P01-pharm-store-back | 0 requests | 0 requests | EQUAL |
| P02-grocery-enter | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12<br>stores/get-stores/all?store_type=all&offset=2&limit=12 | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12<br>stores/get-stores/all?store_type=all&offset=2&limit=12 | EQUAL |
| P02-grocery-chip-Nearest | stores/get-stores/all?store_type=nearest&offset=1&limit=12 | stores/get-stores/all?store_type=nearest&offset=1&limit=12 | EQUAL |
| P02-grocery-chip-Popular | stores/get-stores/all?store_type=popular&offset=1&limit=12 | stores/get-stores/all?store_type=popular&offset=1&limit=12 | EQUAL |
| P02-grocery-chip-Newly | stores/get-stores/all?store_type=newly_joined&offset=1&limit=12 | stores/get-stores/all?store_type=newly_joined&offset=1&limit=12 | EQUAL |
| P02-grocery-chip-All | stores/get-stores/all?store_type=all&offset=1&limit=12<br>stores/get-stores/all?store_type=all&offset=1&limit=12<br>stores/latest?type=all<br>stores/popular?type=all | stores/get-stores/all?store_type=all&offset=1&limit=12<br>stores/get-stores/all?store_type=all&offset=1&limit=12<br>stores/latest?type=all<br>stores/popular?type=all | EQUAL |
| P03-food-enter | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12 | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12 | EQUAL |
| P03-food-chip-Fastest | stores/get-stores/all?store_type=fastest&offset=1&limit=12 | stores/get-stores/all?store_type=fastest&offset=1&limit=12 | EQUAL |
| P03-food-chip-Nearest | stores/get-stores/all?store_type=nearest&offset=1&limit=12 | stores/get-stores/all?store_type=nearest&offset=1&limit=12 | EQUAL |
| P03-food-chip-Popular | stores/get-stores/all?store_type=popular&offset=1&limit=12 | stores/get-stores/all?store_type=popular&offset=1&limit=12 | EQUAL |
| P03-food-chip-Newly | stores/get-stores/all?store_type=newly_joined&offset=1&limit=12 | stores/get-stores/all?store_type=newly_joined&offset=1&limit=12 | EQUAL |
| P03-food-chip-All | stores/get-stores/all?store_type=all&offset=1&limit=12 | stores/get-stores/all?store_type=all&offset=1&limit=12 | EQUAL |
| P03-food-scroll-page2 | stores/get-stores/all?store_type=all&offset=2&limit=12 | stores/get-stores/all?store_type=all&offset=2&limit=12 | EQUAL |
| P03-food-cuisine-Chinese | 0 requests | 0 requests | EQUAL |
| P03-food-cuisine-Indian | 0 requests | 0 requests | EQUAL |
| P03-food-cuisine-reset | stores/get-stores/all?store_type=all&offset=1&limit=12<br>stores/latest?type=all<br>stores/popular?type=all | stores/get-stores/all?store_type=all&offset=1&limit=12<br>stores/latest?type=all<br>stores/popular?type=all | EQUAL |
| P04-shop-enter | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12 | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12 | EQUAL |
| P04-shop-popular-all | 0 requests | 0 requests | EQUAL |
| P04-shop-popular-refresh | stores/popular?type=all | stores/popular?type=all | EQUAL |
| P04-shop-popular-back | 0 requests | 0 requests | EQUAL |
| P04-shop-latest-all | 0 requests | 0 requests | EQUAL |
| P04-shop-latest-refresh | stores/latest?type=all | stores/latest?type=all | EQUAL |
| P04-shop-latest-back | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12 | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12 | EQUAL |
| P05-zone-switch-to-zone1 | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12 | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12 | EQUAL |
| P05-zone-switch-back-to-zone2 | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12<br>stores/get-stores/all?store_type=all&offset=1&limit=12<br>stores/latest?type=all<br>stores/popular?type=all | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12 | DIFF (base row also holds the Shop-home pull-to-refresh get-stores/latest/popular that landed before the next marker; the same 3 requests appear on tip in the v2 replay at 12:02:52) |
| P06-pharm-enter | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12<br>stores/get-stores/all?featured=1&offset=1&limit=50 | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12<br>stores/get-stores/all?featured=1&offset=1&limit=50 | EQUAL |
| P06-backend-down | 0 requests | 0 requests | EQUAL |
| P06-pharm-chip-Popular-while-down | stores/get-stores/all?store_type=popular&offset=1&limit=12 | stores/get-stores/all?store_type=popular&offset=1&limit=12 | EQUAL |
| P06-backend-restored | 0 requests | 0 requests | EQUAL |
| P06-pharm-retry | stores/get-stores/all?store_type=popular&offset=1&limit=12<br>stores/get-stores/all?store_type=popular&offset=1&limit=12<br>stores/latest?type=all<br>stores/popular?type=all | stores/get-stores/all?store_type=popular&offset=1&limit=12<br>stores/latest?type=all<br>stores/popular?type=all | DIFF (local-cache hit vs miss differed between the two full walks; isolated cold trials T2/T3 equal - see trials) |
| P07-shop-enter | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12 | home/all<br>stores/get-stores/all?store_type=all&offset=1&limit=12 | EQUAL |
| P07-backend-down | 0 requests | 0 requests | EQUAL |
| P07-popular-refresh-while-down | stores/popular?type=all | stores/popular?type=all | EQUAL (base run: backend still up on this first refresh, harness defect; second refresh was down on both) |
| P07-popular-refresh-while-down-2 | stores/popular?type=all | stores/popular?type=all | EQUAL |
| P07-backend-restored | 0 requests | 0 requests | EQUAL |
| P07-popular-refresh-after-restore | stores/popular?type=all | stores/popular?type=all | EQUAL |
| P08-reenter-popular-1 | 0 requests | 0 requests | EQUAL |
| P08-reenter-popular-2 | 0 requests | 0 requests | EQUAL |
| P08-reenter-latest | 0 requests | 0 requests | EQUAL |
| P09-store-back | 0 requests | 0 requests | EQUAL |
| P09-allstore-back | 0 requests | 0 requests | EQUAL |
