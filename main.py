#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait

#ev3 setup
ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
sensor = ColorSensor(Port.S1)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=114)

drive_speed = 100 
turn_rate = 50            # constant turning speed
base_turn_hold = 100      # initial time per turn
turn_hold_increase = 50   # how much longer each search lasts before switching


search_direction = 1 # left or right
turn_hold_time = base_turn_hold # current time to turn before switching
lost_counter = 0 # counter for how long robot has been off the line
found_once = False

while True:
    color = sensor.color() #  color sensor reading

    if color == Color.GREEN:
       
        robot.drive(drive_speed, 0)
        lost_counter = 0 
        turn_hold_time = base_turn_hold # reset turn hold time
        found_once = True

    else:

        lost_counter += 1


        if lost_counter >= turn_hold_time: #if lost for too long robot changes direction
            search_direction *= -1 # changing direction
            lost_counter = 0
            turn_hold_time += turn_hold_increase  # increase how long it turns next time


        robot.drive(0, search_direction * turn_rate)

    wait(10)
