import RPi.GPIO as GPIO
import time
import subprocess
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # small door button
GPIO.setup(16, GPIO.OUT)  # small door relay
GPIO.output(16, False)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # small door reed sensor
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # LARGE door reed sensor

try:
    while True:
        sm_door_btn = GPIO.input(22)
        if sm_door_btn == False:
            GPIO.output(16, True)
            time.sleep(0.5)
            GPIO.output(16, False)
            print('sm-door btn press!')
            time.sleep(0.5)
        else:
            print('no press')
            time.sleep(0.5)

        sm_door_sens = GPIO.input(36)
        if sm_door_sens == False:
            print('small door open')
            subprocess.call(["mosquitto_pub", "-h", "192.168.0.97", "-p", "1883", "-m", "open", "-t", "/home/rpi3/garage/small-door-status"])
            time.sleep(0.5)
        else:
            print('small door closed')
            subprocess.call(["mosquitto_pub", "-h", "192.168.0.97", "-p", "1883", "-m", "closed", "-t", "/home/rpi3/garage/small-door-status"])
            time.sleep(0.5)

        lg_door_sens = GPIO.input(40)
        if lg_door_sens == False:
            print('large door open')
            subprocess.call(["mosquitto_pub", "-h", "192.168.0.97", "-p", "1883", "-m", "open", "-t", "/home/rpi3/garage/large-door-status"])
            time.sleep(0.5)
        else:
            print('large door closed')
            subprocess.call(["mosquitto_pub", "-h", "192.168.0.97", "-p", "1883", "-m", "closed", "-t", "/home/rpi3/garage/large-door-status"])
            time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
