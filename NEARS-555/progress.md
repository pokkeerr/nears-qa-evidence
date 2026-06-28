# NEARS-555 QA progress (live, emulator-5556, worktree build)
- worktree: /Users/Apple/Projects/nears-NEARS-555-variation-remove-npe (feat/NEARS-555-variation-remove-npe)
- item 84 Dove Whitening Body Spray, store 2, grocery (newVariation=false legacy), Size 250ml/500ml CONFIRMED in DB
- module.newVariation = (moduleType=='food') => grocery false CONFIRMED (module_controller.dart:357)
- baseUrl http://10.0.2.2:8000 (useHttps=false) CONFIRMED; backend up :8000

## Repro setup (zone 2, store 12 Fresh local — task-sanctioned alternates; item 84 is zone 1 not zone 2 per DB = drift)
- Line A: Tones Mild Chili Powder (item 91) Size 64g — legacy variation, 70 AED
- Line B: 4X4 Rubiks Cube (item 86) Color Green — legacy variation, 430 AED
- Line C: Oreo Choco Cookies (item 62) — SIMPLE non-variation, 400 AED
- All persisted server-side (added via detail/optimistic). Cart = 3 lines.
- NOTE: same-item two-variation (AC3 literal) not creatable via UI — detail screen dedupes same item ("Update In Cart"); used two distinct legacy-variation items instead. Removal is keyed by cartId/index so right-line targeting still validated.
