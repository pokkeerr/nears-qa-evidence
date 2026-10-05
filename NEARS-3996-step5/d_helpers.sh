# source me:  source d.sh
export ANDROID_SERIAL=emulator-5554
Q=/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3996-s5/qa
source /Users/Apple/Projects/nears-NEARS-3996-u5-step5/scripts/app-nav/uinav.sh
PKG_TIP=com.izzes.nears.nears_nears_3996_u5_step5
PKG_BASE=com.izzes.nears.nears_nears_3996_u5_step5_qabase
mk() { curl -s "http://127.0.0.1:8250/__mark?name=$1" >/dev/null; }
labels() { ui_list 2>/dev/null; }
launch() { adb shell monkey -p $1 -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1; }
reqs() { python3 - "$1" <<'PY'
import json,sys
Q='/private/tmp/claude-501/-Users-Apple-Projects-nears/6029ad35-768a-4271-8ca7-36fb0d931010/scratchpad/NEARS-3996-s5/qa'
rows=[json.loads(l) for l in open(Q+'/proxy_access.jsonl')]
idx=[k for k,r in enumerate(rows) if r.get('marker')==sys.argv[1]]
if not idx: print('NO MARKER'); sys.exit()
out=[]
for r in rows[idx[-1]+1:]:
    if r.get('marker'): break
    p=r.get('path','')
    if p.startswith('/storage') or p.startswith('/public'): continue
    out.append('%s %s %s'%(r['m'],p.replace('/api/v1/',''),r['status']))
print('\n'.join(out) if out else '(no requests)')
PY
}
tap1() { ui_tap "$@" 2>&1 | tail -1; }
