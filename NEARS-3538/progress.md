# NEARS-3538 QA progress (scoped confirmation pass)

- Device: emulator-5554, UserApp debug, branch feat/userapp-reskin2, primary tree.
- Login: customer@nears.com, zone 1 (Dhaka, geo-fixed 90.359852,23.82128).
- Store: 42 CarePlus Pharmacy (prescription_order=1, active). business_settings.prescription_order_status=1 (live).
- AC1: PASS — defect reproduced live. FAB "Prescription" node bounds [1161,0][1296,2638] — full-height vertical strip, not compact pill. Screenshot ac2-fab-current-state-full.png + raw dump ac1-fab-vertical-strip-dump.xml.
- AC2: FAIL — no fix landed (zero-code pass); current render fails the compact-pill AC.
- AC3: PASS — tap navigates to prescription checkout screen cleanly. Screenshot ac3-tap-navigates-to-prescription-checkout.png. Logs clean (2 unrelated pre-existing [FAIL] location-timeout lines from login setup, already AppLogger-paired, not filed).
- Verdict: FAIL overall — contradicts TL's static-read stale-finding hypothesis. Recommend re-opening fix cycle, not zero-code close.
- Evidence published: https://github.com/pokkeerr/nears-qa-evidence/tree/main/NEARS-3538
- Comment posted on NEARS-3538.
- Nav-guide gotcha added: qa-run.sh package-suffix breaks primary-tree Gradle build (google-services.json only registers com.izzes.nears).
- Teardown: killed flutter run process tree (59395/59473/59475/61254) + am force-stop com.izzes.nears; qa_lock_release emulator-5554 confirmed clean.
