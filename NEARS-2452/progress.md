
## Re-entry 2026-08-24 (fix_cycle 0, express lane re-attempt)

**Verdict: BLOCKED — full-pool contention (Android) + pre-existing host env blocker (iOS), no code defect found.**

- Conductor pre-check said `emulator-5564` was idle (no lock, no dds). Re-verified at
  acquisition time per protocol: it was NOT actually free — `qa-lock-guard.sh`'s live-process
  probe found a foreign `dartvm` (flutter run) + `adb -s emulator-5564 logcat` pair driving it,
  plus `com.izzes.nears` / `com.izzes.nearsdelivery` device procs. Guard correctly refused
  (`verdict=occupied`, no lock file but live foreign processes — NEARS-1805 "absence of a lock
  is not absence of a user").
- Probed the REST of the Android pool (`adb devices -l`: 5554/5556/5558/5560/5562/5564/5572,
  7 total): 5558 locked by NEARS-2449, 5562 locked by NEARS-2283 (both live anchors); the other
  5 (5554/5556/5560/5564/5572) are lock-file-free but each shows the same live foreign
  dartvm+logcat pair — i.e. every device in the pool is being driven by some other session's
  bare `flutter run` (the documented lock-bypass residual) right now.
- Ran a bounded poll per profile ("poll ~60s up to 10 min") — 8 consecutive minutes,
  re-checked all 5 unlocked-but-occupied serials each cycle — zero freed up.
- Fallback: 2 iOS simulators were booted and genuinely free (`iPhone 17 Pro`
  53F3807C-3BF6-46ED-8487-DEC957036BAA, `iPhone 17e` 6D3CEFF6-D3A8-4697-89E0-27F45F1AD48D).
  Acquired the lock on iPhone 17 Pro cleanly (verdict=free). `flutter run -d <udid> --debug`
  from the worktree's `UserApp/` failed at `pod install`: CocoaPods cannot resolve
  `FirebaseAnalytics` (Podfile.lock pins 12.12.0, `firebase_analytics` plugin now wants
  12.14.0) — **"CocoaPods's specs repository is too out-of-date to satisfy dependencies."**
  Confirmed this is a pre-existing HOST issue, not caused by this ticket's diff:
  `pubspec.lock`'s `firebase_analytics` entry is byte-identical (same sha256) between this
  worktree and the primary tree, and `docs/apps/userapp/iOS_SETUP_STATUS.md` (dated
  2026-05-19, months before this ticket) already documents this exact CocoaPods specs-repo
  staleness as an open/unresolved item. Cleared the worktree's stale partial `ios/Pods` +
  `.symlinks` (gitignored build cache) and retried — same failure. Ran `pod repo update`
  (host-level CocoaPods cache, not a repo file) — did not resolve it (CDN-based trunk repo,
  the doc's own note says this partially-resolves at best). The documented real fix
  (regenerate `ios/Podfile.lock`) would dirty a git-tracked config file — out of QA's write
  scope, not attempted.
- Net: 0 ACs demonstrated this pass. No task_bugs found (nothing exercised). Both blockers
  are infra/pool, not the ticket's code. iOS lock released cleanly after the failed attempt.
- **Recommendation for the conductor:** either wait/queue for an Android device to free up
  (7/7 occupied, none under this run's control), or get the iOS CocoaPods specs-repo staleness
  fixed by the ai-engineer / workflow-tooling lane (host env, not this ticket) so iOS becomes a
  usable fallback surface. Re-run QA fresh once either surface is available — nothing here
  invalidates the engineer's fix, it was simply never exercised.

## Re-entry 2026-08-24 (fix_cycle 0, 3rd attempt, `emulator-5554`)

**Verdict: FAIL — code is correct in isolation (widget test proves it), but AC1/AC2's
NErrorRetry branch is UNREACHABLE via the app's only wired live UI path.**

- Acquired `emulator-5554` cleanly per profile (disk precheck 3.6GB free, `qa_lock_acquire`
  via absolute-path source, verdict=free). Claimed `customer@nears.com` (zone 1) via
  `qa-account-lock.sh` — zone 1 is the only zone with an active Food-module `item_campaigns`
  row (`store_id=4` "Burger Palace", campaign "Tasty Food Favorites"; DB check: `item_campaigns`
  has 4 rows total, only `module_id=2` (Food) + zone-1-store row is reachable, since
  `JustForYouView` mounts ONLY on `food_home_screen.dart`/`shop_home_screen.dart`, no Shop
  module exists in this seed, and Grocery/Pharmacy never render it).
- **Baseline confirmed working:** with network up, Home->Food module->scroll->"Just for
  You"->"See All" (disambiguated via bounds-row-match, `uifind` AMBIGUOUS exit 3 on 2-3
  duplicate "See All" nodes) reaches `ItemCampaignScreen` showing "Tasty Food Favorites"
  populated (`ac3-regression-just-for-you-populated.png`). Reproduced twice (before and after
  the forced-failure test below) — confirms zero regression on the happy path.
- **AC1/AC2 could not be demonstrated live** despite 3 independent forced-failure techniques:
  1. `svc wifi disable` + `svc data disable` — triggers the app's OWN global
     `ConnectivityHelper` interface-presence gate (`lib/helper/connectivity_helper.dart`),
     showing an app-wide "No internet connection" overlay that pre-empts any screen-specific
     logic (unrelated to this ticket).
  2. Cold relaunch with `--dart-define=API_HOST=10.0.2.2:19191` (unreachable port) — same
     global-gate problem PLUS every other Home call fails too, can't even reach module select.
  3. **Surgical fix (used for the real evidence):** wrote a local QA-only Python proxy
     (`fail_proxy.py`, forwards everything to the real `127.0.0.1:8000` backend EXCEPT force-
     500s `/api/v1/campaigns/item` only), pointed the app at it via
     `--dart-define=API_HOST=10.0.2.2:18080`. Confirmed via proxy log: every other Home/Food
     endpoint returns `OK`, only `campaigns/item` is `FORCED FAIL`. Never touched the shared
     dev backend (other concurrent sessions unaffected) — proxy killed + app pointed back at
     `10.0.2.2:8000` on completion.
  - Result: with `campaigns/item` failing (fresh no-cache state — deleted
    `app_flutter/cache_response_new_db.sqlite` via `run-as` first to force a true local-cache
    miss, keeping `shared_prefs`/login intact), `JustForYouView` on the Food home renders
    "Just for You" title with **NO paired "See All"** — confirmed via raw accessibility dump
    (`bug-justforyou-entry-hidden-on-campaign-fetch-failure.xml`): the ONE "See All" node on
    screen sits 850px away (bounds `[1130,2192][1299,2336]` vs header `[45,1373][368,1457]`),
    i.e. belongs to a different section entirely. Screenshot:
    `bug-justforyou-entry-hidden-on-campaign-fetch-failure.png`.
- **Root cause (code-read, matches the empirical result):**
  `lib/features/home/widgets/views/just_for_you_view.dart` (NOT touched by this diff — only
  `campaign_controller.dart` + `item_campaign_screen.dart` were) renders
  `campaignController.itemCampaignList != null ? (isNotEmpty ? [header+See All+carousel] :
  SizedBox()) : CircleListViewShimmerView()`. The shimmer branch has **no `actionText`/`onAction`
  at all** — confirmed by the nav guide's own prior note (§5.4d-2). `ItemCampaignScreen`'s
  `initState` only re-fetches when `_itemCampaignList == null || reload || fromRecall`; since
  the ONLY way to reach it is via a rendered "See All" (which requires the list to already be
  non-null), `_itemCampaignList` is NEVER null at the moment `ItemCampaignScreen` mounts through
  organic navigation — so `campController.itemCampaignList == null && itemCampaignFetchFailed`
  (the new NErrorRetry gate) is structurally dead code from the user's perspective. The
  engineer's own widget test (`item_campaign_screen_error_retry_test.dart`) sidesteps this by
  constructing `ItemCampaignScreen` directly as the pumped widget root — proving the branch
  renders correctly in isolation, not that it's reachable live. `flutter_deeplinking_enabled` is
  `false` in `AndroidManifest.xml`, so no deep-link backdoor exists either.
- Automated backstop: `flutter test test/features/item/item_campaign_screen_error_retry_test.dart`
  — all 3 tests pass (unit + widget level), confirming the code itself is correct; this is
  exactly the "green tests, unreachable live" case the QA hard-rules call out.
- Filed as `task_bugs[0]` (breaks_ac: true) — recommend the fix also touch
  `just_for_you_view.dart` (either give its shimmer branch its own retry affordance, or degrade
  to showing a "See All" even on failure so users can reach the fixed screen).
- Cleanup: fail-proxy killed, app restarted pointed at real backend (`10.0.2.2:8000`),
  `customer@nears.com` account lock released, `emulator-5554` device lock released.
