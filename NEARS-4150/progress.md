# NEARS-4150 live QA (phase 8, cycle 0) - tip 60341953921e475df48d535bdbf803f9e128c178, base 730b280e2

Device-free (Laravel Admin web route). Two scratch trees + own `php artisan serve --no-reload` each, stub `crontab` first on PATH, private clones of one read-only dev dump.

| Server | tree | port | DB | controller sha256 |
|---|---|---|---|---|
| fixed | scratchpad/n4150/qa/fixed/Admin | 8451 | multi_food_db_qa4150 | 535c1741... = worktree tip |
| base  | scratchpad/n4150/qa/base/Admin  | 8452 | multi_food_db_qa4150b | b393410e... = `git show 730b280e2:` blob |

Proof of DB / PATH: `ps eww` of the php -S pid shows DB_DATABASE=<clone>, PATH=<tree>/bin first. Scratch `.env` also pinned to the clone.

## Arms (details in arms.jsonl, arm-B-rows.json, C*.{base,fixed}/, D2.fixed/, ui-*.png)

- A BASE (RED): store time `$(touch M):0` -> marker CREATED; dm time same -> marker CREATED; php path `$(touch M2)` -> marker2 CREATED; php path with LF -> second cron line in crontab.out. 0 [FAIL] lines on base.
- B FIXED: 77 inputs x 2 admins (super + restricted zone-1 settings admin role_id 14) = 154 refusals: each 302 back + validator's own toast, DB snapshot identical, script.sh sha identical, crontab.out ABSENT, no marker, exactly ONE `[FAIL] admin.disbursement_input_refused` (reason invalid_schedule_value, endpoint admin/business-settings/update-disbursement, status 302, correlation_id == X-Request-Id, 154/154 joined), canary grep (touch, marker, INJECTED, `$(`, backtick, xxxx, usr/bin, /a b, funday, hourly, weekly;, auto) = 0 in the 154-line log.
- C legit (base vs fixed, path-normalised): automated daily 09:05 + weekly monday 18:30, monthly, weekly sunday/saturday 00:00/23:59, manual: script.sh, crontab.out, stored *_disbursement_command byte-identical (zero padding `05 09 * * *` kept).
- D FIXED: manual blank php -> stored 0, script REWRITTEN (clear lines with '/usr/bin/php'), crontab.out empty (stale add-lines NOT re-run); BASE shows the stale re-run (add-lines re-appended). manual posted '0' OK; automated '0' refused; 'php', '/a b/php', `$(..)`, LF, backtick, `;`, '00', '0.0', '-0', array-0 refused in manual too, same message; waiting/min-only edits OK (full re-post and minimal post).
- E UI (real Chromium): page renders; automated save success toast; manual save success toast; `php` typed into #system_php_path -> error toast "The system php path format is invalid." + DB unchanged + one [FAIL]; command strings render in the cron modal; both copy buttons put the exact command on the clipboard (base identical). Rendered page HTML base vs fixed under identical state: diff = csrf token + correlation-id meta only (blade untouched in the diff).
- F: item-only admin (role 15) POST -> 302 back + "Access denied" (module gate), zero change, no [FAIL]; unauthenticated POST 419; super POST without CSRF 419; settings admin subject to the same refusals (arm B).
- G: dm-settings and order-settings re-save: 302 + success toast on base and fixed; dashboard 200 on both; no non-disbursement lines in the fixed laravel.log.
- Extra live: scratch root containing a space -> legit save writes quoted root; scratch root containing `%` -> refused pre-write, reason unsafe_cron_token, toast "Access denied", one [FAIL], no script.sh.

NOT live-testable by design: poisoned STORED value / duplicate-row build-gate refusal after the writes (needs clone DML without an advisor stamp).
