#!/usr/bin/env python3
import pigpio
from aiohttp import web

from time import sleep
from gpiozero import Servo

pi = pigpio.pi()
if not pi.connected:
    raise SystemExit("pigpio not running?")

def map(value, in_min, in_max, out_min, out_max):
    return ((out_max-out_min) * (value-in_min))/(in_max-in_min) + out_min

def set_servo_degrees(servo, degrees):
    mapped = map(degrees, -90, 90, -1, 1)
    servo.value = mapped


async def magnet(request):
    print("magnet")

    status = request.query.get("status", "off")
    print(status)
    peer = request.transport.get_extra_info("peername")
    print(peer)

    try:
        return web.json_response({"ok": True, "message": "Magnet Toogle"})
    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)}, status=400)


async def servos(request):
    base_angle = float(request.query.get("base_angle","0"))
    middle_angle = float(request.query.get("middle_angle","0"))
    
    #print(request.query)
    try:
        set_servo_degrees(servobase,base_angle)
        set_servo_degrees(servomiddle,middle_angle)
        return web.json_response({
            "ok": True, 
            "base_angle": base_angle,
            "middle_angle": middle_angle
        })

    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)}, status=400)

baseservopin = 12
middleservopin = 13

sg90_min = 700/1000000
sg90_max = 2500/1000000

servobase = Servo(
    baseservopin, 
    initial_value = 0, 
    min_pulse_width = sg90_min, 
    max_pulse_width = sg90_max
    )

servomiddle = Servo(
    middleservopin, 
    initial_value = 0, 
    min_pulse_width = sg90_min, 
    max_pulse_width = sg90_max
    )



app = web.Application()
app.router.add_get("/servos", servos)
app.router.add_get("/magnet", magnet)

web.run_app(app, host="0.0.0.0", port=8080)

