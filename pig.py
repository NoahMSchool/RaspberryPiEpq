#!/usr/bin/env python3
import pigpio
from aiohttp import web
import aiohttp_cors

from time import sleep

from gpiozero import LED
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

magnet_pin = 26
activity_pin = 6
ready_pin = 5

magnet_led = LED(magnet_pin)
activity_led = LED(activity_pin)
ready_led = LED(ready_pin)

pi = pigpio.pi()
if not pi.connected:
    raise SystemExit("pigpio not running?")

def map(value, in_min, in_max, out_min, out_max):
    return ((out_max-out_min) * (value-in_min))/(in_max-in_min) + out_min

def set_servo_degrees(servo, degrees):
    mapped = map(degrees, -90, 90, -1, 1)
    servo.value = mapped


async def magnet(request):
    activity_led.blink(on_time=0.05, off_time=.05, n=1, background=True)
    status = request.query.get("status", "off")
    if status == "off":
        magnet_led.off()
    else:
        magnet_led.on()
    print(status)
    #peer = request.transport.get_extra_info("peername")
    #print(peer)

    try:
        return web.json_response({"ok": True, "message": "Magnet " + status})
    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)}, status=400)


async def servos(request):
    activity_led.blink(on_time=0.05, off_time=.05, n=1, background=True)
    turntable = float(request.query.get("turntable","0"))
    seg_1 = float(request.query.get("seg_1","0"))
    seg_2 = float(request.query.get("seg_2","0"))
    
    #print(request.query)
    try:
        set_servo_degrees(servo_turn,turntable)
        set_servo_degrees(servo_1,seg_1)
        set_servo_degrees(servo_2,seg_2)
        return web.json_response({
            "ok": True, 
            "turntable": turntable,
            "seg_1": seg_1,
            "seg_2": seg_2


        })

    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)}, status=400)

turntable_pin = 13
seg_1_pin = 12
seg_2_pin = 18

sg90_min = 700/1000000
sg90_max = 2500/1000000

MG996R_min = 1000/1000000
MG996R_max = 2300/1000000

MG92B_min = 650/1000000
MG92B_max = 2500/1000000


servo_turn = Servo(
    turntable_pin,
    initial_value = 0, 
    min_pulse_width = MG996R_min, 
    max_pulse_width = MG996R_max,
    pin_factory = PiGPIOFactory()

    )

servo_1 = Servo(
    seg_1_pin, 
    initial_value = 0, 
    min_pulse_width = MG996R_min, 
    max_pulse_width = MG996R_max,
    pin_factory = PiGPIOFactory()
    )

servo_2 = Servo(
    seg_2_pin, 
    initial_value = 0, 
    min_pulse_width = MG92B_min, 
    max_pulse_width = MG92B_max,
    pin_factory = PiGPIOFactory()
    )


app = web.Application()
servos_route = app.router.add_get("/servos", servos)
magnet_route = app.router.add_get("/magnet", magnet)

cors = aiohttp_cors.setup(app, defaults={
    # Allow everything (for quick LAN testing). Lock down later.
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=False,
        expose_headers="*",
        allow_headers=("Content-Type", "Authorization"),
        allow_methods=("GET", "OPTIONS"),
        max_age=86400,
    )
})

# Attach CORS to each route
cors.add(servos_route)
cors.add(magnet_route)

print("Starting Web Server")
ready_led.on()
web.run_app(app, host="0.0.0.0", port=8080)
ready_led.off()
print("All done")
