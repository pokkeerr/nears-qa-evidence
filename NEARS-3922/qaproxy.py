#!/usr/bin/env python3
# NEARS-3922 QA instrument: pass-through proxy :8122 -> :8124 that logs method, path,
# X-Request-Id (request + echoed), status and a whitelist of non-PII fields only.
import http.client, json, re, sys, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UP_HOST, UP_PORT = "127.0.0.1", int(sys.argv[2]) if len(sys.argv) > 2 else 8124
LISTEN = int(sys.argv[1]) if len(sys.argv) > 1 else 8122
LOG = sys.argv[3] if len(sys.argv) > 3 else "qaproxy.log"
REQ_KEYS = ["date_time", "zone_id", "module_id", "schedule_at", "order_type", "payment_method", "order_amount"]
RESP_KEYS = ["price", "price_type", "title", "order_id", "group_id", "order_ids", "message"]
INTERESTING = ("surge", "place", "order/group", "get-Tax", "delivery-quote", "extra-charge", "get-quote")


def pick(raw: bytes, keys):
    out = {}
    text = raw.decode("utf-8", "replace")
    for k in keys:
        m = (re.search(r'"%s"\s*:\s*("([^"]*)"|[-0-9.]+|null|\[[^\]]*\])' % re.escape(k), text)
             or re.search(r'name="%s"\r?\n\r?\n([^\r\n]*)' % re.escape(k), text)
             or re.search(r'(?:^|&)%s=([^&]*)' % re.escape(k), text))
        if m:
            v = m.group(2) if (m.lastindex and m.lastindex >= 2 and m.group(2) is not None) else m.group(1)
            out[k] = v.strip('"') if isinstance(v, str) else v
    return out


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def _go(self):
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n) if n else b""
        hdrs = {k: v for k, v in self.headers.items() if k.lower() not in ("host", "connection", "accept-encoding")}
        import os
        dfile = os.path.join(os.path.dirname(os.path.abspath(LOG)), "delay_surge")
        if "get-surge-price" in self.path and os.path.exists(dfile):
            time.sleep(float(open(dfile).read().strip() or 0))
        if "get-surge-price" in self.path and os.path.exists(os.path.join(os.path.dirname(os.path.abspath(LOG)), "fail_surge")):
            rid = self.headers.get("X-Request-Id") or ""
            data = b'{"errors":[{"code":"qa","message":"QA injected surge failure"}]}'
            self.send_response(500); self.send_header("Content-Type", "application/json"); self.send_header("x-request-id", rid)
            self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
            with open(LOG, "a") as f:
                f.write(json.dumps({"t": time.strftime("%H:%M:%S"), "m": "POST", "path": self.path.split("?")[0], "status": 500, "rid": rid, "injected": True}) + "\n")
            return
        c = http.client.HTTPConnection(UP_HOST, UP_PORT, timeout=120)
        c.request(self.command, self.path, body=body, headers=hdrs)
        r = c.getresponse()
        data = r.read()
        self.send_response(r.status)
        for k, v in r.getheaders():
            if k.lower() in ("transfer-encoding", "connection", "content-length"):
                continue
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
        path = self.path.split("?")[0]
        if any(s in path for s in INTERESTING):
            rec = {"t": time.strftime("%H:%M:%S"), "m": self.command, "path": path, "status": r.status,
                   "rid": self.headers.get("X-Request-Id"), "rid_echo": r.getheader("x-request-id"),
                   "req": pick(body + b"&" + (self.path.split("?", 1)[1].encode() if "?" in self.path else b""), REQ_KEYS),
                   "resp": pick(data[:4000], RESP_KEYS)}
            with open(LOG, "a") as f:
                f.write(json.dumps(rec) + "\n")

    do_GET = do_POST = do_PUT = do_DELETE = do_PATCH = _go


ThreadingHTTPServer(("0.0.0.0", LISTEN), H).serve_forever()
