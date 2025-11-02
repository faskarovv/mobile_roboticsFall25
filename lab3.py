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

drive_speed = 70  # forward speed
search_turn_rate = 35  # constant turning speed
base_turn_hold = 30 # initial time per turn
turn_hold_increase = 15 # how much of increase gonna be added to turn time
stop_distance = 80  #  ultrasonic reaction distance


lost_counter = 0 # counter for how long robot has been off the line
turn_hold_time = base_turn_hold  # current time to turn before switching
search_direction = 1 # left or right


while True:
    distance = ultra.distance() #ultrasonic distance

    # avoiding objects
    if distance < stop_distance: 
        robot.stop() 
        while ultra.distance() < stop_distance: # wait until object is gone
            wait(100)
        continue

    # line following logic
    refl = sensor.reflection()

    if refl < TARGET - THRESH:
        # On black line
        robot.drive(drive_speed, 0)
        lost_counter = 0  
        turn_hold_time = base_turn_hold
    else:
        # Off the line  zigzag search (moving in opposite directions after each turn)
        lost_counter += 1
        if lost_counter >= turn_hold_time:  #if lost for too long, change direction
            search_direction *= -1 # changing direction
            lost_counter = 0
            turn_hold_time += turn_hold_increase #incresing how long it turns next time
        robot.drive(0, search_direction * search_turn_rate)

    wait(40)
