# NEARS-3769 QA progress (fix_cycle 0)
- AC1 Modes story editable+trigger side by side: PASS (wb-0-modes.png; semantics: INPUT + 1 button)
- AC2 onLight/onNavy stories (field per owner decision B; pill via knob + pill golden): PASS (wb-1-on-navy.png, wb-5-playground.png)
- AC3 search / location_on glyph stories: PASS (wb-2-location-pin.png, wb-5-playground.png)
- AC4 goldens 4 combos (n_search_field_surfaces scenarios) pass: PASS (nears_dls suite 2317 pass / 2 pre-existing store-card fails)
- AC5 store item search live typing+submit 200 EN+AR; location dialog = dead code (not in isolate), parity+typeahead harness: PASS w/ caveat
- AC6 RTL ar @1.3x: PASS (ac6-store-item-search-ar-1.3x.png)
- AC7 trigger = 1 role=button flt-tappable node, no input (widgetbook web): PASS
- AC8 catalog +1 entry NSearchField (94->95), catalog --check OK: PASS
- Regression login/registration NInput: clean
