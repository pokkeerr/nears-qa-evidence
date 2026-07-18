# QA Evidence — NEARS-1291

**RE-QA FAIL — loop/toast FIXED, but per-store get-Tax now 500s (item_type missing) -> tax silently dropped**

**4 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="ac1-checkout-resectioned.png"><img src="ac1-checkout-resectioned.png" width="240"></a><br><sub>ac1 checkout resectioned</sub></td>
<td align="center" width="33%"><a href="ac6-bill-fees-itemized.png"><img src="ac6-bill-fees-itemized.png" width="240"></a><br><sub>ac6 bill fees itemized</sub></td>
<td align="center" width="33%"><a href="reqa-ac1-no-toast-clean-cta.png"><img src="reqa-ac1-no-toast-clean-cta.png" width="240"></a><br><sub>reqa ac1 no toast clean cta</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="reqa-ac6-order-summary.png"><img src="reqa-ac6-order-summary.png" width="240"></a><br><sub>reqa ac6 order summary</sub></td>
</tr>
</table>

### Other artifacts
- [`ac3-db-readback.log`](ac3-db-readback.log)
- [`ac4-payment-group-id.log`](ac4-payment-group-id.log)
- [`bug-gettax-403-loop.log`](bug-gettax-403-loop.log)
- [`reqa-bug-gettax-500-item_type.log`](reqa-bug-gettax-500-item_type.log)

---
*From `nears/docs/qa-evidence/NEARS-1291/` · public-repo scrub policy (no live secrets; verified clean).*
