# NEARS-4129 QA progress (cycle 0) - private clone multi_food_db_qa4129
tip b20e5698885cc69c43d5939e19563fb4aefd5c00 (prompt had a garbled sha b20e5698885cbfba..; 12-char prefix b20e5698885c matches) ; seeder blob a029a04b5d41 OK
backend: fixed = worktree Admin/ php -S :8129 (direct form; artisan serve wrapper segfaulted rc=139, serve-exit.log) ; base = scratch copy with the two controllers = git show 87f15d3b0 bytes (blob hashes proven) :8130
ADMIN fixed: A N=2 +100 (2 rows) | A N=5 +250 (5 rows) | B N=2 +125 (75,50) | B N=5 +275 (75,50x4) | AC2 drain 5 then 2 parallel: 1 success + Insufficient toast, ends 0.00 | C single refused, byte-identical
ADMIN base : A N=2 +50 / 2 grants (RED) | A N=5 +50 / 5 grants | B N=2 +75 / 75,75 | B N=5 +125 / 5 grants | AC2 both succeed (2 grants for one debit) | C single no [FAIL] line
API fixed: B N=2 overlapping +125 (75,50) | B seq +125 | A N=2 +100 | A N=5 +250 | AC2 1x200 + 1x403 | C single 403 | fail grant shift+renew: HTTP 500 errors.message, 5 tables byte-identical, 1 [FAIL] reason=grant_failed each
API base : B N=2 overlapping +150 (75,75) RED | B seq +125 (75,50) GREEN | A N=2 +100 / N=5 +250 (lost-update REFUTED) | AC2 1x200+1x403 (3523 lock holds) | fail grant: 200 application placed + refund credit 32.14 + old sub status 0 committed (RED)
tests: 32/446, 35/503, 34/745, 28/361, 5/17 all OK
