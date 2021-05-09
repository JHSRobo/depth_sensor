import ms5837
import rospy
import time
from std_msgs import Float32

if __name__ == "__main__":
    sensor = ms5837.MS5837()
    sensor.init()
    sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)

    rospy.init_node("depth_sensor")
    pub = rospy.Publisher('depth_sensor', Float32, queue_size=10)

    while not rospy.is_shutdown():
        sensor.read()
        pub.publish(sensor.depth())
        time.sleep(0.01)