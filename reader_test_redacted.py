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
FEED_ID = 'Location'

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
        # The feed_id parameter identifies the feed, and the payload parameter has
        # the new value.
        print('Feed {0} received new value: {1}'.format(feed_id, payload))
        import time
        import pigpio
        import read_PWM
        from datetime import datetime
        now = datetime.now()

        throttle_stop = 0.03
        throttle_cw = 0.083
        throttle_ccw = 0.01
        PWM_GPIO = 4
        RUN_TIME = 5
        SAMPLE_TIME = .05

        pi = pigpio.pi()

        p = read_PWM.reader(pi, PWM_GPIO)
        kit.continuous_servo[0].throttle = throttle_stop
        pw = p.pulse_width()
        print("pw={}".format(int(pw+0.5)))
        time.sleep(2)
        if payload == "Home":
            target = 730
            x = target - 25
            y = target + 25
            if (abs(target - pw)) > 367:
                kit.continuous_servo[0].throttle = throttle_ccw
                print(throttle_ccw)
                start = time.time()
                while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("pw={}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done at ", now)
            if (abs(target - pw)) < 367:
                kit.continuous_servo[0].throttle = throttle_cw
                print(throttle_cw)
                while (pw not in range(x, y)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("pw={}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done at ", now)                
        if payload == "Work":
            target = 370
            x = target - 25
            y = target + 25
            if (abs(target - pw)) > 367:     
                kit.continuous_servo[0].throttle = throttle_ccw
                print(throttle_ccw)
                while (pw not in range(x, y)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("pw={}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done at ", now)
            if (abs(target - pw)) < 367:
                kit.continuous_servo[0].throttle = throttle_cw
                print(throttle_cw)
                while (pw not in range(x, y)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("pw={}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done at ", now)     
        if payload == "Mortal Peril":
            target = 1090
            x = target - 25
            y = target + 25
            if (abs(target - pw)) > 367:
                kit.continuous_servo[0].throttle = throttle_ccw
                print(throttle_ccw)
                while (pw not in range(x, y)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("pw={}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done")
            if (abs(target - pw)) < 367:
                kit.continuous_servo[0].throttle = throttle_cw
                print(throttle_cw)
                while (pw not in range(x, y)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("pw={}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done at ", now)
        if "Distance: " in  payload:
            distance_away = payload.strip("Distance :")
            print(distance_away)
            #target = (distance_away)
            #target = 100 + math.log(distance_away)
            target = 100
            x = target - 25
            y = target + 25
            if (abs(target - pw)) > 367:
                kit.continuous_servo[0].throttle = throttle_ccw
                print(throttle_ccw)
                start = time.time()
                while ((pw not in range(x, y)) & ((time.time() - start) < RUN_TIME)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("pw={}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done at ", now)
            if (abs(target - pw)) < 367:
                kit.continuous_servo[0].throttle = throttle_cw
                print(throttle_cw)
                while (pw not in range(x, y)): 
                    time.sleep(SAMPLE_TIME)
                    pw = p.pulse_width()
                    print("pw={}".format(int(pw+0.5)))
                p.cancel()
                pi.stop()
                kit.continuous_servo[0].throttle = throttle_stop
                print("Done at ", now)                



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
      

#if __name__ == "__main__":
#
#   import time
#   import pigpio
#   import read_PWM
#
#   PWM_GPIO = 4
#   RUN_TIME = 10
#   SAMPLE_TIME = .1
#
#   pi = pigpio.pi()
#
#   p = read_PWM.reader(pi, PWM_GPIO)
#
#   start = time.time()
#   pw = 0
#   x = 700
#   y = 1000
#   if payload == "Home":
#       while (pw not in range(x, y)):
#          time.sleep(SAMPLE_TIME)
#          pw = p.pulse_width()
#         print("pw={}".format(int(pw+0.5)))
#
#       p.cancel()
#
#       pi.stop()

#for i in range(0, 10, 1):
#    throttle = 0.015
#    kit.continuous_servo[0].throttle = throttle
#    print(throttle)
#    time.sleep(2)
#    throttle = .083
#    kit.continuous_servo[0].throttle = throttle
#    print(throttle)
#    time.sleep(2)
#    i= i+1



kit.continuous_servo[0].throttle = 0.03
#for i in range(-400, 400, 1):
#    i /= 1000 
#    #kit.servo[0].actuation_range = 270
#    #kit.servo[1].actuation_range = 270
#    #kit.servo[2].actuation_range = 270
#    #kit.servo[3].actuation_range = 270
#    #kit.servo[0].set_pulse_width_range(1280, 1720)
#    print("i = ", i)
#    kit.continuous_servo[0].throttle = i
#    #kit.continuous_servo[1].throttle = 1
#    #kit.servo[2].angle = 270
#    #kit.servo[3].angle = 270
#    time.sleep(.01)
#    #kit.continuous_servo[0].throttle = -0.1
#    #kit.continuous_servo[1].throttle = -.1
#    #kit.servo[2].angle = 0
#    #kit.servo[3].angle = 0
#    #time.sleep(2)
#    #kit.continuous_servo[1].throttle = 0



#kit.continuous_servo[0].throttle = .03
##print "Hello"