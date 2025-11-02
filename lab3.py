#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

ev3 = EV3Brick()
left = Motor(Port.B)
right = Motor(Port.C)
sensor = ColorSensor(Port.S1)
ultra = UltrasonicSensor(Port.S2)
robot = DriveBase(left, right, wheel_diameter=56, axle_track=114)

min_r = 5      # average reflection on black line
max_r = 33     # reflection on table surface

TARGET = (min_r + max_r) / 2       # midpoint between black and surface
THRESH = (max_r - min_r) * 0.35   # tolerance

DRIVE_SPEED = 70
SEARCH_TURN_RATE = 35
BASE_TURN_HOLD = 30
TURN_HOLD_INCREASE = 15
STOP_DISTANCE = 80  # mm for ultrasonic


lost_counter = 0
turn_hold_time = BASE_TURN_HOLD
search_direction = 1


while True:
    distance = ultra.distance()

    
    if distance < STOP_DISTANCE:
        robot.stop()
        while ultra.distance() < STOP_DISTANCE:
            wait(100)
        continue

    # --- Line following ---
    refl = sensor.reflection()

    if refl < TARGET - THRESH:
        # On black line
        robot.drive(DRIVE_SPEED, 0)
        lost_counter = 0
        turn_hold_time = BASE_TURN_HOLD
    else:
        # Off the line → zigzag search
        lost_counter += 1
        if lost_counter >= turn_hold_time:
            search_direction *= -1
            lost_counter = 0
            turn_hold_time += TURN_HOLD_INCREASE
        robot.drive(0, search_direction * SEARCH_TURN_RATE)

    wait(40)
