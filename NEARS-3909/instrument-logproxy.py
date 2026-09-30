#!/usr/bin/env python3
# QA3909 logging pass-through proxy: 127.0.0.1/0.0.0.0:8141 -> 127.0.0.1:8140. Logs method, path (no query values), status, echoed X-Request-Id.
import http.server, socketserver, urllib.request, urllib.error, sys, time, re
UP="http://127.0.0.1:8140"; LOG=open(sys.argv[1],"a",buffering=1); FLAG=sys.argv[2]
class H(http.server.BaseHTTPRequestHandler):
    protocol_version="HTTP/1.0"
    def _do(self):
        import os
        if self.path.startswith("/payment-mobile") and os.path.exists(FLAG):
            LOG.write(f"{time.strftime('%H:%M:%S')} {self.command} /payment-mobile -> 302 SIMULATED-GATEWAY-CANCEL (proxy instrument) to /payment-cancel\n")
            self.send_response(302); self.send_header("Location","http://10.0.2.2:8141/payment-cancel?flag=cancel"); self.send_header("Content-Length","0"); self.end_headers(); return
        n=int(self.headers.get("Content-Length") or 0); body=self.rfile.read(n) if n else None
        req=urllib.request.Request(UP+self.path,data=body,method=self.command)
        for k,v in self.headers.items():
            if k.lower() not in ("host","connection","accept-encoding"): req.add_header(k,v)
        try: r=urllib.request.urlopen(req,timeout=60); code=r.status; hdr=r.headers; data=r.read()
        except urllib.error.HTTPError as e: code=e.code; hdr=e.headers; data=e.read()
        except Exception as e:
            LOG.write(f"{time.strftime('%H:%M:%S')} {self.command} {self.path.split('?')[0]} PROXY_ERR {e}\n"); self.send_error(502); return
        rid=hdr.get("X-Request-Id","-")
        q=self.path.split("?",1); path=q[0]+("?"+re.sub(r"(token|payment_token)=[^&]*",r"\1=<redacted>",q[1]) if len(q)>1 else "")
        mh=self.headers.get("moduleId","-"); zh=self.headers.get("zoneId","-"); rb=(body.decode("utf8","ignore")[:120] if (body and "delivery-quote" in path) else "-")
        LOG.write(f"{time.strftime('%H:%M:%S')} {self.command} {path} -> {code} x-request-id={rid} hdr[moduleId={mh} zoneId={zh}] reqbody={rb} bytes={len(data)}\n")
        self.send_response(code)
        for k,v in hdr.items():
            if k.lower() not in ("transfer-encoding","connection","content-length"): self.send_header(k,v)
        self.send_header("Content-Length",str(len(data))); self.end_headers(); self.wfile.write(data)
    do_GET=do_POST=do_PUT=do_DELETE=do_PATCH=_do
    def log_message(self,*a): pass
class S(socketserver.ThreadingMixIn,http.server.HTTPServer): daemon_threads=True; allow_reuse_address=True
S(("0.0.0.0",8141),H).serve_forever()
