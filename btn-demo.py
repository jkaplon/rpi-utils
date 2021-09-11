import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # large door button

try:
    while True:
        input_state = GPIO.input(22)
        if input_state == False:
            print('sm-door button press!')
            time.sleep(0.5)
        else:
            print('no press')
            time.sleep(0.5)

        lg_door_btn = GPIO.input(15)
        if lg_door_btn == True:
            print('lg-door btn press!')
            time.sleep(0.5)
        else:
            print('no press')
            time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
