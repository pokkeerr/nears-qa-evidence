# NEARS-3191 QA progress (phase A, cycle 0) — device-free, worktree 067648b4b
| row | AC | status | evidence |
|---|---|---|---|
| 1 | (a) | PASS | advisors.test.sh rc=0; "132 assertion(s) made across 11 case(s); 0 failed"; "assertion count matches the pin (132)"; case 10 advisor-workflow x4 (row1-advisors-test.log L138-141) |
| 2 | (a) control | PASS (confirm-only) | printed pin 132 == EXPECTED_ASSERTS 3+11+16+12+24+9+14+7+7+5+23 +1 tripwire = 132 |
| 3 | (b) | PASS | worktree dry-run: 9 stdout launch lines, 4 stderr notes (qa/dashboard/data/security), 0 naming advisor-workflow. Control primary tree: 9 stdout, 5 notes incl. advisor-workflow (brief absent there) |
| 4 | (c) shape | PASS | fence-aware H2 set identical to template (8/8, same order); wc -l = 236 |
| 5 | (c) self-contained | PASS | 0 pointer bullets over Rules+Known traps (70 bullets); every bullet carries a (...path...) or (NEARS-...) tail (7 strict-regex misses were nested-paren tails, read and confirmed) |
| 6 | (c) verbatim | PASS | 3/3 clauses: 1 hit each in brief AND in cited source (new-task.md L153, L158; run-sprint.md L21) |
| 7 | (c) traps | PASS | NEARS-3140..3156 each exactly once in Known traps (17/17, 0 dupes brief-wide); 10 lesson ids exist, status ACTIVE, scope workflow/*; set == json-side active workflow/* set |
| 8 | (d) | PASS | gitleaks 8.30.1: "no leaks found", report 0 entries; plain grep 19 word-hits all prose ("token(s)" budgets/DLS, "secret" in [10] list, "sk-" = task-/sk-creation substrings), 0 credential-value shapes |
| 9 | registration | PASS | catalog.json first item = new brief; index.md L121 bullet same shape as L117; docs-catalog-check: 39 orphans + 2 dead at base AND worktree, path lists identical (NO DELTA), brief not listed as orphan |
| 10 | (e) pre | PASS | claude agents --json: 0 advisor-workflow entries; EXPECTED_SHA=067648b4b0f92c1277f9d95ec74de41039890f0f; PRE_STATUS="" (porcelain clean) |
| 11 | (e) launch | PASS | up.sh rc=0; exactly 1 entry name=advisor-workflow kind=background id=ab416200 sessionId=ab416200-797c-4a48-8343-e90801daa369 cwd=worktree; T0=2026-09-03T14:06:43Z epoch 1788444403; post-launch porcelain still clean |
| 12 | (e) ask | PENDING | phase B (conductor sends packet) |
| 13 | (e) post | PENDING | phase B |
| 14 | never-do | PASS | Never-do list: Tier C workflow items (merge past sentinel conflict, override QA FAIL) answer "owner" (L231); ledger never checkout/restore/stash/reset + git apply --cached own hunks present at Known traps L134-136 (ticket places it there) |
Blast radius: diff e94982af1..HEAD = 4 files (catalog.json, index.md, new brief, advisors.test.sh); phase-1 briefs unchanged; roster unchanged; 0 .claude/ files changed.

## Phase B (rows 12-13)
| 12 | (e) ask | PASS (merits) | reply q-20260903-140900-wf-2-NEARS-3191-002: H2 ANSWER/EVIDENCE/CONFIDENCE/CAVEATS present (SHA carried as header bullet, full value == EXPECTED_SHA 067648b4b); ANSWER = No, names item 11 worktree-prune as the only post-merge check, gap = NEARS-3140; EVIDENCE cites new-task.md 186-189 (covers 186-187); QA re-read L186 (ends at --ours/--theirs conflict rule, no rc/rev-parse/is-ancestor assertion) and L187 (worktree-prune.sh --keep), jira-map AUD-WF-01 -> NEARS-3140 Critical |
| 13 | (e) post + bound | teardown PASS / ≤180 s FAIL | down.sh rc=0 "stopped ab416200"; claude agents --json 0 advisor-workflow entries; porcelain "" == PRE_STATUS; HEAD unchanged. Elapsed from packet 14:09:00Z: advisor idle 577 s, conductor receipt 594 s, reply-file mtime 638 s vs 180 s bound -> FAIL, out-of-ticket per conductor D6 (advisor-budget miscalibration, regression ticket under NEARS-3122) |
Note: the reply file is the conductor's transcription of the advisor's SendMessage (sections marked "verbatim"/"abridged"); `claude logs ab416200` returned only TUI spinner output, so the raw advisor envelope was not independently inspectable by QA.
