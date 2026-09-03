# QA Evidence — NEARS-3132

**FIX-CYCLE 1 delta re-QA: AC1 FAIL -- onCameraIdle still not firing on nears_qa_wave56 despite config fix (map stays blank, persistent Maps API token error, no geocode/zone [NET] calls from pan; positive control via FAB tap proves instrument is live). AC2/AC3 unchanged PASS from prior pass.**

**2 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="ac1-map-after-swipe-still-blank.png"><img src="ac1-map-after-swipe-still-blank.png" width="240"></a><br><sub>ac1 map after swipe still blank</sub></td>
<td align="center" width="33%"><a href="ac1-map-before-check.png"><img src="ac1-map-before-check.png" width="240"></a><br><sub>ac1 map before check</sub></td>
</tr>
</table>

### Other artifacts
- [`ac1-blocked-device-contention.log`](ac1-blocked-device-contention.log)
- [`ac2-df-reclaim.log`](ac2-df-reclaim.log)
- [`bug-ac1-oncameraidle-still-not-firing.log`](bug-ac1-oncameraidle-still-not-firing.log)

---
*From `nears/docs/qa-evidence/NEARS-3132/` · public-repo scrub policy (no live secrets; verified clean).*
