#LED RGB깜빡이기
import RPi.GPIO as GPIO
import time

colors = [0xFF0000, 0xFF0023, 0xFF00FF, 0x0000FF, 0x00FF00, 0x64EB00, 0x4BFB00]
pins = {'pin_R':17, 'pin_G':27, 'pin_B':22}

GPIO.setmode(GPIO.BCM)

try:
    while True:
        GPIO.output(red, True)
        GPIO.output(green, False)
        GPIO.output(blue, False)
        time.sleep(1)
        GPIO.output(red, False)
        GPIO.output(green, True)
        GPIO.output(blue, False)
        time.sleep(1)
        GPIO.output(red, False)
        GPIO.output(green, False)
        GPIO.output(blue, True)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()