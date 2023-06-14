#LED RGB깜빡이기
import RPi.GPIO as GPIO
import time

red = 17; green = 22; blue = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

GPIO.output(red, True)
GPIO.output(green, True)
GPIO.output(blue, True)         # 여기까지 초기화


try:
    while True:
        # RED,GREEN = YELLO / RED, BLUE = PINK  / GREEN, BLUE = SKYBLUE
        GPIO.output(red, True)
        GPIO.output(green, False)
        GPIO.output(blue, False)
        time.sleep(1)
        GPIO.output(red, True)
        GPIO.output(green, False)
        GPIO.output(blue, True)
        time.sleep(1)
        GPIO.output(red, True)
        GPIO.output(green,True)
        GPIO.output(blue, False)
        time.sleep(1)
  
  
except KeyboardInterrupt:
    GPIO.output(red,True)
    GPIO.output(green,True)
    GPIO.output(blue,True)
    GPIO.cleanup()