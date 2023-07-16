from ast import While
from asyncore import read
from cgi import print_arguments
from csv import reader
from string import printable
import sys
from tkinter import CURRENT
import board
from datetime import datetime
import time
from adafruit_servokit import ServoKit
import pigpio
import read_PWM
#Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient
from time import ctime
kit = ServoKit(channels=16)
kit.continuous_servo[0].throttle = 0.03
PWM_GPIO = 4
RUN_TIME = 60
SAMPLE_TIME = .01
#pulse_width_generator = read_PWM_module.read_pwm_data(RUN_TIME, SAMPLE_TIME, PWM_GPIO)

#.015 throttle is min clockwise speed

#.083 throttle is min counter clockwise speed

# Example of using the MQTT client class to subscribe to a feed and print out
# any changes made to the feed.  Edit the variables below to configure the key,
# username, and feed to subscribe to for changes.


# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'redacted'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'redacted'

# Set to the ID of the feed to subscribe to for updates.
FEED_ID = 'redacted'

payload = "placeholder"


class MQTT:
    

    # Define callback functions which will be called when certain events happen.
    def connected(client):
        # Connected function will be called when the client is connected to Adafruit IO.
        # This is a good place to subscribe to feed changes.  The client parameter
        # passed to this function is the Adafruit IO MQTT client so you can make
        # calls against it easily.
        print('Connected to Adafruit IO!  Listening for {0} changes...'.format(FEED_ID))
        # Subscribe to changes on a feed named DemoFeed.
        client.subscribe(FEED_ID)

    def subscribe(client, userdata, mid, granted_qos):
        # This method is called when the client subscribes to a new feed.
        print('Subscribed to {0} with QoS {1}'.format(FEED_ID, granted_qos[0]))

    def disconnected(client):
        # Disconnected function will be called when the client disconnects.
        print('Disconnected from Adafruit IO!')
        sys.exit(1)

    def message(client, feed_id, payload):
        # Message function will be called when a subscribed feed has a new value.
        # The feed_id parameter identifies the feed, and the payload parameter has
        # the new value.
        print('Feed {0} received new value: {1}'.format(feed_id, payload))
        if payload == "Home":
            print("location is ", payload)
            self = read_PWM.reader.__init__
            pi = pigpio.pi()
            gpio = 4
            read_PWM.reader.pulse_width(self)
            
        else:
            print("Unknown location")

        #reader.pulse_width(self)
    #    if payload == "Home":
    #        target_pulse_width = 500
    #        print("location is ", payload)
    #        for pulse_width in pulse_width_generator:
    #            print(pulse_width)
    #            if pulse_width in range(490, 520):
    #               print("already in position")
    #               kit.continuous_servo[0].throttle = 0.03
    #               break
    #            else:
    #                break

    #        for pulse_width in pulse_width_generator:
    #            if pulse_width in range(520, 1200):
    #               print("moving clockwise...")
    #               #print(pulse_width)
    #               kit.continuous_servo[0].throttle = 0.15
    #               while True:
    #                   print(pulse_width)
    #                   if pulse_width >= target_pulse_width:
    #                       kit.continuous_servo[0].throttle = 0.03
    #                       break
    #            else: 
    #                break
           
    #        for pulse_width in pulse_width_generator:
    #            if pulse_width in range(0, 490):
    #               print("moving counter clockwise...")
    #               print(pulse_width)
    #               kit.continuous_servo[0].throttle = 0.083
    #               while True:
    #                   print(pulse_width)
    #                   if pulse_width <= target_pulse_width:
    #                         kit.continuous_servo[0].throttle = 0.03
    #                         break
    #            else:
    #                break

            
    #           #    while pulse_width >= target_pulse_width:
    #           #        print(pulse_width)
    #           #    kit.continuous_servo[0].throttle = 0.03
    #           #    print("done moving, new posistion is ", pulse_width)
    #           #elif pulse_width in range(0, 590):
    #           #    print("moving counter clockwise...")
    #           #    while pulse_width in range(610, 800):
    #           #         print(pulse_width)
    #           #         kit.continuous_servo[0].throttle = 0.083
    #           #    print("done moving, new posistion is ", pulse_width)
       
    #       #if read_PWM.p in range(590, 610):
    #       #    kit.continuous_servo[0].throttle = 0.03
    #       #    print("already in position ", pw)
    #       #elif read_PWM.p in range(0, 590):
    #       #    print("moving clockwise to ", pw)
    #       #elif read_PWM.p in range(610, 800):
    #       #     print("moving counterclockwise to ", pw)
    #    elif payload != "Home":
    #       print('location is ', payload)        
        

    ##        elif pw < 590:
    ##            print("pw is ", pw)
    ##            kit.continuous_servo[0].throttle = 0.015
    ##        elif pw > 610:
    ##            print("pw is ", pw)
    ##            kit.continuous_servo[0].throttle = 0.083

    # Create an MQTT client instance.
    client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    # Setup the callback functions defined above.
    client.on_connect    = connected
    client.on_disconnect = disconnected
    client.on_message    = message
    client.on_subscribe  = subscribe

    # Connect to the Adafruit IO server.
    client.connect()

    # Start a message loop that blocks forever waiting for MQTT messages to be
    # received.  Note there are other options for running the event loop like doing
    # so in a background thread--see the mqtt_client.py example to learn more.
    #client.loop_background()
    client.loop_blocking()
    
  


#self = read_PWM.__init__
#reader.__init__(self, pi, gpio, weighting=0.0)
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
MQTT.connected(client)
MQTT.message(client, FEED_ID, payload)
#MQTT.client.loop_background()
#MQTT.subscribe(client, userdata, mid, granted_qos)

print('test')