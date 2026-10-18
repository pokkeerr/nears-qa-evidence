# NEARS-4247 QA progress (checkpoint)
- Backstop: search_query_hash_absence_test.dart 22/22 green at 23ed731ff (mem-guard label 4247, peak 1.30 GB)
- Live (emulator-5554, UserApp unsuffixed pkg w/ google-services, API_HOST 10.0.2.2:8147 own backend, customer test acct):
  recent_search_tapped(search) PASS; recent_search_removed(search, remaining 5; persisted in prefs) PASS;
  search_idle_chip_tapped recent + trending PASS; recent_search_removed(global_search, remaining 1) PASS;
  search_result_tapped global_search + search PASS; search_suggestion_tapped PASS
- Details: live-events-4247.log
