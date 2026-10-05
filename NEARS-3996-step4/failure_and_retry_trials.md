# First-fetch failure + retry, isolated cold trials (same ops on both builds)

T3 (never-fetched chip, Grocery Top Rated, backend stopped, then restored): the cache-miss path = getStoreList synthetic-empty + storeLoadFailed.
- base failure : 0 open · 0 total|All|Basket|Categories|Couldn't load stores. Pull down to refresh.|Delivery Type|Home|Nearest|Newly joined|Popular|Profile|Retry|Search|Stores|
- base retry   : list restored (40 labels, first: -17%|-30%|Add To Cart|)
- tip failure : 0 open · 0 total|All|Basket|Categories|Couldn't load stores. Pull down to refresh.|Delivery Type|Home|Nearest|Newly joined|Popular|Profile|Retry|Search|Stores|
- tip retry   : list restored (40 labels, first: -17%|-30%|Add To Cart|)
- T3_failure pixel diff base vs tip: 0 px
- T3_after_retry pixel diff base vs tip: 0 px
- T2_failure pixel diff base vs tip: 1167508 px
- T2_after_retry pixel diff base vs tip: 1167508 px

T2 (chip already fetched on this install, backend stopped): both builds answer from the local cache and keep the list (expected design: only a cache MISS reaches the failure state). In the two full walks the P06 step hit the cache on tip and missed it on base (cache-state difference of the two runs, not a code difference: T2 and T3 above are equal on both builds).

T3 logs: tip logcat of the failed fetch carries the paired line [FAIL] endpoint=/api/v1/stores/get-stores/all http_status=502 type=ApiFailure (expected injection); popular all-store refresh with backend down: [FAIL] endpoint=/api/v1/stores/popular http_status=502 (list kept: warm cache).

AllStoreScreen NearsErrorRetry state (popular/latest with NO cached list): UNVERIFIABLE on device (the rails are always warm from home/all or the local cache by the time the screen is reachable); covered by test/features/store/all_store_screen_error_retry_test.dart (+4) and the characterization G1 pins, both green at the tip.
