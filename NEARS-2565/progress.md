# NEARS-2565 QA progress (this session)

Commit tested: `7b10f1af8`. Device: `emulator-5554`.

- Automated backstop: `n_item_card_price_truncation_test.dart` 16/16 pass (fresh run).
  Full `nears_dls` suite: 1259 passed / 2 failed (both `generate_catalog_test.dart`,
  confirmed pre-existing/unrelated — this branch touches only `n_item_card.dart` +
  the test file). NInput/NSpinner goldens now green (fixed by `4a755ecde` rebaseline).
- Live AC1 (Arabic/RTL, device default persisted locale): Lip Balm / AED 56.69 at
  HealthCare Pharmacy's real 150dp "Recommended For You" rail renders IN FULL, no
  ellipsis. Screenshot: ac1-lipbalm-150dp-rail-no-truncation.png
- Live AC1 (English/LTR, device system locale is actually en-US; app locale flipped
  via SharedPreferences `flutter.6ammart_language_code`): SAME item, SAME store, SAME
  rail renders "56.69 A..." — TRUNCATED. Screenshot:
  bug-lipbalm-english-aed-truncates-150dp-rail.png. Confirmed via a11y dump
  (content-desc carries full "56.69 AED", painted glyphs cut after "A") — genuine
  TextOverflow.ellipsis, not a misread.
- Discovered mid-run: a concurrent session sharing this session's process anchor
  (pid 4639) had already run QA on emulator-5558 and posted Jira comment 16071
  (FAIL) with a very similar root-cause hypothesis (real-device font metrics vs
  flutter-test TextPainter measurement gap at the ~90dp effective budget), AFTER
  an earlier PASS (comments 16064-16066) had already closed the ticket to Done.
- My own finding independently corroborates 16071 and adds one new data point: the
  EXACT SAME item/price straddles the truncation threshold depending on locale
  (Arabic currency abbreviation is narrower than "AED", clearing the same budget
  that English does not).
- Posted Jira comment 16074: FAIL verdict, corroborating 16071, flagging the
  Done status as needing reversion (not something I can transition myself).
- Evidence gallery: https://github.com/pokkeerr/nears-qa-evidence/tree/main/NEARS-2565

Final verdict: FAIL.

---

## 4th session (this spawn) — corroboration via a 3rd distinct angle

Found emulator-5558 already locked/booted under this same worktree's process
anchor (pid 4639) at spawn start, with progress.md above already populated by
sessions posting 16071/16074 (FAIL). Did not trust it — re-drove the repro
myself before writing anything.

- AC1 FAIL, confirmed via narrow-vs-wide comparison (not locale): Lip Balm
  56.69 AED truncates ("56.69 A...") on HealthCare Pharmacy's true 150dp
  "Recommended For You" rail, reproduced twice on fresh navigations, while
  the IDENTICAL item/price renders in full on the same store's 209dp "All
  Products" grid card (same item_card.dart -> NItemCard widget, same data,
  only the width differs).
- AC2 met on the specific cards I hit (Blood Pressure Monitor 44.69->37.99
  AED stacks correctly on the same rail; Organic Strawberry's a11y tree
  carries both price strings intact) -- did not personally reproduce 16071's
  discount-branch failure, likely the same string-length threshold landing a
  different item on the safe side this time. Not a contradiction of 16071.
- Re-ran n_item_card_price_truncation_test.dart: 17/17 pass. Test's
  NItemCard(...) construction omits addControl/favourite/unit -- offered as
  an additional lead alongside 16071's TextPainter-vs-real-font hypothesis
  for why the isolated test passes but the real composition doesn't.
- Posted Jira comment 16075 (FAIL, corroborating), kept brief given 16071/
  16074 already carry the exhaustive analysis. Re-flagged the still-Done
  status (unowned by QA -- conductor/whoever owns transitions needs to act).
- Evidence gallery re-published (idempotent) with new files:
  bug-lipbalm-truncates-rail-confirm2.png,
  bug-lipbalm-still-truncates-on-true-150dp-recommended-rail.png,
  regression-check-openstore-discount-rail.png,
  regression-check2-fullyvisible-discount-card.png.

Final verdict (this session too): FAIL.

---

## Re-QA of fix-cycle 2 (commit 98c7daf385) — 2026-08-29, this spawn

**Everything above this line predates commit `98c7daf385` (the `_priceFitSafetyMargin`
+ iterative re-measure fix) and describes the now-superseded FAIL state. Not trusted,
not edited — fresh repro only, per spawn instructions.**

Worktree: `/Users/Apple/Projects/nears-NEARS-2565-nondiscount-price-scale-to-fit`.
Device: `emulator-5558` (clean uninstall + fresh `flutter run` from this worktree;
APK built 23:06, matching HEAD commit timestamp 23:03:10 — provenance confirmed).
emulator-5556 was excluded: disk precheck failed (542MB free, floor 800MB) even
after one `qa_disk_reclaim --clean` attempt (545MB after). emulator-5554 untouched
(NEARS-2580 lock, live).

- **AC1 (Lip Balm, AED 56.69, HealthCare Pharmacy, non-discounted branch, real
  150dp "Recommended For You" rail):**
  - en/LTR: **PASS** — "56.69 AED" renders in full, no ellipsis. Screenshot:
    `en-lipbalm-recommended-rail.png`. Card also shows AC2 spot check (Blood
    Pressure Monitor 44.69→37.99 AED, discounted branch) rendering cleanly.
  - ar/RTL (switched via in-app Settings→Language→English/Arabic picker, not
    SharedPreferences): **PASS** — "56.69 د.إ." renders in full on the true
    narrow rail (confirmed by locating the horizontal-scroll rail specifically,
    not the 230dp "All Products" grid which sits right below it and is easy to
    mistake for the rail on a quick scroll). Screenshots:
    `ar-lipbalm-recommended-rail-narrow.png` (narrow rail, both Lip Balm +
    Blood Pressure Monitor visible), `ar-lipbalm-a11y-dump.xml` (a11y
    cross-check, both nodes' content-desc carry the full price string,
    matching the painted glyphs).
  - This is the ticket's own named fixture, the one 3 independent live-device
    QA passes (16071/16074/16075/16076) reproduced truncating. It now clears
    with margin in BOTH locales on the true 150dp rail.

- **Sunscreen SPF50, 43.20 AED (MediQuick Pharmacy (Abu Dhabi), zone 2, non-
  discounted branch):** en/LTR **PASS** — "43.20 AED" renders in full on the
  150dp rail. Screenshot: `en-sunscreen-recommended-rail.png`. (ar/RTL not
  separately re-driven for this fixture given budget — same code path as
  Lip Balm, which passed both locales; automated backstop also covers this
  exact price string with real fonts + numeric margin assertion, see below.)
  Noted in passing: an adjacent, out-of-matrix item on the same rail
  ("Omega-3 Fish Oil", 17.10 AED) DOES truncate — logged as a regression
  candidate, not in scope here.

- **Organic Strawberry (6.50→5.85 AED) / Greek Yogurt (4.50→4.28 AED),
  Organic Paradise, zone 1:** **DATA-DoR GAP, not a fix-cycle-2 defect.** DB
  query confirms these are the ONLY seed rows with these names, and BOTH carry
  a real, non-zero item-level discount — so on live device they render via the
  `originalPrice != null` (discounted/stacked) branch, confirmed by the a11y
  dump carrying BOTH price strings (`en-organic-greek-a11y-dump.xml`:
  `"...Organic Strawberry...5.85 AED...6.50 AED..."`). Fix-cycle-2's
  `_priceFitSafetyMargin` only touches the `originalPrice == null` branch (code
  read directly: n_item_card.dart lines ~577-649) — this branch is
  byte-untouched by this ticket, same as the already-known followup from the
  original PASS (comment 16064): "discounted-price current text still
  ellipsis-truncates on 150dp rail at borderline widths... byte-untouched by
  this ticket." **Reproduced live: it DOES still truncate** — "5.85 A..." and
  "4.28 A..." both ellipsis on the real 150dp rail, en/LTR. Screenshot:
  `en-organic-greek-recommended-rail.png`. This CONFIRMS that pre-existing
  regression-candidate (now filed/tracked under the NEARS-2626 consolidated
  ticket per the run file's decisions[]) — logging as `regression_bugs`, not a
  task_bug against NEARS-2565, since the diff never reaches this branch. No
  live non-discounted item with these exact prices exists in the seed DB to
  demonstrate the ticket's literal ask 1:1 — the automated backstop's
  synthetic real-font test (`n_item_card_price_truncation_real_font_test.dart`)
  is the only direct evidence for "5.85 AED"/"4.28 AED" through the ACTUAL
  fixed code path, and it passes with real fonts + a pinned numeric margin
  (>=3.09dp per comment 16087, re-confirmed by re-running the suite this
  session — 19/19 pass in the two targeted files).

- **Additional RTL finding (out of scope, same discounted-branch bucket):**
  Blood Pressure Monitor (44.69→37.99 AED, same HealthCare Pharmacy rail) which
  rendered CLEANLY in en/LTR truncates in ar/RTL ("37. .إ.د..."). Screenshot:
  `ar-lipbalm-recommended-rail-narrow.png` (same shot as the Lip Balm AR pass —
  both cards visible side by side). Same out-of-scope discounted branch as
  above; logged as an additional regression_bugs instance, not a FAIL of this
  ticket.

- **Automated backstop (fresh, this worktree, pinned SDK 3.41.9):**
  `n_item_card_price_truncation_test.dart` + `n_item_card_price_truncation_real_font_test.dart`:
  **19/19 pass** (17 + 2, re-verified twice for stability). Full `nears_dls`
  suite: **1262 passed / 2 failed**, both `generate_catalog_test.dart` (stale
  committed `catalog.yaml` vs a fresh render + a missing `NItemCard: [layout]`
  axis entry) — confirmed pre-existing/unrelated: this ticket's diff never
  touches `catalog.yaml` or the catalog generator, and re-running 3x gave a
  stable 2-failure count (isolated from the flaky-looking 1259/-5 seen on one
  early run, which was itself just the same 2 catalog failures plus transient
  noise not reproduced on 2 subsequent runs).

- **Regression sweep:** Store 230dp "All Products" grid (both locales) —
  clean, AC3 unaffected. Item search screen (multiple searches, both modules)
  — clean. Food & Restaurant module home (ar/RTL) — loads clean, 0 `ui_errors`.
  `ui_errors` scanned clean (0 matches) on every check throughout this session.

**Verdict: PASS.** The ticket's own named fixture (Lip Balm) and one more
non-discounted fixture (Sunscreen SPF50) both clear the real 150dp rail with
genuine margin in the locale(s) driven, live, on a freshly-installed build of
commit `98c7daf385`. The 2 fixtures that don't literally reproduce live
(Organic Strawberry/Greek Yogurt) are a Data DoR gap, not a code defect —
those exact non-discounted price strings ARE covered by the automated
backstop against the real fixed code path, and the DISCOUNTED-branch
truncation those items actually exhibit live is a confirmed, already-tracked,
out-of-scope regression (NEARS-2626 lineage), not this ticket's fault.

Evidence gallery: https://github.com/pokkeerr/nears-qa-evidence/tree/main/NEARS-2565
