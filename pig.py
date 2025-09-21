#!/usr/bin/env python3
import pigpio
from aiohttp import web

pi = pigpio.pi()
if not pi.connected:
    raise SystemExit("pigpio not running?")

async def test(request):
    angle = request.query.get("rocco","dog")
    print(angle)
    print(request.query)
    print("got test")
    try:
        return web.json_response({"ok": True, "angle": 50})
    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)}, status=400)

async def magnet(request):
    print("magnet")

    try:
        return web.json_response({"ok": True, "message": "Magnet Toogle"})
    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)}, status=400)


app = web.Application()
app.router.add_get("/test", test)
app.router.add_get("/magnet", magnet)

web.run_app(app, host="0.0.0.0", port=8080)

