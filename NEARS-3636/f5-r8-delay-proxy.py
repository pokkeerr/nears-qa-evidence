import http.server, socketserver, urllib.request, urllib.error, time, os, sys
TARGET='http://127.0.0.1:8636'; FLAG=sys.argv[2]; PORT=int(sys.argv[1])
HOP={'connection','keep-alive','transfer-encoding','te','trailer','upgrade','proxy-authorization','proxy-authenticate','content-length','host'}
class H(http.server.BaseHTTPRequestHandler):
    protocol_version='HTTP/1.0'
    def _do(self):
        n=int(self.headers.get('Content-Length') or 0); body=self.rfile.read(n) if n else None
        if self.path.startswith('/api/v1/coupon/list') and os.path.exists(FLAG):
            time.sleep(float(open(FLAG).read().strip() or 12))
        req=urllib.request.Request(TARGET+self.path,data=body,method=self.command)
        for k,v in self.headers.items():
            if k.lower() not in HOP: req.add_header(k,v)
        try: r=urllib.request.urlopen(req,timeout=60); code=r.status; hd=r.headers; data=r.read()
        except urllib.error.HTTPError as e: code=e.code; hd=e.headers; data=e.read()
        self.send_response(code)
        for k,v in hd.items():
            if k.lower() not in HOP: self.send_header(k,v)
        self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    do_GET=do_POST=do_PUT=do_DELETE=do_PATCH=_do
    def log_message(self,*a): pass
class S(socketserver.ThreadingMixIn,http.server.HTTPServer): daemon_threads=True
S(('0.0.0.0',PORT),H).serve_forever()
