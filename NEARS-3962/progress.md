# NEARS-3962 QA progress (phase 8, cycle 0) - head 22bf24227 vs base ff4fea929
Device emulator-5680 (spare AVD Pixel_10_Pro_2 booted by this run), 1080x2400 @480 = 360x800dp (wm size override), light mode. Backend :8162 from the NEARS-3962 worktree, DB private copy nears_qa_3962 (from nears_qa_3976; footer_text=QA3962-copy-marker). Head pkg com.izzes.nears.nears_nears_3962_nsnackbar_showoverlay; base pkg com.izzes.nears.qa3962_base (own detached worktree at ff4fea929).
- Trial recipe: mixed basket (Fresh local grocery + Golden Wok restaurant), zone 2 digital 0 at checkout open, flip to 1, Place -> Confirm -> group/validate 403 mixed_basket_cash_unavailable -> payment sheet reopens with the popup toast. t0 = the [WARN] 'modal route on top' line; one dump + screencap at t0.
- BASE (legacy UserApp presenter) pill node [138,228][942,618]; HEAD [138,228][942,618]; wallet Apply [750,1418][972,1490] on both. Pill-band pixel diff (y150-700) = 0 pixels over threshold.
- Hit tests (taps at derived coords while toast live): below pill (540,648) -> sheet dismissed (reaches barrier) on BASE and HEAD; left margin (69,423) -> sheet dismissed on both; pill centre (540,423) -> absorbed (sheet stays) then horizontal swipe -> toast gone, sheet stays, on both.
- HEAD wallet Apply during toast -> sheet re-laid out (wallet applied), then left swipe dismissed the toast.
- Timer: toast visible ~5.94s after first frame (6s cash toast) then gone.
- RE-CHECK A (head): coupon NEARS2924PCT applied, store 51 inactive on COPY, Place -> Confirm -> D1 sheet -> Remove & Continue -> '[INFO] coupon dropped ... trigger=d1_remove' + forced confirm sheet with ONE top-anchored notice 'Coupon was removed. You can place your order.' [138,228][942,420] above Scrim [0,0][1080,852].
- AC6 live (head): empty coupon Apply over coupon sheet -> one '[ERR] error snackbar shown' + one '[WARN] modal route on top, used overlay'.
- FIFO live (head): two empty-Apply taps 0.43s apart -> two [ERR]+[WARN] pairs; toast continuously visible 0.58s-6.31s (2 x 3s), single pill, second after first.
- AR/RTL (head, 360dp): pill [138,228][942,576] -> 138px (46dp) inset both sides.
- Non-popup ScaffoldMessenger path (cart remove Undo): Undo tap -> cart_remove_undone x1 + cart/add x1; node [0,1731][1080,2088] (NSnackBar chrome unchanged).
- Dismiss after popping the sheet route: barrier/margin tap pops the sheet with toast live; toast then expires; no exception/framework_error other than pre-existing checkout_screen_shimmer_view overflow.
