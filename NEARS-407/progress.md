# NEARS-407 QA progress (live)

Build: feat/NEARS-407-address-reskin @ e4386a6f | device emulator-5554 (Android 17/API37) | fix-cycle 1
Backstop: flutter test address + dls = 43 green

## List screen (01-address-list.png)
- Q1 navy header + white title + mint "2 delivery spots" subtitle + mint pin: PASS
- Q2 "Saved Addresses" NearsSectionHeader above list: PASS
- Q3 mint-tint "Home" label pill, navy text, rounded: PASS (both cards)
- Q4 neutral-tint icon tile + navy home glyph: PASS
- Q5 bold address title; _detailLine null for single-string addr (intended, no fabricated 2nd line): PASS
- Q7 edit(pencil)+delete(red trash) icon buttons present: PASS
- Q9 mint AddAddressBanner navy text + add_location glyph: PASS
- Q41 NO search/basket icons in app bar: PASS
- Note: both seeded addrs are type=home -> only 'home' glyph/label observable on list
## Regression: shared card in location-select sheet (00-boot-location-sheet.png)
- Q6 NearsBadge mint "DEFAULT" on selected addr: PASS
- isSelected mint border on default card: PASS
- Q10 pull-to-refresh fires GET /api/v1/customer/address/list 200 (logs): PASS
- Q7 delete dialog (02-...png): rounded, Delete=error-red, Cancel=NearsSecondaryButton(navy outline): PASS; CANCELLED, no delete (DB-safe)
- Analytics: FA screen_view '/address' fired on list open (logs)
- Seeded: id45 Abu Dhabi home tower=Marina Heights, id46 Demo Zone home (both type=home)
## Edit form (03-edit-form-prefill-top.png) — Abu Dhabi id45
- Q13 navy appbar, white back, "Update Address" title: PASS
- Q14 functional Google Map hero, rounded, PICK marker, Google logo: PASS (pan test next)
- Q16 current-loc FAB mint+navy icon bottom-right: PASS
- Q17 fullscreen FAB white card+navy icon top-right: PASS
- Q18 info pill mint-tint + navy info icon + text centered: PASS
- Q19 "Label As" section header: PASS
- Q20 3 chips, Home=mint fill+navy text+home icon selected, others=outline+icon: PASS
- Q21 Home chip selected on edit (seeded home): PASS
- Q24 Delivery Address req asterisk + location_on, prefilled: PASS
- Q25 "Contact Details" header: PASS
- Q26 Tower/Building (Optional) prefilled "Marina Heights" + apartment icon + helper: PASS
- Q27 Contact Person Name req + person icon, prefilled "Customer Nears": PASS
- Q28 phone CustomTextField, UAE flag +971 default, prefilled 565811199, SINGLE clean label (no double-label): PASS
- Q30 Street Number (Optional) signpost icon: PASS
- Q32 edit prefill all fields populated: PASS
- Q35 sticky mint NearsPrimaryButtonLoader "Update Address" + save icon: PASS
- Q40 NO Current Selection floating card: PASS
- Q42 NO help_outline in appbar: PASS
- Q28 country-code picker (05-...png): opens bottom-sheet w/ search + country list, UAE +971 at top w/ flag = default; single clean label, no double-label: PASS; dismissed unchanged
- Q14 MAP CAVEAT: GoogleMap widget instantiated + gesture-enabled + chrome re-themed correctly, BUT tiles blank — Maps SDK "Authorization failure" (dev API key AIzaSyB... not authorized for com.izzes.nears cert). ENV/key issue, pre-existing, NOT introduced by NEARS-407 (reskin preserves the map widget). pan/zoom visual unverifiable due to no tiles.
- Q22 Others->Level-Name field appears (06-...png, animated, optional, other_houses icon); Home->field disappears (07-...png): PASS both directions
- Q31 House(Optional)+Floor(Optional) side-by-side row visible at form bottom: PASS
- No runtime errors (Dart MCP get_runtime_errors clean) on edit form
## Add form + validation wall
- Q13 add ctx title "Add New Address", Q35 footer "Save Location" + save icon: PASS
- Q24/Q34 Delivery Address hint "Delivery Address *" (req asterisk): PASS
- Q26 Tower/Building "(Optional)" no asterisk: PASS
- Q27/Q34 Contact Person Name "*": PASS
- Q28 Contact Person Number required: PASS
- Q30 Street Number "(Optional)": PASS
- Q31 House(Optional)+Floor(Optional) side-by-side: PASS
- Q33 VALIDATION WALL (09/10-...png): cleared 3 required fields -> tap Save -> snackbar "Please enter the delivery address" fires, NO navigation, NO /address/add network write (logcat empty): PASS. DB-SAFE, never completed a save.
## Dark mode (toggled via in-app ThemeController moon icon)
- Q38 list (13-...png): navy header stays navy + white title + mint subtitle; mint banner stays mint+navy text; section header white; card bg dark navy; mint label pill navy text readable; type tile mint glyph. PASS for brand tokens.
  * OBSERVED: address-card TITLE text (textStrong=const #1C1B1B) low-contrast dark-on-dark navy card. Same const-dark-text root cause as NEARS-429. Record as debt (NEARS-429 family), DO NOT fail (per ticket).
- Q38 form (14-...png): navy appbar navy; mint chips+CTA navy text correct; section headers white; phone field (CustomTextField) white text good contrast; helper text legible.
  * NEARS-429 CONFIRMED: NearsInput body text (address/tower/name/street) low-contrast dark-on-dark navyContainer fill. Known debt -> record, DO NOT fail.
- Q39 (delete dialog dark / salmon error button NEARS-428): dialog button is error-red; salmon-in-dark is NEARS-428 known debt. Not re-opened in dark to avoid delete risk; cosmetic, recorded.
## RTL / Arabic (Q37) — app language=Arabic (15 list, 16 form; both also in dark)
- LIST: appbar title right-aligned + back arrow mirrored to right; mint banner icon-tile on right + chevron flipped left; cards mirrored (icon tile right, edit/delete left); "بيت" label pill: PASS
- FORM: appbar back arrow mirrored right; CHIP Wrap RTL ("بيت/مكتب/آحرون" right-aligned w/ icons, بيت selected mint); field labels right-aligned w/ asterisk; phone UAE flag at logical start (right): PASS
- FIXED RTL FAB BUG CONFIRMED: both map FABs now at LOGICAL END (top-LEFT fullscreen + bottom-LEFT current-loc) in RTL — the PositionedDirectional/EdgeInsetsDirectional fix works: PASS
- New contact_details Arabic string renders: "بيانات الاتصال": PASS
## Not-logged-in + remaining
- Q11 (19-...png): logged out -> address screen shows NotLoggedInScreen (illustration + "You are not logged in" + "Please login to continue" + mint Login btn navy text): PASS
- Q8 empty state: CANNOT demo live (test acct has 2 addrs; DB-safety forbids delete/persist; no zero-addr fresh acct available). Code-verified: address_screen wires NearsEmptyState per DoR 2c. Mark unverifiable-live / code-verified.
- Q12 desktop grid: OUT OF SCOPE (mobile QA run, per DoR).
- Q15 map loading spinner: transient + map tiles blocked by API key; not separately demonstrable this env.
- Q34 required asterisks: confirmed via field hints (Delivery Address *, Contact Person Name *, phone Required) + visible labels: PASS
- App restored: English + light. Now logging back in for next run hygiene.
