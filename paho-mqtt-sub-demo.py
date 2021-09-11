#import RPi.GPIO as GPIO
#import time
import paho.mqtt.client as mqtt

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # small door button

def on_connect(client, userdata, flags, rc):
    print("connectd w/code "+str(rc))
    client.subscribe("/home/rpi3/garage/small-door-action")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.97", port=1883, keepalive=60)
#client.loop_start()
client.loop_forever()
