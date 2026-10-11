import requests, re, os, subprocess, json, struct, zlib, time, glob, uuid, html as _html

SP = '/private/tmp/claude-501/-Users-Apple-Projects-nears/a7f5d4bb-4211-4dfc-9952-11437c9104f3/scratchpad/q4148'
W = '/Users/Apple/Projects/nears-NEARS-4148-web-reg-auth/Admin'
B = SP + '/base/Admin'
EV = '/Users/Apple/Projects/nears-NEARS-4148-web-reg-auth/docs/qa-evidence/NEARS-4148'
SERV = {'fixed': ('http://127.0.0.1:8148', W), 'base': ('http://127.0.0.1:8149', B)}
DB = 'multi_food_db_qa4148'


def sql(q):
    r = subprocess.run(['mysql', '-u', 'root', '-N', '-B', DB, '-e', q], capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


class Ev:
    def __init__(self, fname, title):
        self.path = f'{EV}/{fname}'
        self.f = open(self.path, 'a')
        self.line(f'=== {title} ===')

    def line(self, s=''):
        print(s)
        self.f.write(s + '\n')
        self.f.flush()


def png():
    def chunk(t, d):
        c = struct.pack('>I', len(d)) + t + d
        return c + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    raw = b''.join(b'\x00' + b'\xff\x00\x00' * 8 for _ in range(8))
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 8, 8, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b'')


def toasts(body):
    return re.findall(r"toastr\.(error|success|info|warning)\('([^']*)'", body)


def tok(body):
    m = re.search(r'name="_token"\s+value="([^"]+)"', body) or re.search(r'name="csrf-token"\s+content="([^"]+)"', body) \
        or re.search(r'content="([^"]+)"\s+name="csrf-token"', body)
    return m.group(1) if m else None


def counts(sids=()):
    out = {
        'subscription_transactions': sql('select count(*) from subscription_transactions'),
        'store_subscriptions': sql('select count(*) from store_subscriptions'),
        'payment_requests': sql('select count(*) from payment_requests'),
    }
    for s in sids:
        out[f'store{s}'] = sql(f'select concat("package_id=",ifnull(package_id,"NULL")," model=",store_business_model) from stores where id={s}')
    return out


def delta(a, b):
    return 'ZERO-DELTA' if a == b else 'CHANGED ' + json.dumps({k: (a[k], b.get(k)) for k in a if a[k] != b.get(k)})


class Jar:
    def __init__(self, srv, name):
        self.srv = srv
        self.base, self.root = SERV[srv]
        self.name = name
        self.s = requests.Session()
        self.token = None
        self.n = 0
        self.last_rid = None

    def req(self, method, path, data=None, files=None, token=True, hdr=None, rid=None):
        rid = rid or str(uuid.uuid4())
        h = {'X-Request-Id': rid}
        if hdr:
            h.update(hdr)
        if method == 'POST' and token and self.token and data is not None:
            if isinstance(data, dict):
                data = dict(data)
                data.setdefault('_token', self.token)
            else:
                data = list(data) + [('_token', self.token)]
        r = self.s.request(method, self.base + path, data=data, files=files, headers=h, allow_redirects=False, timeout=60)
        r.rid = rid
        r.echo = r.headers.get('X-Request-Id')
        self.last_rid = rid
        return r

    def apply_page(self):
        r = self.req('GET', '/vendor/apply')
        self.token = tok(r.text)
        return r

    def sess_id_cookie(self):
        return self.s.cookies.get('laravel_session')

    def session_file(self):
        if not self.token:
            return None
        files = sorted(glob.glob(self.root + '/storage/framework/sessions/*'), key=os.path.getmtime, reverse=True)[:60]
        for f in files:
            try:
                c = open(f, errors='ignore').read()
            except Exception:
                continue
            if f'"{self.token}"' in c:
                return f
        return None

    def captcha(self):
        f = self.session_file()
        if not f:
            return None
        c = open(f, errors='ignore').read()
        m = re.search(r'six_captcha";s:\d+:"([^"]*)"', c)
        return m.group(1) if m else None

    def session_ids(self):
        f = self.session_file()
        if not f:
            return None
        c = open(f, errors='ignore').read()
        m = re.search(r'registration_store_ids";a:\d+:\{(.*?)\}', c)
        return re.findall(r'i:\d+;i:(\d+);', m.group(1)) if m else []


def logs(rid, srv='fixed', maxlen=420):
    root = SERV[srv][1]
    r = subprocess.run(['grep', '-F', rid, root + '/storage/logs/laravel.log'], capture_output=True, text=True)
    return [l[:maxlen] for l in r.stdout.splitlines()]


def summarize(r, follow=None):
    loc = r.headers.get('Location')
    return f'HTTP {r.status_code}' + (f' Location={loc}' if loc else '') + f' echo={"OK" if r.echo == r.rid else "MISMATCH"}'


REG_BASE = dict(f_name='Nears4148', l_name='Registrant', lang=['default'], latitude='24.45', longitude='54.37',
                zone_id='2', module_id='1', minimum_delivery_time='20', maximum_delivery_time='40', delivery_time_type='min',
                address=['1 Test Street'], password='Regr3ss!onPass')


def register(jar, tag, plan='subscription-base', package_id='1', module_id='1', extra=None, captcha=None, password=None, refresh=True):
    """real POST /vendor/apply; returns response and the (email, password)"""
    suffix = f'{tag}{int(time.time())}'[-14:]
    email = f'qa4148.{suffix}@example.test'
    phone = '+1555' + str(int(time.time() * 1000))[-8:]
    d = dict(REG_BASE)
    d.update(name=[f'QA4148 {suffix}'], email=email, phone=phone, module_id=module_id, business_plan=plan)
    if package_id is not None:
        d['package_id'] = package_id
    if password:
        d['password'] = password
    if extra:
        d.update(extra)
    d['custome_recaptcha'] = captcha if captcha is not None else jar.captcha()
    # requests needs list-of-tuples for arrays
    items = []
    for k, v in d.items():
        if isinstance(v, list):
            for x in v:
                items.append((f'{k}[]', x))
        else:
            items.append((k, v))
    files = {'logo': ('logo.png', png(), 'image/png')}
    jar.pre_cookie, jar.pre_token = jar.sess_id_cookie(), jar.token
    r = jar.req('POST', '/vendor/apply', data=items, files=files)
    jar.post_cookie = jar.sess_id_cookie()
    jar.post_set_cookie = [h for h in r.raw.headers.getlist('Set-Cookie')] if hasattr(r.raw.headers, 'getlist') else []
    if refresh:
        jar.apply_page()
    return r, email, d['password']
