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
