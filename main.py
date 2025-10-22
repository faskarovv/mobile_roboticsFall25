#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# --- Initialize ---
ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
sensor = ColorSensor(Port.S1)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=114)

# --- Drive settings ---
drive_speed = 100
turn_rate = 50            # constant turning speed
base_turn_hold = 100      # initial time per turn
turn_hold_increase = 50   # how much longer each search lasts before switching

# --- State variables ---
search_direction = 1
turn_hold_time = base_turn_hold
lost_counter = 0
found_once = False

while True:
    color = sensor.color()

    if color == Color.GREEN:
        # Found line → drive straight
        robot.drive(drive_speed, 0)
        lost_counter = 0
        turn_hold_time = base_turn_hold  # reset search width
        found_once = True

    else:
        # Lost line → rotate in place
        lost_counter += 1

        # Flip direction when hold time expires
        if lost_counter >= turn_hold_time:
            search_direction *= -1
            lost_counter = 0
            turn_hold_time += turn_hold_increase  # increase how long it turns next time

        # Constant speed turn
        robot.drive(0, search_direction * turn_rate)

    wait(10)
