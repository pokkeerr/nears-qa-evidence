#!/usr/bin/env python3
# NEARS-3993-s2 QA: logging pass-through proxy (listen :8393 -> artisan :8394) so the request log has method+path.
import sys, time, http.client, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
lock=threading.Lock()
LISTEN=int(sys.argv[1]); UP=int(sys.argv[2]); LOG=sys.argv[3]
import os
ARR=os.path.join(os.path.dirname(LOG),'arrivals.log'); DELAY=os.path.join(os.path.dirname(LOG),'delay.txt')
SEQ=[0]
def delay_for(path):
    try:
        for l in open(DELAY):
            p=l.split()
            if len(p)==2 and p[0] in path: return float(p[1])
    except Exception: pass
    return 0.0
FAIL=os.path.join(os.path.dirname(LOG),'fail.txt')
def fail_for(path):
    try:
        for l in open(FAIL):
            p=l.split()
            if len(p)==2 and p[0] in path: return int(p[1])
    except Exception: pass
    return 0
def arr(line):
    with lock:
        SEQ[0]+=1
        with open(ARR,'a') as f: f.write('%d\t%.3f\t%s\n'%(SEQ[0],time.time(),line))
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
        arr(self.command+' '+self.path)
        d=delay_for(self.path)
        if d>0: time.sleep(d)
        fs=fail_for(self.path)
        if fs:
            body=b'{"errors":[{"code":"qa","message":"qa-injected failure"}]}'
            self.send_response(fs); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
            log("%s\t%s\t%s\t%d\t%dB\t%.0fms\trid=injected" % (time.strftime('%H:%M:%S',time.localtime(t0)), self.command, self.path, fs, len(body), (time.time()-t0)*1000))
            return
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
