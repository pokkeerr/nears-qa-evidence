# q-20260903-153000-nears-7b-NEARS-3124-002
- asker: nears-7b (conductor, NEARS-3124 phase 8 delta re-QA, sub-task NEARS-3133 acceptance)
- advisor: advisor-backend (session 27200a9e, launched by scripts/advisors/up.sh with the cycle-2 §5 line from worktree nears-NEARS-3124-advisors-foundation @ 076911573)
- sent: 2026-09-03 15:29:42 +04 · reply received: ~15:33 +04 (inside the 5-min phase-8 budget)
- conductor spot-check: Admin/bootstrap/app.php:107 `'vendor.api' => VendorTokenIsValid::class,` CONFIRMED; VendorTokenIsValid.php:12 class decl CONFIRMED; app.php:25 import CONFIRMED; routes/api/v1/api.php:169 vendor.api group CONFIRMED. Answer matches the conductor's independently pinned ground truth.
- TOOL-LOCK PROBE RESULT (SEC-2 / NEARS-3133): available = Glob, Grep, ListAgents, Read, ToolSearch (+ deferred SendMessage, EndConversation); ABSENT = all 19 deny-listed names; mcp__* = NONE (ToolSearch "mcp__claude-in-chrome" and "mcp__" both "No matching deferred tools found"). Residual: EndConversation (deferred, inert).

## Question (verbatim)
In the Nears backend, which middleware class validates the VENDOR (store owner) API token, under which route-middleware alias is it registered, and in which file (path + line) is that alias registered? One class name, one alias, one file.

## ANSWER
Class: `App\Http\Middleware\VendorTokenIsValid` (`Admin/app/Http/Middleware/VendorTokenIsValid.php:12`).
Alias: `vendor.api`.
Registered in: `Admin/bootstrap/app.php:107` — `'vendor.api' => VendorTokenIsValid::class,` inside `$middleware->alias([...])` (lines 101–129), import at line 25.

Supporting: the alias is consumed by the vendor API route group `Admin/routes/api/v1/api.php:169` — `Route::group(['prefix' => 'vendor', 'namespace' => 'Vendor', 'middleware'=>['vendor.api','actch:vendor_app']], ...)`. No legacy `Admin/app/Http/Kernel.php` exists (Glob returned no files), so `bootstrap/app.php` is the only alias registration point. The class reads `Authorization: Bearer` (line 38), requires a `vendorType` header (48–55), resolves `owner` via `Vendor::where('auth_token', $token)` (58) and `employee` via `VendorEmployee::where('auth_token', $token)` (77), arms the `vendor` / `vendor_employee` guards with `setUser` (73, 95–96), and fails closed with the 401 envelope on unknown `vendorType` (99–108).

## EVIDENCE
Read this session:
- `Admin/bootstrap/app.php` lines 1–130 (import line 25; alias block 101–129; `'vendor.api'` at 107; `'vendor'` => `VendorMiddleware` at 106 and `'dm.api'` at 108 for contrast).
- `Admin/app/Http/Middleware/VendorTokenIsValid.php` lines 1–114 (whole file; class decl line 12, `handle` 21–112).
- `Admin/routes/api/v1/api.php` lines 165–172 (route group at 169).
- `.git` (file, line 1: `gitdir: /Users/Apple/Projects/nears/.git/worktrees/nears-NEARS-3124-advisors-foundation`).
- `/Users/Apple/Projects/nears/.git/worktrees/nears-NEARS-3124-advisors-foundation/HEAD` line 1.
- `/Users/Apple/Projects/nears/.git/refs/heads/feat/NEARS-3124-advisors-foundation` line 1.
Grep only, not read:
- `VendorTokenIsValid` across `Admin/` (excluding `vendor/`): hits in `Admin/tests/Feature/Security/{VendorProfileStoreScopeTest,DeliveryManPreviewReviewsPiiTest,AiQuotaStoreIdIdorTest,VendorGuardSeedingTest,VendorItemGlobalScopeTest,DeliveryManPreviewNullGuardTest}.php`, `Admin/app/Http/Controllers/Api/V1/SearchController.php:329` (comment), plus the three read files above. Only ONE alias-registration hit (`bootstrap/app.php:107`).
- `vendor\.api` across `Admin/routes/`: single hit `api/v1/api.php:169` (then read).
- Glob `Admin/app/Http/Kernel.php`: no files found.

## SHA
0769115735ccfad277175b1ac278a98c2f04c925 (.git -> gitdir /Users/Apple/Projects/nears/.git/worktrees/nears-NEARS-3124-advisors-foundation; HEAD -> ref: refs/heads/feat/NEARS-3124-advisors-foundation; loose ref read from the main repo's `.git/refs/heads/`, not packed-refs)

## CONFIDENCE
High (0.97). Rests on the alias line and class file both read in full at this sha, a single grep hit for the alias registration, and the absence of `app/Http/Kernel.php`. Residual 0.03: `Admin/routes/api/v2/api.php` not grepped for `vendor.api` (out of the question's files_in_play); does not affect the three answers asked.

## CAVEATS
- Read-only, nothing executed. No Bash, no artisan, no DB query; the route-alias resolution is read from source text, not from `route:list`.
- Linked worktree: `.git` is a file; HEAD and the loose ref were read under the paths above (loose ref wins over packed-refs; packed-refs not consulted).
- `VendorMiddleware` (alias `vendor`, `bootstrap/app.php:106`) is the WEB Store-Panel session guard, not the API token guard — distinct class, distinct alias.

QA acceptance items for NEARS-3133:

1. Tool inventory, exact names available to this session:
   Loaded at start: `Glob`, `Grep`, `ListAgents`, `Read`, `ToolSearch`.
   Deferred (per the startup system-reminder), loadable via ToolSearch: `EndConversation`, `SendMessage`. `SendMessage` has been loaded this session (used for this reply); `EndConversation` remains deferred, not loaded.
   Total distinct tools: 7.
   ABSENT (not loaded, not deferred, not returned by any ToolSearch): `Bash`, `Edit`, `Write`, `MultiEdit`, `NotebookEdit`, `WebFetch`, `WebSearch`, `Agent`, `Workflow`, `EnterWorktree`, `ExitWorktree`, `Artifact`, `Skill`, `CronCreate`, `CronDelete`, `ScheduleWakeup`, `SendUserFile`, `RemoteTrigger`, `TaskStop` — all 19 named tools absent.

2. `mcp__*` tools: NONE exist, loaded or deferred. ToolSearch exists and was called twice this session, results verbatim:
   - query `mcp__claude-in-chrome` (max_results 10) -> `No matching deferred tools found`
   - query `mcp__` (max_results 10) -> `No matching deferred tools found`
   Note: the session system prompt contains generic "Claude in Chrome" guidance text naming `mcp__claude-in-chrome__*`, but no such tool is present or loadable; the guidance is inert.

3. Nothing executed: this session made only Read, Grep, Glob, ToolSearch and this one SendMessage call. No file written, no process spawned, no query run. Resolved HEAD path read for the SHA: `/Users/Apple/Projects/nears/.git/worktrees/nears-NEARS-3124-advisors-foundation/HEAD` (content `ref: refs/heads/feat/NEARS-3124-advisors-foundation`), resolved via the `.git` file's `gitdir:` line, then `/Users/Apple/Projects/nears/.git/refs/heads/feat/NEARS-3124-advisors-foundation` -> `0769115735ccfad277175b1ac278a98c2f04c925`.
