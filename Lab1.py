#!/usr/bin/env pybricks-micropython
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

# ======= Tunable constants =======
drive_speed = 80          # normal forward speed
turn_speed = 90           # base turning rate
slight_turn_speed = 30    # when both green (slight bias)
recovery_turn_gain = 1.5  # how much stronger to turn when line is lost
recovery_speed_gain = 0.5 # how much slower to go when line is lost

last_turn = 0             # remembers last turn (-1 = left, 1 = right, 0 = straight)
no_green_count = 0        # how long line has been lost

# ======= Main loop =======
while True:
    left_detected = left_sensor.color()
    right_detected = right_sensor.color()

    if left_detected == Color.GREEN and right_detected != Color.GREEN:
        # Turn left
        robot.drive(drive_speed * 0.6, -turn_speed)
        last_turn = -1
        no_green_count = 0

    elif right_detected == Color.GREEN and left_detected != Color.GREEN:
        # Turn right
        robot.drive(drive_speed * 0.6, turn_speed)
        last_turn = 1
        no_green_count = 0

    elif left_detected == Color.GREEN and right_detected == Color.GREEN:
        # Both sensors on tape → go forward but with slight bias
        robot.drive(drive_speed, last_turn * slight_turn_speed)
        no_green_count = 0

    else:
        # Both sensors off → likely lost the line, recover
        no_green_count += 1

        if last_turn == -1:
            robot.drive(drive_speed * recovery_speed_gain, -turn_speed * recovery_turn_gain)
        elif last_turn == 1:
            robot.drive(drive_speed * recovery_speed_gain, turn_speed * recovery_turn_gain)
        else:
            robot.drive(drive_speed * 0.5, 0)

        # Optional: stop completely if lost too long
        if no_green_count > 120:  # about 1.2 seconds
            robot.stop()
            ev3.speaker.beep()
            break

    wait(10)
