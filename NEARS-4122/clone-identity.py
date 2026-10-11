import re, subprocess
from playwright.sync_api import sync_playwright
PW = next(l.split("|")[3].strip() for l in open("/Users/Apple/Projects/nears/users_test_data.md") if "admin@admin.com" in l)
B = "http://127.0.0.1:8122"
q = lambda db, s: subprocess.run(["mysql","-u","root",db,"-N","-B","-e",s],capture_output=True,text=True,check=True).stdout.strip()
with sync_playwright() as pw:
    br = pw.chromium.launch(headless=True); ctx = br.new_context(); p = ctx.new_page()
    p.goto(B + "/login/admin"); p.get_by_placeholder("email@address.com").fill("admin@admin.com"); p.get_by_placeholder("6+ characters required").fill(PW)
    c = p.locator("#custome_recaptcha"); c.fill(c.input_value())
    p.get_by_role("button", name=re.compile("log ?in", re.I)).first.click(); p.wait_for_load_state("domcontentloaded"); p.wait_for_timeout(1200)
    for oid in (91416, 91417, 91418):
        r = p.goto(f"{B}/admin/parcel/details/{oid}")
        print(f"served admin GET /admin/parcel/details/{oid} -> HTTP {r.status}, landed {p.url.replace(B,'')}, body mentions #{oid}: {str(oid) in p.inner_text('body')}")
    br.close()
for oid in (91416, 91417, 91418):
    print(f"SELECT COUNT(*) FROM orders WHERE id={oid}: clone={q('multi_food_db_qa4122', f'select count(*) from orders where id={oid}')} real={q('multi_food_db', f'select count(*) from orders where id={oid}')}")
