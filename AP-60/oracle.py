#!/usr/bin/env python3
"""
INDEPENDENT ORACLE for AP-60.

Re-derives chars_per_token, the bucket char shares, the signature/attachment shares and each
session's system block STRAIGHT FROM THE RAW FROZEN .jsonl BYTES.

It calls NOTHING from the code under test: no Laravel, no artisan, no ContextSnapshotService,
no ContextAttributor, no TokenEstimator, and it never reads manifest.json for anything it
computes (the manifest is only loaded at the very end, for the ground-truth comparison, and
that is stated explicitly).

Every rule below is re-implemented from the DESIGN, not copied from the PHP.
"""
import base64
import glob
import json
import math
import os
import struct
import sys

FROZEN = sys.argv[1] if len(sys.argv) > 1 else \
    '/Users/Apple/Projects/nears-monitor-AP-60-frozen-corpus/tests/fixtures/context/frozen'

# Pinned by the corpus's own manifest in the shipped command. Hard-coded here so the oracle does
# not depend on a file the pipeline also reads.
CHARS_PER_TOKEN = 2.57
PIXELS_PER_TOKEN = 750
IMAGE_BYTES_PER_TOKEN = 145.0
BUCKETS = ['messages', 'thinking', 'tool_calls', 'tool_results', 'attachments']


def nchars(s):
    """Codepoints, like PHP mb_strlen(.., 'UTF-8')."""
    return len(s or '')


def php_json_len(v):
    """chars of PHP json_encode($v, JSON_UNESCAPED_SLASHES): compact separators, \\uXXXX escapes,
    slashes NOT escaped."""
    s = json.dumps(v, separators=(',', ':'), ensure_ascii=True)
    return len(s.replace('\\/', '/'))


def string_leaf_chars(v):
    """Every string leaf, skipping any key literally named 'type'."""
    if isinstance(v, str):
        return nchars(v)
    if isinstance(v, list):
        return sum(string_leaf_chars(c) for c in v)
    if isinstance(v, dict):
        return sum(string_leaf_chars(c) for k, c in v.items() if k != 'type')
    return 0


def image_dims(b64):
    if not b64:
        return None
    try:
        raw = base64.b64decode(b64[:87384] + '===', validate=False)
    except Exception:
        return None
    if len(raw) < 24:
        return None
    if raw.startswith(b'\x89PNG\r\n\x1a\n'):
        w, h = struct.unpack('>II', raw[16:24])
        return (w, h)
    if raw.startswith(b'\xff\xd8'):
        sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
        i = 2
        while i + 9 < len(raw):
            if raw[i] != 0xFF:
                i += 1
                continue
            m = raw[i + 1]
            if m in sof:
                h, w = struct.unpack('>HH', raw[i + 5:i + 9])
                return (w, h)
            if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7:
                i += 2
                continue
            seg = struct.unpack('>H', raw[i + 2:i + 4])[0]
            if seg < 2:
                return None
            i += 2 + seg
    return None


def image_weight(source):
    data = (source or {}).get('data', '') if isinstance(source, dict) else ''
    d = image_dims(data)
    if d is None:
        tokens = (nchars(data) * 0.75) / IMAGE_BYTES_PER_TOKEN
        return tokens * CHARS_PER_TOKEN
    return ((d[0] * d[1]) / PIXELS_PER_TOKEN) * CHARS_PER_TOKEN


def tool_result_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        out = []
        for b in content:
            if isinstance(b, str):
                out.append(b)
            elif isinstance(b, dict) and b.get('type') == 'text':
                out.append(str(b.get('text') or ''))
        return '\n'.join(out)
    return ''


def total_of(u):
    return int(u.get('input_tokens') or 0) + int(u.get('cache_creation_input_tokens') or 0) \
        + int(u.get('cache_read_input_tokens') or 0)


def effective_usage(msg):
    u = msg.get('usage')
    if not isinstance(u, dict):
        return None
    if total_of(u) > 0:
        return u
    it = u.get('iterations')
    if isinstance(it, list) and it:
        last = it[-1]
        if isinstance(last, dict) and total_of(last) > 0:
            return last
    return None


def block_identity(b):
    t = b.get('type')
    key = {'tool_use': b.get('id'),
           'thinking': b.get('signature') or b.get('thinking'),
           'redacted_thinking': b.get('data'),
           'text': b.get('text')}.get(t)
    return f'{t}:{hash_key(key)}' if isinstance(key, str) and key != '' else None


def hash_key(k):
    import hashlib
    return hashlib.sha1(k.encode('utf-8', 'replace')).hexdigest()


def walk(records, terminal):
    """Chain from terminal back to root, STOPPING AT (excluding) a compact boundary."""
    chain, cur = {}, terminal
    while cur is not None and cur in records and cur not in chain:
        r = records[cur]
        if r['boundary']:
            break
        chain[cur] = True
        cur = r['parent']
    return chain


def parse(path):
    units, index, tool_names, records, emitted = [], {}, {}, {}, set()
    open_unit = None

    for ln in open(path, encoding='utf-8'):
        ln = ln.strip()
        if not ln:
            continue
        o = json.loads(ln)
        if o.get('isSidechain') is True:
            continue
        t = o.get('type')
        msg = o.get('message') if isinstance(o.get('message'), dict) else {}
        uuid = o.get('uuid') if isinstance(o.get('uuid'), str) else None
        boundary = (t == 'system' and o.get('subtype') == 'compact_boundary')

        if uuid is not None:
            p = o.get('parentUuid')
            records[uuid] = {'parent': p if isinstance(p, str) else None, 'boundary': boundary}

        if t == 'assistant':
            mid = msg.get('id')
            if mid is None:
                continue
            fresh = mid not in index
            if fresh:
                index[mid] = len(units)
                units.append({'kind': 'assistant', 'items': [], 'usage': None, 'model': None,
                              'out': -1, 'seen': {}, 'uuids': []})
            u = units[index[mid]]
            if uuid is not None and (fresh or open_unit == index[mid]):
                u['uuids'].append(uuid)
            open_unit = index[mid]

            for b in (msg.get('content') or []):
                if not isinstance(b, dict):
                    continue
                bt = b.get('type')
                if bt == 'tool_use' and b.get('id'):
                    tool_names[b['id']] = str(b.get('name') or '?')
                item = assistant_item(b)
                if item is None:
                    continue
                ident = block_identity(b)
                if ident is not None:
                    if ident in u['seen']:
                        if uuid is not None:
                            u['items'][u['seen'][ident]]['recs'].append(uuid)
                        continue
                    u['seen'][ident] = len(u['items'])
                u['items'].append(item | {'recs': [uuid] if uuid else []})

            out = int((msg.get('usage') or {}).get('output_tokens') or 0)
            if out >= u['out']:
                eu = effective_usage(msg)
                u['usage'] = eu
                u['model'] = msg.get('model')
                u['out'] = out
            continue

        # user/attachment REPLAY dedup, keyed on uuid
        if uuid is not None and uuid in emitted:
            open_unit = None
            continue
        if uuid is not None and t in ('user', 'attachment'):
            emitted.add(uuid)

        recs = [uuid] if uuid else []
        if t == 'user':
            open_unit = None
            units.append({'kind': 'user', 'items': [i | {'recs': recs} for i in user_items(msg.get('content'), tool_names)]})
        elif t == 'attachment':
            open_unit = None
            a = o.get('attachment') if isinstance(o.get('attachment'), dict) else {}
            units.append({'kind': 'attachment', 'items': [
                {'bucket': 'attachments', 'w': float(string_leaf_chars(a)), 'sig': 0.0, 'recs': recs}]})
        elif boundary:
            open_unit = None
            units.append({'kind': 'compact', 'items': []})
        else:
            open_unit = None

    return flatten(units)


def assistant_item(b):
    t = b.get('type')
    if t in ('thinking', 'redacted_thinking'):
        if t == 'redacted_thinking':
            return {'bucket': 'thinking', 'w': float(nchars(str(b.get('data') or ''))), 'sig': 0.0}
        sig = float(nchars(str(b.get('signature') or '')))
        return {'bucket': 'thinking',
                'w': float(nchars(str(b.get('thinking') or ''))) + sig, 'sig': sig}
    if t == 'text':
        if str(b.get('text') or '').strip() == '':
            return None
        return {'bucket': 'messages', 'w': float(nchars(str(b.get('text') or ''))), 'sig': 0.0}
    if t == 'tool_use':
        w = php_json_len(b.get('input', [])) + nchars(str(b.get('name') or ''))
        return {'bucket': 'tool_calls', 'w': float(w), 'sig': 0.0}
    return None


def user_items(content, tool_names):
    if isinstance(content, str):
        if content.strip() == '':
            return []
        return [{'bucket': 'messages', 'w': float(nchars(content)), 'sig': 0.0}]
    if not isinstance(content, list):
        return []
    out = []
    for b in content:
        if not isinstance(b, dict):
            continue
        t = b.get('type')
        if t == 'tool_result':
            out.append({'bucket': 'tool_results',
                        'w': float(nchars(tool_result_text(b.get('content')))), 'sig': 0.0})
        elif t == 'text':
            if str(b.get('text') or '').strip() == '':
                continue
            out.append({'bucket': 'messages', 'w': float(nchars(str(b.get('text') or ''))), 'sig': 0.0})
        elif t == 'image':
            out.append({'bucket': 'attachments', 'w': image_weight(b.get('source')), 'sig': 0.0})
    return out


def flatten(units):
    items, compact_ordinal = [], None
    for u in units:
        if u['kind'] == 'compact':
            compact_ordinal = len(items)
            continue
        for it in u['items']:
            items.append(it | {'ordinal': len(items)})

    header = next((u for u in reversed(units)
                   if u['kind'] == 'assistant' and u['model'] != '<synthetic>' and u['usage']), None)
    turn1 = next((u for u in units
                  if u['kind'] == 'assistant' and u['model'] != '<synthetic>' and u['usage']), None)
    return {
        'items': items,
        'total': total_of(header['usage']) if header else None,
        'turn1_total': total_of(turn1['usage']) if turn1 else None,
        'header_record': header['uuids'][-1] if header and header['uuids'] else None,
        'turn1_record': turn1['uuids'][0] if turn1 and turn1['uuids'] else None,
        'compact_ordinal': compact_ordinal,
    }


def php_round(x):
    return int(math.floor(x + 0.5)) if x >= 0 else -int(math.floor(-x + 0.5))


def facts(path, records_map=None):
    p = parse(path)
    # rebuild the record graph (parse() built it locally; redo for the chain walk)
    records = {}
    for ln in open(path, encoding='utf-8'):
        ln = ln.strip()
        if not ln:
            continue
        o = json.loads(ln)
        if o.get('isSidechain') is True:
            continue
        uuid = o.get('uuid') if isinstance(o.get('uuid'), str) else None
        if uuid is None:
            continue
        pu = o.get('parentUuid')
        records[uuid] = {'parent': pu if isinstance(pu, str) else None,
                         'boundary': o.get('type') == 'system' and o.get('subtype') == 'compact_boundary'}

    live = walk(records, p['header_record'])
    t1r = p['turn1_record']
    turn1_chain = walk(records, records[t1r]['parent']) if t1r and t1r in records else {}

    live_w = t1_live = t1_dead = 0.0
    for it in p['items']:
        is_live = any(r in live for r in it['recs'])
        it['live'] = is_live
        if is_live:
            live_w += it['w']
        on_t1 = any(r in turn1_chain for r in it['recs'])
        if on_t1 and is_live:
            t1_live += it['w']
        elif on_t1:
            t1_dead += it['w']

    total, turn1_total = p['total'], p['turn1_total']
    if total is None:
        state, system, content = 'no_header', None, None
    elif turn1_total is None:
        state, system, content = 'no_turn1', None, None
    elif live_w <= 0:
        state, system, content = 'no_live_weight', None, None
    else:
        a = t1_live / live_w
        if a >= 1.0:
            state, system, content = 'implausible_system', None, None
        else:
            dead = t1_dead / CHARS_PER_TOKEN
            system = php_round((turn1_total - total * a - dead) / (1 - a))
            content = total - system
            if system <= 0 or content < 0:
                state, system, content = 'implausible_system', None, None
            else:
                state = 'attributed'

    live_chars = sum(it['w'] for it in p['items'] if it['live'])
    by_bucket = {b: sum(it['w'] for it in p['items'] if it['live'] and it['bucket'] == b) for b in BUCKETS}
    sig_chars = sum(it['sig'] for it in p['items'] if it['live'])

    return {'stem': os.path.basename(path).replace('.jsonl', ''), 'state': state,
            'system': system, 'content': content, 'total': total, 'turn1_total': turn1_total,
            'live_chars': live_chars, 'by_bucket': by_bucket, 'sig_chars': sig_chars,
            'live_items': sum(1 for it in p['items'] if it['live'])}


def slope(rows, k):
    n = len(rows)
    xs = [r['live_chars'] for r in rows]
    ys = [r['content'] - r['live_chars'] / k for r in rows]
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / sxx if sxx > 0 else 0.0


rows = [facts(p) for p in sorted(glob.glob(os.path.join(FROZEN, '*.jsonl')))]
use = [r for r in rows if r['state'] == 'attributed' and r['content'] > 5000 and r['live_chars'] > 0]

L = sum(r['live_chars'] for r in use)
C = sum(r['content'] for r in use)
k = L / max(1, C)
buckets = {b: sum(r['by_bucket'][b] for r in use) for b in BUCKETS}
tot = sum(buckets.values())
sig = sum(r['sig_chars'] for r in use)

print('=== INDEPENDENT ORACLE (python, raw jsonl bytes) ===')
print(f'sessions_total   {len(rows)}')
print(f'sessions_fitted  {len(use)}')
print(f'sum live_chars   {L:,.1f}')
print(f'sum content tok  {C:,}')
print(f'chars_per_token  {k:.4f}   (rounded {round(k,4)})')
print(f'residual slope   {slope(use,k):+.6f}')
print()
print('bucket char share (of live mass of fitted sessions)')
for b in BUCKETS:
    print(f'  {b:<14} {buckets[b]/tot*100:6.3f}%   ({buckets[b]:,.0f} chars)')
print()
print(f'SIGNATURE share   {sig/tot*100:.3f}%   of live char mass  ({sig:,.0f} chars)')
print(f'ATTACHMENT share  {buckets["attachments"]/tot*100:.3f}%')
thr = (1 - 2.0 / k) * 100
print(f'band-exit threshold: removing >{thr:.3f}% of char mass drops k below 2.0')
print(f'  signature  {sig/tot*100:.2f}% > {thr:.2f}% ? {"YES -> --no-signature MUST exit the band" if sig/tot*100 > thr else "NO  -> mutation passes by luck"}')
print(f'  attachment {buckets["attachments"]/tot*100:.2f}% < {thr:.2f}% ? {"YES -> --no-attachments stays IN band, fails bucket only" if buckets["attachments"]/tot*100 < thr else "NO"}')
print(f'  predicted k with signature dropped: {(L-sig)/C:.4f}')
print()
print('per-session state + SYSTEM BLOCK the shipped attributor rule recovers:')
for r in rows:
    print(f'  {r["stem"]:<26} {r["state"]:<20} S={str(r["system"]):>7}  content={str(r["content"]):>7}  live_chars={r["live_chars"]:>10,.0f}  live_items={r["live_items"]:>3}')

# ---- ground truth: compare recovered S to the AUTHORED S ----
man = json.load(open(os.path.join(FROZEN, 'manifest.json')))
print()
print('=== GROUND TRUTH: authored S (from generator manifest) vs S recovered by MY oracle ===')
bym = {s['stem']: s for s in man['sessions']}
worst = 0
for r in rows:
    m = bym.get(r['stem'])
    if not m or r['system'] is None:
        print(f'  {r["stem"]:<26} authored={m.get("authored_system") if m else "?"}  recovered=None  ({r["state"]})')
        continue
    d = r['system'] - m['authored_system']
    worst = max(worst, abs(d))
    print(f'  {r["stem"]:<26} authored={m["authored_system"]:>7}  recovered={r["system"]:>7}  delta={d:+d}')
print(f'  WORST |delta| = {worst} token(s)')
