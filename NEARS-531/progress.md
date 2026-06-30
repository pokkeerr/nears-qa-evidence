# NEARS-531 QA progress — home appbar location-row leading-edge alignment
device: emulator-5554 (1344x2992, API37) · build: feat/NEARS-531-appbar-inset (uncommitted) from worktree · light mode

- AC1 not-set leading edge flush at ~same x as address-set: PASS — location icon glyph at x=56-93 in BOTH states (pixel-measured); a11y InkWell left x=45 both. [01-address-set-home.png, 02-not-set-home.png, 03-leading-edge-comparison.png]
- AC2 no horizontal jump not-set <-> address-set: PASS — leading light pixel x=55 identical in both states; toggled live via VM (clearAddress + LocationController.update). [03-leading-edge-comparison.png]
- AC3 no other appbar element displaced (bell, trailing arrow): PASS — notification bell rightmost edge x=1262 identical both states; end padding (paddingSizeSmall) unchanged so trailing arrow gap preserved. [03-leading-edge-comparison.png]
- AC4 RTL (Arabic) leading inset mirrors, no jump on toggle: PASS — EdgeInsetsDirectional mirrors; leading icon (right) x=1288 + bell (left) x=72 identical across both RTL states. [05/06/07-*-rtl.png]
- logs: clean across both demo flutter-run sessions (no [ERR]/[FAIL]/overflow). 2 unrelated [FAIL] get-zone-id 404 only during deny-location experiment (env, not the fix; logging contract working).
- automated: dart analyze (changed file) clean; flutter test test/features/home = 44/44 pass.
