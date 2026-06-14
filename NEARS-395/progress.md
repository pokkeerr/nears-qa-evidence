# NEARS-395 QA progress (live, emulator-5554, branch feat/NEARS-395-splash-firstlaunch)

## Automated backstop
- flutter analyze: 8 info-level lints, NONE in the 7 reskinned screens, no errors/warnings. CLEAN for this change.
- flutter test: +858 All tests passed! (matches expected 858). PASS.

## Live demonstrations
- 00 Notifications permission prompt → Allowed (system dialog).
- Splash: auto-advanced too fast to catch live on first cold start; source confirms reskin (navy brand mark CAP-S1, mint loading bar on navy track CAP-S2, all bootstrap/connectivity/deeplink logic preserved). Will re-trigger network-kill NoInternet test (CAP-S4/S5).
- 01 Language screen (LTR, English default): PASS
  - CAP-L1 illustration ✓, CAP-L2 title (Public Sans) + muted subtitle ✓
  - CAP-L3 data-driven rows: flag + NEW 2-letter code badge (EN/AR/ES/BN) + name ✓ (COSM design item built)
  - CAP-L4 single-select visual: selected = mint-soft fill + mint border + mint check; navy/dark text on mint badge (rule 1) ✓
  - CAP-L5 Next CTA = mint fill + navy text + trailing arrow_forward ✓; guard logic preserved (selectedLanguageIndex != -1)
  - Brand rules: mint=action, navy text on mint, ambient shadows no hard borders, warm bg/white cards ✓
- 02/03/04 Onboarding (LTR): PASS — 3 data-driven slides (Get Favorite Items / Rapid Delivery / Eco-Friendly Reach); swipe advances; Skip on early slides HIDDEN on last; "Next"→"Get Started" label swap on last; mint pill + grey dot indicators track; image card elevated surface no border; Get Started → guestLogin+route (CAP-O1..O8) ✓
- 05/06/07 Get Started → location auto-resolved in-zone (Abu Dhabi z2) → reached Home/module screen. No blank/crash. "You're almost there/Login-Sign Up" sheet is the HOME guest-prompt (pre-existing), NOT the firewalled access-location panel.
- 08 Access Location (via Change Location): PASS — navy app bar "Set Location", illustration+title+15-min microcopy, Use Current Location (mint+my_location icon), Set From Map (navy outline+map icon). FIREWALL HELD: NO auth/Login-SignUp panel on this screen (CAP-A1/A2/A5/A6) ✓
- 09 Pick Map (in-zone): PASS — GoogleMap, navy center pin, pill search (navy front-door), my-location FAB, zoom +/- FABs ambient shadow, "Pick Location" mint CTA enabled (CAP-M1..M5,M7). NOTE: map TILES render blank-grey on this emulator (Maps rendering degraded), not an app bug.
- 11/12 Pick Map search: PASS — autocomplete returns results (London...), selecting moves camera label (CAP-M3).
- 13/14 Out-of-zone live trigger BLOCKED by emulator map-tile rendering (camera-idle zone flip didn't fire on blank map). CAP-M6 verified BY SOURCE: warning pill uses NearsTokens.warningSurface(#FFE2CF)+warning(#B8530B amber, Icons.warning_amber_rounded), NOT mint; CTA onPressed:null when !inZone, label→service_not_available. CONFIRMED amber semantic, not mint.
- Interests (interest_screen.dart): verified BY SOURCE+858 tests — CAP-I5 NO min-3 gate (onPressed always enabled except while saving; saveInterest accepts empty); mint fill+textOnMint(navy)+corner check on selected; pillSoftBg "N selected" pill >0; "tap_cards_to_select" helper; NoData/spinner states (CAP-I1..I8). LIVE trigger blocked: interest gate is one-time-per-module-per-user; seeded customer already past it; cannot reset without DB write (read-only rule).
- 17/18/19 Login (sibling DLS screen, navy front-door + mint Sign In) → signed in as customer@nears.com "Customer Nears". No errors.
- 22/23 Language fromMenu (Settings→Language): PASS — opens as bottom-sheet, same reskinned LanguageCardWidget rows, CTA "Update" (not Next), CustomAppBar/Scrim. Shared-widget blast radius OK (CAP-L6/L8) ✓
- 24/25/26/27 RTL flip (CAP-L7): PASS LIVE — selected Arabic → whole app flipped to Arabic/RTL; Settings screen mirrored (icons right, labels right-aligned, back chevron flipped to point right), EdgeInsetsDirectional honored. No errors.
- 28 Dark+RTL Settings: PASS — surfaces flip navy-deep bg + navy-container card, white text legible, mint switch thumbs, navy app bar constant. Dark theme applies.
- 31 Access Location logged-in + dark + RTL: PASS — saved-address ListView (CAP-A3) 2 AddressWidget rows w/ mint home badges on navy cards; app bar mirrored; FIREWALL STILL HELD (no auth panel) in logged-in/dark/RTL.
- 32 Pick Map dark+RTL: PASS — search pill mirrored (location icon right, search icon left), FABs/zoom navy+mint dark, center pin mint in dark, CTA mint. (map tiles blank-grey = emulator rendering, not app bug)
- 33/34 Splash LIVE (dark, offline cold start): PASS — caught reskinned splash: white/mint pin brand mark (logoOnNavy) on navy-deep (CAP-S1) + mint indeterminate loading bar brSm clip animating (CAP-S2). Held gracefully offline, no crash/blank.
- 35 Network restore: PASS — splash recovered, config bootstrap completed, routed to Home (CAP-S3/S4 + splash→home routing through outage+recovery). NoInternetScreen hard-swap (CAP-S5) didn't trigger because emulator connectivity listener kept reporting interface-present during svc-disable (emulator quirk); branch present+unchanged in splash_screen.dart:139, snackbar colors re-tokened (mint connect / error disconnect). Verified by source.
- 36 Reverted English+light: clean state restored.
- 37 Regression sweep (Home, Categories tabs): clean, no errors, no overflow. Theme changes didn't break downstream path-to-Home.

## Verdict: PASS
- New User Setup (new_user_setup_screen.dart): not reached LIVE (only via fresh social/OTP registration; seeded accounts are existing users). Reskin verified by source + 858 tests pass.
- task_bugs: none.
- regression_bugs: none observed in cluster + path-to-Home.

