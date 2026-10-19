import json, sys
# usage: tok_between.py <transcript> <start-marker> <end-marker> [extend=1]
# De-duplicated (by message.id, max output record) usage of assistant messages from the one
# carrying <start-marker> through the one carrying <end-marker>, plus [extend] following
# assistant message(s) (the one that ingests the END call's tool result).
path, a, b = sys.argv[1], sys.argv[2], sys.argv[3]
extend = int(sys.argv[4]) if len(sys.argv) > 4 else 1
recs = []
for line in open(path):
    if line.strip():
        try: recs.append((line, json.loads(line)))
        except Exception: pass
A = [(i, r) for i, (l, r) in enumerate(recs) if r.get('type') == 'assistant']
ia = next(i for i, r in A if a in recs[i][0])
ib = next(i for i, r in A if b in recs[i][0] and i >= ia)
order = []
for i, r in A:
    k = r['message'].get('id')
    if i >= ia and k not in order: order.append(k)
endpos = order.index(recs[ib][1]['message'].get('id'))
sys.stderr.write(f"ia={ia} ib={ib} endpos={endpos} norder={len(order)}\n")
keep = set(order[:endpos + 1 + extend])
best = {}
for i, r in A:
    k = r['message'].get('id'); u = r['message'].get('usage')
    if k in keep and u and (k not in best or (u.get('output_tokens') or 0) >= (best[k].get('output_tokens') or 0)): best[k] = u
F = ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens')
t = {f: sum((u.get(f) or 0) for u in best.values()) for f in F}
t['messages'] = len(best); t['total'] = sum(t[f] for f in F)
t['uncached_in_plus_out'] = t['input_tokens'] + t['cache_creation_input_tokens'] + t['output_tokens']
print(json.dumps(t))
