import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # small door button
GPIO.setup(16, GPIO.OUT)  # small door relay
GPIO.output(16, False)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # large door button
GPIO.setup(18, GPIO.OUT)  # large door relay
GPIO.output(18, False)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # small door reed sensor
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # LARGE door reed sensor

def on_connect(client, userdata, flags, rc):
    print("connectd w/code "+str(rc))
    if rc == 0:
        client.connected_flag = True
        client.subscribe([("/home/rpi3/garage/small-door-btn",0),("/home/rpi3/garage/large-door-btn",0)])

def on_message(client, userdata, msg):
    if msg.topic == "/home/rpi3/garage/small-door-btn":
        GPIO.output(16, True)
        time.sleep(0.25)
        GPIO.output(16, False)
    if msg.topic == "/home/rpi3/garage/large-door-btn":
        GPIO.output(18, True)
        time.sleep(0.25)
        GPIO.output(18, False)

    print(msg.topic+" "+str(msg.payload))

try:
    client = mqtt.Client()
    client.connected_flag = False
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect("192.168.0.97", port=1883, keepalive=60)
        client.loop_start()
    except Exception, e:
        print('MQTT connection error, ' + e.args)   # (111, Connection refused) if broker is down
        # Print a message but keep running, still need to monitor physical garage door buttons.

    while True:
        sm_door_btn = GPIO.input(22)
        if sm_door_btn == False:
            GPIO.output(16, True)
            time.sleep(0.25)
            GPIO.output(16, False)
            print('sm-door btn press!')
            time.sleep(0.25)
        else:
            print('no press')
            time.sleep(0.25)

        lg_door_btn = GPIO.input(15)
        if lg_door_btn == True:
            GPIO.output(18, True)
            time.sleep(0.25)
            GPIO.output(18, False)
            print('lg-door btn press!')
            time.sleep(0.25)
        else:
            print('no press')
            time.sleep(0.25)

        sm_door_sens = GPIO.input(36)
        if sm_door_sens == False:
            print('small door open')
            client.publish("/home/rpi3/garage/small-door-status", payload="open", qos=0, retain=False)
            time.sleep(0.25)
        else:
            print('small door closed')
            client.publish("/home/rpi3/garage/small-door-status", payload="closed", qos=0, retain=False)
            time.sleep(0.25)

        lg_door_sens = GPIO.input(40)
        if lg_door_sens == False:
            print('large door open')
            client.publish("/home/rpi3/garage/large-door-status", payload="open", qos=0, retain=False)
            time.sleep(0.25)
        else:
            print('large door closed')
            client.publish("/home/rpi3/garage/large-door-status", payload="closed", qos=0, retain=False)
            time.sleep(0.25)

except KeyboardInterrupt:
    client.loop_stop()
    #GPIO.cleanup()
finally:
    client.loop_stop()
    #GPIO.cleanup()
