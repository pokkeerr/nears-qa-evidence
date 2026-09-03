# NEARS-3200 QA progress (cycle 0, tested sha 64bd5c62c, base 83ace0fe7, device-free)
| # | AC | verdict | evidence |
|---|----|---------|----------|
| 1 | (a) | PASS | HEAD grep 0 lines rc=1; base 34 unique lines (41 raw, advisors dir double-visited) — row01-*.txt |
| 2 | (a) ctrl | PASS | planted `questions[]` in $TMP copy caught rc=0 — row02 |
| 3 | (b) | PASS | Consult points — exactly three; [2]/[6]/[8] sentences, [8] pre-QA ask, advisor_answers[], "Any agent may return questions[]" removed; tiers/900/1200/spot-check/first-answer-wins/packet/header unchanged (not in any hunk) — row03 |
| 4 | (c) | PASS | 15/15 agent files x1, one md5 0fb6f9311aab58d4184343081d526141; envelope-defining files 15 — row04 |
| 5 | (c) | PASS | new-task.md:33 carries `domain: backend|flutter|dls|product|workflow` on NEEDS_DECISION — row05 |
| 6 | scope | PASS | run-sprint.md diffstat empty; line 93 already NEEDS_DECISION-driven — row06 |
| 7 | scope | PASS | 27 files; agent hunks all outside frontmatter; no tools/name/description lines; extra lines = `domain` added to existing NEEDS_DECISION specs (AC c) + TL step-5 `questions[]` reword — row07 |
| 8 | (d) | PASS | workflow-json-drift 5x PASS clean; cmp identical; jq valid; integrations.advisors.why = the sentence — row08 |
| 9 | (d) | PASS | advisor-latency.test.sh 76/76; advisors.test.sh 132/132 — row09 |
| 10 | (e) | PASS | doc-citation-resolve PASS 393/1192; doc-citation-content --all --root PASS 71 citations; content SELF-TEST case 6c FAIL pre-existing (NEARS-3189; scripts/ untouched in range) — row10 |
| 11 | history | PASS | 3125 rows reworded past-tense, attribution intact; 3200 changelog + design §11 row present — row11 |
| 12 | briefs | PASS | template + 5 briefs: §7 placeholder line only (+ advisor-workflow lines 60/75); H2 sets identical; line counts identical — row12 |
