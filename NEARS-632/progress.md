# NEARS-632 Live QA — progress checkpoint
Device: emulator-5556 (Android) · build: feat/NEARS-632-favourites-menu-entry @221bb36b · light mode · UserApp com.izzes.nears
Verdict: PASS

| AC | Result | Evidence | Logs |
|----|--------|----------|------|
| AC1 logged-in Favourite row in General between My Address & Delete Account | PASS | ac1-favourite-row-general.png | clean |
| AC2 tap -> FavouriteScreen (tabbed Item/Stores); favourited item shows; tab switch | PASS | ac2-favourite-screen-empty.png, ac2-favourite-screen-populated.png | clean |
| AC3 back -> Profile/Menu tab | PASS | ac3-back-to-profile.png | clean |
| AC4 guest: Favourite ABSENT, group renders cleanly | PASS | ac4-guest-no-favourite.png | clean |
| AC5 Arabic "مفضل", heart on right, chevron mirrored left, no clipping | PASS | ac5-rtl-arabic-favourite.png | clean |

Regression: clean (heart add/remove OK; page=favourite->Menu tab unchanged by-inspection zero blast radius; Orders/Address/Delete/Settings/Language tappable+unchanged)
Automated: flutter test menu_screen_reskin_test.dart -> 14/14 pass (incl. guest-only-Settings, all-7-rows-incl-Favourite, tap-routes-getFavouriteScreen)
