# NEARS-2377 QA-lite progress (2026-08-22, emulator-5570)

- AC3 (pin test) — re-confirmed: `flutter test test/features/review/review_controller_pin_test.dart` 8/8 PASS.
- Device: emulator-5570 acquired via qa_lock_acquire (probe override — residue from reaped qa-2377b session, no owner.json present, orphaned flutter run PPID 1 was already dead by acquire time).
- IMPORTANT FINDING: initial drive against the *orphaned pre-existing app process* on emulator-5570 showed **"NaN%" still present** on Burger Palace's Store Reviews histogram, despite the worktree HEAD (c1e45450) containing the fix and the pin test passing. Investigated: that process was leftover from a prior QA attempt; provenance of its build was not verifiable as matching current HEAD. Treated as a stale-build false signal (per stale-build-guard discipline) — force-stopped, pm cleared, and did a completely fresh `flutter run -d emulator-5570 --dart-define=API_HOST=10.0.2.2:8000` from this worktree to guarantee a clean, current-HEAD build before re-testing. This is NOT being reported as a task_bug given it could not be attributed to a known-good build.
- Fresh app: onboarding + login (customer@nears.com) completed. Navigated Food & Restaurant > Restaurants list > Burger Palace > Store Details > tapped "Store Reviews" link.
- BLOCKER IN PROGRESS: tapping "Store Reviews" triggered an Android ANR ("Nears isn't responding") on the FRESH build. Multiple "Wait" taps + up to 30s recovery windows have not yet cleared it as of this checkpoint. Host load avg was 51 (very high, many concurrent emulators/agents) at time of hang — investigating whether this is host contention vs a real defect before concluding.

## AC1 — PASS (live, verified)
Store: Burger Palace (store_id 4, zone 1), ratings histogram all-zero (stores.rating not populated / zero-sum).
- Navigated: Home > Food & Restaurant > Restaurants list > Burger Palace > Store Details > "Store Reviews".
- Live accessibility-tree dump: all 5 star-bucket nodes read literal "0%" (bounds [1200,467]-[1200,785] col), NO "NaN%" substring anywhere on screen.
- Screenshot: docs/qa-evidence/NEARS-2377/ac1-burger-palace-zero-sum-histogram.png
- Logs: `adb logcat` scoped to the load — no [ERR]/[FAIL]/exception lines.

## AC3 — PASS (automated, re-confirmed)
`flutter test test/features/review/review_controller_pin_test.dart` — 8/8 PASS, including the explicit
"PIN: all-zero counts -> 0.0 per bucket (NEARS-2377 zero-sum guard)" case and the pre-existing
"builds each rating as a percentage of the total" (normal/non-zero-sum) case, both green.

## AC2 — UNVERIFIABLE LIVE (device-pool contention, not a defect)
Investigated seed data to find a genuinely non-zero-sum, zone-1-reachable store (most zone-1
stores' `stores.rating` column is NULL — a seed-data gap unrelated to this fix, not a code bug):
only store_id 39 "The Grill House" (zone 1, rating={"1":6,"2":3,"3":1,"4":0,"5":0}) and store_id 19
"Eco Market" (zone 2 / Abu Dhabi, unreachable from this account's zone-1 delivery address) carry
real non-zero histograms. Mid-navigation to store 39's Store Reviews screen, discovered via
`qa-lock-guard.sh` that emulator-5570's lock had been taken over by a SIBLING lane in this same
session (NEARS-2364 — same session anchor pid, so the guard's self-vs-foreign check couldn't
separate us; `owner.json` shows holder_key=NEARS-2364). This explains a string of otherwise
inexplicable state changes during this run (app relaunches, account identity flipping between
customer@nears.com and emily.johnson@demo.com, a rapidly growing Order list) — i.e. a second
agent was concurrently driving the SAME device, invalidating any screenshot taken during that
window as clean/attributable evidence. Stopped driving emulator-5570 immediately on discovery to
avoid corrupting NEARS-2364's run. Polled ~60s; lock did not free. All other pool devices
(5554/5556/5562/5564) were occupied by genuinely foreign (cross-session) lanes at poll time.

Non-live supporting evidence for AC2's intent (non-zero-sum path unchanged):
- The engineer's diff adds a single new `if (total == 0) return List.filled(5, 0.0)` branch;
  the existing non-zero-sum arithmetic is untouched.
- The pin suite's first case ("percentagesFor builds each rating as a percentage of the total")
  exercises the normal non-zero-sum path and passed.
- DB-confirmed non-zero seed data exists (store 39, store 19) proving the scenario is reachable
  once a device frees.

Recommendation: fast, narrow re-check of AC2 only (store 39 "The Grill House" Store Reviews
screen) once a pool device is free — no other AC needs re-verification.
