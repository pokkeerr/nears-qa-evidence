# QA Evidence — NEARS-1035

**PASS — all 5 ACs + rail degrade + cache bump demonstrated live (021d2028, emulator-5554, worktree BE :8035); phpunit 776/776, flutter 2015/2015; 1 pre-existing regression bug filed-ready (details initState setState-during-build)**

**7 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="bug-details-stuck-shimmer.png"><img src="bug-details-stuck-shimmer.png" width="240"></a><br><sub>bug details stuck shimmer</sub></td>
<td align="center" width="33%"><a href="details-error-retry-403.png"><img src="details-error-retry-403.png" width="240"></a><br><sub>details error retry 403</sub></td>
<td align="center" width="33%"><a href="details-happy-zone2.png"><img src="details-happy-zone2.png" width="240"></a><br><sub>details happy zone2</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="details-loaded-empty.png"><img src="details-loaded-empty.png" width="240"></a><br><sub>details loaded empty</sub></td>
<td align="center" width="33%"><a href="rail-degrade-hidden.png"><img src="rail-degrade-hidden.png" width="240"></a><br><sub>rail degrade hidden</sub></td>
<td align="center" width="33%"><a href="rail-zone1-normal.png"><img src="rail-zone1-normal.png" width="240"></a><br><sub>rail zone1 normal</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="rail-zone2-grocery.png"><img src="rail-zone2-grocery.png" width="240"></a><br><sub>rail zone2 grocery</sub></td>
</tr>
</table>

### Other artifacts
- [`ac1a-raw.json`](ac1a-raw.json)
- [`ac1b-unknown-id.json`](ac1b-unknown-id.json)
- [`ac2-crafted-zoneid.txt`](ac2-crafted-zoneid.txt)
- [`ac2-zone1.json`](ac2-zone1.json)
- [`ac2-zone2.json`](ac2-zone2.json)
- [`ac3-fail-log-excerpt.log`](ac3-fail-log-excerpt.log)
- [`ac3-fault-items.json`](ac3-fault-items.json)
- [`ac3-fault-rail.json`](ac3-fault-rail.json)
- [`bug-details-initstate-update-during-build.log`](bug-details-initstate-update-during-build.log)
- [`progress.md`](progress.md)

---
*From `nears/docs/qa-evidence/NEARS-1035/` · public-repo scrub policy (no live secrets; verified clean).*
