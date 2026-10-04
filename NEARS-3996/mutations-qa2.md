# NEARS-3996 step 2, fix cycle 2 - QA2 independent mutations (scratch copy of ae9bf9825; live worktree never mutated)

Protocol: unmutated new file green first (64/64), mutation applied to scratch copy only, landed proof = non-empty `diff -U0` vs live worktree (quoted in the run log), run the new file under mem-guard; if green, run the unmodified net (store_availability_weekday_matrix / edge_fixtures / store_facade_scope baseline files); restore from the live file; restore proof = empty diff.

| id | mutation | new file | net (3 files) | verdict | restore diff |
|---|---|---|---|---|---|
| S01 | `-      r'^(\d{1,2}):(\d{2})', ⟶ +      r'^(\d{2}):(\d{2})', ⟶ ` | RED 5 (00:00 +59 -5) | n/a (red above) | KILLED | empty |
| S02 | `-    ).firstMatch((time ?? '').trim()); ⟶ +    ).firstMatch((time ?? '')); ⟶ ` | RED 1 (00:00 +63 -1) | n/a (red above) | KILLED | empty |
| S11 | `-      r'^(\d{1,2}):(\d{2})', ⟶ +      r'(\d{1,2}):(\d{2})', ⟶ ` | RED 2 (00:00 +62 -2) | n/a (red above) | KILLED | empty |
| N01 | `-      r'^(\d{1,2}):(\d{2})', ⟶ +      r'^(\d{1,2}):(\d{1,2})', ⟶ ` | RED 1 (00:00 +63 -1) | n/a (red above) | KILLED | empty |
| N02 | `-    if (hour > 24 \|\| minute > 59) return null; ⟶ +    if (hour > 24 \|\| minute > 60) return null; ⟶ ` | RED 1 (00:00 +63 -1) | n/a (red above) | KILLED | empty |
| N03 | `-    if (hour > 24 \|\| minute > 59) return null; ⟶ +    if (hour > 25 \|\| minute > 59) return null; ⟶ ` | RED 2 (00:00 +62 -2) | n/a (red above) | KILLED | empty |
| N04 | `-    return hour * 60 + minute; ⟶ +    return hour * 60; ⟶ ` | RED 12 (00:00 +52 -12) | n/a (red above) | KILLED | empty |
| N05 | `-  static const int _lastMinuteOfDay = 23 * 60 + 59; ⟶ +  static const int _lastMinuteOfDay = 23 * 60 + 58; ⟶ ` | RED 2 (00:00 +62 -2) | n/a (red above) | KILLED | empty |
| N06 | `-      if (opening <= 0 && closing >= _lastMinuteOfDay) { ⟶ +      if (opening < 0 && closing >= _lastMinuteOfDay) { ⟶ ` | RED 14 (00:00 +50 -14) | n/a (red above) | KILLED | empty |
| N07 | `-      return closing - nowMinute <= thresholdMinutes; ⟶ +      return closing - nowMinute < thresholdMinutes; ⟶ ` | RED 6 (00:00 +58 -6) | n/a (red above) | KILLED | empty |
| N08 | `-      if (nowMinute < opening \|\| nowMinute >= closing) continue; ⟶ +      if (nowMinute < opening \|\| nowMinute > closing) continue; ⟶ ` | RED 4 (00:00 +60 -4) | n/a (red above) | KILLED | empty |
| N09 | `-      if (nowMinute < opening \|\| nowMinute >= closing) continue; ⟶ +      if (nowMinute <= opening \|\| nowMinute >= closing) continue; ⟶ ` | RED 3 (00:00 +61 -3) | n/a (red above) | KILLED | empty |
| N10 | `-    if (hour > 24 \|\| minute > 59) return null; ⟶ +    if (hour >= 24 \|\| minute > 59) return null; ⟶ ` | RED 5 (00:00 +59 -5) | n/a (red above) | KILLED | empty |
| N11 | `-    if (hour > 24 \|\| minute > 59) return null; ⟶ +    if (hour > 24 \|\| minute >= 59) return null; ⟶ ` | RED 11 (00:00 +53 -11) | n/a (red above) | KILLED | empty |
| N12 | `-      if (opening <= 0 && closing >= _lastMinuteOfDay) { ⟶ +      if (opening <= 0 && closing > _lastMinuteOfDay) { ⟶ ` | RED 13 (00:00 +51 -13) | n/a (red above) | KILLED | empty |
| N13 | `-    final int nowMinute = now.hour * 60 + now.minute; ⟶ +    final int nowMinute = now.hour * 60; ⟶ ` | RED 3 (00:00 +61 -3) | n/a (red above) | KILLED | empty |
| N14 | `-    if (isStoreOpen24h(store)) return false; ⟶ ` | RED 5 (00:00 +59 -5) | n/a (red above) | KILLED | empty |
| N15 | `-    if (weekday == 7) weekday = 0; ⟶ ` | RED 3 (00:00 +61 -3) | n/a (red above) | KILLED | empty |
| N16 | `-    if (store.active == false) { ⟶ -      return false; ⟶ -    } ⟶ ` | RED 1 (00:00 +63 -1) | n/a (red above) | KILLED | empty |
| N17 | `-    ).firstMatch((time ?? '').trim()); ⟶ +    ).firstMatch((time ?? '').trimRight()); ⟶ ` | RED 1 (00:00 +63 -1) | n/a (red above) | KILLED | empty |
| N18 | `-    ).firstMatch((time ?? '').trim()); ⟶ +    ).firstMatch((time ?? '0:00').trim()); ⟶ ` | green 64/64 | 0 red (00:02 +45) | SURVIVED | empty |
| N19 | `-      r'^(\d{1,2}):(\d{2})', ⟶ +      r'^(\d{1,2})[:.](\d{2})', ⟶ ` | green 64/64 | 0 red (00:01 +45) | SURVIVED | empty |
| N20 | `-    final int hour = int.parse(match.group(1)!); ⟶ -    final int minute = int.parse(match.group(2)!); ⟶ +    final int hour = int.parse(match.group(` | RED 29 (00:00 +35 -29) | n/a (red above) | KILLED | empty |
| N21 | `-    return hour * 60 + minute; ⟶ +    return hour * 59 + minute; ⟶ ` | RED 19 (00:00 +45 -19) | n/a (red above) | KILLED | empty |
| N22 | `-    return false; ⟶ +    return true; ⟶ ` | RED 14 (00:00 +50 -14) | n/a (red above) | KILLED | empty |
| N23 | `-  static const int defaultClosingSoonMinutes = 60; ⟶ +  static const int defaultClosingSoonMinutes = 59; ⟶ ` | RED 5 (00:00 +59 -5) | n/a (red above) | KILLED | empty |
| N24 | `-  }) => _availability.isStoreClosingSoon( ⟶ -    store, ⟶ -    thresholdMinutes: thresholdMinutes, ⟶ -  ); ⟶ +  }) => _availability.isStoreClosingSoo` | RED 2 (00:00 +62 -2) | n/a (red above) | KILLED | empty |
| N25 | `-  bool isStoreOpen24h(Store store) => _availability.isStoreOpen24h(store); ⟶ +  bool isStoreOpen24h(Store store) => false; ⟶ ` | RED 2 (00:00 +62 -2) | n/a (red above) | KILLED | empty |
| N26 | `-    isWithinWindow: DateConverter.isAvailable, ⟶ +    isWithinWindow: (String? o, String? c) => true, ⟶ ` | RED 4 (00:00 +60 -4) | n/a (red above) | KILLED | empty |
| N27 | `-      _availability.isStoreOpenNow(active, schedules); ⟶ +      _availability.isStoreOpenNow(true, schedules); ⟶ ` | green 64/64 | 2 red (00:01 +43 -2) | KILLED-by-net | empty |
| N28 | `-      _availability.isStoreClosed(today, active, schedules); ⟶ +      _availability.isStoreClosed(true, active, schedules); ⟶ ` | RED 1 (00:00 +63 -1) | n/a (red above) | KILLED | empty |
| N29 | `-      return true; ⟶ +      return false; ⟶ ` | RED 2 (00:00 +62 -2) | n/a (red above) | KILLED | empty |
| N30 | `-      date = date.add(const Duration(days: 1)); ⟶ +      date = date.add(const Duration(days: 2)); ⟶ ` | RED 3 (00:00 +61 -3) | n/a (red above) | KILLED | empty |
| N31 | `-    if (isStoreClosed(true, active, schedules)) { ⟶ +    if (isStoreClosed(false, active, schedules)) { ⟶ ` | RED 6 (00:00 +58 -6) | n/a (red above) | KILLED | empty |
| N32 | `-        } else if (nowTime.compareTo(closeTime) < 0) { ⟶ +        } else if (nowTime.compareTo(closeTime) <= 0) { ⟶ ` | RED 1 (00:00 +63 -1) | n/a (red above) | KILLED | empty |
| N33 | `-      _availability.isStoreClosed(today, active, schedules); ⟶ +      _availability.isStoreClosed(today, true, schedules); ⟶ ` | green 64/64 | 2 red (00:02 +43 -2) | KILLED-by-net | empty |

Survivors (genuine, non-equivalent - a scratch probe went red under each): N18, N19.
