# NEARS-3833 QA [8] — fix_cycle 0 — progress checkpoint

Surface: Laravel API only (no device; no device lock acquired). Worktree server 127.0.0.1:8733 on private DB copy `nears_3833_qa`.
Backend: /Users/Apple/Projects/nears-NEARS-3833-cart-cross-module @ 3ce16f7ea (backend-freshness-check PASS, exit 0)
Base-code comparator: scratch copy of worktree Admin with CartController.php + Helpers.php at da4435d75, 127.0.0.1:8734, same copy DB (stopped after AC-REG).
DB proof: copy-only marker business_name='Nears QA3833 COPY' read back via GET /api/v1/config on :8733 while multi_food_db still 'Nears' (restored after).

| AC | Status | Evidence (transcript.txt / other file) | Logs |
|---|---|---|---|
| AC1 | PASS | flag OFF, list no header -> 400 {errors:[{code:moduleId,"Module id required"}]} (AC1-off-list-nohdr) | clean |
| AC2 | PASS | flag OFF, header 1 -> 3 rows all m1; header 3 -> 2 rows all m3 (AC2-off-list-hdr1/hdr3) | clean |
| AC3 | PASS | flag ON, no header -> 200, 5 rows, module_ids [1,3] (user); guest 1968 -> rows m1+m3 | clean |
| AC4 | PASS | flag ON, header 1 / 3 / 4 / 999 / slug "grocery" -> body byte-identical to no-header body | clean |
| AC5 | PASS | flag ON, add m3 item under header 1 -> 6 rows [1,3], new cart 982 stamped m3; increment -> qty 2, 6 rows; m4 item under header 3 -> 7 rows [1,3,4]; update m3 row under header 1 -> 7 rows [1,3,4] | clean |
| AC6 | PASS | flag ON, remove-item cart 982 no header -> 200, only 982 gone (DB snapshots), list basket-wide [1,3,4]; other owner's 971 and guest row 981 -> no-op | clean |
| AC7 | PASS | flag ON, clear no header (user), header 4 (guest 1968), header 1 on m1+m3 basket (user), no header (guest 1969) -> DB rows 0, re-list []; u2/u6/g6 rows untouched | clean |
| AC8 | PASS | flag OFF, remove-item + clear no header (user + guest) -> 400 moduleId, DB counts unchanged (total 78); header-1 clear on guest 1968 left the m3 row 979 | clean |
| AC9 | PASS | store-less row 989 skipped (200, other rows present) flag ON and OFF; 'cart row skipped: item store missing' {cart_id,item_id,item_type}; deleted-item row 990 still 'catalog item missing' (ac9-log.txt) | expected WARNINGs only |
| AC10 | PASS | item 688 category_ids NULL -> [] row shown; item 663 variations NULL -> [] row shown; flag ON and OFF | clean |
| AC-LOG | PASS | no raw prints in added Admin/app lines; single Log::warning with allow-list keys | n/a |
| AC-REG | PASS | acreg.txt — 12 flag-OFF request pairs worktree vs base: 5 raw-identical, 7 identical after normalising the request-host port in *_full_url; add-incr differs only in updated_at | n/a |
| AC-TEST | PASS | phpunit.txt — 68 tests / 350 assertions OK across all 7 suites; CartModuleIdGuardTest + CartNullModuleTest diff empty | n/a |
