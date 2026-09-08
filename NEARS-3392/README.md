# QA Evidence — NEARS-3392

**Delta QA fix-cycle 2 -- delivery-quote mechanism live-tested for the first time; found a stale-state defect where a failed quote fetch does not surface the retry UI and Place Order is not disabled**

**6 screenshot(s).** Click any thumbnail for full resolution.

<table>
<tr>
<td align="center" width="33%"><a href="address-change-out-of-zone.png"><img src="address-change-out-of-zone.png" width="240"></a><br><sub>address change out of zone</sub></td>
<td align="center" width="33%"><a href="bug-delivery-quote-failed-state-not-shown.png"><img src="bug-delivery-quote-failed-state-not-shown.png" width="240"></a><br><sub>bug delivery quote failed state not shown</sub></td>
<td align="center" width="33%"><a href="bug-stale-tax-after-coupon-removal.png"><img src="bug-stale-tax-after-coupon-removal.png" width="240"></a><br><sub>bug stale tax after coupon removal</sub></td>
</tr>
<tr>
<td align="center" width="33%"><a href="checkout-initial.png"><img src="checkout-initial.png" width="240"></a><br><sub>checkout initial</sub></td>
<td align="center" width="33%"><a href="checkout-pricing-breakdown.png"><img src="checkout-pricing-breakdown.png" width="240"></a><br><sub>checkout pricing breakdown</sub></td>
<td align="center" width="33%"><a href="multistore-fee-breakdown-coupon-removed.png"><img src="multistore-fee-breakdown-coupon-removed.png" width="240"></a><br><sub>multistore fee breakdown coupon removed</sub></td>
</tr>
</table>

### Other artifacts
- [`bug-ac4-place-order-not-disabled-after-quote-failure.log`](bug-ac4-place-order-not-disabled-after-quote-failure.log)
- [`bug-delivery-quote-failed-state-not-shown.log`](bug-delivery-quote-failed-state-not-shown.log)
- [`bug-delivery-quote-failed-state-not-shown.xml`](bug-delivery-quote-failed-state-not-shown.xml)

---
*From `nears/docs/qa-evidence/NEARS-3392/` · public-repo scrub policy (no live secrets; verified clean).*
