# NEARS-3999 step 3 (refund family) - QA walk, base vs tip (EN + light only)

BASE 97e09b0b3e11feb2fbe0add110caf745687fd355 (detached scratch worktree), TIP 609f43209a24bc30637b4c4ed041ba6d8512a977 (detached scratch worktree).
`git diff 97e09b0b3 609f43209 -- Admin` is empty; UserApp/lib diff = order_controller.dart + new order_refund_owner.dart only.
Device emulator-5554 (Android 17, 1344x2992), account customer@nears.com (user 6), scratch COPY DB multi_food_db_qa3999s3 reset to one seeded snapshot before each leg,
own php -S backend :8413 from the base scratch worktree Admin (DB target proven by changing users.l_name only in the copy and reading it back via GET /customer/info).

Layout:
- dumps/   a11y label dumps (`*.txt`) and label|enabled|selected|clickable|bounds state dumps (`*.state.txt`) per step, `base-*` vs `tip-*`; digests = pixel hashes of the screen body (status bar cropped)
- requests/ server-side request sequences (QA router logger in front of Admin/server.php): whole-leg logs and the R5 after-submit sequences
- frames/  on-device screencap/dump bursts with ms stamps; frame-classes-OCR.txt = per frame L(label) S(spinner) H(home) classification via macOS Vision OCR
- PNG: one screenshot per distinct screen per build (R1 refund screen, R4 image preview)
- automated-backstop-summary.txt + analyze-*.txt

Result: 37 paired a11y/state dumps identical, 0 differ; selected-card pixel digests identical (A, B, A); preview digest identical; request sets identical (order identical for the deterministic head, concurrent home-load GETs interleave).
Toast text not observable on either build (see ticket comment).
