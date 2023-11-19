#SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for a standard servo on channel 0 and a continuous rotation servo on channel 1."""
import time
import pigpio
from adafruit_servokit import ServoKit
from Adafruit_IO import MQTTClient
import read_PWM
import sys
import math
kit = ServoKit(channels=16)

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
kit.continuous_servo[0].throttle = 0.03

# Example of using the MQTT client class to subscribe to a feed and print out
# any changes made to the feed.  Edit the variables below to configure the key,
# username, and feed to subscribe to for changes.

# Import standard python modules.
#import sys

# Import Adafruit IO MQTT client.
#from Adafruit_IO import MQTTClient

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'redacted'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'redacted'

# Set to the ID of the feed to subscribe to for updates.
FEED_ID = 'redacted'

class reader:
   """
   A class to read PWM pulses and calculate their frequency
   and duty cycle.  The frequency is how often the pulse
   happens per second.  The duty cycle is the percentage of
   pulse high time per cycle.
   """
   def __init__(self, pi, gpio, weighting=0.0):
      """
      Instantiate with the Pi and gpio of the PWM signal
      to monitor.

      Optionally a weighting may be specified.  This is a number
      between 0 and 1 and indicates how much the old reading
      affects the new reading.  It defaults to 0 which means
      the old reading has no effect.  This may be used to
      smooth the data.
      """
      self.pi = pi
      self.gpio = gpio

      if weighting < 0.0:
         weighting = 0.0
      elif weighting > 0.99:
         weighting = 0.99

      self._new = 1.0 - weighting # Weighting for new reading.
      self._old = weighting       # Weighting for old reading.

      self._high_tick = None
      self._period = None
      self._high = None

      pi.set_mode(gpio, pigpio.INPUT)

      self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)

  
   def pulse_width(self):
      """
      Returns the PWM pulse width in microseconds.
      """
      if self._high is not None:
         return self._high
      else:
         return 0.0
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
        # The feed_id parameter identifies the feed, and the payload parameter has the new value.
        print('Feed {0} received new value: {1}'.format(feed_id, payload))
        import time
        import pigpio
        import read_PWM
        from datetime import datetime
        
        now = datetime.now()
        print(now)
        throttle_stop = 0.03 #experimentally derived 0 speed throttle value
        throttle_cw = 0.083 #experimentally derived minimum clockwise throttle value
        throttle_ccw = 0.01 #experimentally derived minimum counter clockwise throttle value


        pi = pigpio.pi()
       
        target_home = 350 #set location of home
        target_work = 700 #set location of work
        target_mortalperil = 1050 #set location of mortal peril
        target_test = 100 #set location of test


        
        if payload == "Home": #move routine for Home location
            PWM_GPIO = 4 #set GPIO pin that PWM output is connected to
            RUN_TIME = 15 #set run time of PWM monitoring
            SAMPLE_TIME = .05 #set time between PWM value reporting
            p = read_PWM.reader(pi, PWM_GPIO)
            kit.continuous_servo[0].throttle = throttle_stop #command 0 speed throttle value
            pw = p.pulse_width() #get initial PWM value//location
            print("pw={}".format(int(pw + 0.5)))
            time.sleep(2) #grabbing current position takes a second or two, no sleep time results in PWM reporting a value of 0
            print("Start move at ", now)
            delta = int(pw - target_home + 1100)
            x = target_home - 25
            y = target_home + 25
            move_distance = delta - 1100
            print("delta = ", delta)
            print("move distance is ", move_distance)
            if delta > 1100:
                kit.continuous_servo[0].throttle = throttle_cw
                print("throttle is ", throttle_cw)
                start = time.time()
                while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("current position = {}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                now = datetime.now()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done move at ", now)
            if delta < 1100:
                kit.continuous_servo[0].throttle = throttle_ccw
                print("throttle is ", throttle_ccw)
                start = time.time()
                while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("current position = {}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                now = datetime.now()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done move at ", now)
        if payload == "Work":
            PWM_GPIO = 4 #set GPIO pin that PWM output is connected to
            RUN_TIME = 15 #set run time of PWM monitoring
            SAMPLE_TIME = .05 #set time between PWM value reporting
            p = read_PWM.reader(pi, PWM_GPIO)
            kit.continuous_servo[0].throttle = throttle_stop #command 0 speed throttle value
            pw = p.pulse_width() #get initial PWM value//location
            print("pw={}".format(int(pw + 0.5)))
            time.sleep(2) #grabbing current position takes a second or two, no sleep time results in PWM reporting a value of 0
            print("Start move at ", now)
            delta = int(pw - target_work + 1100)
            x = target_work - 25
            y = target_work + 25
            move_distance = delta - 1100
            print("delta = ", delta)
            print("move distance is ", move_distance)
            if delta > 1100:
                kit.continuous_servo[0].throttle = throttle_cw
                print("throttle is ", throttle_cw)
                start = time.time()
                while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("current position = {}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                now = datetime.now()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done move at ", now)
            if delta < 1100:
                kit.continuous_servo[0].throttle = throttle_ccw
                print("throttle is ", throttle_ccw)
                start = time.time()
                while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("current position = {}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                now = datetime.now()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done move at ", now)        
        if payload == "Mortal Peril":
            PWM_GPIO = 4 #set GPIO pin that PWM output is connected to
            RUN_TIME = 15 #set run time of PWM monitoring
            SAMPLE_TIME = .05 #set time between PWM value reporting
            p = read_PWM.reader(pi, PWM_GPIO)
            kit.continuous_servo[0].throttle = throttle_stop #command 0 speed throttle value
            pw = p.pulse_width() #get initial PWM value//location
            print("pw={}".format(int(pw + 0.5)))
            time.sleep(2) #grabbing current position takes a second or two, no sleep time results in PWM reporting a value of 0
            print("Start move at ", now)
            delta = int(pw - target_mortalperil + 1100)
            x = target_mortalperil - 25
            y = target_mortalperil + 25
            move_distance = delta - 1100
            print("delta = ", delta)
            print("move distance is ", move_distance)
            if delta > 1100:
                kit.continuous_servo[0].throttle = throttle_cw
                print("throttle is ", throttle_cw)
                start = time.time()
                while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("current position = {}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                now = datetime.now()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done move at ", now)
            if delta < 1100:
                kit.continuous_servo[0].throttle = throttle_ccw
                print("throttle is ", throttle_ccw)
                start = time.time()
                while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("current position = {}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                now = datetime.now()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done move at ", now)
        if payload == "Test":
            PWM_GPIO = 4 #set GPIO pin that PWM output is connected to
            RUN_TIME = 15 #set run time of PWM monitoring
            SAMPLE_TIME = .05 #set time between PWM value reporting
            p = read_PWM.reader(pi, PWM_GPIO)
            kit.continuous_servo[0].throttle = throttle_stop #command 0 speed throttle value
            pw = p.pulse_width() #get initial PWM value//location
            print("pw={}".format(int(pw + 0.5)))
            time.sleep(2) #grabbing current position takes a second or two, no sleep time results in PWM reporting a value of 0
            print("Start move at ", now)
            delta = int(pw - target_test + 1100)
            x = target_test - 25
            y = target_test + 25
            move_distance = delta - 1100
            print("delta = ", delta)
            print("move distance is ", move_distance)
            if delta > 1100:
                kit.continuous_servo[0].throttle = throttle_cw
                print("throttle is ", throttle_cw)
                start = time.time()
                while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("current position = {}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                now = datetime.now()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done move at ", now)
            if delta < 1100:
                kit.continuous_servo[0].throttle = throttle_ccw
                print("throttle is ", throttle_ccw)
                start = time.time()
                while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("current position = {}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                now = datetime.now()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done move at ", now) 
        if payload == "Alexa Home": #move routine for Home location
            PWM_GPIO = 5 #set GPIO pin that PWM output is connected to
            RUN_TIME = 15 #set run time of PWM monitoring
            SAMPLE_TIME = .05 #set time between PWM value reporting
            p = read_PWM.reader(pi, PWM_GPIO)
            kit.continuous_servo[2].throttle = throttle_stop #command 0 speed throttle value
            pw = p.pulse_width() #get initial PWM value//location
            print("pw={}".format(int(pw + 0.5)))
            time.sleep(2) #grabbing current position takes a second or two, no sleep time results in PWM reporting a value of 0
            print("Start move at ", now)
            delta = int(pw - target_home + 1100)
            x = target_home - 25
            y = target_home + 25
            move_distance = delta - 1100
            print("delta = ", delta)
            print("move distance is ", move_distance)
            if delta > 1100:
                kit.continuous_servo[2].throttle = throttle_cw
                print("throttle is ", throttle_cw)
                start = time.time()
                while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("current position = {}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                now = datetime.now()
                kit.continuous_servo[2].throttle = throttle_stop
                print("Done move at ", now)
            if delta < 1100:
                kit.continuous_servo[2].throttle = throttle_ccw
                print("throttle is ", throttle_ccw)
                start = time.time()
                while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("current position = {}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                now = datetime.now()
                kit.continuous_servo[2].throttle = throttle_stop
                print("Done move at ", now)
        if payload == "Alexa Work": #move routine for Work location
            PWM_GPIO = 5 #set GPIO pin that PWM output is connected to
            RUN_TIME = 15 #set run time of PWM monitoring
            SAMPLE_TIME = .05 #set time between PWM value reporting
            p = read_PWM.reader(pi, PWM_GPIO)
            kit.continuous_servo[2].throttle = throttle_stop #command 0 speed throttle value
            pw = p.pulse_width() #get initial PWM value//location
            print("pw={}".format(int(pw + 0.5)))
            time.sleep(2) #grabbing current position takes a second or two, no sleep time results in PWM reporting a value of 0
            print("Start move at ", now)
            delta = int(pw - target_work + 1100)
            x = target_work - 25
            y = target_work + 25
            move_distance = delta - 1100
            print("delta = ", delta)
            print("move distance is ", move_distance)
            if delta > 1100:
                kit.continuous_servo[2].throttle = throttle_cw
                print("throttle is ", throttle_cw)
                start = time.time()
                while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("current position = {}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                now = datetime.now()
                kit.continuous_servo[2].throttle = throttle_stop
                print("Done move at ", now)
            if delta < 1100:
                kit.continuous_servo[2].throttle = throttle_ccw
                print("throttle is ", throttle_ccw)
                start = time.time()
                while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("current position = {}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                now = datetime.now()
                kit.continuous_servo[2].throttle = throttle_stop
                print("Done move at ", now)
       
        # if "Distance: " in  payload:
        #     distance_away = payload.strip("Distance :")
        #     print(distance_away)
        #     #target = (distance_away)
        #     #target = 100 + math.log(distance_away)
        #     print("Start move at ", now)
        #     delta = pw - target_out + 1100
        #     x = delta - 25
        #     y = delta + 25
        #     if delta > 550:
        #         kit.continuous_servo[0].throttle = throttle_ccw
        #         print(throttle_ccw)
        #         start = time.time()
        #         while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
        #             time.sleep(SAMPLE_TIME)
        #             pw = p.pulse_width()
        #             print("current position = {}".format(int(pw+0.5)))
        #         p.cancel()
        #         pi.stop()
        #         kit.continuous_servo[0].throttle = throttle_stop
        #         print("Done move at ", now)
        #     if delta < 550:
        #         kit.continuous_servo[0].throttle = throttle_cw
        #         print(throttle_cw)
        #         start = time.time()
        #         while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
        #             time.sleep(SAMPLE_TIME)
        #             pw = p.pulse_width()
        #             print("current position = {}".format(int(pw+0.5)))
        #         p.cancel()
        #         pi.stop()
        #         kit.continuous_servo[0].throttle = throttle_stop
        #         print("Done move at ", now)             



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
   #client.loop_background()

kit.continuous_servo[0].throttle = 0.03
