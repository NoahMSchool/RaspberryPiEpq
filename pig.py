#!/usr/bin/env python3
import pigpio
from aiohttp import web
import aiohttp_cors

import asyncio
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

global target_turntable
global target_seg_2
global target_seg_1

global current_turntable
global current_seg_1
global current_seg_2

pi = pigpio.pi()
if not pi.connected:
    raise SystemExit("pigpio not running?")

def map(value, in_min, in_max, out_min, out_max):
    return ((out_max-out_min) * (value-in_min))/(in_max-in_min) + out_min

def set_servo_degrees(servo, degrees):
    print(degrees)
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


async def servos_direct(request):
    activity_led.blink(on_time=0.05, off_time=.05, n=1, background=True)
    turntable = float(request.query.get("turntable","0"))
    seg_1 = float(request.query.get("seg_1","0"))
    seg_2 = float(request.query.get("seg_2","0"))
    
    #print(request.query)
    try:
        target_baseseg = turntable
        set_servo_degrees(servo_turn,turntable)
        set_servo_degrees(servo_1,seg_1)
        set_servo_degrees(servo_2,seg_2)
        
        return web.json_response({
            "ok": True, 
            "message": "moving directly",
            "turntable": turntable,
            "seg_1": seg_1,
            "seg_2": seg_2
        })

    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)}, status=400)

async def servos_smooth(request):
    global current_turntable, target_turntable
    global current_seg_1, target_seg_1
    global current_seg_2, target_seg_2

    activity_led.blink(on_time=0.05, off_time=.05, n=1, background=True)
    turntable = float(request.query.get("turntable","0"))
    seg_1 = float(request.query.get("seg_1","0"))
    seg_2 = float(request.query.get("seg_2","0"))
    print("smooth")
    #print(request.query)
    try:
        target_turntable = turntable
        target_seg_1 = seg_1
        target_seg_2 = seg_2
        
        return web.json_response({
            "ok": True, 
            "message": "moving smoothly towards",
            "turntable": turntable,
            "seg_1": seg_1,
            "seg_2": seg_2
        })

    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)}, status=400)

async def stop_server(request):
    activity_led.blink(on_time=0.05, off_time=.05, n=1, background=True)
    raise web.GracefulExit()


async def motion_loop():
    global current_turntable, target_turntable
    global current_seg_1, target_seg_1
    global current_seg_2, target_seg_2
    current_turntable = 0
    target_turntable = 0
    current_seg_1 = 0
    target_seg_1 = 0
    current_seg_2 = 0
    target_seg_2 = 0
    
    speed = 90
    dt = 0.04
    print("motion")
    while  True:
        print(current_turntable, target_turntable)
        print("moving")

        if target_turntable > current_turntable and target_turntable < 90.1:
            current_turntable = min(current_turntable+speed*dt, target_turntable)
            set_servo_degrees(servo_turn, current_turntable)
        elif target_turntable < current_turntable and target_turntable > -90.1:
            current_turntable = max(current_turntable-speed*dt, target_turntable)
            set_servo_degrees(servo_turn, current_turntable)

        if target_seg_1 > current_seg_1 and target_seg_1 < 90.1:
            current_seg_1 = min(current_seg_1+speed*dt, target_seg_1)
            set_servo_degrees(servo_1, current_seg_1)
        elif target_seg_1 < current_seg_1 and target_seg_1 > -90.1:
            current_seg_1 = max(current_seg_1-speed*dt, target_seg_1)
            set_servo_degrees(servo_1, current_seg_1)

        if target_seg_2 > current_seg_2 and target_seg_2 < 90.1:
            current_seg_2 = min(current_seg_2+speed*dt, target_seg_2)
            set_servo_degrees(servo_2, current_seg_2)
        elif target_seg_2 < current_seg_2 and target_seg_2 > -90.1:
            current_seg_2 = max(current_seg_2-speed*dt, target_seg_2)
            set_servo_degrees(servo_2, current_seg_2)


        await asyncio.sleep(dt)

async def on_startup(app):
    print("on_startup")
    app['motion_task'] = asyncio.create_task(motion_loop())

async def on_cleanup(app):
    print("on_cleanup")
    task = app.get('motion_task')
    if task:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task
        
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

app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)

servos_smooth_route = app.router.add_get("/servos", servos_smooth)
servos_direct_route = app.router.add_get("/servos_direct", servos_direct)
stop_route = app.router.add_get("/stop", stop_server)
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
cors.add(servos_smooth_route)
cors.add(servos_direct_route)
cors.add(magnet_route)
cors.add(stop_route)

print("Starting Web Server")
ready_led.on()
web.run_app(app, host="0.0.0.0", port=8080)
ready_led.off()
print("All done")
