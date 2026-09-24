# NEARS-3743 — QA [8], fix cycle 0

**VERDICT: PASS**

| | |
|---|---|
| Branch under test | `fix/NEARS-3743-ratelimiter-cache-deadlock` @ `a385e2217` |
| Red baseline | `feat/human-qa-uiux` @ `385df54ed` (primary tree, stock `Illuminate\Cache\DatabaseStore`) |
| Backend (fix) | `/Users/Apple/Projects/nears-NEARS-3743-ratelimiter-cache-deadlock @ a385e2217` — own server, `:8743`, freshness-check PASS |
| Backend (baseline) | `/Users/Apple/Projects/nears @ 385df54ed` — own server, `:8744` |
| Device lock | none — backend-only ticket, no app surface (profile §"Device-free ticket ⇒ NO device lock") |
| DB | read-only; `php artisan cache:clear` only (sanctioned), no DML |

---

## 1. Both faking traps were handled BEFORE any result was trusted

### Trap 1 — the prescribed concurrency instrument does not work on this host

`PHP_CLI_SERVER_WORKERS=4 php artisan serve` was **measured, and it does not fork workers here**:

```
artisan serve, PHP_CLI_SERVER_WORKERS=4 : PARALLEL_8_WALL=1.165s  SERIAL_8_WALL=1.179s
ps: exactly ONE `php -S` process, no children
```

Parallel wall == serial wall ⇒ fully serialised ⇒ a two-curl repro would have passed on broken
code, exactly as the Team Lead warned. `ServeCommand.php:100` reads the variable through `env()`
and it did not resolve in this shell.

**Working fallback (used for every run below)** — drive the built-in server directly, which *does*
fork:

```
cd <tree>/Admin/public && PHP_CLI_SERVER_WORKERS=32 php -S 127.0.0.1:<port> ../server.php
```

32 forked children visible in `ps`; `PARALLEL_8_WALL=0.733s` vs `SERIAL_8_WALL=1.825s` — real
overlap, proven by measurement, not assumed.

### Trap 2 — no red baseline, no meaning

The prescribed repro shape (cold `cache:clear` + simultaneous burst) **never reproduces the defect
on this host**:

| | requests | non-2xx | `1213` ERROR lines |
|---|---|---|---|
| BASELINE (unpatched), 40 cold bursts n=250 c=32 | 10 000 | 0 | 0 |
| FIX, identical shape | 10 000 | 0 | 0 |

Two greens prove nothing. The amplifier that **does** reproduce it is interleaving the cache
**flush** (`DELETE FROM cache`) *into* the load, so `DELETE` races `insert ignore into cache` —
which is also a realistic production shape (any settings save flushes the cache under traffic).

### The two trees really do differ (positive control)

```
fix worktree : Cache::getStore()  =>  App\Cache\DeadlockRetryingDatabaseStore
primary tree : Cache::getStore()  =>  Illuminate\Cache\DatabaseStore
```

### The endpoint really does write the limiter counters (positive control)

After `cache:clear` + **one** `GET /api/v1/stores/get-stores/all`, the `cache` table held exactly
the two limiter buckets and their timers — `9f4563f327dc70d317580383179debc2` (`v1-total`, the key
named in the AC2 predicate) and `887427d1c0b6e3d1d3ff8eb5a3b77317` (`v1-blanket`). Route confirmed
inside `routes/api/v1/api.php`'s top-level `throttle:v1-total` + `throttle:v1-blanket` group.
`cache`/`cache_locks` are InnoDB; `innodb_deadlock_detect=1`; `REPEATABLE-READ`.

---

## 2. RED BASELINE — reproduced, with a correlated request id

Unpatched `feat/human-qa-uiux` @ `385df54ed`, flush-storm amplifier:

* ab-driven storm, 5 000 requests → **9 non-2xx**, **10** `production.ERROR … 1213 Deadlock …
  insert ignore into \`cache\`` lines.
* curl-driven storm, 5 120 requests → **1 × HTTP 500**, body `{"message":"Something went wrong"}`,
  `X-Request-Id: 4f5f3f37-87b5-49e9-9711-57df0b12a456`, correlating **exactly** to:

```
[2026-09-24 15:10:53] production.ERROR: [FAIL] SQLSTATE[40001]: Serialization failure: 1213
Deadlock found when trying to get lock; try restarting transaction (Connection: mysql, …,
SQL: insert ignore into `cache` (`key`, `value`, `expiration`) values
(laravel_cache887427d1c0b6e3d1d3ff8eb5a3b77317, i:0;, 1790248313))
{"trace_id":"…","correlation_id":"4f5f3f37-87b5-49e9-9711-57df0b12a456", …}
```

Same statement shape as the only historical occurrence in the repo's `laravel.log`
(2026-06-21 16:00:48). The baseline is genuinely RED.

---

## 3. Per-AC results

| AC | Status | Evidence | Logs |
|---|---|---|---|
| **AC1** `[api]` — concurrent `GET /api/v1/stores/get-stores/all` never 500s; all callers 200 | **PASS** | 23 285 live requests on the fix across three shapes (10 000 cold-burst + 10 240 flush-storm with exact per-request codes + 3 000 store reqs during login load) → **zero** non-2xx. Same amplifier on the unpatched baseline produced a 500. | clean — 0 `1213` ERROR lines in either fix-run log delta |
| **AC2** `[behav]` — transient contention retried gracefully, not surfaced | **PASS** | **10 real deadlocks absorbed** on the fix (1 in the flush-storm, 9 under login-load). Every line: `[WARN] cache write deadlock retried`, `method:add`, `attempt:1`, `max_attempts:3`, `sqlstate:"40001"`, `errno:1213`, `cache_keys:["9f4563f327dc70d317580383179debc2"]` — an **array**, and the exact `v1-total` bucket the predicate names. The request behind the first one (`correlation_id 63622a55-…`) returned **HTTP 200 OK** — before the fix the identical event was a 500. | 10 × `[WARN]` (expected), 0 × `[FAIL] … retries exhausted` |
| **AC3** `[api]` — no deadlock **error** line for this endpoint | **PASS** | Matched by error-line **shape** (`production.ERROR` carrying a `QueryException` on the `cache` table), never the substring `deadlock` — the AC2 `[WARN]` line deliberately contains that word. Fix deltas: **0**. **Positive control satisfied**: the same shape-grep on the red baseline returns **11** such lines. | clean (see caveat below) |

### AC3 caveat, stated plainly

`laravel.log` carries **pre-existing, unrelated** `production.ERROR: [FAIL] OpenTelemetry export
failed` lines on **both** branches (cURL error 7 → `localhost:5080`; OpenObserve is not running on
this host). Because `SetRequestId` shares log context, those lines *do* carry a `correlation_id`,
so a purely literal reading of AC3 ("no `production.ERROR` correlated to a captured
`X-Request-Id`") fails on the baseline and the fix alike. Scoped to the cache/deadlock error shape
— which is what the AC is about — AC3 passes on the fix and fails on the baseline. Logged below as
a non-blocking pre-existing item, not a defect of this change.

---

## 4. Also-worth-a-pass items (Team Lead's list)

| Item | Result |
|---|---|
| Successful login (`RateLimiter::clear` → `forget()` ×2) **concurrently** with contention on the same buckets | **45/45 → HTTP 200**, run over 15 rounds each combining 3 concurrent logins + 200 store requests (c=32) + 7 cache flushes. 9 deadlocks were absorbed during exactly these rounds; no login saw a 5xx. |
| `php artisan cache:clear` still works | Yes — executed ~600 times across the run; verified by the counter rows disappearing and by `throttle:auth` resetting. |
| `throttle:auth` still 429s at 5/min | **PASS** — requests 1–5 → `200`, 6–8 → `429 Too Many Requests`. |
| `v1-total` / `v1-blanket` caps + bucket keys unchanged | **PASS** — both bucket md5s observed unchanged in the `cache` table; no 429 anywhere in a 250-request cold window (cap 300/min). |

## 5. Automated backstop

```
vendor/bin/phpunit tests/Feature/Nears3743CacheDeadlockRetryTest.php
  OK (11 tests, 34 assertions)

vendor/bin/phpunit --configuration phpunit.xml   (full suite, regression sweep)
  Tests: 2755, Assertions: 18568, Failures: 6, Skipped: 1
```

The 6 failures are **exactly** the pre-declared set (`ConfigContractTest`,
`ItemModuleFollowsStoreTest` ×2, `ModuleIdDriftGuardTest` fixture leak, `BulkImportZoneScopeTest`,
`Nears2927ItemDescriptionXssTest`) — all bulk-import / module-drift, none within the cache-store
blast radius. Not chased, per instruction.

## 6. Regression sweep

Blast radius of this change is app-wide (it replaces the `database` cache store for every caller),
so the sweep was the full backend suite above plus the live limiter/auth paths in §4. **Clean.**

## Files

* `bug-red-baseline-deadlock-500.log` — the reproduced 500 + its correlated deadlock log line
* `red-baseline-abstorm-10-deadlocks.log` — the 10 baseline deadlock ERROR lines
* `ac2-retry-warn-lines.log` — all 10 absorbed-deadlock `[WARN]` lines from the fix
* `ac1-ac3-live-http-totals.log` — request totals + the AC3 shape-grep results
* `instrument-validation.log` — the two traps, measured

---

# Appendix — full QA envelope tail (recorded here because the notification transport truncated it)

## A. `posted_comment` — **true**

Posted to NEARS-3743 by this QA agent, comment id **21479**, `2026-09-24T15:29:08+04:00`.
It carries the verdict, the `Backend:` attribution line, the full per-AC table with per-AC log
results, the gallery link, the automated-backstop result and the pre-existing-noise note.
**No action needed from the Team Lead** — do not re-post.

## B. `GALLERY_URL`

```
https://github.com/pokkeerr/nears-qa-evidence/tree/main/NEARS-3743
```

`scripts/qa-evidence-publish.sh NEARS-3743 "<verdict line>"` succeeded. 5 artifacts:
`qa-report.md` (this file), `bug-red-baseline-deadlock-500.log`,
`red-baseline-abstorm-10-deadlocks.log`, `ac2-retry-warn-lines.log`,
`ac1-ac3-live-http-totals.log`, `instrument-validation.log`.
Local source: `<worktree>/docs/qa-evidence/NEARS-3743/`.

## C. `task_bugs[]` — **`[]`, and that is final**

Zero defects found in this change. All three ACs were demonstrated live against a *reproduced*
red baseline; the retry path was exercised by **10 genuine deadlocks**, not by a seam fake; the
DELETE path was exercised by 45 successful logins under contention; and the limiter caps, bucket
keys and `throttle:auth` behaviour are unchanged. Nothing was deferred, skipped or rounded up.

## D. `regression_bugs[]` — one entry, complete

### 1. OpenTelemetry exporter logs a `production.ERROR` per dropped batch while OpenObserve is down

* **Where:** `Admin/` — OTel exporters (`OpenTelemetry\Contrib\Otlp\MetricExporter` and the trace
  exporter), surfacing in `Admin/storage/logs/laravel.log`.
* **Surface:** Backend. **Pre-existing** — present identically on `feat/human-qa-uiux` @ `385df54ed`
  and on the fix branch. **Not caused by, and not affected by, NEARS-3743.**
* **Severity: Low** (revised down from the Medium I first reported — see the rate analysis below,
  which was run specifically to answer the Team Lead's question and changes the framing).
* **Evidence (verbatim, scrubbed — no secrets/PII in the line):**

```
[2026-09-24 14:47:18] production.ERROR: [FAIL] OpenTelemetry export failed (telemetry batch
dropped): Export failure {"suppressed_since_last":0,
"source":"OpenTelemetry\\Contrib\\Otlp\\MetricExporter","signal":"metrics",
"otlp_endpoint":"localhost:5080/api/default",
"error_type":"GuzzleHttp\\Exception\\ConnectException",
"error_message":"cURL error 7: Failed to connect to localhost:5080 after 0 ms: Could not
connect to server ... for http://localhost:5080/api/default/v1/metrics"}
```

* **Exact counts and windows:**

| window | what was running | `[FAIL] OpenTelemetry export failed` lines |
|---|---|---|
| fix flush-storm, ~254s (`15:13`–`15:17`) | 10 240 requests at c=32 | **1 588** over **127 distinct seconds** (mean ~12.5/s, peak **34/s**) |
| baseline cold-burst, ~169s | 10 000 requests at c=32 | 805 |
| `2026-09-24 14:00` (QA hour) | QA load | 1 516 |
| `2026-09-24 15:00` (QA hour) | QA load | 2 492 |

  Signal mix in the storm window: 1 088 `metrics`, 718 `traces`. The circuit breaker is working —
  162 `closed` / 56 `half` / 14 `open` transitions in the same window.

### Answer to the Team Lead's question: **load-dependent, not fixed-interval.**

Measured against the primary tree's `laravel.log` across the preceding days, counting the identical
line per clock hour:

```
2026-09-22 00h : 51      2026-09-24 01h : 8
2026-09-22 09h : 6       2026-09-24 02h : 2
2026-09-22 10h : 12      2026-09-24 06h : 2
2026-09-22 18h : 28      2026-09-24 13h : 8
2026-09-22 19h : 30      2026-09-24 14h : 1516   <- QA load starts
2026-09-22 20h : 44      2026-09-24 15h : 2492   <- QA load
2026-09-22 21h : 19
2026-09-23 14h : 27
```

Every hour not listed emitted **zero**. So on an ordinary day the rate is **2–51 lines per hour**,
and it only reaches ~1 500–2 500/hour when a load test is running. Export is driven by request/batch
activity, not by a timer, and the circuit breaker damps it further.

**Correct framing for filing:** *"noisy under load — it buries real errors in QA and load-test
windows"*, **not** *"continuously burning disk in every environment where OpenObserve is down."*
An idle or low-traffic environment with OpenObserve down costs a few dozen lines an hour, which is
not a disk problem.

The reason it still matters is **signal quality, not volume**: because `SetRequestId` shares log
context, each of these lines carries a `correlation_id`. Any AC phrased as *"no `production.ERROR`
correlated to this `X-Request-Id`"* — AC3 here, and any future AC written the same way — is
therefore literally unsatisfiable on **every** branch, independent of the code under test. That is
what makes it worth a ticket at all.

## E. `followups[]`

1. **Put the working concurrency invocation in the profile's QA-drivers section** (see §F below for
   the exact text). The next backend-concurrency ticket must not re-derive it.
2. **Record the flush-interleave amplifier as the reusable recipe** for cache-table contention
   repros (see §G).
3. **The ticket's "Affected areas" is wrong** — it names
   `Admin/app/Http/Controllers/Api/V1/StoreController.php`, which caches nothing. The defect lives
   in the framework cache-write path reached by `throttle:v1-total` / `throttle:v1-blanket`.
   `get-stores/all` is merely the busiest v1 route. Worth correcting on the ticket so a future
   reader does not chase the controller.
4. **The ticket's scope-out line is now moot and should say so.** It reserves *"a general audit of
   every cached endpoint's deadlock exposure"* as a followup, but the fix registers app-wide via
   `Cache::extend('database', …)`, so **every** database-cache caller is already covered — not just
   this endpoint. Leaving the line as written implies residual exposure that does not exist.
5. **A `[WARN] cache write deadlock retried` rate is worth alerting on.** It is now the only signal
   that contention is happening at all; if it ever climbs toward
   `[FAIL] … retries exhausted`, the 3-attempt bound is too small for that load.

## F. `drift[]`

1. **`PHP_CLI_SERVER_WORKERS=<n> php artisan serve` is a FALSE-PASS TRAP on this host.** Documented
   nowhere, load-bearing everywhere a concurrency AC is tested. **Measured, not inferred:**

   ```
   artisan serve, PHP_CLI_SERVER_WORKERS=4:
     PARALLEL_8_WALL=1.165s   SERIAL_8_WALL=1.179s     -> zero overlap, fully serialised
     ps: exactly ONE `php -S` process, no forked children
   ```

   `Illuminate/Foundation/Console/ServeCommand.php:100` resolves the value with
   `transform((int) env('PHP_CLI_SERVER_WORKERS', 1), …)` and then merges it into the subprocess
   environment at line 189. The variable is **not** in `ServeCommand::$passthroughVariables`
   (lines 79–94), and `env()` did not resolve it from an exported shell variable in a
   non-interactive agent shell, so it silently falls back to 1 worker. **Exit code 0, plausible
   output, single-threaded server** — a two-curl repro therefore passes on broken code.

   **Working invocation — verified, use this verbatim:**

   ```bash
   cd <tree>/Admin/public && PHP_CLI_SERVER_WORKERS=32 php -S 127.0.0.1:<port> ../server.php
   ```

   (`Admin/public` as cwd and `../server.php` as the router are exactly what `artisan serve`
   itself uses.) Verified two ways, and **both checks should be repeated by any future run before
   trusting a concurrency result**:

   * `ps -ax -o pid,ppid,command | grep 127.0.0.1:<port>` → **32 children** under one parent, not one process;
   * timing: `PARALLEL_8_WALL=0.733s` vs `SERIAL_8_WALL=1.825s` (2.5× overlap; the ratio is below
     32× because the DB, not PHP, is the bottleneck — overlap is the predicate, not speedup).

   A third, independent confirmation: `php -S` at `PHP_CLI_SERVER_WORKERS=4` forked 4 children
   under the identical shell that produced **zero** children under `artisan serve`. The difference
   is `artisan serve`, not the environment.

2. **Jira AC text matches the conductor's relayed brief exactly** — verified with one live
   `getJiraIssue` read. No AC drift.

3. **AC3 is literally unsatisfiable as written, on both branches** (per §D). I applied the
   shape-scoped predicate the brief mandated and stated the divergence explicitly rather than
   quietly narrowing it.

4. **The primary tree was already dirty before this run** — `.codex/config.toml`,
   `Admin/config/system-addons.php`, `docs/apps/userapp/userapp-navigation-guide.md`,
   `tasks/.atlassian-sync.json` plus untracked dirs. Foreign, not mine. My baseline server did
   **not** rewrite `system-addons.php` (its `domain` still reads `127.0.0.1:8000`, another
   session's server). The fix worktree is clean. Both QA backends were torn down; no device lock
   and no APK were ever taken.

## G. The reusable repro recipe (the part that outlives this ticket)

**The prescribed shape is vacuous on this host.** Cold `php artisan cache:clear` + a simultaneous
burst produced, at n=250 c=32 × 40 bursts:

| branch | requests | non-2xx | `1213` lines |
|---|---|---|---|
| **unpatched** `feat/human-qa-uiux` @ `385df54ed` | 10 000 | 0 | 0 |
| patched `a385e2217` | 10 000 | 0 | 0 |

Both green. A pass built on that shape proves nothing — the unpatched code passes it too. **Any
concurrency QA that does not first show the defect on the base branch is reporting noise.**

**Why it is vacuous:** on a cold table every request runs the *same* `add` → `increment` sequence
in the *same* order on the *same* two keys. Uniform lock ordering does not deadlock; it queues.
A cycle needs two statements acquiring the same rows in *opposite* order.

**The amplifier that does reproduce it** — interleave the cache **flush** *into* the load, so
`DELETE FROM cache` (whole-table, reverse index order) races `insert ignore into cache`:

```bash
for r in $(seq 1 "$ROUNDS"); do
  ( for k in $(seq 1 6); do (cd "$TREE/Admin" && php artisan cache:clear >/dev/null 2>&1); done ) &
  FLUSHER=$!
  ab -n 250 -c 32 -s 60 -q "$URL" > "$OUT/ab-$r.txt" 2>&1   # n <= 300 so a 429 can never be
  wait $FLUSHER                                              # mistaken for a 500
done
```

Yield on the unpatched baseline: **11** `SQLSTATE[40001] … 1213` ERROR lines and a real
**HTTP 500** across ~10 000 requests. Ten of those events, reproduced against the fix, came back
**200** with a `[WARN]` line each.

This is **not** an artificial stressor. Any `business_settings` save, `cache:clear` on deploy, or
settings edit flushes the cache while traffic is in flight — the same interleave, in production.

**Method notes for whoever reuses this:**

* Keep each burst **≤ 300 requests** (the `v1-blanket` cap) so a `429` can never be misread as the
  `500` you are hunting.
* Prefer `ab` (present at `/usr/sbin/ab`) over backgrounded `curl` fan-out for volume. 100
  simultaneous backgrounded curls **killed the server** mid-run here and returned `code=000` for
  2 840 of 3 000 requests — an instrument failure that must not be read as a product result.
  Use `curl` only where you need per-request status + `X-Request-Id`, and keep it at c≈32.
* Scope the log by **byte offset** (`wc -c` before, `tail -c +$OFF` after), not by `tail -n`.
  On a shared tree it is the only way to attribute lines to your own window, and it captures
  everything written in it. Note `wc -c <file` emits leading spaces on macOS — `tr -d ' '` it or
  `tail -c +` fails with *"illegal offset"*.
* **Match the error-line SHAPE, never the substring `deadlock`.** The fix's `[WARN]` line names the
  deadlock it absorbed, so a substring grep fails a *correct* fix. The predicate that works:
  a `production.ERROR` whose payload is a `QueryException` on the `cache` table.
* **Prove the two trees differ before trusting either result:**
  `php artisan tinker --execute='echo get_class(Cache::getStore());'` →
  `App\Cache\DeadlockRetryingDatabaseStore` on the fix, `Illuminate\Cache\DatabaseStore` on the base.
