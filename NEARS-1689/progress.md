# NEARS-1689 — QA evidence (phase [8], first full pass)

**Verdict: PASS** (2 non-blocking doc `task_bug`s filed, neither breaks an AC)

- Worktree `/Users/Apple/Projects/nears-NEARS-1689-qa-lock-liveness`, branch `feat/NEARS-1689-qa-lock-liveness`, HEAD `01b545c7`, base `feat/userapp-reskin2` @ `b41c99fd`.
- **Device: N/A.** `QA_LOCKS_DIR` redirects the whole protocol to a temp dir, so every AC is demonstrable with zero emulators, zero APKs, zero `adb`. No pool device was locked or booted. Build-freshness discipline (md5 of the installed artifact, live-isolate symbol probe) is therefore **not applicable** — there is no installed artifact, not "skipped".
- The real pool dir `$HOME/.nears/qa-locks/` was **read only** (`ls`), never written. All QA locks used `QA_LOCKS_DIR=<scratch>/ac1locks`, removed at teardown.
- **No screenshots.** AC4/AC5 are doc-vs-code parity, not UI; the visual-verification channel was correctly not opened (0 images this run).

## Per-AC results

| AC | Verify tag | met | Evidence | Logs |
|----|-----------|-----|----------|------|
| AC1 — a live run's lock reads *held* from a second concurrent session, across ≥2 separate Bash calls | `[behav]` | **true** | Bash call 1: `qa_lock_acquire ac1-serial NEARS-1689` → owner pid **39147** (`pid_kind: anchor`, `ps comm=claude`). Bash call 2 (fresh shell, `$$`=31783): call 1's `$$`=**28953 is DEAD**, recorded owner **39147 is ALIVE** — the defect and the fix side by side. Foreign checker (reparented to pid 1; ancestor chain = `31793` only, anchor **not** in it) → `rc=1` "BLOCKED — held by another LIVE QA session", read back in Bash call 3. Second foreign observation in Bash call 5 (chain `33632`) → still `rc=1`. | clean |
| AC2 — a genuinely dead owner still reads reclaimable, bounded | `[behav]` | **true** | Sentinel-path acquire gave a killable owner **33612**; foreign checker while alive → `rc=1`. Killed it (`alive_before=YES`, `alive_after=NO`); foreign checker → `rc=0` "stale lock (pid 33612 dead), reclaimable" immediately. Over-correction guard: `qa_lock_acquire` then **actually reclaimed** it (`RECLAIM_OK`, owner.json now `NEARS-1689-RECLAIM`), no orphan `.reclaimed.*` dir left. | clean |
| AC3 — `qa_lock_check` returns held for case 1, permits acquisition for case 2 | `[behav]` | **true** | Called directly in both states: case 1 → `rc=1` + the full BLOCKED banner naming serial/key/pid/lock file; case 2 → `rc=0` + reclaimable message. Self-check from the owning session → `rc=0` (no self-block). Integration: `scripts/qa-run.sh UserApp fake-serial-1689` against a foreign live holder → **rc=1, refused before `exec flutter`** (no flutter process spawned). | clean |
| AC4 — `nears-qa.md` §"Device pool" and `qa-lock-guard.sh` describe the same scheme | doc parity (not UI) | **true** | Claim-by-claim: API `qa_lock_acquire <serial> [key]` / `qa_lock_release <serial>` / `qa_lock_check <serial>` ✓; `{pid, pid_kind, anchor_started, key, started}` ✓ (`_qa_lock_write_owner`); temp-file + `mv` ✓; `mkdir` is the first op (TOCTOU) ✓; `pid_kind` anchor\|sentinel + the printed `export QA_LOCK_OWNER_PID=…` ✓ (both observed live); `anchor_started` optional ✓; release refuses loudly on a foreign live lock ✓ (observed) and never kills an `anchor` pid ✓ (my harness survived); same-session different-key **warns, never blocks** ✓ (observed `rc=0` + WARNING); all three launchers call the guard ✓. One vestigial clause filed as a non-blocking bug (below). | clean |
| AC5 — disk floor matches at ≥800MB in both files | `[behav]` | **true** | `.claude/agents/nears-qa.md:42` = "**≥800MB (819200 KB) free**"; `.claude/workflow-profile.md:27` = "**≥800MB free floor**". Identical. `docs/workflow/workflow.json` + `tasks/workflow.json.golden` also updated to `>=800MB`. | clean |

## Automated backstop

`bash scripts/qa-lock-guard.test.sh` — **67 assertions, PASS, exit 0**, exit code captured directly (not through a pipe).
Determinism: 3 consecutive runs, all `exit_code=0`, all `assertions executed: 67`, `ok_lines=67`, `fail_lines=0` (3-4s each).
Assertion count **predicted as 67 from reading the suite before running it**, and it matched.

`shellcheck` 0.11.0: `scripts/qa-lock-guard.sh` clean (rc=0). `scripts/qa-lock-guard.test.sh` clean under `shellcheck -x` (rc=0); without `-x` it emits 5 `SC1091` *info* notices ("Not following: qa-lock-guard.sh"), which is the expected artifact of an unfollowed `source`, not a finding.

Sourced-library invariants (verified independently of the suite, not just via P1/P2):
`bash -c 'set -euo pipefail; before=$(set +o); source guard; after=$(set +o)'` → `OPTIONS_UNCHANGED`, `SHELL_SURVIVED`, rc=0; the busy path under `set -e` left the caller alive; the guard has **only function definitions at top level** and **zero real `exit` statements** (its 2 `exit` string matches are both in comments).

## Declared residual — confirmed, not a FAIL

`scripts/run_apps.sh:5` hardcodes `ROOT_DIR="/Users/Apple/Projects/nears"` and line 14 derives `LOCK_GUARD` from it, so from the worktree it sources the **primary tree's unfixed** guard. Verifiable only post-merge. Honestly declared in `docs/solutions/NEARS-1689-qa-lock-liveness.md` (lines 235-238, 270-271). Its only call is `qa_lock_check <serial>`, whose signature and semantics are unchanged by this branch, so the post-merge behaviour is the guard's — not a false green.
`scripts/qa-run.sh` and `scripts/qa-reconnect.sh` use their own `SCRIPT_DIR`, so both exercise the **fixed** worktree copy; qa-run.sh was proven live above.

## Traps avoided (each was a real prior failure on this ticket)

1. Foreign checker is **reparented to pid 1** and records its own ancestor chain, so foreignness is proven, not assumed — a child of my own shell would be a descendant of my anchor and correctly read as self.
2. Every backgrounded owner was liveness-checked (`kill -0`) **before** being relied on as a "live foreign holder".
3. The hand-written fixture's `anchor_started` was produced by the guard's own `_qa_lock_proc_started`, not raw `ps -o lstart=`.
4. No pipelines around backgrounded sentinels; every result crossed Bash calls through **files**.
5. Counts were **predicted before measuring** (67 assertions), and each grep's output was read as lines, never inferred.
