import re, http.server, http.client, sys, time, threading, socketserver
UP=int(sys.argv[1]); LISTEN=int(sys.argv[2]); LOG=sys.argv[3]
lock=threading.Lock()
class H(http.server.BaseHTTPRequestHandler):
    protocol_version='HTTP/1.0'
    def log_message(self,*a): pass
    def do(self):
        n=int(self.headers.get('Content-Length') or 0); body=self.rfile.read(n) if n else None
        import os
        if os.path.exists(LOG+'.fail') and any(k in self.path for k in open(LOG+'.fail').read().split()):
            rid=self.headers.get('X-Request-Id','')
            with lock: open(LOG,'a').write(f"{time.strftime('%H:%M:%S')} {self.command} {re.sub(r'token=[^&]*','token=X',self.path)} -> 500 (injected) rid={rid}\n")
            self.send_response(500); self.send_header('Content-Type','application/json'); self.send_header('x-request-id',rid); b=b'{"errors":[{"code":"x","message":"boom"}]}'; self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b); return
        c=http.client.HTTPConnection('127.0.0.1',UP,timeout=120)
        hdrs={k:v for k,v in self.headers.items() if k.lower() not in ('host','connection')}
        try:
            c.request(self.command,self.path,body,hdrs); r=c.getresponse(); data=r.read()
        except Exception as e:
            self.send_response(502); self.end_headers(); 
            with lock: open(LOG,'a').write(f"{time.strftime('%H:%M:%S')} {self.command} {self.path} -> 502 {e}\n")
            return
        with lock: open(LOG,'a').write(f"{time.strftime('%H:%M:%S')} {self.command} {re.sub(r'token=[^&]*','token=X',self.path)} -> {r.status}\n")
        self.send_response(r.status)
        for k,v in r.getheaders():
            if k.lower() in ('transfer-encoding','connection','content-length'): continue
            self.send_header(k,v)
        self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    do_GET=do_POST=do_PUT=do_DELETE=do
class S(socketserver.ThreadingMixIn,http.server.HTTPServer): daemon_threads=True
S(('0.0.0.0',LISTEN),H).serve_forever()
