#!/usr/bin/env python3

import ms5837
import rospy
from std_msgs.msg import Float32, Bool

if __name__ == "__main__":
    rospy.init_node("depth_sensor")

    # Set up leak detection pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(27, GPIO.IN)

    pub = rospy.Publisher('rov/depth_sensor', Float32, queue_size=10)
    leak_pub = rospy.Publisher('leak_detect', Bool, queue_size=10)
    rate = rospy.Rate(10)
    
    sensor = ms5837.MS5837()
    try:
      sensor.init()
    except IOError:
        rospy.logwarn("Cannot connect to depth sensor. Ignore this if the sensor is unplugged.")
        connected = False
        while not connected:
            try:
                sensor.init()
            except IOError:
                pass
            else:
                connected = True
            finally:
                rospy.sleep(1)
  
    sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)


    while not rospy.is_shutdown():
        try:
            sensor.read()
            pub.publish(sensor.depth())
        except IOError:
            pass
        if GPIO.input(27):
            leak_pub.publish(GPIO.input(27))
        rate.sleep()
