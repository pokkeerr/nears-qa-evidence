import sys, json
for l in sys.stdin:
    r = json.loads(l); b = r['body']
    try:
        j = json.loads(b) if b else {}
        keep = {k: j.get(k) for k in ('cart_id','item_id','quantity','price','variant','variation','model','add_on_ids','add_on_qtys','item_type') if k in j}
        b = json.dumps(keep) if keep else b
    except Exception:
        pass
    print('  %sZ(%s) %s %s?%s moduleId=%s zoneId=%s status=%s body=%s' % (r['iso'], r['ts'], r['method'], r['path'], r['query'], r['moduleId'], r.get('zoneId'), r['status'], b))
