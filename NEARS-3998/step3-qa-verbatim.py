#!/usr/bin/env python3
"""QA-own verbatim-move check. member-by-member, comments stripped (strings kept), whitespace collapsed,
ONLY the substitutions in SUBS applied to the base text. usage: qa_verbatim.py base.dart ownerfile.dart [mutated-owner]"""
import re, sys

def strip_comments(src):
    out = []; i = 0; n = len(src)
    while i < n:
        c = src[i]
        if src.startswith('//', i):
            j = src.find('\n', i); i = n if j < 0 else j; continue
        if src.startswith('/*', i):
            j = src.find('*/', i + 2); i = n if j < 0 else j + 2; continue
        if c == 'r' and i + 1 < n and src[i+1] in '\'"' and (i == 0 or not (src[i-1].isalnum() or src[i-1] == '_')):
            q = src[i+1]; k = i + 2; raw = True; s0 = i
        elif c in '\'"':
            q = c; k = i + 1; raw = False; s0 = i
        else:
            out.append(c); i += 1; continue
        tri = src.startswith(q * 3, k - 1) if not raw else src.startswith(q * 3, k - 1)
        if tri: k += 2
        while k < n:
            ch = src[k]
            if not raw and ch == '\\': k += 2; continue
            if tri:
                if src.startswith(q * 3, k): k += 3; break
            elif ch == q: k += 1; break
            if not raw and ch == '$' and src[k+1:k+2] == '{':
                d = 1; k += 2
                while k < n and d:
                    if src[k] == '{': d += 1
                    elif src[k] == '}': d -= 1
                    k += 1
                continue
            k += 1
        out.append(src[s0:k]); i = k
    return ''.join(out)

def class_body(src, cls):
    m = re.search(r'\bclass\s+' + cls + r'\b[^{]*\{', src)
    start = m.end(); d = 1; i = start
    # strings were kept, so brace counting must skip strings
    while d:
        c = src[i]
        if c in '\'"':
            q = c; tri = src.startswith(q * 3, i)
            i += 3 if tri else 1
            while True:
                if src[i] == '\\': i += 2; continue
                if tri and src.startswith(q * 3, i): i += 3; break
                if (not tri) and src[i] == q: i += 1; break
                if src[i] == '$' and src[i+1] == '{':
                    dd = 1; i += 2
                    while dd:
                        if src[i] == '{': dd += 1
                        elif src[i] == '}': dd -= 1
                        i += 1
                    continue
                i += 1
            continue
        if c == '{': d += 1
        elif c == '}': d -= 1
        i += 1
    return src[start:i-1]

def members(body):
    res = []; i = 0; n = len(body); start = 0
    def skip_str(i):
        q = body[i]; tri = body.startswith(q * 3, i); i += 3 if tri else 1
        while True:
            if body[i] == '\\': i += 2; continue
            if tri and body.startswith(q * 3, i): return i + 3
            if (not tri) and body[i] == q: return i + 1
            if body[i] == '$' and body[i+1] == '{':
                dd = 1; i += 2
                while dd:
                    if body[i] == '{': dd += 1
                    elif body[i] == '}': dd -= 1
                    i += 1
                continue
            i += 1
    while i < n:
        c = body[i]
        if c in '\'"': i = skip_str(i); continue
        if c.isspace() and i == start: i += 1; start = i; continue
        # scan one member
        par = 0; mode = None; j = i
        while j < n:
            c = body[j]
            if c in '\'"': j = skip_str(j); continue
            if c in '([': par += 1
            elif c in ')]': par -= 1
            elif par == 0:
                if c == ';': j += 1; break
                if body.startswith('=>', j) or (c == '=' and body[j-1] not in '=!<>' and body[j+1] != '='):
                    # to semicolon at depth 0
                    p = 0; j += 1
                    while True:
                        ch = body[j]
                        if ch in '\'"': j = skip_str(j); continue
                        if ch in '([{': p += 1
                        elif ch in ')]}': p -= 1
                        elif ch == ';' and p == 0: j += 1; break
                        j += 1
                    break
                if c == '{':
                    d = 1; j += 1
                    while d:
                        ch = body[j]
                        if ch in '\'"': j = skip_str(j); continue
                        if ch == '{': d += 1
                        elif ch == '}': d -= 1
                        j += 1
                    break
            j += 1
        text = body[start:j]
        res.append(text.strip()); i = j; start = j
    return [r for r in res if r]

def name_of(text):
    t = re.sub(r'@\w+(\([^)]*\))?', '', text).strip()
    head = re.split(r'\(|=>|=|\{|;', t, 1)[0]
    head = re.sub(r'<[^<>]*>', '', head)
    toks = head.split()
    return toks[-1] if toks else ''

def norm(t):
    t = re.sub(r'@visibleForTesting', '', t)
    return re.sub(r'\s+', ' ', t).strip()

# allowed substitutions, applied to BASE text (documented class in comment)
SUBS = [
    # (1) renames
    (r'\b_checkPermission\(String page, \{bool alreadyOnPickMap = false\}\)', 'run(String page, {bool alreadyOnPickMap = false})'),
    (r'\b_shouldShowLocationRationale\b', 'shouldShowLocationRationale'),
    # (2) seams
    (r'await readLocationPermission\(\)', 'await readPermission()'),
    (r'await resolvePermissionAndLocate\(page, alreadyOnPickMap: alreadyOnPickMap\)', 'await resolveChain(page, alreadyOnPickMap: alreadyOnPickMap)'),
    (r'await resolveLocationAfterPermission\(', 'await resolveTail('),
    (r'\b_logEvent\(', 'logEvent('),
    (r"'source': _permissionPromptSource", "'source': promptSource()"),
    # (3) lazy Get.find
    (r'Get\.find<LocationController>\(\)\.getCurrentLocation\(false\)', 'currentLocation()'),
    (r'_onPickAddressButtonPressed\(\s*Get\.find<LocationController>\(\),\s*page,\s*resolvedAddress: value,?\s*\)', 'onResolvedAddress(page, value)'),
    # checkPermission: facade call -> same-name interface member (kept)
]
MOVED = ['checkPermission', '_rationaleGateReadTimeout', 'readLocationPermission', '_shouldShowLocationRationale',
         '_checkPermissionTimeout', '_checkPermissionEpoch', '_isCurrentCheckPermission', '_checkPermission',
         '_handleResolutionTimeout', '_logPermissionResult', '_recordPermissionPromptResult',
         '_navigateToPickMapFallback', 'resolvePermissionAndLocate', 'resolveLocationAfterPermission', '_locationCheck']
OWNER_NAME = {'_checkPermission': 'run', '_shouldShowLocationRationale': 'shouldShowLocationRationale'}

def load(path, cls):
    s = strip_comments(open(path).read())
    ms = members(class_body(s, cls))
    d = {}
    for m in ms:
        d.setdefault(name_of(m), []).append(m)
    return d

if __name__ == '__main__':
    base = load(sys.argv[1], 'LocationController')
    owner = load(sys.argv[2], 'LocationPermissionFlow')
    bad = 0
    for nm in MOVED:
        bt = base.get(nm)
        if not bt:
            print('MISSING in base', nm); bad += 1; continue
        # checkPermission in base may have 2 entries? choose all and test any match
        on = OWNER_NAME.get(nm, nm.lstrip('_') if False else nm)
        ot = owner.get(on)
        if not ot:
            print('MISSING in owner', on); bad += 1; continue
        b = norm(bt[0])
        for pat, rep in SUBS:
            b = re.sub(pat, rep, b)
        b = norm(b)
        o = norm(ot[0])
        if b == o:
            print('IDENTICAL after allowed subs:', nm, '->', on)
        else:
            bad += 1
            print('DIFF:', nm)
            import difflib
            for l in difflib.unified_diff(re.split(r'(?<=[;{}]) ', b), re.split(r'(?<=[;{}]) ', o), lineterm='', n=0):
                print('   ', l)
    print('RESULT', 'ALL IDENTICAL' if not bad else f'{bad} DIFFER')
    sys.exit(1 if bad else 0)
