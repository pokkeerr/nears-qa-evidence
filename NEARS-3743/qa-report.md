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
