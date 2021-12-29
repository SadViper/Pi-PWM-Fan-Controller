#!/usr/bin/python3
# -*- coding: utf-8 -*-
#INSTALL PACKAGE
#sudo apt install python3-lgpio

import lgpio
import time
import signal
import sys
import os
import atexit
import threading

# Configuration
FAN_PIN = 13            # BCM pin used to drive PWM fan
FAN_RPM = 16            # BCM pin used to read fan rpm
WAIT_TIME = 1           # [s] Time to wait between each refresh
MAX_FAN_SPEED = 1500    # Max fan speed to calculate 
PWM_FREQ = 10000        # [kHz] 25kHz for Noctua PWM control

# Configurable temperature and fan speed
MIN_TEMP = 30
LOW_TEMP = 35
MAX_TEMP = 60
FAN_OFF = 0
FAN_LOW = 20
FAN_HIGH = 100
FAN_MAX = 100
TEMP_STEP = (FAN_HIGH - FAN_LOW) / (MAX_TEMP - LOW_TEMP)

# Variable definition
count = 0
h = lgpio.gpiochip_open(0)
lgpio.exceptions = False

# Get CPU's temperature
def getCpuTemperature():
    res = os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
    temp = float(res)/1000
    return temp

# Set fan speed
def setFanSpeed(speed):
    lgpio.tx_pwm(h, FAN_PIN, PWM_FREQ, round(speed))
    rpm_print_speed(speed)
    return()

# Handle fan speed
def handleFanSpeed(temperature):
    # Turn off the fan if lower than lower dead band
    if temperature <= MIN_TEMP:
        setFanSpeed(FAN_OFF)
        return
    # Run fan at lowest speed
    elif temperature >= MIN_TEMP and temperature <= LOW_TEMP:
        setFanSpeed(FAN_LOW)
        return
    elif temperature >= LOW_TEMP and temperature <= MAX_TEMP:
        temperature -= LOW_TEMP
        setFanSpeed(FAN_LOW + ( temperature * TEMP_STEP))
        return
    # Run fan at Max speed
    elif temperature > MAX_TEMP:
        setFanSpeed(FAN_MAX)
        return
    else:
        return

# Reset fan to 100% by cleaning GPIO ports
def resetFan():
    lgpio.gpiochip_close(h) # resets all GPIO ports used by this function

def rpm_print_speed(speed):
    f = open("/tmp/fan-rpm", "w")
    f.write(str(round(speed*19)))
    f.write('\r\n')
    f.close()

try:
    FAN_OFFSET = round( MAX_FAN_SPEED / 100 )
    while True:
        temp = float(getCpuTemperature())
        handleFanSpeed(temp)
        time.sleep(WAIT_TIME)


except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
    lgpio.gpiochip_close(h)

atexit.register(resetFan)