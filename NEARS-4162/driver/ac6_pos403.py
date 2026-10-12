from q import *
exec(open('ac5.py').read().split("with Browser() as b:")[0])
with Browser() as b:
    o,op,resp=open_pos(b)
    op.evaluate("() => { window.__toasts = []; }")
    op.locator('.place-order-submit').first.click(force=True); time.sleep(2.5)
    ms=modal_state(op)
    P('POS business 403 (empty cart place-order): toasts', ms['toasts'], '| modal', ms['popup'], '| responses', [r for r in resp if 'pos/order' in r[2]], '| latch', ms['latch'], '| #loading', ms['loading_display'])
    d=fetch(o,'GET','/vendor-panel/','xrw_any'); P('session alive after:', d['status'], 'X-Panel-Session', d['x_panel_session'])
    # a stock 403? try add-to-cart with huge quantity
    opn=True
    save('ac6_pos_business403.txt','\n'.join(out))
