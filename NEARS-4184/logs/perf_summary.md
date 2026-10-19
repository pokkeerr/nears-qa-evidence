# NEARS-4184 AC30 / AC13 performance record (QA run, sha 610e68043, base b326327ec, load twin multi_food_db_qa4184_load, php -S x4 workers each, ab -n 200 -c 4, warm-up 15, 1 run per calendar minute, every run clean 2xx)

Official (3 runs per server, alternating; median p95):
- zone-wide plain list   base 177 ms  head 184 ms  ratio 1.040  (dataset: base 1149 stores, head 1047 after the walking hide)
- zone-wide fastest      base 178 ms  head 192 ms  ratio 1.079
- food-module plain      base 155 ms  head 169 ms  ratio 1.090
- food-module fastest    base 221 ms  head 175 ms  ratio 0.792 (base had two 220+ ms runs)
Confirmation (5 runs per server) on the two closest paths:
- food-module plain      base 169 ms  head 168 ms  ratio 0.994
- zone-wide fastest      base 184 ms  head 188 ms  ratio 1.022
Engineer pre-flight (3 runs): 0.95 .. 1.057. Script verdict on every path: WITHIN 10%.

SQL level (mysqlslap, concurrency 1, 100 queries x 3 iterations, 3 rounds alternating base/head; per query):
- zone-wide list   base 19.2 ms  head 24.9 ms (+30%)   count  base 1.31 ms  head 1.55 ms (+18%)
- food-module list base  7.9 ms  head 10.2 ms (+28%)   count  base 0.68 ms  head 0.80 ms (+18%)
=> the inline ETA expression costs about +6 ms per request (~3%) at 1000 stores; HTTP p95 is dominated by PHP (CACHE_DRIVER=database row lock), so the HTTP ratio stays within the gate.
Query count per request (in-process kernel, 2nd request): zone-wide base 34 head 34; food base 36 head 36; normalised statement multiset identical.
EXPLAIN (FORMAT=TRADITIONAL, list and COUNT, zone-wide and food, base and head; explain_all.txt): base and head both show Using filesort + Using temporary on the list and Using temporary on the COUNT (store_subscriptions derived table); head adds exactly one DEPENDENT SUBQUERY on modules (eq_ref PRIMARY, the module prep default). No new filesort/temporary beyond base.
