#!/usr/bin/env python3

import ms5837
import rospy
from std_msgs.msg import Float32

if __name__ == "__main__":
    rospy.init_node("depth_sensor")
    pub = rospy.Publisher('rov/depth_sensor', Float32, queue_size=10)
    rate = rospy.Rate(10)
    
    sensor = ms5837.MS5837()
    try:
      sensor.init()
    except IOError:
        rospy.logerr("depth_sensor.py: depth sensor not plugged in. will retry every second.")
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
        rate.sleep()
