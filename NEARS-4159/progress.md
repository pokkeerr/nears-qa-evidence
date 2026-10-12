# NEARS-4159 QA progress (cycle 0), tested sha 04cfd731f56f1bb3510d64e8999984285bda607a, base dee1260131cae06130ba43d02bf89c7fc828942a
- AC4 PASS: route:list --json identical (1466 routes; language group 11 routes) -> route-inventory-ac4.txt
- AC1/AC7 PASS: 245 hostile arms + 30 symlink/protected/target arms on scratch copy B, all refused, 1 [FAIL] line per refusal per stream, nothing created/moved/deleted, settings identical, zero outbound -> B-tested-*.tsv, refusal-log-samples.txt
- AC2/AC8 PASS: 15-step positive trace identical base vs tested for settings employee and role_id 1 -> positive-controls-base-vs-tested.txt
- AC9 PASS: target_exists x3 live; mkdir 0755 at tested vs 0777 at base (umask 000)
- AC5 PASS: real UI (Playwright) add/edit/hostile/delete/translate/auto-translate/auto-translate-all on ar -> ui-*.png, ui2.json
- RED at base: C.red.json (11 arms create/move/include/rewrite/delete outside resources/lang)
- backstop: 342 tests green (310 in the new file)
- real-tree guard: worktree Admin/resources/lang fingerprint identical before/after; Modules listing hash identical; git status clean
