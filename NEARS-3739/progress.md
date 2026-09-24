# NEARS-3739 QA [8] progress — 2026-09-24

- AC1 NEARS_2411_QA: PASS — identity NEARS_2411_QA on emulator-5562; df /data 10167132K total / 9379320K avail; config 10G; qa_disk_reclaim verdict=ok free_mb=9159 (report-only). ac1-NEARS_2411_QA.log
- AC1 NEARS_2414_QA: PASS — identity NEARS_2414_QA; df 10167132K / 9391656K; config 10G; reclaim verdict=ok free_mb=9168. ac1-NEARS_2414_QA.log
- AC1 Pixel_10_Pro: PASS — identity Pixel_10_Pro; df 10167132K / 9381172K; config 10G; reclaim verdict=ok free_mb=9160. ac1-Pixel_10_Pro.log
- AC1 isolation: PASS — Pixel_10_Pro_2 6G, Pixel_10_Pro_3 10G, NEARS_2424_QA 6G, nears_qa_delivery 6G, nears_qa_wave56 6442450944; all qcow2 present; config mtimes predate 2026-09-24; 5554=Pixel_10_Pro_2, 5558=nears_qa_delivery, 5560=NEARS_2424_QA still attached. ac1-isolation.log
- AC2: PASS — doc section verification-checks.md:1699-1753 has every required element; the recipe edit block on scratch spaced/unspaced/absent copies each printed disk.dataPartition.size=10G (count=1). ac2-recipe-scratch.log
