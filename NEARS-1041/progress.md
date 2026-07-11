# Batch 5 live QA — progress checkpoint
Device: emulator-5554 · Backend: PRIMARY tree (/Users/Apple/Projects/nears/Admin) :8010 behind logging proxy :8020
Post-fix build: qa/batch5-tail @ 10f9cd8b · Pre-fix baseline: 7ded60a2 (detached worktree)

## NEARS-1041
- AC1 PASS — pre-fix zone2: img1.jpg0/1/2 -> 404 x3 ; zone1: img1.jpg4 + d-5bed135c7c.png3 -> 404.
        post-fix cold-boot empty-cache zone1: 3 URLs all 200, zero digit-suffixed.
        post-fix cold-boot empty-cache zone2: img1.jpg -> 200, zero digit-suffixed.
- AC2 PASS — zone2 carousel: 4 slides, 4 pagination dots. ac2-zone2-carousel-4slides.png
- AC3 PASS — banner 28 (image NULL) -> stock img1.jpg via 200, not a broken tile.
- AC4 PASS — 4 identical-photo slides -> 4 distinct targets:
        campaign-1 -> basic-campaign-details 200
        banner-24 -> /stores/details/12 ; banner-25 -> /13 ; banner-26 -> /14
        NOTE: item-type + link-type banners DO NOT EXIST in DB (all 12 are store_wise) -> those sub-cases undemonstrable.
