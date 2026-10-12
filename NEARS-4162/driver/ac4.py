import sys, json
from q import *
DB='multi_food_db_qa4162'
OW4=('john.smith@demo.com','123456789')
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
SET='/vendor-panel/business-settings/store-setup'
def sched(): return sql(DB,"select group_concat(id order by id) from store_schedule where store_id=4")
def msgs(): return sql(DB,"select count(*) from messages where conversation_id in (49,70)")
def active(): return sql(DB,"select active from stores where id=4")
def mkctx(b, block_js=False):
    o=b.ctx(); o.add_init_script(INIT_TOASTS)
    if block_js: o.route('**/vendor-session-refusal.js*', lambda r: r.abort())
    return o
def open_owner(b, path, block_js=False):
    o=mkctx(b, block_js); op=login(o,'vendor',*OW4)
    resp=[]
    op.on('response', lambda r: resp.append((r.status, r.request.method, r.url.replace(BASE,''), r.headers.get('x-panel-session'))) if ('/vendor-panel/' in r.url and r.request.resource_type in ('xhr','fetch')) else None)
    op.goto(BASE+path, wait_until='domcontentloaded'); time.sleep(2)
    return o, op, resp
def end(ap, mode):
    admin_post(ap,'/admin/store/status/4/0')
    if mode=='expired': admin_post(ap,'/admin/store/status/4/1')
def restore(ap, mode):
    if mode=='suspended': admin_post(ap,'/admin/store/status/4/1')

def do_delete(op, row_id):
    op.locator('.delete-schedule[data-url$="/remove-schedule/%d"]' % row_id).click()
    op.wait_for_selector('.swal2-confirm', state='visible'); op.locator('.swal2-confirm').click()
def do_add(op, start, end_):
    op.locator('span.add--primary[data-day="Monday"]').click()
    op.wait_for_selector('#exampleModal', state='visible'); time.sleep(0.6)
    op.evaluate("([s,e]) => { document.querySelector('#add-schedule input[name=start_time]').value=s; document.querySelector('#add-schedule input[name=end_time]').value=e; }", [start,end_])
    op.locator('#add-schedule button.btn--primary').click()
def open_conv(op):
    op.locator('.chat-user-info').first.click()
    op.wait_for_selector('#reply-form-vnd', timeout=15000)
def do_send(op, text):
    op.locator('#reply-form-vnd textarea').first.fill(text)
    op.locator('#reply-form-vnd button[type=submit]').first.click()

def wait_end_modal(op):
    op.wait_for_function("() => { const p=document.querySelector('.swal2-popup'); return p && getComputedStyle(p).display !== 'none' && /session|suspend|inactive/i.test(p.innerText); }", timeout=25000)
    time.sleep(0.5)
def report(op, resp, label, banned):
    ms=modal_state(op)
    P('  [%s] responses: %s' % (label, [r for r in resp if r[3]=='ended' or r[0]>=400] or resp))
    P('  [%s] MODAL %r buttons=%s #loading=%s toasts=%s' % (label, ms['popup'], ms['buttons_visible'], ms['loading_display'], ms['toasts']))
    bad=[t for t in ms['toasts'] if any(x in t for x in banned)]
    P('  [%s] banned-copy toasts present: %s' % (label, bad or 'NONE'))
    return ms, bad

with Browser() as b:
    a=b.ctx(); ap=login(a,'admin','admin@admin.com','123456789')
    # ======== AC6 controls (unheld owner)
    P('=== AC6 CONTROL: schedule add / delete, message send (approved, not-held owner)')
    s0=sched(); P('schedule rows before:', s0)
    o,op,resp=open_owner(b, SET)
    do_add(op,'00:30','01:30'); time.sleep(2.5)
    ms=modal_state(op); P('add-schedule toasts:', ms['toasts'], 'resp:', [r for r in resp if 'add-schedule' in r[2]], 'rows:', sched())
    new_ids=[int(x) for x in sched().split(',')]; added=[i for i in new_ids if str(i) not in s0.split(',')]
    time.sleep(1)
    if added:
        op.evaluate("() => { window.__toasts=[]; }")
        do_delete(op, added[0]); time.sleep(2.5)
        ms=modal_state(op); P('delete-schedule toasts:', ms['toasts'], 'rows:', sched(), 'equals before:', sched()==s0)
    o.close()
    o,op,resp=open_owner(b,'/vendor-panel/message/list'); m0=msgs()
    open_conv(op); do_send(op,'QA4162 control message'); time.sleep(2.5)
    ms=modal_state(op); P('message send toasts:', ms['toasts'], 'resp:', [r for r in resp if '/message/store' in r[2]], 'messages before/after:', m0, msgs())
    o.close()
    # ======== AC4 refusal arms
    P('=== AC4 4a schedule delete under a session-ended owner (expired)')
    s0=sched()
    o,op,resp=open_owner(b, SET); end(ap,'expired'); resp.clear()
    do_delete(op, 16); wait_end_modal(op)
    ms,bad=report(op,resp,'4a',['Schedule not found','Schedule removed'])
    op.screenshot(path='%s/ac4_4a_modal.png' % EVD)
    op.locator('.swal2-confirm').click(); op.wait_for_url(lambda u:'/login/' in u); P('  post-OK', op.url, '| schedule rows unchanged:', sched()==s0, sched())
    o.close()
    P('=== AC4 4b add-schedule under a marker-held owner (suspended)')
    o,op,resp=open_owner(b, SET); end(ap,'suspended'); resp.clear()
    do_add(op,'02:00','03:00'); wait_end_modal(op)
    ms,bad=report(op,resp,'4b',['{"errors"','Schedule added','errors'])
    op.locator('.swal2-confirm').click(); op.wait_for_url(lambda u:'/login/' in u); P('  post-OK', op.url, '| schedule rows unchanged:', sched()==s0, sched())
    restore(ap,'suspended'); o.close()
    P('=== AC4 4c message send under a session-ended owner (expired)')
    o,op,resp=open_owner(b,'/vendor-panel/message/list'); m0=msgs()
    open_conv(op); op.locator('#reply-form-vnd textarea').first.fill('QA4162 stuck message'); end(ap,'expired'); resp.clear()
    op.locator('#reply-form-vnd button[type=submit]').first.click(); wait_end_modal(op)
    ms,bad=report(op,resp,'4c',['Write something','Message sent'])
    op.locator('.swal2-confirm').click(); op.wait_for_url(lambda u:'/login/' in u); P('  post-OK', op.url, '| messages unchanged:', m0==msgs())
    o.close()
    P('=== restaurant-index:547 open/close toggle under a session-ended owner (expired)')
    a0=active()
    o,op,resp=open_owner(b, SET); end(ap,'expired'); resp.clear()
    op.locator('.restaurant-open-status').first.click(force=True) if False else op.locator('label[for="restaurant-open-status"], .toggle-switch:has(.restaurant-open-status)').first.click()
    op.wait_for_selector('.swal2-confirm', state='visible'); op.locator('.swal2-confirm').click(); wait_end_modal(op)
    ms,bad=report(op,resp,'547',['Successfully','updated'])
    P('  location.reload raced? url still', ms['url'], '| stores.active before/after', a0, active())
    op.locator('.swal2-confirm').click(); op.wait_for_url(lambda u:'/login/' in u); P('  post-OK', op.url)
    o.close()
    # ======== base-equivalent client (prefilter blocked) observations: suspended door 403 JSON, old client code
    P('=== BASE-EQUIVALENT CLIENT (vendor-session-refusal.js request aborted; server = 4155 door JSON) - NOT a base checkout')
    for label,path,mode,fn in [('4a base-equiv',SET,'suspended','del'),('4b base-equiv',SET,'suspended','add'),('4c base-equiv','/vendor-panel/message/list','suspended','msg')]:
        o,op,resp=open_owner(b,path,block_js=True)
        P('  prefilter loaded on page? ', op.evaluate("() => !!window.nearsPanelSessionEnded || typeof window.nearsPanelSessionEnded"), '(undefined expected when blocked)')
        if fn=='msg': open_conv(op); op.locator('#reply-form-vnd textarea').first.fill('QA4162 base-equiv msg')
        end(ap,'suspended'); resp.clear()
        if fn=='del': do_delete(op,16)
        elif fn=='add': do_add(op,'02:00','03:00')
        else: op.locator('#reply-form-vnd button[type=submit]').first.click()
        time.sleep(3.5)
        ms=modal_state(op)
        P('  [%s] responses %s | toasts %s | modal %r | #loading %s' % (label, [r for r in resp if r[0]>=400 or r[3]], ms['toasts'], ms['popup'], ms['loading_display']))
        restore(ap,'suspended'); o.close()
save('ac4_ac6_schedule_message.txt','\n'.join(out))
