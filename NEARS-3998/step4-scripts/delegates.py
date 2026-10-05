import sys,re
sys.path.insert(0,'.')
from dartlex import *
def member_text(src, head_re):
    b=blank(src)
    body_start=re.search(r'\bclass\s+LocationController\b[^{]*\{',b).end()
    m=re.search(head_re,b[body_start:],re.M)
    if not m: return None
    i=body_start+m.start(); 
    # find end: first top-level ; or matching } of body
    j=i;par=0
    while j<len(b):
        ch=b[j]
        if ch in '([': par+=1
        elif ch in ')]': par-=1
        elif par==0 and ch=='{':
            d=0
            while True:
                if b[j]=='{': d+=1
                elif b[j]=='}':
                    d-=1
                    if d==0: break
                j+=1
            return re.sub(r'\s+',' ',b[i:j+1])
        elif par==0 and ch==';': return re.sub(r'\s+',' ',b[i:j+1])
        j+=1
def check(path):
    src=open(path).read()
    res={}
    g=member_text(src,r'^\s*Future<ZoneResponseModel> getZone\(')
    s=member_text(src,r'^\s*Future<void> syncZoneData\(')
    res['getZone']=g; res['syncZoneData']=s
    ok=True; why=[]
    for name,t,call in (('getZone',g,r'=> _zoneResolution\.getZone\(\s*lat, lng, markerLoad, updateInAddress: updateInAddress, handleError: handleError\s*\);$'),('syncZoneData',s,r'=> _zoneResolution\.syncZoneData\(\);$')):
        if t is None: ok=False; why.append(name+' missing'); continue
        if re.search(r'\basync\b|\bawait\b',t): ok=False; why.append(name+' has async/await')
        if '{' in t.split('=>')[0][-1:]: pass
        if not re.search(call,t): ok=False; why.append(name+' not a one-statement arrow to owner')
        if t.count(';')!=1: ok=False; why.append(name+' multiple statements')
    return ok,why,res
if __name__=='__main__':
    ok,why,res=check(sys.argv[1])
    print('OK' if ok else 'FAIL',why); 
    for k,v in res.items(): print(k,'::',v)
    sys.exit(0 if ok else 1)
