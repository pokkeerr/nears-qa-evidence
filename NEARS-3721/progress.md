# NEARS-3721 QA [8] cycle 0 — progress (light-mode n/a; workflow tooling)
- AC1 FAIL/partial: backend, /admin, /login/vendor, widgetbook :8090, watchers 6/6, tabs admin/store/widgetbook UP. UserApp + DeliveryApp UP on 5560/5564 (boot2). UNVERIFIABLE (env): monitor x3 + tab:monitor (host PATH php 8.2.33 < nears-monitor platform req >=8.4.1); emulator/app VendorApp (every free AVD /data < 800MB floor; reclaim cannot touch com.izzes.*).
- AC2 FAIL: boot3 re-run - no second backend/emulator/app/widgetbook/watchers (counts equal pre/post) BUT app:UserApp dropped from state.tsv while its pid 91184 was alive (bug-rerun-drops-app-row.log).
- AC3 PASS: self-test + live widgetbook kill -> --status exit 1 names widgetbook.
- AC4 PASS live (teardown1: 11 stopped/3 gone/1 kept/0 refused; teardown2: 10/4/1/0) - backend loop KEPT both times. Caveat: the AC2 bug makes a dropped row un-teardown-able.
- AC5 PASS file-read. AC6 PASS diff. AC7 PASS (static bans in self-test + code read; wedged bounded case in self-test).
- AC8 PARTIAL: 3 NEW distinct serials 5560/5562/5564 each ppid=1, none of 5554/5556/5558; only 2/3 apps UP (VendorApp disk env).
- AC9 FAIL: tab reuse over-match (bug-tab-reuse-overmatch.log). 3/4 tabs opened after 200; monitor tab correctly gated.
- AC10 PASS file-read. AC11 PASS close-session.test 95/95 (+ control pairs).
- Self-tests: boot-session.test 132/132, close-session.test 95/95.
- Snapshot: all NEARS-3720 pids/pgids/lstart + :8000 loop identical, except the peer's own UserApp relaunch (55201 -> 67790, log in the peer's own scratchpad). No QA-3721 leftovers.

# Cycle 1 (HEAD d115570e7) — delta
- AC1 PASS*: bootA 16 UP incl monitor/reverb/queue on auto-detected php 8.5, 4 tabs; VendorApp DOWN names NEARS_2411_QA=567MB Pixel_10_Pro=657MB NEARS_2414_QA=612MB + reclaim hint -> UNVERIFIABLE(env).
- AC2 PASS: bootB every UP row reused, same pid/lstart, process counts identical; low-disk VendorApp retried (followup). bootC with 5564 at 743MB (own 150MB filler) keeps app:DeliveryApp started+UP; teardown stopped it.
- AC8 PASS*: 5568/5564 new, ppid 1; 5560/5562/5566 low-disk boots stopped by stop_fresh; VendorApp env.
- AC9 PASS: live store tab present, admin opened fresh on /login/admin; bootB reused all 4; replay path-boundary correct.
- TB3 PASS: launch [FAIL] lines once each (UserApp 2/2, DeliveryApp 9/9).
- Snapshot: 12/12 identical, zero delta. No leftovers. Self-test 158/158.

# Cycle 2 (HEAD da5614f41) — final delta
- AC12 PASS: secrets:UserApp copied (mode 600, cmp identical, 239B, gitignored, git status clean, no tmp leftover); Vendor/Delivery WARN absent-in-primary; key-prefix hits 0 in boot output/state.tsv/watch.log (positive control 1).
- AC12 purpose: map tiles blank -> Maps SDK 'Authorization failure' for com.izzes.nears.nears_nears_3721_live_boot (key delivered, package/cert restriction) -> UNVERIFIABLE (owner Cloud Console).
- stderr fix PASS: 0 'No such file' lines.
- AC1/AC8 VendorApp still DOWN: Pixel_10_Pro=657MB; reclaim reverted by quickboot snapshot (-no-snapshot-save) -> UNVERIFIABLE(env) + task bug on the hint.
- Snapshot 12/12 identical; teardown 14/0/1/0; package uninstalled.
