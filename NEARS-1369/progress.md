# NEARS-1369 NInput — QA progress
Build: worktree /Users/Apple/Projects/nears-NEARS-1369-ninput @ ed01ab77
Devices: 5554 (en/LTR/light) primary, 5556 (ar/RTL) mirror

- AC1 login eye toggle (5554): PASS — a11y flipped "Show password"->"Hide password" on tap; toggle at trailing (1212,1052). logs: clean
- AC2 signup (5554): PASS — uppercase labels, required * markers, glass, eye toggle on Password+Confirm; Form.validate fired red error messages below NInput fields. logs: clean
- AC4 registration no-eye (5554): MET (component+wiring) — live nav image-upload gated at step 1; obscureToggle:false wired at delivery:2552 store:3765; unit test n_input_test:244 asserts obscureToggle:false ⇒ NO IconButton (no eye), obscured. AC1 toggle also asserted n_input_test:215. logs: n/a
- AC5 update_profile (5554): PASS — NInput name/email/phone render (plain path, no validator=no double FormField); email trailing verified_user icon overrides managed toggle. logs: clean
- AC5 add_address (5554): PASS — NInput fields render + required markers; Save validated single & persisted (nav to Saved Addresses, "3 delivery spots"). logs: clean. NOTE: added 1 test address (feature-under-test write).
- AC3 new_pass (light variant, lock/verified_user): MET (component+wiring) — live forget-flow SMS-OTP gated (no dev OTP/demo mode). Wiring new_pass_screen:201-238 = NVariant.primary(light), leadingIcon lock+verified_user, obscure:true; n_input_test covers variant/leadingIcon/obscure (259/259). logs: n/a
- AC6 RTL (5556, ar): PASS — NInput glass password field mirrored: leading lock icon RIGHT, trailing eye toggle LEFT, label right-aligned + required *; eye toggle flips إظهار->إخفاء (Show->Hide). logs: clean
