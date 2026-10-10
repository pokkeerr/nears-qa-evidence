# NEARS-4107 QA progress (build d7764d3c6b34dc826b09ebf3aa1ada3adaddff49)
Own server 127.0.0.1:8107 from this worktree, DB multi_food_db_qa4107 (dump of multi_food_db_test), php -d pcre.jit=0, OTEL_SDK_DISABLED=true.
All orders staged through real routes (customer place-order / offline-payment API, admin deny/verify, admin settings routes); no DML.
- AC1/AC4/AC6 refusal matrix: 68/68 (N1 no-row, P1 pending, D1 denied, B1 partial+offline pre-submit) x vendor API / store panel POST / store panel PUT / admin status / admin assign. Files: ac1-refusal-matrix-results.json, be-log-fail-lines.log
- AC2/AC6 verify via real admin route then advance: ac2-verify-then-advance.txt
- AC3 controls: ac3-controls-1.txt, ac3-controls-2-partial-cod.txt, ac3-canceled-on-unverified.txt
- AC7 partial+offline: ac7-partial-offline-flow.txt
- odd/array status + foreign vendor: ac5-odd-status-and-foreign-vendor.txt
- en/ar: ac7-locale-en-ar.txt
- regression sweep: regression-sweep-1.txt, regression-sweep-2-4083.txt
- automated: automated-backstop-phpunit.txt (497 tests / 3883 assertions OK); strict-sites guard OK
