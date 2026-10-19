# NEARS-4184 QA progress (tested sha 610e68043a07a495888a61d3fa0b6ac8b49824ac, base b326327ec3f218f0836c683f117d25a16b7addae)
Own backend: php -S 127.0.0.1:8191 from the worktree, DB_DATABASE=multi_food_db_qa4184 (twin; shared DB has 0 rows of ids 91400-91495, twin 96). backend-freshness-check PASS.
- E automated: 18 PHPUnit files, 493 tests green (logs/phpunit_summary.txt)
- A API: ladder/floors/types/speeds/settings/hostile headers 146+44 cases vs oracle, 0 product FAIL (logs/ac_api_out.txt, ac_settings_out.txt); 40-surface sweep + base-vs-head payload diff (logs/sweep_surfaces.json, regdiff_out.txt)
- B behav: 15 scratch mutations all killed (logs/mutate_out.txt, mutate2_out.txt); AC15 migrations up/down/up PASS; AC22 money diff IDENTICAL + control OK (logs/money_diff.log); AC28 PASS; AC30 perf see logs/perf_summary.md; AC36 guard refusals + idempotent rerun PASS
- C ui AC18: Admin create/edit/settings + Store Panel, EN and AR: persists, tamper rejected, failed-save generic toast + paired [FAIL] line; screenshots ac18-*.png
- D regression: payload diff base vs head limited to designed deltas
- twin restored after the run (stores 17/22, created stores removed, local_storage 0, vendor hash, cart row, admin name)
