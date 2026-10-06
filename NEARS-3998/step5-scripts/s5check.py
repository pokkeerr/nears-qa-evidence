#!/usr/bin/env python3
"""NEARS-3998 step 5 QA host scanners. usage: s5check.py <base_lc> <tip_lc> <owner> ; prints per-check verdicts; exit 0 only if every check passes.
Every check returns (ok, detail). Positive controls live in s5controls.py (seeded edits must turn each check red)."""
import sys,re,difflib
sys.path.insert(0,'/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa/scan')
from dartlex import blank,class_body,heads,public,name_of

def norm(t): return re.sub(r'\s+',' ',t).strip()
def fmtins(x): return re.sub(r',\s*([)\]}])',r'\1',re.sub(r'\s*([(){}\[\],;:<>=?.])\s*',r'\1',x))

def stmt_end(b,i):
    d=0
    while i<len(b):
        ch=b[i]
        if ch in '({[': d+=1
        elif ch in ')}]': d-=1
        elif ch==';' and d==0: return i+1
        i+=1
def member_end(b,i):
    par=0;j=i
    while j<len(b):
        ch=b[j]
        if ch in '([': par+=1
        elif ch in ')]': par-=1
        elif par==0 and b.startswith('=>',j): return stmt_end(b,j)
        elif par==0 and ch=='{':
            d=0
            while True:
                if b[j]=='{': d+=1
                elif b[j]=='}':
                    d-=1
                    if d==0: return j+1
                j+=1
        elif par==0 and ch==';': return j+1
        j+=1

# (name, kind, head regex) — 19 moved pieces
MEMBERS=[
 ('_debounce','field',r'^\s*Timer\? _debounce\b'),
 ('searchLocation','method',r'^\s*Future<List<PredictionModel>> searchLocation\('),
 ('_suggestionFanoutGeneration','field',r'^\s*int _suggestionFanoutGeneration\b'),
 ('_suggestionCacheVisit','field',r'^\s*int _suggestionCacheVisit\b'),
 ('_suggestionOutOfZoneCache','field',r'^\s*final Map<String, bool> _suggestionOutOfZoneCache\b'),
 ('_suggestionZoneIdCache','field',r'^\s*final Map<String, int> _suggestionZoneIdCache\b'),
 ('_suggestionProbesInFlight','field',r'^\s*final Map<String, Future<bool\?>> _suggestionProbesInFlight\b'),
 ('_topSuggestionPlaceIds','field',r'^\s*Set<String> _topSuggestionPlaceIds\b'),
 ('_pendingSuggestionPlaceIds','field',r'^\s*Set<String> _pendingSuggestionPlaceIds\b'),
 ('isSuggestionUnavailable','method',r'^\s*bool isSuggestionUnavailable\('),
 ('isSuggestionAvailable','method',r'^\s*bool isSuggestionAvailable\('),
 ('isSuggestionPending','method',r'^\s*bool isSuggestionPending\('),
 ('resetSuggestionAvailability','method',r'^\s*void resetSuggestionAvailability\('),
 ('suggestionAvailability','method',r'^\s*String suggestionAvailability\('),
 ('allTopSuggestionsUnavailable','method',r'^\s*bool allTopSuggestionsUnavailable\('),
 ('_startSuggestionZoneFanout','method',r'^\s*void _startSuggestionZoneFanout\('),
 ('_runSuggestionZoneFanout','method',r'^\s*Future<void> _runSuggestionZoneFanout\('),
 ('_probeSuggestion','method',r'^\s*Future<bool\?> _probeSuggestion\('),
 ('_isSuggestionOutOfZone','method',r'^\s*Future<bool\?> _isSuggestionOutOfZone\('),
]
def extract(src,kind,rx):
    b=blank(src,keep_strings=True)
    ms=list(re.finditer(rx,b,re.M))
    if len(ms)!=1: return None if not ms else 'MULTI'
    i=ms[0].start()+ (len(ms[0].group(0))-len(ms[0].group(0).lstrip()))
    e=stmt_end(b,i) if kind=='field' else member_end(b,i)
    return b[i:e]

def subs(name,t):
    s=[]
    if 'suggestionZoneCheckLimit' in t:
        c=t.count('suggestionZoneCheckLimit'); t=t.replace('suggestionZoneCheckLimit','checkLimit'); s.append('S1x%d'%c)
    if name=='_startSuggestionZoneFanout':
        assert t.count('update();')==1; t=t.replace('update();','onPendingPublished();'); s.append('S2')
    if name=='_runSuggestionZoneFanout':
        assert t.count('update();')==1; t=t.replace('update();','onCandidateSettled();'); s.append('S3')
        assert t.count('_logEvent(')==1; t=t.replace('_logEvent(','logEvent('); s.append('S4')
    return t,s

def check_verbatim(base,owner):
    rows=[];ok=True
    subtotals={'S1':0,'S2':0,'S3':0,'S4':0}
    for n,k,rx in MEMBERS:
        bt=extract(base,k,rx); ot=extract(owner,k,rx)
        if bt in (None,'MULTI') or ot in (None,'MULTI'):
            rows.append('%-30s base=%s owner=%s'%(n,bt if bt in (None,'MULTI') else 'ok',ot if ot in (None,'MULTI') else 'ok')); ok=False; continue
        t,s=subs(n,bt)
        for x in s: subtotals[x[:2]]+=int(x[3:]) if len(x)>2 else 1
        a=norm(t);b=norm(ot)
        ex=a==b; fm=fmtins(a)==fmtins(b)
        rows.append('%-30s subs=%-8s exact=%s fmt-insensitive=%s'%(n,','.join(s) or '-',ex,fm))
        if not fm:
            ok=False
            for l in difflib.unified_diff(re.split(r'(?<=[;{}])\s',a),re.split(r'(?<=[;{}])\s',b),lineterm='',n=0): rows.append('    '+l)
    # expected substitution totals: S1 x2, S2 x1, S3 x1, S4 x1
    exp={'S1':2,'S2':1,'S3':1,'S4':1}
    if subtotals!=exp: ok=False; rows.append('substitution totals %s != expected %s'%(subtotals,exp))
    else: rows.append('substitution totals %s == expected (S1 x2, S2 x1, S3 x1, S4 x1; nothing else)'%subtotals)
    return ok,rows

LIT=[('Duration(milliseconds: 400)',r'Duration\(milliseconds: 400\)'),('Future.wait',r'Future\.wait\b'),('putIfAbsent',r'putIfAbsent\b'),
     ('handleError: false',r'handleError: false'),('lat==0&&lng==0',r'latLng\.latitude == 0 && latLng\.longitude == 0'),
     ('403',r'\b403\b'),('404',r'\b404\b'),('zoneIds.first',r'zoneIds\.first'),
     ("'location searchLocation failed'",r"'location searchLocation failed'"),("'pick-map suggestion availability probe threw'",r"'pick-map suggestion availability probe threw'"),
     ('locationSearchSuggestionsFiltered',r'locationSearchSuggestionsFiltered'),
     ("'suggestions_before_filter'",r"'suggestions_before_filter'"),("'suggestions_after_filter'",r"'suggestions_after_filter'"),("'screen': 'pick_map'",r"'screen': 'pick_map'"),("'section': 'search_dialog'",r"'section': 'search_dialog'"),
     ('AppLogger.',r'AppLogger\.'),('showCustomSnackBar(',r'showCustomSnackBar\('),('ApiFailure(',r'ApiFailure\('),('print(',r'(?<![\w.])print\('),('unawaited(',r'unawaited\('),('Timer(',r'(?<![\w])Timer\('),
     ('generation guards',r'generation != _suggestionFanoutGeneration'),('visit guard',r'visit == _suggestionCacheVisit'),('.take(',r'\.take\(')]
def check_literals(base,owner):
    bm=''.join(extract(base,k,rx) for n,k,rx in MEMBERS); om=''.join(extract(owner,k,rx) for n,k,rx in MEMBERS)
    rows=[];ok=True
    for name,pat in LIT:
        cb=len(re.findall(pat,bm)); co=len(re.findall(pat,om))
        # owner: S1..S4 replace names only; literals must match
        rows.append('%-52s base-moved %2d owner-moved %2d %s'%(name,cb,co,'' if cb==co else 'MISMATCH'))
        if cb!=co: ok=False
    # whole-owner-file extra: only 2 accessor members beyond the 19; owner has exactly one Timer( and no literal 5
    ob=blank(owner)
    t=len(re.findall(r'(?<![\w])Timer\(',ob)); f5=len(re.findall(r'(?<![\w.$])5(?![\w.])',ob))
    rows.append('whole owner file code: Timer( x%d (expect 1), literal 5 x%d (expect 0), update( x%d (expect 0), LocationController token x%d (expect 0), Get.find x%d (expect 0), print( x%d (expect 0)'%(
        t,f5,len(re.findall(r'\bupdate\s*\(',ob)),len(re.findall(r'\bLocationController\b',ob)),len(re.findall(r'\bGet\.find\b',ob)),len(re.findall(r'(?<![\w.])print\(',ob))))
    if t!=1 or f5!=0 or re.search(r'\bupdate\s*\(',ob) or re.search(r'\bLocationController\b',ob) or re.search(r'\bGet\.find\b',ob) or re.search(r'(?<![\w.])print\(',ob): ok=False
    return ok,rows

def surface(src):
    hs=heads(class_body(src,'LocationController')); return hs,public(hs)
def check_surface(base,tip):
    bh,bp=surface(base); th,tp=surface(tip)
    rows=['base heads %d public %d ; tip heads %d public %d'%(len(bh),len(bp),len(th),len(tp))]
    d=list(difflib.unified_diff(bp,tp,lineterm='',n=0))
    rows.append('public-head diff lines: %d'%len(d)); rows+=['   '+x for x in d]
    return (len(d)==0 and len(bp)==len(tp)),rows

DELEG=[('searchLocation',r'^\s*Future<List<PredictionModel>> searchLocation\(',r'=> _suggestions\.searchLocation\(\s*context, query, filterServiceableZone: filterServiceableZone\s*\);$'),
 ('isSuggestionUnavailable',r'^\s*bool isSuggestionUnavailable\(',r'=> _suggestions\.isSuggestionUnavailable\(placeId\);$'),
 ('isSuggestionAvailable',r'^\s*bool isSuggestionAvailable\(',r'=> _suggestions\.isSuggestionAvailable\(placeId\);$'),
 ('isSuggestionPending',r'^\s*bool isSuggestionPending\(',r'=> _suggestions\.isSuggestionPending\(placeId\);$'),
 ('resetSuggestionAvailability',r'^\s*void resetSuggestionAvailability\(',r'=> _suggestions\.resetSuggestionAvailability\(\);$'),
 ('suggestionAvailability',r'^\s*String suggestionAvailability\(',r'=> _suggestions\.suggestionAvailability\(placeId\);$'),
 ('allTopSuggestionsUnavailable',r'^\s*bool allTopSuggestionsUnavailable\(',r'=> _suggestions\.allTopSuggestionsUnavailable\(suggestions\);$')]
def check_delegates(tip):
    b=blank(tip,keep_strings=True); rows=[];ok=True
    for n,hrx,call in DELEG:
        ms=list(re.finditer(hrx,b,re.M))
        if len(ms)!=1: rows.append('%s: head matches %d'%(n,len(ms))); ok=False; continue
        i=ms[0].start(); e=member_end(b,i); t=norm(b[i:e])
        bad=[]
        if re.search(r'\basync\b|\bawait\b',t): bad.append('async/await')
        if not re.search(call,t): bad.append('not the exact owner arrow')
        if t.count(';')!=1 or '{' in t.split('=>')[0].split('(',1)[0]+t.split('=>')[0][-1:] and False: pass
        if t.count('=>')!=1: bad.append('arrow count')
        if t.count(';')!=1: bad.append('statements')
        rows.append('%-30s %s :: %s'%(n,'OK ' if not bad else 'BAD '+','.join(bad),t[:150]))
        if bad: ok=False
    return ok,rows

MOVED_PRIV=['_debounce','_suggestionFanoutGeneration','_suggestionCacheVisit','_suggestionOutOfZoneCache','_suggestionZoneIdCache','_suggestionProbesInFlight','_topSuggestionPlaceIds','_pendingSuggestionPlaceIds','_startSuggestionZoneFanout','_runSuggestionZoneFanout','_probeSuggestion','_isSuggestionOutOfZone']
def check_moved_names(base,tip):
    bb=blank(base);tb=blank(tip);rows=[];ok=True
    for n in MOVED_PRIV:
        cb=len(re.findall(r'\b'+n+r'\b',bb)); ct=len(re.findall(r'\b'+n+r'\b',tb))
        rows.append('%-30s base %d tip %d'%(n,cb,ct))
        if ct!=0 or cb==0: ok=False
    return ok,rows

def census(src):
    b=blank(src);bare=[];keyed=[]
    for m in re.finditer(r'(?<![\w.])update\s*\(',b):
        j=m.end();d=1;k=j
        while d>0:
            if b[k]=='(': d+=1
            elif b[k]==')': d-=1
            k+=1
        arg=b[j:k-1].strip(); line=b.count('\n',0,m.start())+1
        (bare if arg=='' else keyed).append((line,arg))
    return bare,keyed
def check_census(base,tip,owner):
    bb,bk=census(base);tb,tk=census(tip);ob,ok_=census(owner)
    rows=['base %d bare / %d keyed ; tip %d bare / %d keyed ; owner %d/%d'%(len(bb),len(bk),len(tb),len(tk),len(ob),len(ok_))]
    return (len(bb)==18 and len(bk)==0 and len(tb)==18 and len(tk)==0 and len(ob)==0 and len(ok_)==0),rows

def check_facade_extras(base,tip):
    # facade keeps the const 5 exactly once, logSuggestionSelected + suggestionArea head unchanged, 'onClose' delegates cancel
    tb=blank(tip,keep_strings=True); rows=[];ok=True
    c=re.findall(r'static const int suggestionZoneCheckLimit = 5;',tb); rows.append('suggestionZoneCheckLimit = 5 declarations: %d'%len(c)); ok&=len(c)==1
    lit=len(re.findall(r'\.take\(\s*5\s*\)',tb)); rows.append('.take(5) literal in facade: %d'%lit); ok&=lit==0
    cx=len(re.findall(r'_suggestions\.cancelDebounce\(\)',tb)); rows.append('_suggestions.cancelDebounce() in onClose region: %d'%cx); ok&=cx==1
    zx=len(re.findall(r'_suggestions\.zoneIdOf\(suggestion\.placeId\)',tb)); rows.append('_suggestions.zoneIdOf( in logSuggestionSelected: %d'%zx); ok&=zx==1
    inst=len(re.findall(r'LocationSuggestions\(',tb)); rows.append('LocationSuggestions( constructions in facade: %d (expect 1)'%inst); ok&=inst==1
    return ok,rows

def run(base,tip,owner):
    res={}
    res['surface']=check_surface(base,tip); res['verbatim']=check_verbatim(base,owner); res['literals']=check_literals(base,owner)
    res['delegates']=check_delegates(tip); res['moved_names']=check_moved_names(base,tip); res['census']=check_census(base,tip,owner); res['facade_extras']=check_facade_extras(base,tip)
    return res
if __name__=='__main__':
    base=open(sys.argv[1]).read();tip=open(sys.argv[2]).read();owner=open(sys.argv[3]).read()
    res=run(base,tip,owner);allok=True
    for k,(ok,rows) in res.items():
        print('=== %s : %s'%(k,'PASS' if ok else 'FAIL'))
        for r in rows: print('  '+r)
        allok&=ok
    print('ALL PASS' if allok else 'SOME FAIL'); sys.exit(0 if allok else 1)
