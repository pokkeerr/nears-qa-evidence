# NEARS-4010 step 1 QA (independent), HEAD e7650e62e. Performance effect: UNVERIFIED, no number (owner waiver NEARS-3987 c23343).
Device emulator-5574 (Pixel_10_Pro_2 AVD), own backend :8410 (worktree), scratch DB nears4010_qa, VendorApp debug build from the worktree at HEAD.
Add/update/delete success: green toast, correct landing, one request + one list GET each. Validation toasts block the request. Delete 500 + add transport failure: no pop, no banner toast.
Double tap on Add = 2 banners on HEAD AND on base (pre-existing, unchanged). Arabic delete toast verified. banner_create analytics fired once.
