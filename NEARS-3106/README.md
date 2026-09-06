# QA Evidence — NEARS-3106

**PASS — config-driven Pusher key wired for UserApp+DeliveryApp; live /api/v1/config serves websocket_key unconditionally; protocol-level handshake proof with positive/negative controls; both apps boot clean with the pre-existing (unrelated) websocket_status gate skipping gracefully in this env**

**2 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="deliveryapp-online-status.png"><img src="deliveryapp-online-status.png" width="240"></a><br><sub>deliveryapp online status</sub></td>
<td align="center" width="33%"><a href="userapp-order-tracking.png"><img src="userapp-order-tracking.png" width="240"></a><br><sub>userapp order tracking</sub></td>
</tr>
</table>

### Other artifacts
- [`ac3-config-body.json`](ac3-config-body.json)
- [`ac3-config-headers.txt`](ac3-config-headers.txt)
- [`ws-handshake-proof.log`](ws-handshake-proof.log)

---
*From `nears/docs/qa-evidence/NEARS-3106/` · public-repo scrub policy (no live secrets; verified clean).*
