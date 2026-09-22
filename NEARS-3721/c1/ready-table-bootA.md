READY — QA-3721
| surface | status | detail |
|---|---|---|
| backend | UP | port 8000 pid 7597 /Users/Apple/Projects/nears@53e4dda4f · freshness rc 0 |
| admin-panel | UP | 200 http://127.0.0.1:8000/login/admin |
| store-panel | UP | 200 http://127.0.0.1:8000/login/vendor |
| emulator:UserApp | UP | serial=emulator-5568 avd=nears_qa_wave56 pid 19935 ppid=1 /data=4192MB reverse tcp:80->8000 · started |
| emulator:VendorApp | DOWN | every free AVD booted below the 800MB /data floor: NEARS_2411_QA=567MB Pixel_10_Pro=657MB NEARS_2414_QA=612MB — reclaim space in one by hand (read-only survey: source scripts/qa-lock-guard.sh; qa_disk_reclaim <serial>) and re-run. Boot never wipes or uninstalls. |
| emulator:DeliveryApp | UP | serial=emulator-5564 avd=NEARS_2424_QA pid 19256 ppid=1 /data=893MB reverse tcp:80->8000 · started |
| app:UserApp | UP | serial=emulator-5568 pkg=com.izzes.nears.nears_nears_3721_live_boot pid 20840 /Users/Apple/Projects/nears-NEARS-3721-live-boot@d115570e7 · reload: kill -USR1 20840 · started |
| app:VendorApp | DOWN | no UP emulator for VendorApp |
| app:DeliveryApp | UP | serial=emulator-5564 pkg=com.izzes.nearsdelivery pid 21556 /Users/Apple/Projects/nears-NEARS-3721-live-boot@d115570e7 · reload: kill -USR1 21556 · started |
| widgetbook | UP | port=8090 pid 18154 /Users/Apple/Projects/nears-NEARS-3721-live-boot@d115570e7 http://127.0.0.1:8090/ |
| monitor | UP | port=9090 pid 18060 http://127.0.0.1:9090/ |
| monitor-reverb | UP | port=9091 pid 17917 |
| monitor-queue | UP | queue:work pid 17964 in /Users/Apple/Projects/nears-monitor |
| tab:admin | UP | opened http://127.0.0.1:8000/login/admin |
| tab:store | UP | reused tab http://127.0.0.1:8000/login/vendor |
| tab:widgetbook | UP | reused tab http://127.0.0.1:8090/ |
| tab:monitor | UP | opened http://127.0.0.1:9090/ |
| watchers | UP | 6/6 pipelines -> /Users/Apple/Projects/nears-NEARS-3721-live-boot/docs/qa-evidence/NEARS-3721/c1/state/watch.log |

DOWN emulator:VendorApp: every free AVD booted below the 800MB /data floor: NEARS_2411_QA=567MB Pixel_10_Pro=657MB NEARS_2414_QA=612MB — reclaim space in one by hand (read-only survey: source scripts/qa-lock-guard.sh; qa_disk_reclaim <serial>) and re-run. Boot never wipes or uninstalls.
DOWN app:VendorApp: no UP emulator for VendorApp
READY: 16 UP · 2 DOWN · 0 OPENED-UNCONFIRMED
validity: 18 surfaces asserted
