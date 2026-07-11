# QA progress — Sprint 5 Batch 2 (flash sale) — NEARS-1067 / 1069 / 1086
Worktree: /Users/Apple/Projects/nears-qa-batch2-flashsale @ qa/batch2-flashsale (6353f869)
Device: emulator-5554 (died mid-run after adb-root attempt) -> emulator-5556
Backend: php artisan serve (primary tree Admin) :8010 ; app via --dart-define=API_HOST=10.0.2.2:8010

## Observed (live, emulator-5554)
- flutter analyze: 5 info (pre-existing, unrelated test files), 0 errors/warnings
- flutter test (full UserApp): 2181/2181 PASS
- FOOD cold-load: 1x GET /api/v1/flash-sales (200). Rail y=720 (LIVE + countdown 03d19h22m), banner y=2088, categories y=2592 => TOP SLOT. 1 rail.
- FOOD pull-to-refresh: exactly 1 GET.
- PHARMACY cold-load: 1x GET. Rail y=720 (First Aid Kit), banner y=2088 => TOP SLOT. 1 rail.
- PHARMACY pull-to-refresh: exactly 1 GET.
- GROCERY cold-load: 1x GET. Rail y=720 (Banana/Red Apples), TOP SLOT, unchanged (regression control OK).
- Countdown ticks live 1/s (sec 12->08->04->00->57->53, minute rolled 22->21) — NOT frozen.
- Module hops food->grocery->food->grocery: rails=1 each hop, 1 GET each hop. Never stranded/double-mounted.
- Session-wide flash-sale GET tally: 5 = exactly the 5 triggered. Zero strays.
- PARCEL: structurally unreachable in UI (isModuleServiceable = storesCount>0; parcel has 0 stores) — see notes.
- Zero Flutter build-phase / setState / "cannot be marked as needing to build" / overflow warnings all session.
