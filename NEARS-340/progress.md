# NEARS-340 QA progress — live evidence checkpoints
Device: emulator-5554 (Android 17) · build: worktree feat/NEARS-340-navbar-a11y @ 5387e1be · backend :8000 live multi_food_db
Pre-flight: baseUrl=http://10.0.2.2:8000 (real local backend) OK · order #152 pending for customer@nears.com OK · lock acquired.

## AC1 — logged-in WITH running order (#152 pending)
- [x] 5 tabs in a11y dump: Home/Categories/Search/Basket/Profile all content-desc non-empty, clickable="true"; Home selected="true"
- [x] Banner "Your Order is Pending Order #152" present, clickable; bounds [0,2479][1344,2725] vs nav top y=2728 → above nav, non-overlapping
- shot: ac1-banner-above-nav-5tabs.png
- [x] Tab tap with banner up: Profile tap → selected=true, banner persisted (NOT dismissed)
- [x] Banner tap → Order Tracking screen for #152 (shot: ac1-banner-tap-order-tracking.png)
- [x] Swipe-dismiss → banner gone, 5 tabs same bounds, ui_errors clean (shot: ac1-banner-swiped-nav-stays.png)
AC1: MET (live, not engineer-evidence — order #152 still pending so no order placement needed)

## AC3 partial (persistentContentHeight=0 path via dismissed banner)
- [x] content bottom y=2725 vs nav top 2728 → no blank strip; bottom edge: pixels below nav continuous surface + gesture pill (gesture-nav mode 2), no gap
## AC7 partial
- [x] §5.10 exact dump command runs, 5 tabs resolve clickable=true; defect(minor): grep over-matches (e.g. "Edit Profile") and drops selected/bounds attrs

## AC2 — logged-in, NO running-order banner (RESUMED RUN 2026-06-12, lock reclaimed pid 40425)
CAVEAT: true no-order state would require cancelling pending order #152 (DB mutation; parallel NEARS-338 QA run shares the DB → not done). Used the dismissed-banner state instead; code-verified identical render path: dashboard_screen.dart `hasRunningOrderSheet=false` for BOTH dismissed (`showBottomSheet=false`) and empty-orders → same persistentContentHeight:0 / SizedBox / enableToggle:false branch.
- [x] 5 tabs: class=android.widget.Button, content-desc Home/Categories/Search/Basket/Profile, clickable=true, Home selected=true, bounds y=2728-2920, no banner node in dump
- [x] Tab tap in no-banner state: Categories tap -> selected=true (shot: ac2-no-banner-categories-selected.png)
AC2: MET (with dismissed-banner caveat above)

## AC4 — TalkBack-style semantics
- [x] All 5 tabs: class=android.widget.Button (TalkBack announces "button"), content-desc = announced label, selected="true" only on active tab
- [x] Activation: clickable="true" = semantics tap action (ACTION_CLICK, what TalkBack double-tap invokes); full 5-tab cycle Search->Basket->Profile->Home each moved selected correctly; ui_errors clean
AC4: MET

## AC5 — header module-switcher
- [x] Grocery home: "Switch module" class=android.widget.Button clickable=true bounds [15,195][111,291]; tap -> module-selection screen (shot: ac5-module-selection-after-switch-tap.png)
- [!] FOOD home: app renders fine (shot: ac5-food-home-renders-but-a11y-dead-nears339.png) but a11y tree dies (uiautomator dump = 4 nodes, ui_list empty, no flutter errors) = KNOWN sibling bug NEARS-339, fix not on this branch -> regression_bugs lane, noted + moved on. Back from food home -> module selection (tree alive, 43 nodes) -> re-entered Grocery.
AC5: MET on grocery (food-home gap = NEARS-339, pre-existing on this branch)

## AC6 — regression sweep (part 1)
- [x] 5 tab switches incl Profile: Categories/Search/Basket/Profile/Home all moved selected= correctly, ui_errors clean
- [x] Back-press chain (multi-module zone): Home back#1 -> module selection (intended removeModule() path, dashboard_screen.dart:161-164), back#2 -> "Back press again to exit" toast (a11y-visible), rapid back#3 -> app exits to launcher. Double-back exit WORKS; intermediate module-selection hop is intended multi-module behavior, not a regression.
- [x] Cold restart (mcp launch_app, worktree build): banner RE-APPEARS ("Your Order is Pending Order #152" [0,2479][1344,2725]) + 5 tabs intact -> swipe-dismiss confirmed session-only (showBottomSheet in-memory), AC2 caveat behavior proven
- [~] Keyboard hides nav: ENVIRONMENT-LIMITED live — AVD has hardware keyboard, Gboard renders floating strip (mInputShown=true, zero inset) -> nav correctly STAYS (floating IME = no viewInsets; shot ac6-keyboard-state-probe.png). Docked IME not producible on this AVD. Verified instead by code-equivalence: identical `keyboardVisible` guard pre/post change (old `? SizedBox()` -> new `? null` on Scaffold.bottomNavigationBar). IME open->dismiss cycle: tabs same bounds, ui_errors clean. FOLLOWUP: widget test pinning viewInsets matrix.
- note: Search-tab field semantics thin (EditText node full-screen bounds, no label/hint exposed) — pre-existing, followup lane
- [x] Dark mode + Arabic RTL (banner up): nav row correctly MIRRORED (حساب تعريفي/Profile leftmost [0,2728] -> بيت/Home rightmost [1075,2728]), all 5 Arabic labels clickable=true, selected tracks taps; banner "طلبك هو قيد الانتظار طلب #152" [0,2479][1344,2725] stacked above nav non-overlapping (shot: ac6-dark-arabic-rtl-banner-stack.png)
- [x] 'تبديل الوحدة' (switch module, ar): Button clickable=true, RTL-mirrored to top-RIGHT [1233,195] (LTR: top-left [15,195]); tap -> module selection; re-entered grocery. ui_errors clean
- [x] Reverted to English + light; LTR nav restored clean
- [x] bn/es 'basket' raw-key fallback CONFIRMED pre-existing: 'basket' key absent from bn.json + es.json (all other nav keys + switch_module present in all 4 langs) -> tab label falls back to raw key "basket" in Bengali/Spanish. Regression lane (pre-existing), not this change.
- note: language-update flow + earlier removeModule() back-test reset the module -> Home shows module selection until a module is picked (intended multi-module behavior)

## AC2-guest — logged out
- [x] Logout flow (Profile > Logout > Yes) -> Guest User state; 5 tabs present + clickable=true, tap switches (Categories selected=true)
- [x] Login-suggestion sheet: pref 6ammart_login_suggestion is ONCE PER INSTALL (set true on first install, false after shown — splash_repository.dart:66-68,105), NOT "once per cold start" as guide §5.10 says -> guide wording fixed this run. Reproduced via run-as pref reset + cold start: sheet up ("Log in or sign up...", Login/Sign Up Button) -> nav buttons = 0 in dump = EXPECTED modal-barrier semantics (shot: ac2guest-login-sheet-tabs-hidden-expected.png)
- [x] Back-dismiss sheet -> all 5 tabs return: content-desc non-empty, clickable=true, Home selected=true; Basket tap -> selected=true (shot: ac2guest-tabs-clickable-after-dismiss.png); ui_errors clean
AC2-guest: MET

## AC7 — §5.10 recipe (completed)
- [x] Recipe validated across guest / logged-in-no-banner / logged-in-with-banner states this run
- [x] Recipe grep defect FIXED in docs/userapp-navigation-guide.md §5.10: one-node-per-line (tr '<'), anchored exact tab labels (no "Edit Profile" over-match), Button filter, keeps class/clickable/selected/bounds, leading-space excludes long-clickable; + locale note (ar labels, RTL mirroring)
- [x] Guide wording fixed: login-suggestion sheet is once per INSTALL (pref-gated), not per cold start; documented run-as re-arm command for debug builds
AC7: MET
