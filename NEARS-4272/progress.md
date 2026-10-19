# NEARS-4272 QA [8] progress (cycle 0)
- AC3: PASS - all 9 self-tests green (wrapper 217, flows 14, catalog 16, check-asserts 17, check-ac-coverage 18, check-ids 29, logcat-gate 38, junit-ac-table 50, secret-forms 18); lock-guard 497 unchanged green; guards live on real corpus (selftests/, ac3-guards-live-corpus.log)
- AC2 cloud half: PASS live - cloud/--analyze/--include-tags --api-key/--api-key/login/mcp each rc 2, 0 JVMs, 0 tests folders (ac2-cloud-flag-refusals.log)
- AC2 lock half: PASS live - foreign sentinel hold in temp QA_LOCKS_DIR -> rc 2 'qa_lock_acquire emulator-5572 refused', owner.json unchanged (ac2-foreign-lock-refusal.log)
- Build BLOCKED: mem-guard exit 96, swap 6.3 GB > 6.0 GB, flat 00:44-01:06 (blocked-memguard-swap.log)
- AC1/AC4/AC5/AC6 live: not run (no APK)

# cycle 1 (delta re-QA, 2026-10-20)
- Build: first attempt mem-guard KILLED tree 6.4 GB > 6.0 (gradle.properties -Xmx8G daemon 2.6 GB); retry with GRADLE_OPTS -Dorg.gradle.jvmargs=-Xmx2560m + kotlin in-process under same --max-gb 6 --max-swap-gb 7.5 -> installed OK. Swap 6.45->6.11 GB.
- Backend: own artisan serve :8272 from worktree @ 7c2ca0184, DB multi_food_db_qa4272 (request-level marker proven, restored); freshness PASS.
- AC2 delta smoke: cloud / --include-tags --api-key / --evidence-key --x / --evidence-key (no value) each rc 2, 0 JVM, 0 tests folders (ac2-fix1-arg-refusals.log); foreign-lock refusal rc 2, owner.json unchanged (ac2-fix1-foreign-lock-refusal.log)
- TB3: QA_MAESTRO_PYTHON=/usr/bin/python3 -> rc 2 before lock, real owner.json unchanged (tb3-python-resolution.log); default run prints 'python: /Users/Apple/.hermes/hermes-agent/venv/bin/python3 (first python3 with yaml)'
- AC1: run 20261020-024125-94002 flows 01+02: maestro exit 0, junit 2/2 SUCCESS, gate DIRTY app_lines=1279 err_fail=8 (Firebase-unconfigured class, 4 per cold launch, app-pid 15103/15592, tag flutter level I), markers START/END true -> rc 1 'FAIL (log has [ERR]/[FAIL])' = parity PASS
