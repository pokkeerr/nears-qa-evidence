# usage: summ.sh <tag>  -- reads the checkout Order Summary from a fresh dump + screenshot
T=$1; D=/private/tmp/claude-501/-Users-Apple-Projects-nears/272c552a-66ed-4d99-a9d9-aa7b921f5263/scratchpad/qa3925r2/ev
adb -s emulator-5590 exec-out screencap -p > $D/dev-$T-summary.png
for i in 1 2 3; do adb -s emulator-5590 shell uiautomator dump /sdcard/a.xml >/dev/null 2>&1; adb -s emulator-5590 exec-out cat /sdcard/a.xml > $D/dev-$T-summary.xml; grep -q "Order Summary" $D/dev-$T-summary.xml && break; done
python3 - $D/dev-$T-summary.xml <<'PY'
import re,sys
x=open(sys.argv[1]).read()
rows=[(int(m.group(2)),int(m.group(3)),m.group(1).replace('⁦','').replace('⁩','')) for m in re.finditer(r'(?:content-desc|text)="([^"]+)"[^>]*bounds="\[(\d+),(\d+)\]',x)]
for a,b,t in rows:
    if re.search(r'Subtotal|Discount|VAT|Delivery Fee|Free|AED$|^\d$|^\.$|Tax|Total',t) and 'Cash' not in t: print(a,b,t)
PY
