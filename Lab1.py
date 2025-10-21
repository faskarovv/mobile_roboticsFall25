#!/usr/bin/env  pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# Initialize EV3 and devices
ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

left_sensor = ColorSensor(Port.S1)
right_sensor = ColorSensor(Port.S3)

# Configure the robot base
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=114)

# Movement constants
drive_speed = 80          # forward speed
hard_turn_speed = 90      # sharp turn rate
slight_turn_speed = 30    # gentle bias when both sensors see green

last_turn = 0             # remembers last direction (-1 = left, 1 = right, 0 = straight)
no_green_count = 0        # counts cycles where no green is seen

while True:
    # Read colors
    left_detected = left_sensor.color()
    right_detected = right_sensor.color()

    if left_detected == Color.GREEN and right_detected != Color.GREEN:
        robot.drive(drive_speed, -hard_turn_speed)
        last_turn = -1
        no_green_count = 0

    elif right_detected == Color.GREEN and left_detected != Color.GREEN:
        robot.drive(drive_speed, hard_turn_speed)
        last_turn = 1
        no_green_count = 0

    elif left_detected == Color.GREEN and right_detected == Color.GREEN:
        # go forward but with slight bias in the last direction
        robot.drive(drive_speed, last_turn * slight_turn_speed)
        no_green_count = 0

    else:
        no_green_count += 1

        if last_turn == -1:
            robot.drive(drive_speed, -hard_turn_speed)
        elif last_turn == 1:
            robot.drive(drive_speed, hard_turn_speed)
        else:
            robot.drive(drive_speed, 0)

        # optional: stop after being off tape for too long
        if no_green_count > 100:  # roughly 1 second if wait(10)
            robot.stop()
            ev3.speaker.beep()  # signal that it lost the line
            break

    wait(10)
