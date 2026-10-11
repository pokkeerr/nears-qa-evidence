#!/usr/bin/env python3
"""NEARS-4122 QA driver. Logs into the admin panel (own server, clone DB) through the real login form + dev captcha,
reads the page CSRF token, then performs direct authenticated POST /admin/order/parcel-return cases. Each case:
snapshot (SELECT-only, clone) -> POST -> snapshot -> diff; response status/Location/X-Request-Id, the flashed toast
(from the followed redirect page), and the request-id-scoped laravel.log lines. Password is read at runtime, never printed.
usage: drive.py <base> <case-json> <out-json>   (case-json = list of {name, method, id?, token: bool, referer_id})
"""
import json, re, subprocess, sys, uuid, pathlib
from playwright.sync_api import sync_playwright

BASE, CASES, OUT = sys.argv[1].rstrip("/"), json.load(open(sys.argv[2])), sys.argv[3]
DB = "multi_food_db_qa4122"
import os
LOG = os.environ.get("QA_LOG", "/Users/Apple/Projects/nears-NEARS-4122-parcel-return-guard/Admin/storage/logs/laravel.log")
PW = next(l.split("|")[3].strip() for l in open("/Users/Apple/Projects/nears/users_test_data.md") if "admin@admin.com" in l)


def sql(q):
    assert "multi_food_db_qa4122" in DB
    return subprocess.run(["mysql", "-u", "root", DB, "-N", "-B", "-e", q], capture_output=True, text=True, check=True).stdout


def snap(oid):
    tabs = ["orders", "parcel_cancellations", "order_transactions", "expenses", "admin_wallets", "delivery_man_wallets"]
    s = {}
    s["checksums"] = dict(l.split("\t") for l in sql("CHECKSUM TABLE " + ",".join(tabs)).strip().splitlines())
    s["counts"] = {t: int(sql(f"SELECT COUNT(*) FROM {t}").strip()) for t in tabs}
    if oid:
        s["order"] = sql(f"SELECT id,order_status,payment_status,order_type,order_amount,canceled_by,delivery_man_id,updated_at FROM orders WHERE id={int(oid)}").strip()
        s["parcel_cancellation"] = sql(f"SELECT id,order_id,cancel_by,before_pickup,return_otp,return_fee,return_fee_payment_status,dm_penalty_fee FROM parcel_cancellations WHERE order_id={int(oid)}").strip()
        s["order_transactions_for_order"] = sql(f"SELECT COUNT(*),COALESCE(SUM(admin_commission),0) FROM order_transactions WHERE order_id={int(oid)}").strip()
        s["expenses_for_order"] = sql(f"SELECT COUNT(*) FROM expenses WHERE order_id={int(oid)}").strip()
    s["admin_wallet"] = sql("SELECT total_commission_earning,digital_received,manual_received FROM admin_wallets WHERE id=1").strip()
    s["dm2_wallet"] = sql("SELECT total_earning,collected_cash,total_withdrawn,pending_withdraw FROM delivery_man_wallets WHERE delivery_man_id=2").strip()
    return s


def toasts(html):
    return re.findall(r"toastr\.(success|error|warning|info)\(\s*['\"]([^'\"]*)['\"]", html)


res = []
with sync_playwright() as pw:
    br = pw.chromium.launch(headless=True)
    ctx = br.new_context()
    page = ctx.new_page()
    page.goto(BASE + "/login/admin")
    page.get_by_placeholder("email@address.com").fill("admin@admin.com")
    page.get_by_placeholder("6+ characters required").fill(PW)
    cap = page.locator("#custome_recaptcha")
    if cap.count() and cap.input_value():
        cap.fill(cap.input_value())
    page.get_by_role("button", name=re.compile("log ?in", re.I)).first.click()
    page.wait_for_load_state("domcontentloaded"); page.wait_for_timeout(1500)
    login_url = page.url
    for c in CASES:
        oid = c.get("id")
        ref = f"{BASE}/admin/parcel/details/{c.get('referer_id', 153)}"
        page.goto(ref)
        page.wait_for_load_state("domcontentloaded")
        if page.locator('meta[name="csrf-token"]').count() == 0:
            raise SystemExit(f"no csrf meta at case {c['name']!r}: url={page.url} title={page.title()!r}")
        tok = page.locator('meta[name="csrf-token"]').get_attribute("content")
        before = snap(oid)
        off = pathlib.Path(LOG).stat().st_size
        url = BASE + "/admin/order/parcel-return"
        seen = []
        page.on("response", lambda rp: seen.append(rp))
        # real browser navigation/form submit: carries the admin session cookie like a user's click would
        if c["method"] == "GET":
            with page.expect_navigation():
                page.evaluate("u => { window.location.href = u }", url + f"?id={oid}&order_status=returned")
        else:
            fields = {"id": str(oid), "order_status": "returned"}
            if c.get("token", True):
                fields["_token"] = tok
            with page.expect_navigation():
                page.evaluate("""([u, f]) => { const form = document.createElement('form'); form.method = 'POST'; form.action = u;
                    for (const [k, v] of Object.entries(f)) { const i = document.createElement('input'); i.type = 'hidden'; i.name = k; i.value = v; form.appendChild(i); }
                    document.body.appendChild(form); form.submit(); }""", [url, fields])
        page.wait_for_load_state("domcontentloaded"); page.wait_for_timeout(400)
        first = next(rp for rp in seen if rp.url.split("?")[0].endswith("/admin/order/parcel-return"))
        rid = first.headers.get("x-request-id")
        row = {"case": c["name"], "method": c["method"], "id": oid, "token_sent": c.get("token", True), "status": first.status,
               "location": first.headers.get("location"), "x_request_id": rid, "landed": page.url.replace(BASE, ""), "toasts": toasts(page.content())}
        after = snap(oid)
        new = pathlib.Path(LOG).read_bytes()[off:].decode("utf8", "replace")
        row["log_lines_for_request"] = [l[:400] for l in new.splitlines() if rid and rid in l]
        row["fail_refused_in_window"] = sum(1 for l in new.splitlines() if "[FAIL] parcel.return_refused" in l)
        row["before"], row["after"] = before, after
        row["db_diff"] = {k: [before[k], after[k]] for k in before if before[k] != after[k]}
        res.append(row)
    br.close()
json.dump({"login_landed": login_url.replace(BASE, ""), "results": res}, open(OUT, "w"), indent=1)
for r in res:
    print(r["case"], r["status"], r["toasts"], "refused_logs_in_window=", r["fail_refused_in_window"], "diff_keys=", list(r["db_diff"].keys()))
