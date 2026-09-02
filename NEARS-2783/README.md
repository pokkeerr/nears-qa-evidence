# QA Evidence — NEARS-2783

**regression-candidate CONFIRMED: reorder_helper.dart _openStore's fire-and-forget clearCartOnline() leaves a stale wrong-module cart line reachable at checkout on a forced clear-cart failure**

**4 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="bug-clearcart-null-module-400-false-empty.png"><img src="bug-clearcart-null-module-400-false-empty.png" width="240"></a><br><sub>bug clearcart null module 400 false empty</sub></td>
<td align="center" width="33%"><a href="cycle1-forced-fail-toast.png"><img src="cycle1-forced-fail-toast.png" width="240"></a><br><sub>cycle1 forced fail toast</sub></td>
<td align="center" width="33%"><a href="pass-clearcart-null-module-cycle1.png"><img src="pass-clearcart-null-module-cycle1.png" width="240"></a><br><sub>pass clearcart null module cycle1</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="regression-candidate-reorder-helper-silent-orphan.png"><img src="regression-candidate-reorder-helper-silent-orphan.png" width="240"></a><br><sub>regression candidate reorder helper silent orphan</sub></td>
</tr>
</table>

### Other artifacts
- [`bug-clearcart-null-module-400.log`](bug-clearcart-null-module-400.log)
- [`progress.md`](progress.md)
- [`regression-candidate-reorder-helper-silent-orphan.log`](regression-candidate-reorder-helper-silent-orphan.log)

---
*From `nears/docs/qa-evidence/NEARS-2783/` · public-repo scrub policy (no live secrets; verified clean).*
