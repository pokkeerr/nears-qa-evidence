# NEARS-4116 QA progress (checkpoint log)
- server: php -S 127.0.0.1:8416 from worktree (pid 80547), DB multi_food_db_qa4116, route:list shows POST only
- AC1 PASS (curl GET/HEAD 405, ledger identical) - ac1-ac2-curl.log
- AC2 PASS (419 no/bad token, 405 spoof GET/PUT, validation 302 back no change, unauth 302, positive control tokened POST ok) - ac1-ac2-*.log
- C4 settlement parity PASS (paid-digital settles, unpaid-digital refused x2 paths w/ one WARN each, COD settles) - c4-settlement-parity.log, log-refused-warn-excerpt.log
- pending: AC3 UI, AC4 grep, AC5, probe 153, employee role
