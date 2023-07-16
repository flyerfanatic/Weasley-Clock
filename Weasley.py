# Example of using the MQTT client class to subscribe to a feed and print out
# any changes made to the feed.  Edit the variables below to configure the key,
# username, and feed to subscribe to for changes.

# Import standard python modules.
from cgi import print_arguments
from string import printable
import sys
from tkinter import CURRENT
import board
import time
from datetime import datetime

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

from time import ctime

kit = MotorKit(i2c=board.I2C())

kit.stepper1.release()
kit.stepper2.release()

current_position = 0
target_position = 0
delta = 0
current_position2 = 0
target_position2 = 0

#Home routine
print("Homing Stepper 1")
for i in range(650):
    kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
    time.sleep(.02)
    i=i+1
for i in range(650):
    kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
    time.sleep(.02)
    i=i+1
print("Done")
print("Homing Stepper 2")
for j in range(720):
    kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
    time.sleep(.02)
    j=j+1
for j in range(720):
    kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
    time.sleep(.02)
    j=j+1
print("Done")
kit.stepper1.release()
kit.stepper2.release()

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'redacted'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'redacted'

# Set to the ID of the feed to subscribe to for updates.
FEED_ID = 'redacted'


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
    global current_position
    global target_position
    global current_position2
    global target_position2
    global delta
    now = datetime.now()
    if payload == "Home":
        target_position=250
        print("current_position is ", current_position)
        print("target_position is ", target_position)
        delta=target_position-current_position
        current_position=target_position
        print("move distance is ", delta)
        print(now)
        if delta>0:
            print("Moving...")
            for i in range(abs(delta)):
             kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
             time.sleep(.02)
             i=i+1
        elif delta<0:
            print("Moving...")
            for i in range(abs(delta)):
             kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
             time.sleep(.02)
             i=i+1
        elif delta==0:
            print("target position is already current position")
        print("current position is ", current_position)
        kit.stepper1.release()
    elif payload == "Work":
        target_position=500
        print("current_position is ", current_position)
        print("target_position is ", target_position)
        delta=target_position-current_position
        current_position=target_position
        print("move distance is ", delta)
        print(now)
        if delta>0:
            print("Moving...")
            for i in range(abs(delta)):
             kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
             time.sleep(.02)
             i=i+1
        elif delta<0:
            print("Moving...")
            for i in range(abs(delta)):
             kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
             time.sleep(.02)
             i=i+1
        elif delta==0:
            print("target position is already current position")
        print("current position is ", current_position)
    elif payload == "Out":
        target_position=125
        print("current_position is ", current_position)
        print("target_position is ", target_position)
        delta=target_position-current_position
        current_position=target_position
        print("move distance is ", delta)
        print(now)
        if delta>0:
            print("Moving...")
            for i in range(abs(delta)):
             kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
             time.sleep(.02)
             i=i+1
        elif delta<0:
            print("Moving...")
            for i in range(abs(delta)):
             kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
             time.sleep(.02)
             i=i+1
        elif delta==0:
            print("target position is already current position")
        print("current position is ", current_position)
    elif payload == "Alexa Home":
        target_position2=250
        print("current position 2 is ", current_position2)
        print("target position 2 is ", target_position2)
        delta=target_position2-current_position2
        current_position2=target_position2
        print("move distance is ", delta)
        print(now)
        if delta>0:
            print("Moving...")
            for i in range(abs(delta)):
             kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
             time.sleep(.02)
             i=i+1
        elif delta<0:
            print("Moving...")
            for i in range(abs(delta)):
             kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
             time.sleep(.02)
             i=i+1
        elif delta==0:
            print("target position is already current position")
        print("current position 2 is ", current_position2)
        kit.stepper1.release()
    elif payload == "Alexa Work":
        target_position2=500
        print("current position 2 is ", current_position2)
        print("target position 2 is ", target_position2)
        delta=target_position2-current_position2
        current_position2=target_position2
        print("move distance is ", delta)
        print(now)
        if delta>0:
            print("Moving...")
            for i in range(abs(delta)):
             kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
             time.sleep(.02)
             i=i+1
        elif delta<0:
            print("Moving...")
            for i in range(abs(delta)):
             kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
             time.sleep(.02)
             i=i+1
        elif delta==0:
            print("target position is already current position")
        print("current position 2 is ", current_position2)
    elif payload == "Alexa Out":
        target_position2=125
        print("current position 2 is ", current_position2)
        print("target position 2 is ", target_position2)
        delta=target_position2-current_position2
        current_position2=target_position2
        print("move distance is ", delta)
        print(now)
        if delta>0:
            print("Moving...")
            for i in range(abs(delta)):
             kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
             time.sleep(.02)
             i=i+1
        elif delta<0:
            print("Moving...")
            for i in range(abs(delta)):
             kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
             time.sleep(.02)
             i=i+1
        elif delta==0:
            print("target position is already current position")
        print("current position 2 is ", current_position2)
            

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
client.loop_blocking()
