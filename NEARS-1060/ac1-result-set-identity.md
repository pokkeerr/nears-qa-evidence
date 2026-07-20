# NEARS-1060 AC1 — result-set identity (live BEFORE vs AFTER)

Method: same running backend, same read-only dev DB (`multi_food_db`), zone 2 / module 1
(13 active stores: 3 reviewed avg 5.00/4.20/3.40, 10 zero-review NULL-avg). Captured full
ordered store-ID list + `total_size` for each permutation, first against the fix (AFTER),
then after swapping `StoreLogic.php` to base `f91fb365` via `git show` (BEFORE), then
restored the fix (md5 verified identical). Harness: trap-guarded, no mutation left behind.

## Verdict: IDENTICAL — byte-identical across all 20 permutations (diff empty)

```
A1 get-stores/all p1 : total=15 ids=[9, 12, 13, 14, 16, 17, 18, 19, 20, 21]
A2 get-stores/all p2 : total=15 ids=[22, 4117, 4118, 8, 35]
A_nearest get-stores : total=15 ids=[12, 21, 22, 4117, 9, 20, 4118, 14, 16, 13, 17, 19, 18, 8, 35]
A_top_rated get-stores : total=3 ids=[35, 21, 19]
A_newly_joined get-stores : total=15 ids=[4117, 4118, 35, 9, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 8]
A_popular get-stores : total=15 ids=[35, 12, 9, 8, 13, 14, 16, 18, 17, 19, 20, 21, 22, 4117, 4118]
B1 get-data rating_count=4 p1 : total=2 ids=[21, 35]
B2 get-data rating_count=4 p2 : total=2 ids=[]
B3 get-data rating_count=5 : total=1 ids=[35]
B4 get-data rating_count=3.4 : total=3 ids=[19, 21, 35]
C1 get-data currently_open : total=13 ids=[12, 21, 22, 4117, 9, 20, 4118, 14, 16, 13, 17, 19, 18]
C2 get-data top_rated filter : total=3 ids=[21, 19, 35]
D1 get-data rating_count=9 : total=0 ids=[]        (empty result set)
E1 latest : total=15 ids=[4117, 4118, 35, 9, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 8]
E2 popular : total=15 ids=[12, 21, 22, 4117, 9, 20, 4118, 14, 16, 13, 17, 19, 18, 8, 35]
E3 recommended : total=0 ids=[]
E4 discounted : total=14 ids=[9, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 4117, 8, 35]
E5 top-offer-near-me : total=0 ids=[]
```

Edge cases confirmed inline:
- Zero-review (NULL-avg) stores APPEAR in currently_open (total 13) and default listing, but are
  EXCLUDED by rating_count>=4 (total 2 = only avg 5.0 & 4.2 stores). Matches base exactly.
- Temporarily-closed store excluded by currently_open identically before/after.
- Empty result set (rating_count=9) identical.

The admin priority-list sort permutation (all_stores_sort_by_general='rating',
unavailable='remove') is NOT settable live (business_settings/priority_lists are read-only dev
DB, and default to status=1 which skips that branch). It is pinned by the mutation-checked
regression test `StoreListCountQueryPerfTest::test_rating_sort_count_drops_correlated_subquery_and_counts_open_only`
(exact avg_r-desc order [high,mid,low], closed removed) — falsifiable: revert whereOpenNow→having and it fails.
