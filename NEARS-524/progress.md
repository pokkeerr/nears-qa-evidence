# NEARS-524 Buy It Again — QA (fix_cycle 2, AC1-focused re-QA)

Device emulator-5554 (nears_qa_wave56 headless). Backend worktree Admin @:8000. NEW code (nearest = client-side delivery-origin distance; (0,0)->hide).

## PRECONDITION (verified BEFORE judging AC1)
Delivery address in SharedPref = latitude 24.453884, longitude 54.3773438 (zone_ids [400,2]) — NON-ZERO. (QA-1 was (0,0) → store 9 from Gulf of Guinea.) Set via login → saved zone-2 "Abu Dhabi Home" → Set Location.

## AC1 — PASS ✅ (the fix)
- Grocery home → Buy It Again resolved store 8 "Abu Dhabi Fresh Market" (nearest ~5m) → item 145 "Orange Juice 1L" (user6 store-8 history). NOT store 9.
- Card tap → items/details/145 200 → detail store = "Abu Dhabi Fresh Market". shots 30 (rail) + 31 (detail).
- buy-it-again fired 200 on first fresh-install grocery load (CR-2 self-heal re-confirmed w/ correct store).

## Carry-forward (cycle-1 PASS; quick re-confirm)
- AC2: card→detail PASS (items/details/145). "+" quick-add proven cycle-1; store 8 is closed/"advance ordering unavailable" so pill→detail (correct, can't order) this run.
- AC5: rail shows ONLY store 8's item (Orange Juice) — no store-9/cross-zone/campaign leak.
- AC3 guest / AC4 Arabic RTL / CR-2 / CR-3: PASS in cycle-1 (unchanged by this fix which only touched nearest-store resolution).
- Logs: zero [ERR]/[FAIL] this session.
- Automated (cycle-1): flutter 14/14, phpunit 8/8 (nearest_store now resolves via delivery-origin).

## VERDICT: PASS
AC1 now resolves the actual nearest store (8) with a valid delivery location; the QA-1 wrong-store (store 9) bug is fixed. Guard (0,0→hide) is the mechanism; valid-location populated case demonstrated live.
