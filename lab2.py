#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, DataLog
import math

# ev3 setup
ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
sensor = ColorSensor(Port.S1)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=114)

# datalog setup
watch = StopWatch()
data = DataLog('time_ms', 'x_mm', 'y_mm', 'heading_deg', name='path_log', timestamp=False, extension='csv')
x, y, heading = 0.0, 0.0, 0.0
last_distance = 0.0

#drive settings
drive_speed = 100
turn_rate = 50 # constant turning speed
base_turn_hold = 100 # initial time per turn
turn_hold_increase = 50  # how much longer each search lasts before switching

search_direction = 1 # left or right
turn_hold_time = base_turn_hold # current time to turn before switching
lost_counter = 0 # counter for how long robot has been off the line
found_once = False

loop_counter = 0 # loop counter for logging

while True:
    color = sensor.color()

    
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

    
    loop_counter += 1
    if loop_counter % 5 == 0:  # logging every 5th loop
        distance = robot.distance() # get distance traveled since last call
        delta_d = distance - last_distance # change in distance
        last_distance = distance # updating last distance

        heading = robot.angle() # current heading
        rad = math.radians(heading) # converting heading to radians
        x += delta_d * math.cos(rad) #  x position
        y += delta_d * math.sin(rad) #  y position

        data.log(watch.time(), x, y, heading)

    wait(10)
