#!/usr/bin/env  pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait

ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

right_sensor = ColorSensor(Port.S3)
left_sensor = ColorSensor(Port.S1)


robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=114)

drive_speed = 100
turn_speed = 50
hard_turn_speed = 80

last_turn = 0

while True:
    left_detected = left_sensor.color()
    right_detected = right_sensor.color()

    if left_detected == Color.GREEN and right_detected != Color.GREEN:

        robot.drive(drive_speed, -hard_turn_speed)
        last_turn = -1

    elif right_detected == Color.GREEN and left_detected != Color.GREEN:
        robot.drive(drive_speed, hard_turn_speed)
        last_turn = 1

    elif left_detected == Color.GREEN and right_detected == Color.GREEN:
        # robot.drive(drive_speed + 15, 0)
        robot.drive(drive_speed, 0)
        last_turn = 0

    else:
        if last_turn == -1:
            robot.drive(drive_speed, -hard_turn_speed)  # forward + left
        elif last_turn == 1:
            robot.drive(drive_speed, hard_turn_speed)   # forward + right
        else:
            robot.drive(drive_speed, 0)      

    wait(10)
