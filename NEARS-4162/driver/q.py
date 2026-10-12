"""NEARS-4162 QA driver lib (Python Playwright, /usr/bin/python3). Scratch only."""
import json, os, re, subprocess, time, uuid, sys
from playwright.sync_api import sync_playwright

WT = '/Users/Apple/Projects/nears-NEARS-4162-store-panel-ajax-refusals'
EVD = WT + '/docs/qa-evidence/NEARS-4162'
LOGS = [WT + '/Admin/storage/logs/laravel-structured.log', WT + '/Admin/storage/logs/laravel.log']
PORT = int(os.environ.get('QPORT', '8162'))
BASE = 'http://127.0.0.1:%d' % PORT

SHAPES = {
    'xrw_any': {'X-Requested-With': 'XMLHttpRequest', 'Accept': '*/*'},
    'json_only': {'Accept': 'application/json'},
    'xrw_html': {'X-Requested-With': 'XMLHttpRequest', 'Accept': 'text/html,*/*;q=0.01'},
}
NAV = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


def grep_log(rid, needle=None):
    """count log lines (structured log) containing request id (and needle)"""
    out = []
    for f in LOGS[:1]:
        try:
            for line in open(f, errors='replace'):
                if rid in line and (needle is None or needle in line):
                    out.append(line.strip())
        except FileNotFoundError:
            pass
    return out


def logs_for(rid):
    time.sleep(0.3)
    lines = grep_log(rid)
    fails = [l for l in lines if 'vendor.session_refused' in l]
    return fails, lines


def sql(db, q):
    r = subprocess.run(['mysql', '-u', 'root', '-N', '-B', db, '-e', q], capture_output=True, text=True)
    return r.stdout.strip()


class Browser:
    def __enter__(self):
        self.pw = sync_playwright().start()
        self.br = self.pw.chromium.launch(headless=True)
        return self

    def __exit__(self, *a):
        self.br.close()
        self.pw.stop()

    def ctx(self, **kw):
        c = self.br.new_context(viewport={'width': 1440, 'height': 900}, **kw)
        c.set_default_timeout(20000)
        return c


def login(ctx, role, email, pw, tab=None):
    tab = tab or {'vendor': 'vendor', 'vendor_employee': 'vendor-employee', 'admin': 'admin'}[role]
    page = ctx.new_page()
    page.goto('%s/login/%s' % (BASE, tab), wait_until='domcontentloaded')
    page.wait_for_selector('#custome_recaptcha')
    page.fill('input[name=email]', email)
    page.fill('input[name=password]', pw)
    page.locator('form#form-id button[type=submit]').click()
    page.wait_for_url(lambda u: '/login/' not in u, timeout=20000)
    return page


def csrf_of(page):
    return page.evaluate("() => (document.querySelector('meta[name=csrf-token]')||document.querySelector('input[name=_token]')||{}).content || (document.querySelector('input[name=_token]')||{}).value")


def fetch(ctx, method, path, shape, data=None, csrf=None, extra=None, follow=False):
    """request-level (cookie jar of ctx). returns dict"""
    rid = str(uuid.uuid4())
    h = dict(SHAPES[shape]) if shape in SHAPES else dict(NAV)
    h['X-Request-Id'] = rid
    if csrf:
        h['X-CSRF-TOKEN'] = csrf
    if extra:
        h.update(extra)
    kw = dict(method=method, headers=h, max_redirects=(20 if follow else 0))
    if data is not None:
        kw['form'] = data
    r = ctx.request.fetch(BASE + path, **kw)
    body = r.text()
    hd = {k.lower(): v for k, v in r.headers.items()}
    try:
        j = json.loads(body)
    except Exception:
        j = None
    err = (j or {}).get('errors', [{}]) if isinstance(j, dict) else None
    e0 = err[0] if err and isinstance(err, list) and err and isinstance(err[0], dict) else {}
    fails, lines = logs_for(rid)
    return {
        'shape': shape, 'method': method, 'path': path, 'rid': rid,
        'status': r.status, 'x_panel_session': hd.get('x-panel-session'), 'location': hd.get('location'),
        'ctype': hd.get('content-type'), 'echo_rid_ok': hd.get('x-request-id') == rid,
        'code': e0.get('code'), 'message': e0.get('message'),
        'body_head': (body[:160] if j is None else None),
        'fail_lines': len(fails), 'fail_line_sample': (fails[0][:260] if fails else None),
        'all_log_lines_for_rid': len(lines),
    }


def admin_post(admin_page, path):
    """POST from the admin page (same-origin fetch with its CSRF)"""
    tok = csrf_of(admin_page)
    return admin_page.evaluate(
        """async ([p,t]) => { const r = await fetch(p,{method:'POST',headers:{'X-CSRF-TOKEN':t,'X-Requested-With':'XMLHttpRequest','Accept':'application/json'},credentials:'same-origin'}); return {status:r.status, url:r.url, redirected:r.redirected}; }""",
        [path, tok])


def save(name, obj):
    os.makedirs(EVD, exist_ok=True)
    p = '%s/%s' % (EVD, name)
    with open(p, 'w') as f:
        f.write(obj if isinstance(obj, str) else json.dumps(obj, indent=1, default=str))
    return p


def row(d):
    return '%-9s %-4s %-30s -> %s hdr=%s loc=%s code=%s msg=%r FAIL=%s echo=%s' % (
        d['shape'], d['method'], d['path'], d['status'], d['x_panel_session'], d['location'], d['code'], d['message'], d['fail_lines'], d['echo_rid_ok'])


INIT_TOASTS = """
window.__toasts = [];
window.__navs = [];
setInterval(() => { document.querySelectorAll('.toast-message').forEach(e => { const t = e.innerText; if (t && !window.__toasts.includes(t)) { window.__toasts.push(t); try { const k = JSON.parse(sessionStorage.getItem('__toasts_ss') || '[]'); k.push(t); sessionStorage.setItem('__toasts_ss', JSON.stringify(k)); } catch (e) {} } }); }, 40);
window.__loadSeen = false; setInterval(() => { const l = document.querySelector('#loading'); if (l && getComputedStyle(l).display !== 'none') window.__loadSeen = true; }, 15);
window.__pageshows = [];
window.addEventListener('pageshow', e => window.__pageshows.push({persisted: e.persisted, t: Date.now()}));
"""


def modal_state(page):
    return page.evaluate("""() => {
      const vis = e => !!e && getComputedStyle(e).display !== 'none' && e.offsetParent !== null;
      const pop = document.querySelector('.swal2-popup');
      const popVis = vis(pop);
      const conf = document.querySelector('.swal2-confirm'), canc = document.querySelector('.swal2-cancel');
      const ld = document.querySelector('#loading');
      return {url: location.href,
        popup: popVis ? pop.innerText.replace(/\\s+/g,' ').trim() : null,
        confirm_visible: vis(conf), cancel_visible: vis(canc),
        buttons_visible: [...document.querySelectorAll('.swal2-actions button')].filter(vis).length,
        confirm_focused: document.activeElement === conf,
        loading_display: ld ? getComputedStyle(ld).display : null,
        latch: !!window.nearsPanelSessionEnded, loading_seen: !!window.__loadSeen,
        toasts: window.__toasts || []};
    }""")


def wait_modal(page, timeout=20000):
    page.wait_for_function("() => { const p = document.querySelector('.swal2-popup'); return p && getComputedStyle(p).display !== 'none'; }", timeout=timeout)


def set_notification_mode(b, mode):
    """replay the whole admin order-settings form (FormData of the real form) with ONE field changed; real route POST admin/business-settings/update-order"""
    c = b.ctx(); ap = login(c, 'admin', 'admin@admin.com', '123456789')
    ap.goto(BASE + '/admin/business-settings/business-setup/order', wait_until='domcontentloaded')
    r = ap.evaluate("""async (m) => {
      const f = document.querySelector('form[action*="update-order"]');
      const fd = new FormData(f); fd.set('order_notification_type', m);
      const resp = await fetch(f.action, {method: 'POST', body: fd, credentials: 'same-origin', headers: {'X-CSRF-TOKEN': document.querySelector('meta[name=csrf-token]').content}});
      return {status: resp.status, url: resp.url, redirected: resp.redirected, fields: [...fd.keys()].length};
    }""", mode)
    return r


IMGDIR = '/private/tmp/claude-501/-Users-Apple-Projects-nears/a7f5d4bb-4211-4dfc-9952-11437c9104f3/scratchpad/n4162/'


def fill_item(op, name):
    op.evaluate("(n) => { document.querySelector('#default_name').value = n; document.querySelector('#description-default').value = 'QA4162 item'; }", name)
    op.evaluate("""() => { const s = document.querySelector('#category_id'); s.value = s.options[1].value; $(s).trigger('change'); }""")
    time.sleep(0.8)
    op.evaluate("""() => { const s = document.querySelector('#veg'); s.value = s.options[0].value; $(s).trigger('change'); document.querySelector('#available_time_starts').value='08:00'; document.querySelector('#available_time_ends').value='22:00'; document.querySelector('#unit_price').value='12.5'; }""")
    op.set_input_files('#customFileEg1', IMGDIR + 'item200.png')


def fill_ad(op, title):
    op.evaluate("(t) => { const ti=[...document.querySelectorAll('input[name=\"title[]\"]')][0]; ti.value=t; ti.dispatchEvent(new Event('input',{bubbles:true})); const d=[...document.querySelectorAll('textarea[name=\"description[]\"]')][0]; d.value='QA4162 ad desc'; d.dispatchEvent(new Event('input',{bubbles:true})); }", title)
    op.set_input_files('input[name=profile_image]', IMGDIR + 'emp400.png')
    op.set_input_files('input[name=cover_image]', IMGDIR + 'ad_banner.png')
