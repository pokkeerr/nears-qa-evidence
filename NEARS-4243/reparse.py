import re,sys
# usage: reparse.py RUNDIR YES_HOST_EPOCH SKEW  -> prints logcat lines relative to Yes tap
d,t,k=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
for ln in open(d+'/logcat.txt'):
    m=re.match(r"\s*(\d+\.\d+)\s+\d+\s+\d+\s+\S\s+(\S+)\s*:\s*(.*)",ln)
    if m and any(x in ln for x in ('[NET]','[FAIL]','[ERR]','order_accept','Logging event')):
        print(f"+{float(m.group(1))+k-t:7.2f}s  {m.group(3)[:200]}")
