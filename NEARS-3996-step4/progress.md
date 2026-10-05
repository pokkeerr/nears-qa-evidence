# NEARS-3996 step 4 (UA-026 discovery family) QA [8] progress - tested sha cf67afd23c2a99f14051858b1a53d807f8c02e08, base 0f4ab3979, EN + light

- start: HEAD == cf67afd23, git status clean, branch feat/NEARS-3996-u5-step4-discovery-family; lessons selector run: lessons_read=97 (selector exit 0)
- AC1 PASS: lib diff = store_controller.dart + store_discovery_owner.dart; own public listing identical (names+kinds, 162 members); ctor `({required storeServiceInterface, now})`; get_di/pubspec/assets/app_constants untouched; update ids identical (3x update([fabVisibilityId]); id-less 50 -> 41 + owner 10 - 1 shim def)
- AC2 PASS: 12 verbatim block diffs rc=0, 15 shifted controls rc=1, converse accounted (ac1_ac2_surface_verbatim.txt)
- AC3 PASS (+2 expected non-gating rows): 21 required files rc=0 unmodified; store_offers_extraction_source_scan_test rc=1 (Expected 48 Actual 39) = by-design pending ruling, passes on base; item_view_closed_now_divider rc=1 on tip AND base = pre-existing
- AC4 PASS: 164 effective fresh mutants, 159 killed, 5 survivors all EQUIVALENT, 0 REAL (1 own syntax slip re-formulated)
- AC5 PASS (see wire_counts.md, rendered_parity.md, failure_and_retry_trials.md): base vs tip route walk, family requests EQUAL on 46/48 actions (2 explained), static screens 0 px / equal text, list order + Closed Now divider identical, zone switch Loading then new-zone stores only, store open 7 requests on both, re-enter 0 duplicate requests, first-fetch failure + Retry identical on both builds, logs clean
- AC6 PASS: analyze 13 infos (9 controller + 4 owner) vs 13 base, 0 in new tests; golden_manifest +5 green; 0 PNG
- AC7 PASS: PD-S4-1..4 pins present (6 tests: PD-S4-1 x1, -2 x2, -3 x2, -4 x1), green in the 72-test characterization file; verbatim moves => no behaviour change; not probed on device (stale-write races not reachable by cheap device steps) => covered by tests
- AC8 gaps stated: perf UNVERIFIED; AR/RTL/dark DEFERRED (owner scope decision 2026-10-04); FA SDK wire UNVERIFIABLE (suffixed build); featured 'view all' has no UI entry; AllStoreScreen NearsErrorRetry w/o cache UNVERIFIABLE on device (tests cover it)
