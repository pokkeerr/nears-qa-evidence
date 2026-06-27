# NEARS-621 QA progress (live, emulator-5554, zone1=Dhaka/zone2=AbuDhabi)
- Backend: worktree served on :8000 (oauth keys synced from primary). Endpoint GET /api/v1/search/unified 200 OK.
- BLOCKER FOUND: unified results list does not render. search_result_widget.dart:282 shrinkWrap ListView fails 'hasSize' paint assertion on EVERY search. Items(N)/Stores(M) headers show, rows blank, Stores section unpainted. Evidence: bug-blank-results-list.png/.log
