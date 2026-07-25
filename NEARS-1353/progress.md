# NEARS-1353 NCountBadge — QA progress checkpoint

Device: emulator-5556 · build HEAD c82c0dd5 · UserApp from worktree · light mode · zone 2 (Abu Dhabi) · guest user · locale ar/RTL live.

- AC2 ring badge (bottom nav): PASS — 02/03 show mint circle + 2dp navy ring + navy numeral; live 2→3 on add; 04 hidden when empty. RTL: badge at top-LEFT (end→left).
- AC1 app-bar pill: MET via golden (pill-single + pill-99plus growth, LTR top-right) + UserApp tests (renders mint cart badge count; cartCount:3). Not live-cart-drivable in-app (no cartCount call site — pre-existing; confirmed in pre-1353 code). Followup filed.
- CR-1 a11y single 'cart' label: PASS — UserApp a11y test "tooltip only, not merged label".
- RTL mirror: PASS live (02/03) + golden rtl-ring.
- Dark: DEFERRED (light-first). Goldens dark-pill/dark-ring exist, not verified live.
- Clean boot: PASS — 406-line run log, zero [ERR]/[FAIL]/exception/overflow/NCountBadge.

Backstop: nears_dls flutter test 230/230; analyze package 0; UserApp a11y+DLS 45/45.
