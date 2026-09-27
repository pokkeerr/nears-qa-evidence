import asyncio, json, sys, websockets
URI=sys.argv[1]
EXPR = r"""(() { final out = <String>[]; void v(RenderObject r) { if (r is RenderParagraph) { final t = r.text.toPlainText(); if (t.contains('AED') || t.contains('د') || t.contains('Pepperoni') || t.contains('Jalapeno') || t.contains('Margherita') || t.contains('Chicago') || t.contains('Fresh') || t.contains('Croissant') || t.contains('(') ) { final o = r.localToGlobal(Offset.zero); out.add('${t.replaceAll('\n',' ')}|h=${r.size.height}|w=${r.size.width}|y=${o.dy}|x=${o.dx}|ml=${r.maxLines}|fs=${r.text.style?.fontSize}'); } } r.visitChildren(v); } for (final rv in RendererBinding.instance.renderViews) { v(rv); } return out.join('\n'); })()"""
async def main():
    async with websockets.connect(URI, max_size=2**30) as ws:
        n=[0]
        async def call(method, params=None):
            n[0]+=1; i=n[0]
            await ws.send(json.dumps({"jsonrpc":"2.0","id":i,"method":method,"params":params or {}}))
            while True:
                r=json.loads(await ws.recv())
                if r.get("id")==i: return r
        vm=await call("getVM")
        for iso in vm["result"]["isolates"]:
            iid=iso["id"]
            isor=await call("getIsolate",{"isolateId":iid})
            libs=[l for l in isor["result"]["libraries"] if l["uri"]=="package:flutter/src/widgets/binding.dart"]
            if not libs: continue
            r=await call("evaluate",{"isolateId":iid,"targetId":libs[0]["id"],"expression":EXPR})
            if "result" in r and r["result"].get("type")=="@Instance":
                ref=r["result"]
                if ref.get("valueAsStringIsTruncated"):
                    full=await call("getObject",{"isolateId":iid,"objectId":ref["id"],"count":10**7})
                    print(full["result"].get("valueAsString"))
                else: print(ref.get("valueAsString"))
            else: print(json.dumps(r)[:2000])
asyncio.run(main())
