import sys,re,difflib
sys.path.insert(0,'.')
from dartlex import *
def stmt_end(b,i):
    d=0
    while i<len(b):
        ch=b[i]
        if ch in '({[': d+=1
        elif ch in ')}]': d-=1
        elif ch==';' and d==0: return i+1
        i+=1
def block_end(b,i):
    # first '{' at paren depth 0 from i, return index after matching '}'
    par=0
    while i<len(b):
        ch=b[i]
        if ch in '([': par+=1
        elif ch in ')]': par-=1
        elif ch=='{' and par==0:
            d=0
            while True:
                if b[i]=='{': d+=1
                elif b[i]=='}':
                    d-=1
                    if d==0: return i+1
                i+=1
        i+=1
def norm(t): return re.sub(r'\s+',' ',t).strip()
MEMBERS=[
 ('_CachedZoneResponse','class',r'^class _CachedZoneResponse\b'),
 ('_zoneRequestToken','field',r'^\s*int _zoneRequestToken\b'),
 ('_inFlightZoneRequests','field',r'^\s*final Map<String, Future<ZoneResponseModel>> _inFlightZoneRequests\b'),
 ('_recentZoneByCoord','field',r'^\s*final Map<String, _CachedZoneResponse> _recentZoneByCoord\b'),
 ('_zoneResponseCacheTtl','field',r'^\s*static const Duration _zoneResponseCacheTtl\b'),
 ('_zoneResponseCacheMaxEntries','field',r'^\s*static const int _zoneResponseCacheMaxEntries\b'),
 ('_pruneZoneResponseCache','method',r'^\s*void _pruneZoneResponseCache\('),
 ('getZone','method',r'^\s*Future<ZoneResponseModel> getZone\('),
 ('_reuseZoneResponse','method',r'^\s*Future<ZoneResponseModel> _reuseZoneResponse\('),
 ('_fetchZone','method',r'^\s*Future<ZoneResponseModel> _fetchZone\('),
 ('syncZoneData','method',r'^\s*Future<void> syncZoneData\('),
]
def extract(src,kind,rx):
    b=blank(src,keep_strings=True)
    m=re.search(rx,b,re.M)
    if not m: return None
    i=m.start()
    e = stmt_end(b,i) if kind=='field' else block_end(b,i)
    return b[i:e]
def get_members(path,which):
    src=open(path).read()
    return {n:extract(src,k,rx) for n,k,rx in MEMBERS if (n in which)}
BASE_SUBS=lambda name,t: t
if __name__=='__main__':
    base=open(sys.argv[1]).read(); owner=open(sys.argv[2]).read()
    mutate=sys.argv[3] if len(sys.argv)>3 else None
    results=[];allok=True
    for n,k,rx in MEMBERS:
        bt=extract(base,k,rx); ot=extract(owner,k,rx)
        if bt is None: print(n,'MISSING IN BASE'); allok=False; continue
        if ot is None: print(n,'MISSING IN OWNER'); allok=False; continue
        # mechanical substitutions, exhaustive list
        s=[]
        t=bt
        if n=='_fetchZone':
            head=re.search(r'\{\s*if \(markerLoad\) \{.*?update\(\);\s*\}\s*(?=ZoneResponseModel responseModel)',t,re.S)
            hd=head.group(0)
            t=t.replace(hd,'{ beginFetch(markerLoad, updateInAddress); ',1); s.append('S2 head->beginFetch')
        if '_applyZoneEffects(' in t:
            c=t.count('_applyZoneEffects('); t=t.replace('_applyZoneEffects(','applyEffects('); s.append('S1 x%d'%c)
        if n=='syncZoneData':
            assert 'await getZone(' in t; t=t.replace('await getZone(','await resolveZone(',1); s.append('S3')
            assert '_lastAppliedZoneResponse' in t; t=t.replace('_lastAppliedZoneResponse','lastApplied()'); s.append('S4')
            assert t.rstrip().endswith('update();\n  }') or re.search(r'update\(\);\s*\}\s*$',t); t=re.sub(r'update\(\);(\s*\})\s*$',r'notify();\1',t); s.append('S5')
        # owner: strip nothing; compare normalised
        a=norm(t); bb=norm(ot)
        # formatter-insensitive second pass: drop whitespace adjacent to punctuation + trailing commas
        f=lambda x: re.sub(r',\s*([)\]}])',r'\1',re.sub(r'\s*([(){}\[\],;:<>=?.])\s*',r'\1',x))
        same_exact = a==bb
        same_fmt = f(a)==f(bb)
        print('%-30s subs=%-22s exact=%s fmt-insensitive=%s'%(n,','.join(s) or '-',same_exact,same_fmt))
        if not same_fmt:
            allok=False
            for l in difflib.unified_diff(re.split(r'(?<=[;{}])\s',a),re.split(r'(?<=[;{}])\s',bb),lineterm='',n=0): print('   ',l)
        results.append((n,same_exact,same_fmt))
    print('ALL-MATCH' if allok else 'RESIDUE-NONEMPTY')
    sys.exit(0 if allok else 1)
