#!/usr/bin/env python3
"""QA logging proxy: listen :8235 -> backend :8234. Logs one JSON line per request (ts, method, path, status, ms).
Mode file proxy_mode: 'ok' | 'zone500' (get-zone-id answers 500 without reaching the backend).
GET /__mark?name=X writes a marker line (window delimiter)."""
import http.server, http.client, json, time, sys, os, threading, socketserver
HERE=os.path.dirname(os.path.abspath(__file__))
LOG=os.path.join(HERE,'proxy_access.jsonl'); MODE=os.path.join(HERE,'proxy_mode')
BACK=('127.0.0.1',8234)
lock=threading.Lock()
def log(d):
    with lock:
        with open(LOG,'a') as f: f.write(json.dumps(d)+'\n')
HOP={'connection','keep-alive','proxy-authenticate','proxy-authorization','te','trailers','transfer-encoding','upgrade','content-length','host'}
class H(http.server.BaseHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def log_message(self,*a): pass
    def _do(self):
        t0=time.time()
        if self.path.startswith('/__mark'):
            log({'ts':round(t0,3),'marker':self.path.split('name=',1)[-1]}); 
            self.send_response(200); self.send_header('Content-Length','2'); self.end_headers(); self.wfile.write(b'ok'); return
        n=int(self.headers.get('Content-Length') or 0); body=self.rfile.read(n) if n else None
        mode=(open(MODE).read().strip() if os.path.exists(MODE) else 'ok')
        path=self.path.split('?')[0]
        if mode=='zone500' and path.endswith('/config/get-zone-id'):
            b=b'{"errors":[{"code":"qa","message":"injected"}]}'
            self.send_response(500); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
            log({'ts':round(t0,3),'m':self.command,'path':self.path,'status':500,'injected':True,'ms':0}); return
        dly=0.0
        if path.endswith('/config/get-zone-id'):
            m=mode.split(':')
            if m[0]=='delayall' and len(m)>1: dly=float(m[1])
        try:
            if dly: time.sleep(dly)
            c=http.client.HTTPConnection(*BACK,timeout=120)
            hdr={k:v for k,v in self.headers.items() if k.lower() not in HOP}
            c.request(self.command,self.path,body=body,headers=hdr)
            r=c.getresponse(); data=r.read()
            if path.endswith('/config/get-zone-id') and mode.startswith('delay200:') and r.status==200:
                time.sleep(float(mode.split(':')[1]))
            self.send_response(r.status)
            for k,v in r.getheaders():
                if k.lower() not in HOP: self.send_header(k,v)
            self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
            log({'ts':round(t0,3),'m':self.command,'path':self.path,'status':r.status,'ms':int((time.time()-t0)*1000)})
        except Exception as e:
            b=b'proxy error'; self.send_response(502); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
            log({'ts':round(t0,3),'m':self.command,'path':self.path,'status':502,'err':type(e).__name__})
    do_GET=do_POST=do_PUT=do_DELETE=do_PATCH=do_HEAD=do_OPTIONS=_do
class S(socketserver.ThreadingMixIn,http.server.HTTPServer): daemon_threads=True; allow_reuse_address=True
if __name__=='__main__':
    S(('0.0.0.0',8235),H).serve_forever()
