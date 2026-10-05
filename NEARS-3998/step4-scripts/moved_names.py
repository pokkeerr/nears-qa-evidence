import sys,re
sys.path.insert(0,'.')
from dartlex import *
t=blank(open('tip_lc.dart').read(),keep_strings=True); b=blank(open('base_lc.dart').read(),keep_strings=True)
for n in ['_CachedZoneResponse','_zoneRequestToken','_inFlightZoneRequests','_recentZoneByCoord','_zoneResponseCacheTtl','_zoneResponseCacheMaxEntries','_pruneZoneResponseCache','_reuseZoneResponse','_fetchZone']:
    pat=r'\b'+n+r'\b'
    print('  %s: base %d tip %d' % (n,len(re.findall(pat,b)),len(re.findall(pat,t))))
