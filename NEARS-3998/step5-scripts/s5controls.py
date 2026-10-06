import sys,re
sys.path.insert(0,'/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa/scan')
import s5check as C
W='/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/nears3998s5-qa/wt/'
LC='UserApp/lib/features/location/controllers/location_controller.dart'; OW='UserApp/lib/features/location/controllers/location_suggestions.dart'
base=open(W+'base/'+LC).read();tip=open(W+'tip/'+LC).read();owner=open(W+'tip/'+OW).read()
base_res=C.run(base,tip,owner)
assert all(v[0] for v in base_res.values()),'premise: unmutated tip must be all-green'
def rep(s,a,b,count=1):
    assert s.count(a)>=1,'LANDING FAILED: %r not in source'%a
    return s.replace(a,b,count)
CONTROLS=[
 # (id, which source, mutation fn, check expected red)
 ('C1 extra param on searchLocation delegate (facade surface)','tip',lambda s:rep(s,'bool filterServiceableZone = false,\n  })','bool filterServiceableZone = false, int extra = 0,\n  })') if 'bool filterServiceableZone = false,\n  })' in s else rep(s,'bool filterServiceableZone = false','bool filterServiceableZone = false, int extra = 0'),'surface'),
 ('C2 extra public member in facade','tip',lambda s:rep(s,'void resetSuggestionAvailability() =>','int zzExtra() => 1;\n  void resetSuggestionAvailability() =>'),'surface'),
 ('C3 delegate gains async','tip',lambda s:rep(s,'bool isSuggestionPending(String? placeId) =>','bool isSuggestionPending(String? placeId) async =>'),'delegates'),
 ('C4 delegate awaits first','tip',lambda s:rep(s,'=> _suggestions.suggestionAvailability(placeId);','=> (() async { await Future<void>.value(); return _suggestions.suggestionAvailability(placeId); })();'),'delegates'),
 ('C5 moved private name re-appears in facade','tip',lambda s:rep(s,'  late final LocationSuggestions _suggestions','  int _suggestionCacheVisit = 0;\n  late final LocationSuggestions _suggestions'),'moved_names'),
 ('C6 census: one tear-off closure (17)','tip',lambda s:rep(s,'onPendingPublished: () => update(),','onPendingPublished: update,'),'census'),
 ('C7 census: keyed update (18+... keyed 1)','tip',lambda s:rep(s,'onCandidateSettled: () => update(),',"onCandidateSettled: () => update(['x']),"),'census'),
 ('C8 facade literal 5 in take','tip',lambda s:rep(s,'checkLimit: suggestionZoneCheckLimit,','checkLimit: 5,')+'\n// x\nvoid zzz(){ var a = [].take(5); }','facade_extras'),
 ('C9 owner 400->399','owner',lambda s:rep(s,'Duration(milliseconds: 400)','Duration(milliseconds: 399)'),'verbatim'),
 ('C10 owner limit literal','owner',lambda s:rep(s,'.take(checkLimit)','.take(4)'),'verbatim'),
 ('C11 owner generation guard flipped','owner',lambda s:rep(s,'if (generation != _suggestionFanoutGeneration) return;','if (generation == _suggestionFanoutGeneration) return;'),'verbatim'),
 ('C12 owner 403/404 swapped','owner',lambda s:rep(s,'zone.status == 403 || zone.status == 404','zone.status == 403 || zone.status == 405'),'verbatim'),
 ('C13 owner zoneIds.first->last','owner',lambda s:rep(s,'zone.zoneIds.first','zone.zoneIds.last'),'verbatim'),
 ('C14 owner handleError dropped','owner',lambda s:rep(s,'handleError: false,','handleError: true,'),'verbatim'),
 ('C15 owner a second Timer( / update( text','owner',lambda s:s+'\n// pad\nvoid zz(){ Timer(Duration.zero, (){}); update(); }','literals'),
 ('C16 owner extra notify call (S2 landing doubled)','owner',lambda s:rep(s,'onPendingPublished();','onPendingPublished(); onPendingPublished();'),'verbatim'),
 ('C17 owner event param key changed','owner',lambda s:rep(s,"'suggestions_after_filter'","'suggestions_after_filtr'"),'verbatim'),
 ('C18 owner Get.find added','owner',lambda s:rep(s,'int? zoneIdOf(String? placeId)','void zq(){ Get.find<LocationController>(); }\n  int? zoneIdOf(String? placeId)'),'literals'),
 ('C19 owner raw print added to a moved member','owner',lambda s:rep(s,"showCustomSnackBar(result.errorMessage);","showCustomSnackBar(result.errorMessage); print('x');"),'verbatim'),
]
bad=0
for cid,which,fn,expect in CONTROLS:
    b,t,o=base,tip,owner
    if which=='tip': t=fn(t)
    else: o=fn(o)
    src_changed=(t!=tip) or (o!=owner); assert src_changed,'mutation did not change source: '+cid
    r=C.run(b,t,o); red=[k for k,v in r.items() if not v[0]]
    ok=expect in red
    bad+= (not ok)
    print('%-58s expected-red=%-13s got-red=%s %s'%(cid,expect,red,'OK(control fires)' if ok else '<<< CONTROL DID NOT FIRE'))
print('CONTROLS ALL FIRE' if not bad else 'CONTROL FAILURES: %d'%bad); sys.exit(bad)
