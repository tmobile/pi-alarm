# coding=utf-8
# =========================================================================
# Copyright © 2018 T-Mobile USA, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================

import RPi.GPIO as GPIO
import sys, termios, tty

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

print("Setup:")
print("pin 12 (bcm 18) to S")
print("pin 6 (ground) to +)")
print("pin 4 (5V) to -)")
print("Commands:")
print("1 - turn on, 0 - turn off, q - quit")

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

while True:
    char = getch()

    if (char == "q"):
        print("")
        exit(0)

    if (char == "1"):
        GPIO.output(18,GPIO.HIGH)
        print("on")

    elif (char == "0"):
        print("off")
        GPIO.output(18,GPIO.LOW)
