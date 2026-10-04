# NEARS-3996 step 2 QA progress (QA'd sha e6055bd3b2df71b741f96b7ee999eddcfc7e9d2f, base ca8f0d612, first pass, fix_cycle 0)
- AC-0 PASS scope diff = 6 paths; get_di/helper/pubspec diff empty; PNG 0
- AC-1 PASS policy file has no get/flutter/.tr/Get./Timer/addListener/DateTime.now code lines
- AC-2 PASS facade bodies one-line delegates; 0 `update(` added; ctor + _now untouched; analyze 14 infos == base 14 (identical modulo line numbers)
- AC-3..AC-7, AC-9 PASS automated net 31/31 files green (new file 54, +2 random seeds, share default and with WEB_HOSTED_URL)
- AC-8 PASS 34 independent mutations: 31 red; 3 SURVIVORS (S01,S02,S11) -> Medium pin gap (mutations-qa.md)
- AC-10 PASS emulator walk base vs step2, same data/clock, 3 clock points (13:30, 22:30, 23:30); see compare-*.txt
- AC-11 UNVERIFIED (waiver) ; AC-12 UNVERIFIABLE

## Delta re-QA fix cycle 2 (sha ae9bf9825, device-free; lib byte-identical to e6055bd3b so AC-10 emulator PASS carries over)
- diff e6055bd3b..ae9bf9825 = 2 test-side files only; UserApp/lib diff 0 bytes; 0 PNG vs base
- AC-5/AC-8: S01,S02,S11 re-landed: all RED in the new file (5/1/2 red). 33 further own mutations (N01-N33): 29 red in new file, 2 red only in unmodified net (N27,N33), 2 SURVIVORS (N18 null time default, N19 separator class) -> Medium vacuous pins (mutations-qa2.md, bug-vacuous-pins-minuteofday-null-and-separator.log)
- tests live: new 64 (+seed 12345 64), matrix 10, edge 24, facade_scope 11, smart_mgmt 10, distance 11, dispose 1, golden_manifest 5; analyze scoped 14 infos 0 new
