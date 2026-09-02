# QA Evidence — NEARS-2763

**Delta re-QA cycle 1: FAIL — NEARS-2797 crash CONFIRMED FIXED (deferred update() verified live under the exact triple-mount repro), AC1/AC2 hold. NEW defect found: _timedOut never resets, permanently disarming the watchdog after its first fire — a second genuine hang on the same long-lived rail instance produces zero [FAIL], silently losing the 8s early-warning signal.**

**0 screenshot(s).** Click any thumbnail for full resolution.

### Other artifacts
- [`ac3-regression6-genuine-hang.log`](ac3-regression6-genuine-hang.log)
- [`bug-dispatch-notify-during-build.log`](bug-dispatch-notify-during-build.log)
- [`bug-timedout-never-reset.log`](bug-timedout-never-reset.log)
- [`nears2797-repro-fixed.log`](nears2797-repro-fixed.log)

---
*From `nears/docs/qa-evidence/NEARS-2763/` · public-repo scrub policy (no live secrets; verified clean).*
