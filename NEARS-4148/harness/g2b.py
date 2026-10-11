import sys; sys.path.insert(0,'.')
from q import *
E=Ev('g2-owner-positive-controls-fixed.txt','G2 (vi) REDO: rotation measured by SESSION ID (session file basename), not the encrypted cookie value (which differs on every response)')
E.line('NOTE: the (vi-a)/(vi-c) lines above that print "cookie unchanged ...: False" compared the ENCRYPTED laravel_session cookie value, which Laravel re-encrypts (new IV) on every response; that comparison is invalid and is superseded by the session-id measurement below.')
sid=lambda j: os.path.basename(j.session_file() or 'NONE')
V=Jar('fixed','validation2'); V.apply_page(); id0,t0=sid(V),V.token
E.line(f'start: session id={id0[:10]}.. token={t0[:8]}..')
r,email,pw=register(V,'w1',extra={'f_name':''},refresh=False)
E.line(f'(vi-a) validation failure (f_name empty): HTTP {r.status_code} {r.text[:90]} | session id unchanged={sid(V)==id0} | token unchanged={V.token==t0} (no regenerate on early return)')
r,email,pw=register(V,'w2',captcha='WRONG',refresh=False)
E.line(f'(vi-c) wrong captcha: HTTP {r.status_code} {r.text[:80]} | session id unchanged={sid(V)==id0}')
V.token=t0
r,email,pw=register(V,'w3',refresh=False)
E.line(f'(vi-b) same-session retry with the SAME token after those two failures: HTTP {r.status_code} (not 419: {r.status_code!=419}) {r.text[:130]}')
old_file_exists=os.path.exists(f'{W}/storage/framework/sessions/{id0}')
r=V.req('GET','/vendor/apply'); t1=tok(r.text); V.token=t1
E.line(f'(vi) after successful store(): session id rotated={sid(V)!=id0} (old session file still on disk: {old_file_exists}); CSRF token rotated={t1!=t0}; new session id={sid(V)[:10]}.. registration_store_ids={V.session_ids()}')
