# NEARS-2828 — QA evidence (phase [8], device-free, surface = GitHub Actions)

Verdict: **PASS** · worktree `/Users/Apple/Projects/nears-NEARS-2828-ci-triggers` · branch `feat/NEARS-2828-ci-triggers` · HEAD `9e7553ad08ce75d0f9f87fdb7123ef3c084253a3` · base `feat/userapp-reskin2` @ `f37e27c0f` · fix_cycle 0 · QA window 2026-09-03T19:42Z → 20:05Z.

## AC1 [behav] — remote + integration branch re-confirmed; policy stated in the solution doc — PASS
- `git -C /Users/Apple/Projects/nears remote -v` → `origin https://github.com/pokkeerr/nears.git` (fetch + push)
- `git -C /Users/Apple/Projects/nears branch --show-current` → `feat/userapp-reskin2`
- Jira comment **17728** "[2] Team Lead solution doc — NEARS-2828" opens with `POLICY (decided): (a-glob) — push-based, local-merge workflow kept.` and carries the reasoning (§2 option table, §3 rejected alternatives), decided by advisor-workflow qid `q-20260903-190834-conductor-2828-NEARS-2828-001` (comment 17722), ratified at [2b] by advisor-product (comment 17723).

## AC2 [behav] — both workflows fire for a real commit on the integration-branch line — PASS (recorded exactly per the advisor-product ruling)
`GET /repos/pokkeerr/nears/actions/runs?head_sha=9e7553ad08ce75d0f9f87fdb7123ef3c084253a3` → `total_count: 2`

| Run | Workflow | event | head_branch | status | conclusion | created → updated |
|---|---|---|---|---|---|---|
| https://github.com/pokkeerr/nears/actions/runs/33797721568 | DLS CI | push | feat/NEARS-2828-ci-triggers | completed | **success** | 19:39:32Z → 19:46:09Z |
| https://github.com/pokkeerr/nears/actions/runs/33797721411 | UserApp CI | push | feat/NEARS-2828-ci-triggers | completed | **failure** | 19:39:32Z → 20:03:05Z |

DLS CI steps (job `nears-dls` 100789334481): Checkout, Set up Flutter, Install deps, Catalog up to date (blocking), Analyze, Test (contract/widget, blocking), Golden tests (informational) — all `success`. Job `widgetbook` 100789334825: Install deps, Analyze, Test — all `success`.

UserApp CI (job `analyze-and-test` 100789333901): **fired; conclusion=failure; red at step 7 "Test"**; steps 1–6 (Set up job, Checkout, Set up Flutter, Install dependencies, Check vertical layering, Analyze) all `success`; step 8 Golden tests `skipped` (downstream of the red step). **Cause = pre-existing NEARS-3117 test regression**: reporter tally `##[error]5633 tests passed, 26 failed.` — all 26 `❌` markers in `test/features/home/home_app_bar_switcher_test.dart`, exception `type 'Null' is not a subtype of type 'bool'` thrown building `HomeAppBar`, stack `#0 _MockSplashService.hasSeenModuleIdsBaseline (…/home_app_bar_switcher_test.dart:42:7)`. Identical to the local baseline recorded in comment 17728 (5633/26, same file). Byproduct Bug to be filed by the conductor; NOT a defect of this change. **UserApp CI is not green.**

Negative shape (history before this change): `event=push` runs ever = 5 → the 2 above plus 3 older ones, all DLS CI on `main` ×1 (31899056793) / `feat/init-storybook` ×2 (30766213575, 30763833958) — the old branch list never matched the integration branch. `event=pull_request` on `feat/userapp-reskin2` = 118 runs via PR #37; most recent 3 pairs: 4a99c5338 (DLS 33641076301 success / UserApp 33641076292 failure), ca0c954c5 (33638515282 success / 33638515281 failure), 3854e31d2 (33589614756 success / 33589614902 failure). `pull_request:` trigger still present in both workflow files after the change (YAML parse below).

## AC3 [behav] — audit "never executed" finding superseded — PASS
`docs/design/audit-f2-f7.md` in the worktree:
- L484 `### 7.1 Execution evidence` → table → **L495** `**Superseded by NEARS-2828 (2026-09-03).** …both workflows DID execute during F7 via the pull_request trigger on the open PR #37 … verified 2026-09-03 via the read-only GitHub REST API GET /repos/pokkeerr/nears/actions/runs … latest at 4a99c5338: DLS CI success run 33641076301, UserApp CI failure run 33641076292, both event=pull_request). "Never" WAS true for the push trigger … https://nears-izzes.atlassian.net/browse/NEARS-2828` → L497 `### 7.2 Mutation tests` (note sits directly under the §7.1 table, before 7.2).
- L20 Check-6 row ends `— CI rows superseded by NEARS-2828, see §7.1 note`.
- L667 `- C6-2. … (answered by NEARS-2828)`.

## QA Test Scope checks
1. YAML (`yaml.safe_load`, key `True`): dls-ci → `pull_request.paths [packages/nears_dls/**, widgetbook/**, .github/workflows/dls-ci.yml]`, `push.branches ['**']`, same paths. userapp-ci → `pull_request.paths [UserApp/**, .github/workflows/userapp-ci.yml]`, `push.branches ['**']`, `push.paths [UserApp/**, .github/workflows/userapp-ci.yml]`. PASS
2. `git diff --stat feat/userapp-reskin2` → exactly 4 files: dls-ci.yml, userapp-ci.yml, docs/design/audit-f2-f7.md, docs/platform/dls-storybook.md (+23/−13). PASS
3. `doc-citation-resolve.sh --all` → `PASS … 393 citation(s) across 1193 doc(s)`; `doc-citation-content.sh --all` → `PASS … 38 doc(s) asserted, 71 citation(s) asserted`. PASS
4. `git diff feat/userapp-reskin2 -- .github/workflows/backend-isolation-ci.yml` → 0 bytes. PASS
5. Automated backstop: none beyond 1–3 (no product code; the live Actions runs ARE the executable check).

## Artifacts in this folder
`runs-summary.txt`, `steps.txt`, `jobs-33797721568.json`, `jobs-33797721411.json`, `workflow-diff.txt`, `bug-nears3117-userapp-ci-test-red.log`, `progress.md`.
