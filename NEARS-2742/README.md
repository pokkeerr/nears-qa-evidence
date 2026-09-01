# QA Evidence — NEARS-2742

**FAIL — AC1/AC4/AC5/AC6/AC7 pass; AC2/AC3 fail: fixed-window revert bug (bug-timeout-reverts-to-silent-hide) makes the recoverable NLoadMoreError state undo itself ~32s later**

**8 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="ac1-happy-path-rail-cards.png"><img src="ac1-happy-path-rail-cards.png" width="240"></a><br><sub>ac1 happy path rail cards</sub></td>
<td align="center" width="33%"><a href="ac2-nloadmoreerror-shown.png"><img src="ac2-nloadmoreerror-shown.png" width="240"></a><br><sub>ac2 nloadmoreerror shown</sub></td>
<td align="center" width="33%"><a href="ac3-retry-success-cards.png"><img src="ac3-retry-success-cards.png" width="240"></a><br><sub>ac3 retry success cards</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="ac3-second-timeout-reshown.png"><img src="ac3-second-timeout-reshown.png" width="240"></a><br><sub>ac3 second timeout reshown</sub></td>
<td align="center" width="33%"><a href="ac5-empty-state-self-hides.png"><img src="ac5-empty-state-self-hides.png" width="240"></a><br><sub>ac5 empty state self hides</sub></td>
<td align="center" width="33%"><a href="ac6-decoded-500-self-hides.png"><img src="ac6-decoded-500-self-hides.png" width="240"></a><br><sub>ac6 decoded 500 self hides</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="ac7-rtl-nloadmoreerror.png"><img src="ac7-rtl-nloadmoreerror.png" width="240"></a><br><sub>ac7 rtl nloadmoreerror</sub></td>
<td align="center" width="33%"><a href="bug-timeout-reverts-to-silent-hide.png"><img src="bug-timeout-reverts-to-silent-hide.png" width="240"></a><br><sub>bug timeout reverts to silent hide</sub></td>
</tr>
</table>

### Other artifacts
- [`bug-timeout-reverts-to-silent-hide.log`](bug-timeout-reverts-to-silent-hide.log)

---
*From `nears/docs/qa-evidence/NEARS-2742/` · public-repo scrub policy (no live secrets; verified clean).*
