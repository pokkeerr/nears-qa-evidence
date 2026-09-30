#!/usr/bin/env python3
# NEARS-3945 QA instrument: pass-through proxy LISTEN -> UP that logs method, path (+ query for
# cashback only), X-Request-Id, status and a whitelist of money/non-PII fields only.
import http.client, json, os, re, sys, time
FAILFLAG = '/private/tmp/claude-501/-Users-Apple-Projects-nears/19315c20-7616-4951-9fdf-d3ff66f7c689/scratchpad/fail_store2_quote'
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LISTEN, UP_PORT, LOG = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
REQ_KEYS = ["payment_method", "order_amount", "order_type", "store_id", "module_id"]
RESP_KEYS = ["tax_amount", "tax_included", "total_ammount", "total_amount", "order_id", "order_ids", "group_id",
             "calculated_amount", "cashback_amount", "cashback_type", "min_purchase", "max_discount", "message"]
INTERESTING = ("place", "get-Tax", "getCashback", "delivery-quote", "order/group")


def pick(raw, keys):
    out, text = {}, raw.decode("utf-8", "replace")
    for k in keys:
        m = (re.search(r'"%s"\s*:\s*("([^"]*)"|[-0-9.eE]+|null|true|false|\[[^\]]*\])' % re.escape(k), text)
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
        path0 = self.path.split("?")[0]
        if path0.endswith("/config/delivery-quote") and os.path.exists(FAILFLAG):
            m = re.search(rb'"order_amount"\s*:\s*([0-9.]+)', body)
            amt = float(m.group(1)) if m else -1
            if 0 <= amt < 10:
                data = b'{"errors":[{"code":"qa","message":"QA3945 forced failure"}]}'
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                with open(LOG, "a") as f:
                    f.write(json.dumps({"t": time.strftime("%H:%M:%S"), "m": self.command, "path": path0, "status": 500,
                                        "rid": self.headers.get("X-Request-Id"), "req": {"order_amount": amt}, "forced": True}) + "\n")
                return
        hdrs = {k: v for k, v in self.headers.items() if k.lower() not in ("host", "connection", "accept-encoding")}
        c = http.client.HTTPConnection("127.0.0.1", UP_PORT, timeout=120)
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
            q = self.path.split("?", 1)[1] if "?" in self.path else ""
            rec = {"t": time.strftime("%H:%M:%S"), "m": self.command,
                   "path": path + ("?" + q if "getCashback" in path else ""), "status": r.status,
                   "rid": self.headers.get("X-Request-Id"),
                   "req": pick(body, REQ_KEYS), "resp": pick(data[:6000], RESP_KEYS)}
            with open(LOG, "a") as f:
                f.write(json.dumps(rec) + "\n")

    do_GET = do_POST = do_PUT = do_DELETE = do_PATCH = _go


ThreadingHTTPServer(("0.0.0.0", LISTEN), H).serve_forever()
