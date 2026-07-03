# QA Evidence — NEARS-721

**PASS — order-tracking poll survives transient failure; no Timer-zone crash, no map freeze, auto-recovers; terminal + not-found regressions intact**

**5 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="ac1-baseline-map-render.png"><img src="ac1-baseline-map-render.png" width="240"></a><br><sub>ac1 baseline map render</sub></td>
<td align="center" width="33%"><a href="ac1-outage-map-persists.png"><img src="ac1-outage-map-persists.png" width="240"></a><br><sub>ac1 outage map persists</sub></td>
<td align="center" width="33%"><a href="ac1-recovered-after-restore.png"><img src="ac1-recovered-after-restore.png" width="240"></a><br><sub>ac1 recovered after restore</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="ac3-canceled-terminal.png"><img src="ac3-canceled-terminal.png" width="240"></a><br><sub>ac3 canceled terminal</sub></td>
<td align="center" width="33%"><a href="ac3-delivered-terminal.png"><img src="ac3-delivered-terminal.png" width="240"></a><br><sub>ac3 delivered terminal</sub></td>
</tr>
</table>

### Other artifacts
- [`ac1-ac5-poll-crash-absence.log`](ac1-ac5-poll-crash-absence.log)
- [`ac2-genuine-404-contract.log`](ac2-genuine-404-contract.log)
- [`bug-offline-geocode-nosuchmethod.log`](bug-offline-geocode-nosuchmethod.log)
- [`progress.md`](progress.md)

---
*From `nears/docs/qa-evidence/NEARS-721/` · public-repo scrub policy (no live secrets; verified clean).*
