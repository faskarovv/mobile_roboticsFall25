#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, DataLog
import math

# --- EV3 setup ---
ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
sensor = ColorSensor(Port.S1)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=114)

# --- DataLog setup ---
watch = StopWatch()
data = DataLog('time_ms', 'x_mm', 'y_mm', 'heading_deg', name='path_log', timestamp=False, extension='csv')
x, y, heading = 0.0, 0.0, 0.0
last_distance = 0.0

# --- Movement parameters ---
drive_speed = 100
turn_rate = 50
base_turn_hold = 100
turn_hold_increase = 50

search_direction = 1
turn_hold_time = base_turn_hold
lost_counter = 0
found_once = False

# --- Loop counter for logging less frequently ---
loop_counter = 0

while True:
    color = sensor.color()

    # --- Line following logic ---
    if color == Color.GREEN:
        robot.drive(drive_speed, 0)
        lost_counter = 0
        turn_hold_time = base_turn_hold
        found_once = True
    else:
        lost_counter += 1
        if lost_counter >= turn_hold_time:
            search_direction *= -1
            lost_counter = 0
            turn_hold_time += turn_hold_increase
        robot.drive(0, search_direction * turn_rate)

    # --- Odometry & logging (every 5 loops) ---
    loop_counter += 1
    if loop_counter % 5 == 0:   # adjust this number if needed
        distance = robot.distance()
        delta_d = distance - last_distance
        last_distance = distance

        heading = robot.angle()
        rad = math.radians(heading)
        x += delta_d * math.cos(rad)
        y += delta_d * math.sin(rad)

        data.log(watch.time(), x, y, heading)

    wait(10)
