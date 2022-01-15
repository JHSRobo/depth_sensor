#!/usr/bin/env python

import ms5837
import rospy
import time
from std_msgs.msg import Float32

if __name__ == "__main__":
    rospy.init_node("depth_sensor")
    pub = rospy.Publisher('depth_sensor', Float32, queue_size=10)
    rate = rospy.Rate(10)
    
    sensor = ms5837.MS5837()
    try:
      sensor.init()
    except IOError:
        rospy.logerr("depth_sensor.py: depth sensor not plugged in")
    else:
        sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)

        while not rospy.is_shutdown():
            try:
                sensor.read()
                pub.publish(sensor.depth())
            except IOError:
                pass
            rate.sleep()
