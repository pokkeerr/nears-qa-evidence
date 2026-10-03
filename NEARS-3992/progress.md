# NEARS-3992 step 3 QA evidence (tested sha e1848251aa16896b5cdf8c0e71cce474bcae3f97, base f79afae79)
- logs/live-vm-service-log-full-session.txt : VM-service Logging/Stdout stream, MARK lines delimit cycles (branch build, then base build)
- shots/bell-crop-*.png : home bell crop, DOT vs CONTROL (cold-start guest, no dot)
- shots/bug-*.png : confirm-only regression candidates (a) search history, (b) bell dot
- logs/bug-global-search-semantics-assert.log : Flutter semantics assertion on the global-search results screen (debug)
- mutation-results.txt + mutation-diffs/*.diff : scratch-copy mutation proof (each diff proves the mutation landed)
- logs/suite-{head,base}-per-file.txt, pins-base-vs-head.txt, analyze-*.txt, git-diff-stat-base-head.txt
