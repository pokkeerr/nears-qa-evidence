#!/usr/bin/env python3
import subprocess,sys,os,re,json,time
S='/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s4-qa'
W=S+'/tipscratch'; APP=W+'/UserApp'
O='UserApp/lib/features/location/controllers/location_zone_resolution.dart'
F='UserApp/lib/features/location/controllers/location_controller.dart'
T='UserApp/test/'
FILES=[ 'test/features/location/location_zone_resolution_test.dart',
        'test/features/location/location_zone_resolution_characterization_test.dart',
        'test/baseline/location/location_zone_effects_baseline_test.dart',
        'test/baseline/location/location_zone_sync_baseline_test.dart',
        'test/baseline/location/location_update_ids_source_baseline_test.dart',
        'test/features/location/location_controller_part1_test.dart',
        'test/features/location/location_get_zone_non_json_200_test.dart']
FETCH_OLD="""    beginFetch(markerLoad, updateInAddress);
    ZoneResponseModel responseModel = await locationServiceInterface.getZone(
      lat,
      lng,
      handleError: handleError,
    );
"""
CACHE_BLOCK="""    _pruneZoneResponseCache();
    _recentZoneByCoord['$lat,$lng'] = _CachedZoneResponse(
      responseModel,
      _clock(),
    );
"""
GUARD_FETCH="""    if (request != _zoneRequestToken) {
      return responseModel;
    }
"""
GUARD_REUSE="""    if (request != _zoneRequestToken) {
      return cachedResponse;
    }
"""
M=[
('M01','beginFetch moved after the service await (head no longer synchronous before the request)',[(O,FETCH_OLD,FETCH_OLD.split('\n')[1]+'\n'+FETCH_OLD.split('\n')[2]+'\n'+FETCH_OLD.split('\n')[3]+'\n'+FETCH_OLD.split('\n')[4]+'\n'+FETCH_OLD.split('\n')[5]+'\n    beginFetch(markerLoad, updateInAddress);\n')]),
('M02','beginFetch called twice per fetch',[(O,'    beginFetch(markerLoad, updateInAddress);\n    ZoneResponseModel','    beginFetch(markerLoad, updateInAddress);\n    beginFetch(markerLoad, updateInAddress);\n    ZoneResponseModel')]),
('M03','beginFetch also called on the reuse path',[(O,'    await Future<void>.microtask(() {});','    beginFetch(markerLoad, updateInAddress);\n    await Future<void>.microtask(() {});')]),
('M04','reuse microtask removed',[(O,'    await Future<void>.microtask(() {});\n','')]),
('M05','reuse microtask doubled',[(O,'    await Future<void>.microtask(() {});','    await Future<void>.microtask(() {});\n    await Future<void>.microtask(() {});')]),
('M06','reuse microtask replaced by Future.delayed(Duration.zero)',[(O,'await Future<void>.microtask(() {});','await Future<void>.delayed(Duration.zero);')]),
('M07','overtaken guard removed in _fetchZone',[(O,GUARD_FETCH,'')]),
('M08','overtaken guard removed in _reuseZoneResponse',[(O,GUARD_REUSE,'')]),
('M09','request token never bumped',[(O,'final int request = ++_zoneRequestToken;','final int request = _zoneRequestToken;')]),
('M10','lastApplied captured BEFORE the await (not after)',[(O,'    ZoneResponseModel response = await resolveZone(','    final ZoneResponseModel? la0 = lastApplied();\n    ZoneResponseModel response = await resolveZone('),(O,'if (!identical(response, lastApplied()))','if (!identical(response, la0))')]),
('M11','notify wired as the update tear-off (census 17)',[(F,'notify: () => update(),','notify: update,')]),
('M12','syncZoneData calls the owner own getZone, not the resolveZone seam',[(O,'await resolveZone(','await getZone(')]),
('M13','TTL boundary < to <= on the reuse check',[(O,'_clock().difference(cached.at) < _zoneResponseCacheTtl','_clock().difference(cached.at) <= _zoneResponseCacheTtl')]),
('M14','TTL prune >= to >',[(O,'now.difference(cached.at) >= _zoneResponseCacheTtl','now.difference(cached.at) > _zoneResponseCacheTtl')]),
('M15','cache cap 20 to 21',[(O,'_zoneResponseCacheMaxEntries = 20','_zoneResponseCacheMaxEntries = 21')]),
('M16','in-flight slot cleared by a non-identical future (identity check removed)',[(O,"""      if (identical(_inFlightZoneRequests[key], future)) {
        _inFlightZoneRequests.remove(key);
      }""","""      _inFlightZoneRequests.remove(key);""")]),
('M17','in-flight key loses handleError',[(O,"'$lat,$lng,$markerLoad,$updateInAddress,$handleError'","'$lat,$lng,$markerLoad,$updateInAddress'")]),
('M18','cache write moved after the overtaken return',[(O,CACHE_BLOCK,''),(O,GUARD_FETCH,GUARD_FETCH+"    _pruneZoneResponseCache();\n    _recentZoneByCoord['$lat,$lng'] = _CachedZoneResponse(responseModel, _clock());\n")]),
('M19','clock frozen at owner construction (facade passes a captured instant)',[(F,'clock: _clock,','clock: (() { final DateTime t0 = _clock(); return () => t0; })(),')]),
('M20','offline gate ignored in syncZoneData',[(O,'if (!hasInternet) {','if (false) {')]),
('M21','syncZoneData trailing notify dropped',[(O,'    notify();\n  }\n}','  }\n}')]),
('M22','syncZoneData trailing notify doubled',[(O,'    notify();\n  }\n}','    notify();\n    notify();\n  }\n}')]),
('M23','facade syncZoneData delegate made async/await',[(F,'Future<void> syncZoneData() => _zoneResolution.syncZoneData();','Future<void> syncZoneData() async => await _zoneResolution.syncZoneData();')]),
('M24','a second owner instance per call (getter instead of late final)',[(F,'late final LocationZoneResolution _zoneResolution = LocationZoneResolution(','LocationZoneResolution get _zoneResolution => LocationZoneResolution(')]),
('M25','checkInternet seam bypassed (always true)',[(F,'    clock: _clock,\n    checkInternet: checkInternet,','    clock: _clock,\n    checkInternet: () async => true,')]),
]
def sh(cmd,**k): return subprocess.run(cmd,shell=True,capture_output=True,text=True,**k)
def run_file(mid,f):
    slug=re.sub(r'[^A-Za-z0-9]','_',f)
    log=f'{S}/mut/{mid}_{slug}.log'
    r=sh(f'cd {APP} && python3 ~/.nears/bin/mem-guard.py --label s4qa-{mid}-{slug} --max-gb 6 --wait-s 3600 -- /Users/Apple/Tools/flutter/bin/flutter test --reporter compact {f} > {log} 2>&1; echo $?')
    rc=int(r.stdout.strip().splitlines()[-1])
    txt=open(log,errors='replace').read().replace('\r','\n')
    plus=re.findall(r'\+(\d+)',txt); minus=re.findall(r' -(\d+)',txt)
    fails=sorted(set(re.findall(r'\[E\]\s*$',txt,re.M)))
    names=[]
    for line in txt.split('\n'):
        if '[E]' in line:
            names.append(re.sub(r'^\d+:\d+ \+\d+( -\d+)?:\s*','',line.strip())[:200])
    names=list(dict.fromkeys(names))
    comp='Error:' in txt and ('lib/' in txt) and rc!=0 and not names
    return rc,names,comp,txt
def main(ids):
    os.makedirs(S+'/mut',exist_ok=True)
    out=open(S+'/mut_results.jsonl','a')
    for mid,desc,edits in M:
        if ids and mid not in ids: continue
        st=sh(f'cd {W} && git status --short').stdout.strip()
        assert st=='' , 'scratch dirty before '+mid+': '+st
        # apply
        for (path,old,new) in edits:
            p=f'{W}/{path}'; t=open(p).read()
            assert t.count(old)==1, f'{mid}: pattern count {t.count(old)} for {old[:60]!r}'
            open(p,'w').write(t.replace(old,new))
        diff=sh(f'cd {W} && git diff -U0').stdout
        assert diff.strip(), mid+' mutation did not land'
        open(f'{S}/mut/{mid}.diff','w').write(diff)
        res={'id':mid,'desc':desc,'landed_diff_lines':len(diff.splitlines()),'killed_by':None,'red_names':[],'compile_error':False,'ran':[]}
        for f in FILES:
            rc,names,comp,txt=run_file(mid,f)
            res['ran'].append({'file':f,'rc':rc,'plus':re.findall(r'\+(\d+)',txt)[-1:] ,'red':names[:6]})
            if rc!=0:
                if comp: res['compile_error']=True
                res['killed_by']=f; res['red_names']=names[:6]; break
        # restore
        sh(f'cd {W} && git checkout -- UserApp')
        res['restored_clean']= (sh(f'cd {W} && git diff --stat').stdout.strip()=='' and sh(f'cd {W} && git status --short').stdout.strip()=='')
        out.write(json.dumps(res)+'\n'); out.flush()
        print(mid,'KILLED by '+str(res['killed_by']) if res['killed_by'] else 'SURVIVED', 'compile_err' if res['compile_error'] else '', 'restored' if res['restored_clean'] else 'DIRTY!',flush=True)
if __name__=='__main__': main(sys.argv[1:])
