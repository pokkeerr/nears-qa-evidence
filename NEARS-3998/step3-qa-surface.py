#!/usr/bin/env python3
"""QA-own facade-surface lister: public (non _) depth-1 member heads of class LocationController,
including annotations; comments and string contents blanked; normalised by dropping body markers + async."""
import re, sys

def blank(src):
    out = []
    i, n = 0, len(src)
    def skip_string(i, quote, raw, triple):
        # returns index after closing quote; handles ${...} nesting (non-raw)
        while i < n:
            c = src[i]
            if not raw and c == '\\':
                i += 2; continue
            if triple:
                if src.startswith(quote * 3, i):
                    return i + 3
            else:
                if c == quote:
                    return i + 1
                if c == '\n':
                    return i + 1
            if not raw and c == '$' and i + 1 < n and src[i+1] == '{':
                depth = 1; i += 2
                while i < n and depth:
                    if src[i] == '{': depth += 1
                    elif src[i] == '}': depth -= 1
                    elif src[i] in '\'"':
                        q = src[i]
                        tri = src.startswith(q*3, i)
                        i = skip_string(i + (3 if tri else 1), q, False, tri) - 1
                    i += 1
                continue
            i += 1
        return i
    while i < n:
        c = src[i]
        if src.startswith('//', i):
            j = src.find('\n', i)
            j = n if j < 0 else j
            i = j; continue
        if src.startswith('/*', i):
            depth = 1; j = i + 2
            while j < n and depth:
                if src.startswith('/*', j): depth += 1; j += 2
                elif src.startswith('*/', j): depth -= 1; j += 2
                else: j += 1
            out.append('\n' * src.count('\n', i, j)); i = j; continue
        raw = False
        if c == 'r' and i + 1 < n and src[i+1] in '\'"' and (i == 0 or not (src[i-1].isalnum() or src[i-1] == '_')):
            raw = True
            q = src[i+1]; k = i + 1
        elif c in '\'"':
            q = c; k = i
        else:
            out.append(c); i += 1; continue
        tri = src.startswith(q * 3, k)
        j = skip_string(k + (3 if tri else 1), q, raw, tri)
        out.append(q + q); out.append('\n' * src.count('\n', i, j)); i = j
    return ''.join(out)

def surface(path):
    src = blank(open(path).read())
    m = re.search(r'\bclass\s+LocationController\b[^{]*\{', src)
    start = m.end()
    # find matching close
    depth = 1; i = start
    while depth:
        ch = src[i]
        if ch == '{': depth += 1
        elif ch == '}': depth -= 1
        i += 1
    body = src[start:i-1]
    heads = []
    buf = []
    j = 0; n = len(body)
    par = 0
    def skip_braces(j):
        d = 1; j += 1
        while d:
            if body[j] == '{': d += 1
            elif body[j] == '}': d -= 1
            j += 1
        return j
    def skip_to_semi(j):
        p = 0
        while True:
            ch = body[j]
            if ch in '([{': p += 1
            elif ch in ')]}': p -= 1
            elif ch == ';' and p == 0:
                return j + 1
            j += 1
    while j < n:
        ch = body[j]
        if ch in '([': par += 1
        elif ch in ')]': par -= 1
        if par == 0:
            if ch == '{':
                heads.append(''.join(buf)); buf = []
                j = skip_braces(j); continue
            if ch == ';':
                heads.append(''.join(buf)); buf = []; j += 1; continue
            if ch == '=' and body[j:j+2] == '=>':
                heads.append(''.join(buf)); buf = []
                j = skip_to_semi(j + 2); continue
            if ch == '=' and body[j-1] not in '=!<>' and body[j+1] != '=':
                heads.append(''.join(buf)); buf = []
                j = skip_to_semi(j + 1); continue
        buf.append(ch); j += 1
    out = []
    for h in heads:
        h = re.sub(r'\s+', ' ', h).strip()
        if not h: continue
        h = re.sub(r'\basync\*?\b', '', h)
        h = re.sub(r'\s+', ' ', h).strip()
        # name = identifier before '(' or last identifier
        mm = re.search(r'([A-Za-z_$][\w$]*)\s*(?:\(|$)', h.split('@visibleForTesting')[-1])
        # public when its name (the identifier before first '(' or the last token) does not start with _
        core = re.sub(r'@\w+(\([^)]*\))?', '', h).strip()
        nm = re.search(r'([A-Za-z_$][\w$]*)\s*(?:<[^>(]*>)?\s*\(', core)
        name = nm.group(1) if nm else core.split()[-1]
        if name.startswith('_'):
            continue
        out.append(h)
    return out

if __name__ == '__main__':
    for h in surface(sys.argv[1]):
        print(h)
