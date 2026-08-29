# NEARS-2095 QA progress

- AC1 [behav] .rich() compile-time semanticLabel requirement: PASS — live scratch
  omission-call analyze at packages/nears_dls (deleted after check) produced
  `error • The named parameter 'semanticLabel' is required, but there's no
  corresponding argument • missing_required_argument`. Independent re-verification,
  not just trusting the code-reviewer's finding.
- AC2 [behav] base-constructor runtime FlutterError still live (defense-in-depth):
  PASS — `flutter test packages/nears_dls/test/elements/n_checkbox_test.dart` group
  "NCheckbox — the labelChild/semanticLabel invariant" (negative throw + positive
  control pair, untouched lines ~627-663) both green, plus new .rich() positive
  proof test green.
- AC3 [ui]/[behav] all 3 labelChild call sites migrated to .rich(), suite green,
  widgetbook gallery visual unchanged: PASS —
  packages/nears_dls/test/elements/n_checkbox_test.dart 32/32 green (incl. migrated
  :284/:482 -> exclusion-asymmetry + error-status tests both now via .rich());
  widgetbook/test/n_checkbox_stories_test.dart 4/4 green; booted widgetbook
  (`flutter run -d chrome --web-port=9192`), screenshotted the NCheckbox Gallery
  use-case via uinav_web.py (/usr/bin/python3, playwright installed there) — "rich
  labelChild" row renders as mint-filled checked box + "I agree to the Terms &
  Conditions" with the link in its own underlined style, matching the pre-ticket
  composition. Interactive tap-toggle + independent link-tap-target already proven
  by the exclusion-asymmetry automated test (line ~273, migrated to .rich()) —
  no additional live click-through needed since interaction code is untouched by
  this diff (comment-only changes).
- flutter analyze packages/nears_dls: 3 pre-existing infos (n_item_card_price_truncation_test.dart,
  n_select_test.dart x2) — none in n_checkbox.dart, 0 NEW issues.
- flutter analyze widgetbook: No issues found.
- Automated backstop: flutter test packages/nears_dls -> 1247/1249 (2 pre-existing
  unrelated failures in test/tool/generate_catalog_test.dart — NButton prop diff +
  axes-test hardcoded map staleness; confirmed NCheckbox entry byte-identical in
  both Expected/Actual blocks of that failure's diff, i.e. NCheckbox does not
  appear in the failing diff at all). flutter test widgetbook -> 11/11 green.
- Widgetbook flutter-run log: no [ERR]/[FAIL]/exception lines during boot or
  screenshot capture.
- Widgetbook teardown: killed the `flutter run -d chrome` process (pid 8124),
  confirmed ports 9192/51465 no longer listening.
- Verdict: PASS
- Evidence gallery: published via scripts/qa-evidence-publish.sh
