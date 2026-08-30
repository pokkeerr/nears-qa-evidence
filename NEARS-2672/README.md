# QA Evidence — NEARS-2672

**Re-QA delta: FAIL — TB1 STILL REPRODUCES on normal-login path (4/4), passes on cold-restart (3/3). Root-cause lead: get-zone-id 404 precedes every failure. Watchdog degrades permanent-stuck to bounded 8s self-hide (real improvement, not a full fix).**

**5 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="ac1-sophie-home.png"><img src="ac1-sophie-home.png" width="240"></a><br><sub>ac1 sophie home</sub></td>
<td align="center" width="33%"><a href="bug-stuck-skeleton-home.png"><img src="bug-stuck-skeleton-home.png" width="240"></a><br><sub>bug stuck skeleton home</sub></td>
<td align="center" width="33%"><a href="regression-track-transient-noorder.png"><img src="regression-track-transient-noorder.png" width="240"></a><br><sub>regression track transient noorder</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="reqa-customer7-coldrestart-pass.png"><img src="reqa-customer7-coldrestart-pass.png" width="240"></a><br><sub>reqa customer7 coldrestart pass</sub></td>
<td align="center" width="33%"><a href="reqa-tb1-customer7-normallogin-fail.png"><img src="reqa-tb1-customer7-normallogin-fail.png" width="240"></a><br><sub>reqa tb1 customer7 normallogin fail</sub></td>
</tr>
</table>

### Other artifacts
- [`bug-stuck-skeleton-home-dump.xml`](bug-stuck-skeleton-home-dump.xml)
- [`bug-stuck-skeleton-nolog.log`](bug-stuck-skeleton-nolog.log)
- [`bug-transient-noorder-91124.log`](bug-transient-noorder-91124.log)
- [`reqa-customer7-coldrestart-pass.log`](reqa-customer7-coldrestart-pass.log)
- [`reqa-tb1-customer7-normallogin-fail.log`](reqa-tb1-customer7-normallogin-fail.log)

---
*From `nears/docs/qa-evidence/NEARS-2672/` · public-repo scrub policy (no live secrets; verified clean).*
