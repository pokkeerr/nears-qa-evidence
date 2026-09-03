# NEARS-3124 QA progress — part 1 (device-free, first pass) — 2026-09-03, HEAD 5aeff56d7, cwd = worktree
- (a) PASS — advisors.test.sh rc 0; "-- result: PASS", "118 assertion(s) made across 11 case(s); 0 failed", "assertion count matches the pin (118)"; advisor-* listing identical before/after (0/0). ac-a-selftest.txt
- (b) PASS — up.sh --dry-run all: 9 stdout lines, diff vs design line 69 × roster names = empty (md5 b2461d51…); `all --dry-run` identical; 5 expected "brief missing" stderr notes. ac-b-dryrun.txt
- (c) STEP 1 PASS — precondition empty; up.sh advisor-backend → "launched: advisor-backend"; listed name=advisor-backend kind=background at t+2s, id 12e21e95; re-run → "present: advisor-backend (12e21e95)", count 1; replies dir exists (pre-existing). Steps 2+ PENDING PART 2 (conductor §7 packet). ac-c-step1-launch.txt, ac-c-step1-listing.json, ac-c-step0-precondition-listing.json
- (d) PASS — H2 sets equal to template ×4; 203/189/178/174 lines; 4 never-do items ×4; 3 rules per brief traced to source (+1 extra each). ac-d-structural.txt, ac-d-advisor-{backend,flutter,dls,product}.md
- (e) PASS — gitleaks "no leaks found" ×2; bounded secret grep empty. ac-e-secret-scan.txt
- (f) PASS — owner-queue.sh rc 0, both JQLs verbatim + searchJiraIssuesUsingJql hint; live JQL result cited from conductor (accepted, 0 each). ac-f-owner-queue.txt
- SEC-1 PASS (static half) — --strict-mcp-config right after bypassPermissions in lib.sh:87, all 9 dry-run lines, argv element check; behavioural half PENDING PART 2. sec-1-strict-mcp-config.txt
- Regression A PASS — catalog.json valid, 5 advisors items exist; review-lessons.json valid, rule id count 1. regression-a-catalog-lessons.txt
- Regression B NOTE — docs-catalog-check.sh rc 1 on pre-existing 35 new-orphans + 2 dead F7 paths (none in branch diff, none under docs/workflow/advisors). regression-b-docs-catalog-check.txt
- Regression C PASS — qa-run-stop.test.sh 74/74 (detached run; base-tree control also 74/74). regression-c-qa-run-stop-test.txt

## Part 2 — 2026-09-03 11:16Z (after the conductor's §7 exchange, reply q-20260903-151300-nears-7b-NEARS-3124-001)
- (c) STEP 2 PASS — reply copy md5-identical to ~/.nears/advisors/replies; headings ANSWER/EVIDENCE/SHA/CONFIDENCE/CAVEATS in order; ## SHA 5aeff56d747d…c99 == git rev-parse HEAD, resolved via .git gitdir pointer → worktrees/…/HEAD → loose ref (packed-refs 0); QA opened Admin/bootstrap/app.php:108 = `'dm.api' => DmTokenIsValid::class,`, DmTokenIsValid.php:12/:28, routes/api/v1/api.php:105 — all as ANSWER claims. ac-c-step2-verification.txt
- SEC-1 behavioural PASS — reply: "No `mcp__atlassian*` tool"; ToolSearch "mcp__atlassian" → "No matching deferred tools found". 
- TB-1 candidate recorded (High, not adjudicated) — session still holds Workflow, EnterWorktree/ExitWorktree, Artifact, Skill, Cron*/ScheduleWakeup/RemoteTrigger/SendUserFile/Task*, 23 deferred mcp__claude-in-chrome__*; ABSENT = exactly the 8 disallowed. bug-tb1-advisor-tool-surface-not-removed.log
- (c) STEP 3 PASS — down.sh advisor-backend → "stopped: advisor-backend (12e21e95)" rc 0; listing: 0 advisor-*; audit-userapp 7c6da713 + helper c245890c survived; replies dir holds the qid file; git status clean. ac-c-step3-teardown.txt, ac-c-step3-listing-after-down.json
