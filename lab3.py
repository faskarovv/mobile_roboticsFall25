#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait

ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
sensor = ColorSensor(Port.S1)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=114)

# --- Movement parameters ---
drive_speed = 100
turn_rate = 30            # slower turn for tighter track
base_turn_hold = 80
turn_hold_increase = 30   # smaller increment per lost search

# --- State variables ---
search_direction = 1
turn_hold_time = base_turn_hold
lost_counter = 0
found_once = False

# --- Smart path memory ---
path_stack = []           # stores 'F', 'L', 'R' moves
recent_directions = []    # prevents flipping back and forth endlessly

while True:
    color = sensor.color()

    if color == Color.BLACK:
        # --- Follow line ---
        robot.drive(drive_speed, 0)
        lost_counter = 0
        turn_hold_time = base_turn_hold
        found_once = True

        # Record forward movement if last move wasn't 'F'
        if not path_stack or path_stack[-1] != 'F':
            path_stack.append('F')

    else:
        # --- Line lost ---
        lost_counter += 1

        if lost_counter >= turn_hold_time:
            # Dead end / search timeout reached
            lost_counter = 0
            turn_hold_time += turn_hold_increase

            # Backtrack if we have moves
            if path_stack:
                last_move = path_stack.pop()
                robot.drive(-50, 0)  # reverse a bit
                wait(300)

            # Flip search direction, avoid repeating recent directions
            search_direction *= -1
            recent_directions.append(search_direction)
            if len(recent_directions) > 4:
                recent_directions.pop(0)
            # Avoid flipping to a recent direction
            if recent_directions.count(search_direction) > 1:
                search_direction *= -1

        # Rotate in place searching for line
        robot.drive(0, search_direction * turn_rate)

    wait(10)
