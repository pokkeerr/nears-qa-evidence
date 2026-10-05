#!/usr/bin/env python3
"""NEARS-3996 s5 QA recording proxy: listen :8250 -> backend :8251 (own php -S from the tested worktree).
One JSON line per request (ts, m, path incl. query, status, ms, zone header). GET /__mark?name=X writes a marker line.
Mode file `proxy_mode` (re-read per request): ok | down (every request answers 502 without reaching the backend)
| failpath:<substr> (a request whose path contains <substr> answers 500 without reaching the backend)
| delay:<substr>:<secs> (a request whose path contains <substr> is held <secs> before forwarding)."""
import http.server, http.client, json, time, os, threading, socketserver
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, 'proxy_access.jsonl'); MODE = os.path.join(HERE, 'proxy_mode')
BACK = ('127.0.0.1', 8251)
lock = threading.Lock()
def log(d):
    with lock:
        with open(LOG, 'a') as f: f.write(json.dumps(d) + '\n')
HOP = {'connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization', 'te', 'trailers', 'transfer-encoding', 'upgrade', 'content-length'}  # Host is preserved on purpose: *_full_url fields echo the request host, so images resolve through this proxy
class H(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def log_message(self, *a): pass
    def _reply(self, status, body, ctype='application/json'):
        self.send_response(status); self.send_header('Content-Type', ctype); self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)
    def _do(self):
        t0 = time.time()
        if self.path.startswith('/__mark'):
            log({'ts': round(t0, 3), 'marker': self.path.split('name=', 1)[-1]}); self._reply(200, b'ok', 'text/plain'); return
        n = int(self.headers.get('Content-Length') or 0); body = self.rfile.read(n) if n else None
        mode = (open(MODE).read().strip() if os.path.exists(MODE) else 'ok')
        zone = self.headers.get('zoneId', '')
        if mode == 'down':
            self._reply(502, b'{"errors":[{"code":"qa","message":"injected down"}]}')
            log({'ts': round(t0, 3), 'm': self.command, 'path': self.path, 'status': 502, 'injected': True, 'zone': zone}); return
        if mode.startswith('failpath:') and mode.split(':', 1)[1] in self.path and not self.path.startswith('/storage'):
            self._reply(500, b'{"errors":[{"code":"qa","message":"injected"}]}')
            log({'ts': round(t0, 3), 'm': self.command, 'path': self.path, 'status': 500, 'injected': True, 'zone': zone}); return
        if mode.startswith('delay:'):
            _, sub, secs = mode.split(':', 2)
            if sub in self.path: time.sleep(float(secs))
        try:
            c = http.client.HTTPConnection(*BACK, timeout=120)
            hdr = {k: v for k, v in self.headers.items() if k.lower() not in HOP}
            c.request(self.command, self.path, body=body, headers=hdr)
            r = c.getresponse(); data = r.read()
            self.send_response(r.status)
            for k, v in r.getheaders():
                if k.lower() not in HOP: self.send_header(k, v)
            self.send_header('Content-Length', str(len(data))); self.end_headers(); self.wfile.write(data)
            log({'ts': round(t0, 3), 'm': self.command, 'path': self.path, 'status': r.status, 'ms': int((time.time() - t0) * 1000), 'zone': zone})
        except Exception as e:
            self._reply(502, b'proxy error', 'text/plain')
            log({'ts': round(t0, 3), 'm': self.command, 'path': self.path, 'status': 502, 'err': type(e).__name__, 'zone': zone})
    do_GET = do_POST = do_PUT = do_DELETE = do_PATCH = do_HEAD = do_OPTIONS = _do
class S(socketserver.ThreadingMixIn, http.server.HTTPServer): daemon_threads = True; allow_reuse_address = True
if __name__ == '__main__':
    S(('0.0.0.0', 8250), H).serve_forever()
