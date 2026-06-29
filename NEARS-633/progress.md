# NEARS-633 QA progress (live checkpoint)
device: emulator-5554 (Android 17) + chrome (web)
build: worktree feat/NEARS-633-staples-guest-gate

AC3 (guest menu): PASS — Menu/Profile tab as Guest User shows GENERAL=Settings only; My Staples/Orders/Edit-Profile/Address absent. logs clean. shot=ac3-guest-menu-no-staples.png

AC1 (guest staples gate): PASS — Get.toNamed(/staples) as guest -> NotLoggedInScreen (You are not logged in / Please login to continue / Login), NOT no_staples_yet empty state. FAB 'Save current cart' ABSENT with empty cart AND with guest cart=2 items. getStaples NOT fired (no /api/v1/customer/staples). logs clean. shots=ac1-guest-staples-notloggedin.png, ac1-guest-staples-cart2-no-fab.png

AC2 (authed staples): PASS — after login the authed body renders the staples list (Weekly staples, Item #62); FAB 'Save current cart' PRESENT (cart non-empty). logs: [200] /api/v1/auth/login then [200] /api/v1/customer/staples, clean. shot=ac2-authed-staples-list-fab.png
POST-LOGIN CALLBACK: PASS — logged in FROM NotLoggedInScreen 'Login' button; callBack->getStaples fired (staples API 200), list loaded in place without re-nav.
