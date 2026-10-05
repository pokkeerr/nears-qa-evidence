#!/usr/bin/env python3
# NEARS-3993-s2 QA: logging pass-through proxy (listen :8393 -> artisan :8394) so the request log has method+path.
import sys, time, http.client, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
LISTEN=int(sys.argv[1]); UP=int(sys.argv[2]); LOG=sys.argv[3]
lock=threading.Lock()
def log(line):
    with lock:
        with open(LOG,'a') as f: f.write(line+"\n")
class H(BaseHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def log_message(self,*a): pass
    def _do(self):
        n=int(self.headers.get('Content-Length') or 0)
        body=self.rfile.read(n) if n else None
        hdrs={k:v for k,v in self.headers.items() if k.lower() not in ('connection','keep-alive','proxy-connection','transfer-encoding')}
        t0=time.time()
        try:
            c=http.client.HTTPConnection('127.0.0.1',UP,timeout=120)
            c.request(self.command,self.path,body=body,headers=hdrs)
            r=c.getresponse(); data=r.read()
            self.send_response(r.status)
            for k,v in r.getheaders():
                if k.lower() in ('transfer-encoding','connection','content-length','keep-alive'): continue
                self.send_header(k,v)
            self.send_header('Content-Length',str(len(data)))
            self.end_headers(); self.wfile.write(data)
            log("%s\t%s\t%s\t%d\t%dB\t%.0fms\trid=%s" % (time.strftime('%H:%M:%S',time.localtime(t0)), self.command, self.path, r.status, len(data), (time.time()-t0)*1000, r.getheader('X-Request-Id','-')))
            c.close()
        except Exception as e:
            log("%s\t%s\t%s\tERR %r" % (time.strftime('%H:%M:%S'), self.command, self.path, e))
            try: self.send_error(502)
            except Exception: pass
    do_GET=do_POST=do_PUT=do_PATCH=do_DELETE=do_OPTIONS=do_HEAD=_do
ThreadingHTTPServer(('0.0.0.0',LISTEN),H).serve_forever()
