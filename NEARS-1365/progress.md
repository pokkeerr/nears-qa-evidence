# NEARS-1365 NBottomNav — QA progress checkpoint

Build: worktree feat/NEARS-1365-nbottomnav @ a2fdbef7. Devices: 5556 (RTL/ar, light), 5554 (LTR/en, light).

- AC1 5-tab icon-only + active fill/navy tint: PASS — 5556 & 5554. Home active filled+navy; others outline. logs clean.
- AC2 floating frosted bar + onChange routing: PASS — frosted blur visible (5554), rounded/inset; tab taps route (Home selected after cycle). logs clean.
- AC3 live cart badge reactivity: PASS — 5556 badge 1->2 on add, hidden at empty cart. NCountBadge ring mint+navy. logs clean.
- AC4 running-order banner above bar: PASS — 5556 order #158 card rests above floating bar (NEARS-591 geometry intact). logs clean.
- AC5 nav-hide gate + RTL: PASS — hides on module-selection home + keyboard-open; RTL row mirrors (Profile..Home L->R), glyphs un-mirrored, badge corner mirrors. logs clean.
- Goldens: PASS without --update-goldens (floating/docked, rtl, dark).
- Backstop: pkg contract 22/22, UserApp touched 33/33.

Note (non-blocking): 5554 stale /api/v1/auth/login 401 from OLD pid 29993 (pre-uninstall), properly logged, unrelated to nav.
