# NEARS-2154 QA progress (fix-cycle 0)

Device: emulator-5560 (lock reclaimed from stale/low-disk state, disk reclaimed via uninstall of
4 stale worktree package variants: 91%->71% used, then re-verified >=800MB free).
Package installed as base `com.izzes.nears` (NEARS_PKG_SUFFIX not set for this run).
Account: QA SingleStore (qa.singlestore@nears.com, user id 409, zone 3).

## AC1 — decision recorded
N/A-recorded. Owner ruled option (a) matching system BACK. Documentation fact, not live-demoed.

## AC2 — notif-opened Wallet with live back stack, app-bar arrow returns to previous route
PASS. Repro: logged in as QA SingleStore -> Profile -> Favourite (pushed route, live back
stack Home->Profile->Favourite). Real backend Add Fund via Admin panel
(admin/customer/wallet/add-fund, 0.01 AED, verified DB row wallet_transactions id=45,
transaction_type=add_fund_by_admin). Real FCM push delivered while app foregrounded on
Favourite -> logcat `[INFO] msg="FCM onMessage type=add_fund"` -> local tray notification
"Fund added"/"Fund added to your wallet" appeared -> tapped it -> WalletScreen pushed on top
(same pid 10827 throughout, so this is the live-back-stack path, not a cold start). Tapped the
app-bar `Back` control -> landed back on `Favourite` screen (not Home). Logs: only pre-existing
unrelated `[FAIL] endpoint=/api/v1/customer/wish-list transport_error=client` (Favourite's own
list load, unrelated to wallet/back-arrow) — no new [ERR]/[FAIL] from the back-arrow action.
