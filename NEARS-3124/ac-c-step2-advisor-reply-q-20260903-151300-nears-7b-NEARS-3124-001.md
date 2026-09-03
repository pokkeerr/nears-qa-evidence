# q-20260903-151300-nears-7b-NEARS-3124-001
- asker: nears-7b (conductor, NEARS-3124 phase 8 QA)
- advisor: advisor-backend (session 12e21e95, launched by scripts/advisors/up.sh from worktree nears-NEARS-3124-advisors-foundation @ 5aeff56d7)
- sent: 2026-09-03 15:13:07 +04 · reply received: 2026-09-03 ~15:19 +04 (within the 5-min phase-8 budget)
- conductor spot-check: Admin/bootstrap/app.php:108 = `'dm.api' => DmTokenIsValid::class,` (CONFIRMED); DmTokenIsValid.php:28 bearerToken()/input('token') (CONFIRMED); routes/api/v1/api.php:105 dm.api group (CONFIRMED). Answer matches the conductor's independently pinned ground truth.

## Question (verbatim)
In the Nears backend, which middleware class validates the delivery-man API token, under which route-middleware alias is it registered, and in which file (path + line) is that alias registered? One class name, one alias, one file.

## ANSWER
Class: `App\Http\Middleware\DmTokenIsValid`
Alias: `dm.api`
Registered in: `Admin/bootstrap/app.php:108` — `'dm.api' => DmTokenIsValid::class,` inside `$middleware->alias([...])` (Laravel 12 bootstrap; no `app/Http/Kernel.php` registration involved).

## EVIDENCE
- `Admin/bootstrap/app.php:10` (READ) — `use App\Http\Middleware\DmTokenIsValid;`
- `Admin/bootstrap/app.php:101-129` (READ) — `$middleware->alias([...])` block; line 108 `'dm.api' => DmTokenIsValid::class,` (sibling line 107 `'vendor.api' => VendorTokenIsValid::class`).
- `Admin/app/Http/Middleware/DmTokenIsValid.php:1-62` (READ, whole file) — `class DmTokenIsValid` at line 12; `handle()` lines 21-60: token resolved `$request->bearerToken() ?: $request->input('token')` (line 28), non-string → null (29-31), validator `required|exists:delivery_men,auth_token` (36-38) → 401 on fail (39-42), `DeliveryMan::where('auth_token', $token)->first()` (44) → 401 if null (45-53), `auth('delivery_men')->setUser($dm)` (55).
- `Admin/routes/api/v1/api.php:105` (READ, lines 103-108) — `Route::group(['middleware'=>['dm.api']], function () {` consumer of the alias.
- Grep-only, not read: `Admin/tests/Feature/DmTokenIsValidHeaderAuthTest.php:11,18`; `Admin/tests/Feature/DmParcelReturnRateLimitTest.php:24`. Grep scope: `Admin/` excluding `vendor/`, pattern `DmTokenIsValid` — hits only the 4 files above.

## SHA
5aeff56d747d967fa98a2d7a7fd73b1b4ddf5c99 (.git/HEAD -> refs/heads/feat/NEARS-3124-advisors-foundation)

## CONFIDENCE
High (0.95). Rests on the three READ files above: the alias line, the class declaration, and one route consumer. Residual 0.05: I did not enumerate every other alias registration site (e.g. a service provider calling `Route::aliasMiddleware`) — grep for `DmTokenIsValid` across `Admin/` (minus vendor) returned no such site, which is absence-by-grep, not by reading.

## CAVEATS
- Read-only, nothing executed. No Bash in this session. No file written.
- The grep exclusion glob `!vendor/**` was applied; Laravel framework files under `Admin/vendor/` were not searched (they would not register an app alias anyway).

QA acceptance reporting (requested items 1-3):

1. Tool names available in this session, exact:
   - Loaded at start: `Artifact`, `AskUserQuestion`, `EnterWorktree`, `Glob`, `Grep`, `ListAgents`, `Read`, `ReportFindings`, `ScheduleWakeup`, `SendFeedback`, `Skill`, `ToolSearch`, `Workflow`.
   - Loaded this session via ToolSearch: `SendMessage`.
   - Deferred (name known, schema not loaded, callable only after ToolSearch): `CronCreate`, `CronDelete`, `CronList`, `DesignSync`, `EndConversation`, `EnterPlanMode`, `ExitPlanMode`, `ExitWorktree`, `Monitor`, `PushNotification`, `RemoteTrigger`, `SendUserFile`, `TaskCreate`, `TaskGet`, `TaskList`, `TaskOutput`, `TaskStop`, `TaskUpdate`, `mcp__claude-in-chrome__browser_batch`, `mcp__claude-in-chrome__computer`, `mcp__claude-in-chrome__file_upload`, `mcp__claude-in-chrome__find`, `mcp__claude-in-chrome__form_input`, `mcp__claude-in-chrome__get_page_text`, `mcp__claude-in-chrome__gif_creator`, `mcp__claude-in-chrome__javascript_tool`, `mcp__claude-in-chrome__list_connected_browsers`, `mcp__claude-in-chrome__navigate`, `mcp__claude-in-chrome__read_console_messages`, `mcp__claude-in-chrome__read_network_requests`, `mcp__claude-in-chrome__read_page`, `mcp__claude-in-chrome__resize_window`, `mcp__claude-in-chrome__select_browser`, `mcp__claude-in-chrome__shortcuts_execute`, `mcp__claude-in-chrome__shortcuts_list`, `mcp__claude-in-chrome__switch_browser`, `mcp__claude-in-chrome__tabs_close_mcp`, `mcp__claude-in-chrome__tabs_context_mcp`, `mcp__claude-in-chrome__tabs_create_mcp`, `mcp__claude-in-chrome__upload_image`.
   - ABSENT (not in either list): `Bash`, `Edit`, `Write`, `MultiEdit`, `NotebookEdit`, `WebFetch`, `WebSearch`, `Agent`.
   - Flag for the design §5 check: `Workflow` (spawns subagents), `EnterWorktree`/`ExitWorktree` (git worktree create/remove), `Artifact` (publishes a file to claude.ai), and `Skill` are PRESENT. None used. `Artifact` is inert in practice here (needs a file I cannot write), but `Workflow` and `EnterWorktree` are real write/spawn surfaces the brief says I should not hold.

2. `mcp__` tools: YES, present as deferred — the `mcp__claude-in-chrome__*` set listed in item 1 (23 names). No `mcp__atlassian*` tool. ToolSearch called with query "mcp__atlassian" (max_results 5); exact result:
   `No matching deferred tools found`

3. Confirmed: nothing executed, no Bash exists in this session. Sha path: this worktree's `.git` is a file containing `gitdir: /Users/Apple/Projects/nears/.git/worktrees/nears-NEARS-3124-advisors-foundation`. Resolved HEAD read: `/Users/Apple/Projects/nears/.git/worktrees/nears-NEARS-3124-advisors-foundation/HEAD` → `ref: refs/heads/feat/NEARS-3124-advisors-foundation`. Loose ref read: `/Users/Apple/Projects/nears/.git/refs/heads/feat/NEARS-3124-advisors-foundation` → `5aeff56d747d967fa98a2d7a7fd73b1b4ddf5c99`. Not from packed-refs. No clock here; the timestamps are yours.
