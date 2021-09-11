import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        input_state = GPIO.input(36)
        if input_state == False:
            print('small door open')
            time.sleep(1)
        else:
            print('small door closed')
            time.sleep(1)
        input_state = GPIO.input(40)
        if input_state == False:
            print('large door open')
            time.sleep(1)
        else:
            print('large door closed')
            time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
