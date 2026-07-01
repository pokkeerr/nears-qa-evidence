# NEARS-536 QA progress
- device: emulator-5556, worktree feat/NEARS-536-sectionheader-affordance
- backend: 10.0.2.2:8000 up (302 admin)
- app booted, logged in as James, Home loaded, no runtime errors

## FINDING (conclusive)
- NearsSectionHeader "See All" (Categories, category_view.dart:109) renders NAVY but NO underline.
- Verified 3 ways: raw-RGB scan (pure cream #fcf9f8 below baseline row 1532), inter-word-gap continuity (gap never filled), 10x visual zoom.
- Reproduced byte-identically on TWO independent fresh builds: session1 MCP launch_app build; session2 rm-rf-build clean Gradle rebuild (data wiped -> onboarding, proving fresh install).
- Change confirmed present: git diff shows +decoration: TextDecoration.underline; file mtime 15:04 predates all builds; flutter compiles working-tree (uncommitted) source.
- VERDICT: AC1/AC2/AC3 underline NOT met on device -> FAIL. This is exactly the failure the golden (underline-blind) cannot catch.
- Positive control (labelMd+underline renders elsewhere) NOT isolated live due to fresh-install onboarding instability; app ships 13+ TextDecoration.underline usages so a global "no underline" cause is implausible.

## DEVICE CONTENTION (drift)
- My qa-lock owner.json recorded pid from the FIRST Bash subshell ($$=61404), which exits after that call -> lock looked stale.
- NEARS-704 reclaimed emulator-5556 at 15:29 local (11:29Z) mid-run; likely caused the late-run onboarding-reset/logout/order-screen flakiness (concurrent device drive).
- Primary evidence ac1-home-seeall-top.png captured 15:13 in my exclusive window (lock 15:10) -> uncontaminated. Verdict unaffected.
- Left NEARS-704 lock intact (did not release someone else's lock).

## CYCLE 2 (fix re-QA) — 2026-07-01
- Fix under test: TextDecoration.underline REPLACED by painted Container bottom BorderSide(color: primaryColor, width:1.5) under Center(widthFactor:1).
- Durability fix: reclaimed stale NEARS-704 lock (pid 73609 dead); used a long-lived host anchor process as lock pid instead of transient $$.
- Contention (drift, again): another parallel run (pid 1278 `flutter run -d emulator-5556 --dart-define=API_HOST=10.0.2.2:8001`) reinstalled com.izzes.nears on 5556 at 16:15:10, overwriting my worktree build and killing my flutter-run. 5556 unusable.
- RELOCATED to emulator-5558 (free; locked with durable anchor pid 4348); launched my worktree build (installed 16:22:34, backend :8000). Clean exclusive window.
- PROOF (raw-RGB scan, store NearsSectionHeader "موصى به لك / رؤية الكل" = store_screen.dart:1352, Arabic/RTL): text glyphs y1345-1381, clean gap y1382-1395, then SOLID contiguous navy rule y1396-1399, 139px wide x[45..183], every pixel exactly (0,0,128)=navy #000080 on (255,255,255) white = 16.0:1. This below-baseline zone was pure background in cycle 1 (underline never painted).
- RTL preserved: header flipped (title cx=1160 right, action cx=132 left); border on left, hugs label width.
- Tap "رؤية الكل" -> navigates to store-item search/filter route (Brand/Price/Organic). No runtime errors (DTD), no [ERR]/[FAIL]/RenderFlex overflow in logcat before/after nav. Store headers lay out clean.
- Golden backstop: flutter test test/golden/dls_golden_test.dart -> +2 All tests passed (rebaselined goldens capture the border).
- VERDICT: PASS. AC1/AC2/AC3 met on device; border renders where underline did not.
