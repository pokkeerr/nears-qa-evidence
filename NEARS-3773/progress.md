# NEARS-3773 QA [8] progress — fix_cycle 0
Device emulator-5560 (Pixel_10_Pro spare AVD, own lock). AFTER pkg com.izzes.nears.nears_nears_3773_nsearchfield_migration @31a51ff63; BEFORE pkg com.izzes.nears.qabase2840 @2840a5ac4 (detached scratch worktree).
Backend: /Users/Apple/Projects/nears-NEARS-3773-nsearchfield-migration @ 31a51ff63 (:8073)
- AC1 PASS m1 trigger -> search_screen, no event on tap
- AC2 PASS glass/field look matches NEARS-3769 look B (composite)
- AC3 PASS m2 + m3 -> global search; global_search_opened home/categories params before trending GET
- AC4 PASS m4(desktop via wm density 140),m5,m7,m8 typing/submit/results parity; @#$ stripped; voice sheet; clear/voice swap. m6 UNVERIFIABLE live (enableCrossStoreSearch=false, no deep link)
- AC5 PASS chat submit-filter identical to base
- AC6 PASS m10 (desktop) + m11 typeahead, availability rows, event parity; blur-restore by widget test
- AC7 PASS all 10 reachable mounts: trigger=1 Button, editable=1 EditText + separate labelled trailing
- AC8 PASS AR 1.3x no clipping, glyph not mirrored
- AC9 PASS before/after composite; findings: chat double magnifier (Low), pick-map decorative trailing search icon dropped
- AC10 PASS via debug analytics mirror (FA transport dead on suffixed pkg at base too)
- AC11 PASS no new [FAIL]/[ERR]; semantics Table assert reproduces at base
- AC12 PASS goldens untouched + 51 NSearchField tests; store item search device spot-check
