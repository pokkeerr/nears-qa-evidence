| surface | status | detail |
|---|---|---|
| backend | UP | port 8000 pid 7597 /Users/Apple/Projects/nears@53e4dda4f · freshness rc 0 |
| admin-panel | UP | 200 http://127.0.0.1:8000/login/admin |
| store-panel | UP | 200 http://127.0.0.1:8000/login/vendor |
| emulator:UserApp | UP | serial=emulator-5566 avd=Pixel_10_Pro pid 69290 ppid=1 /data=498MB reverse tcp:80->8000 · reused (started by this session) · below the 800MB install floor: a running app is kept, a new install is refused |
| emulator:VendorApp | UP | serial=emulator-5568 avd=nears_qa_wave56 pid 69784 ppid=1 /data=4101MB reverse tcp:80->8000 · reused (started by this session) |
| emulator:DeliveryApp | UP | serial=emulator-5564 avd=NEARS_2424_QA pid 68213 ppid=1 /data=898MB reverse tcp:80->8000 · reused (started by this session) |
| app:UserApp | UP | serial=emulator-5566 pkg=com.izzes.nears.nears_nears_3721_live_boot pid 70500 /Users/Apple/Projects/nears-NEARS-3721-live-boot@da5614f41 · reload: kill -USR1 70500 · reused (started by this session) |
| app:VendorApp | UP | serial=emulator-5568 pkg=com.izzes.nearsvendor pid 76132 /Users/Apple/Projects/nears-NEARS-3721-live-boot@da5614f41 · reload: kill -USR1 76132 · started |
| app:DeliveryApp | UP | serial=emulator-5564 pkg=com.izzes.nearsdelivery pid 71127 /Users/Apple/Projects/nears-NEARS-3721-live-boot@da5614f41 · reload: kill -USR1 71127 · reused (started by this session) |
| widgetbook | UP | port=8090 pid 67030 /Users/Apple/Projects/nears-NEARS-3721-live-boot@da5614f41 http://127.0.0.1:8090/ |
| monitor | UP | port=9090 pid 66940 http://127.0.0.1:9090/ |
| monitor-reverb | UP | port=9091 pid 66801 |
| monitor-queue | UP | queue:work pid 66848 in /Users/Apple/Projects/nears-monitor |
| tab:admin | UP | reused tab http://127.0.0.1:8000/login/admin |
| tab:store | UP | reused tab http://127.0.0.1:8000/login/vendor |
| tab:widgetbook | UP | reused tab http://127.0.0.1:8090/ |
| tab:monitor | UP | reused tab http://127.0.0.1:9090/ |
| watchers | UP | 6/6 pipelines -> /private/tmp/claude-501/-Users-Apple-Projects-nears/1b6474ab-aaca-4398-9b48-32b83e413f29/scratchpad/v3721/state/watch.log |
| secrets:UserApp | UP | present |
| secrets:VendorApp | WARN | absent-in-primary |
| secrets:DeliveryApp | WARN | absent-in-primary |
