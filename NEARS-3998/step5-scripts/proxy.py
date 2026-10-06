#!/usr/bin/env python3
"""QA logging proxy (step 5): listen :8335 -> backend :8334. One JSON line per request (ts, path-without-query, status, ms, +id=sha1[:6] of place id / q for autocomplete).
Mode file proxy_mode = comma tokens: ok | search500 (autocomplete answers 500, never reaches backend) | zone500 | delayzone:<s> (every get-zone-id delayed) | delaysearch:<s>.
place-api-autocomplete / place-api-details / config/get-zone-id answers are memoised per full URL for the proxy lifetime (deterministic base-vs-tip data; live Google ranking drifts) — the app still sends every request and every one is logged (cached:true when replayed).
GET /__mark?name=X writes a marker line (window delimiter)."""
import http.server, http.client, json, time, os, threading, socketserver, hashlib, urllib.parse
HERE=os.path.dirname(os.path.abspath(__file__))
LOG=os.path.join(HERE,'proxy_access.jsonl'); MODE=os.path.join(HERE,'proxy_mode')
BACK=('127.0.0.1',8334)
lock=threading.Lock(); memo={}
def log(d):
    with lock:
        with open(LOG,'a') as f: f.write(json.dumps(d)+'\n')
HOP={'connection','keep-alive','proxy-authenticate','proxy-authorization','te','trailers','transfer-encoding','upgrade','content-length','host'}
def tokens():
    return open(MODE).read().strip().split(',') if os.path.exists(MODE) else ['ok']
def tok(name):
    for t in tokens():
        if t==name: return ''
        if t.startswith(name+':'): return t.split(':',1)[1]
    return None
class H(http.server.BaseHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def log_message(self,*a): pass
    def _do(self):
        t0=time.time()
        if self.path.startswith('/__mark'):
            log({'ts':round(t0,3),'marker':self.path.split('name=',1)[-1]})
            self.send_response(200); self.send_header('Content-Length','2'); self.end_headers(); self.wfile.write(b'ok'); return
        n=int(self.headers.get('Content-Length') or 0); body=self.rfile.read(n) if n else None
        u=urllib.parse.urlsplit(self.path); path=u.path; qs=urllib.parse.parse_qs(u.query)
        rec={'ts':round(t0,3),'m':self.command,'path':path}
        if path.endswith('place-api-autocomplete'): rec['q']=(qs.get('search_text') or [''])[0]
        if path.endswith('place-api-details'): rec['id']=hashlib.sha1((qs.get('placeid') or [''])[0].encode()).hexdigest()[:6]
        if path.endswith('get-zone-id'): rec['id']=hashlib.sha1(((qs.get('lat') or [''])[0]+','+(qs.get('lng') or [''])[0]).encode()).hexdigest()[:6]
        if path.endswith('place-api-autocomplete') and tok('search500') is not None:
            b=b'{"errors":[{"code":"qa","message":"injected search failure"}]}'
            self.send_response(500); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
            rec.update(status=500,injected=True,ms=0); log(rec); return
        if path.endswith('get-zone-id'):
            if tok('zone500') is not None:
                b=b'{"errors":[{"code":"qa","message":"injected"}]}'
                self.send_response(500); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
                rec.update(status=500,injected=True,ms=0); log(rec); return
            d=tok('delayzone')
            if d: time.sleep(float(d))
        if path.endswith('place-api-autocomplete'):
            d=tok('delaysearch')
            if d: time.sleep(float(d))
        memokey=None
        if path.endswith(('place-api-autocomplete','place-api-details','get-zone-id')) and self.command=='GET': memokey=self.path
        try:
            if memokey and memokey in memo:
                status,hdrs,data=memo[memokey]; rec['cached']=True
            else:
                c=http.client.HTTPConnection(*BACK,timeout=120)
                hdr={k:v for k,v in self.headers.items() if k.lower() not in HOP}
                c.request(self.command,self.path,body=body,headers=hdr)
                r=c.getresponse(); data=r.read(); status=r.status; hdrs=r.getheaders()
                if memokey and status in (200,404): memo[memokey]=(status,hdrs,data)
            self.send_response(status)
            for k,v in hdrs:
                if k.lower() not in HOP: self.send_header(k,v)
            self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
            rec.update(status=status,ms=int((time.time()-t0)*1000)); log(rec)
        except Exception as e:
            b=b'proxy error'; self.send_response(502); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
            rec.update(status=502,err=type(e).__name__); log(rec)
    do_GET=do_POST=do_PUT=do_DELETE=do_PATCH=do_HEAD=do_OPTIONS=_do
class S(socketserver.ThreadingMixIn,http.server.HTTPServer): daemon_threads=True; allow_reuse_address=True
if __name__=='__main__':
    S(('0.0.0.0',8335),H).serve_forever()
