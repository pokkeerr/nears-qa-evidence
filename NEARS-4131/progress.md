# NEARS-4131 QA progress (checkpoint) - tested sha ec9a11cb193cc27ad4c0707e8caccc03c6ff5cbb
Backend: /Users/Apple/Projects/nears-NEARS-4131-wallet-purchase-extraction @ ec9a11cb1 (own server :8131, PHP_CLI_SERVER_WORKERS=8, served env DB_DATABASE=multi_food_db_qa4131; clone-only package probe returned 1)
- AC1/AC2/AC6 strict-sites: PASS (guard OK; per-file base 86/20/34 -> head 78/12/26; 3 TSV rows each with column-3 note; 0 strict tokens added in controllers) - ac126-strict-sites.txt
- AC3 live parallel: PASS all three surfaces. Natural bursts A/B N=2,5 (+100/+250, +125/+275), underfunded N=2 after drain (1 grant, 1 refusal, balance 0.00, 1 [FAIL] insufficient_balance w/ correlation_id==X-Request-Id), held-lock N=5 overlap proof (data_lock_waits distinct waiting trx = 5) - ac3-*.txt
- AC7 eligibility: PASS all three surfaces (retired/rental/nonexistent/array x wallet/gateway(/manual) zero writes; positive controls) - ac7-*.txt
- AC8 live: PASS (insufficient_balance 403 keys [code,message]; grant_failed 500 keys [code,message]; nonexistent/array code-less); exception reason: not live-reachable (test-proven)
- AC9 live: PASS retire + reprice on all three surfaces (held wallet row lock, real admin toggle/update) - ac9-*.txt
- cross-actor: PASS; package_view parity: PASS; type[]=x: no 500; smoke pages: 200
- mutations m1..m8 in scratch copy: all RED (see mutations/*.json); extra x1..x10 pending
- BASE (scratch worktree at 1e2e8a2e1, own server :8132 same clone, stopped): AC9 RED live on all 3 surfaces (retire: base sells retired pkg and debits 7.00; reprice: base debits 7.00 but records tx 20.00); success/gateway/type[]/free_trial bodies identical tip vs base (base-vs-tip-api-bodies.txt); panel/admin nonexistent+gateway = base 500, tip toast+redirect
- mutations: m1..m8 RED; extras x1..x10: x7 equivalent mutant survives, x8 survives (API subscription_transactions.reference literal unpinned) - mutations/SUMMARY.md
- backstop (live worktree, targeted 8 files): 213 tests OK - automated-backstop.txt
