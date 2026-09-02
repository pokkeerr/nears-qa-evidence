# QA Evidence — NEARS-2763

**FAIL — genuine live defect found: dispatch-notify update() can throw setState-during-build, leaving a marked-dispatched request that never actually sends, producing a false [FAIL] 8s later (breaks AC2). AC3/regression-4/5/6 confirmed clean live.**

**0 screenshot(s).** Click any thumbnail for full resolution.

### Other artifacts
- [`ac3-regression6-genuine-hang.log`](ac3-regression6-genuine-hang.log)
- [`bug-dispatch-notify-during-build.log`](bug-dispatch-notify-during-build.log)

---
*From `nears/docs/qa-evidence/NEARS-2763/` · public-repo scrub policy (no live secrets; verified clean).*
