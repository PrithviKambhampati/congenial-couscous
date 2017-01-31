#!/usr/bin/env python
import rospy
import random
import sys
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time

def scan_callback(msg):
    global g_range_ahead
    g_range_ahead = min(msg.ranges)

def getTime(data):
    global last_time
    last_time = rospy.get_time()

if __name__ == "__main__":
    last_time=0.0
    g_range_ahead = 1.0
    try:
    	rospy.init_node("random_map")
    	rospy.Subscriber("/front/scan", LaserScan, scan_callback)
    	rate = rospy.Rate(50)
	pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    	while not rospy.is_shutdown():
    	    if g_range_ahead < 0.8:
		print g_range_ahead
    	        twist = Twist()
    	        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
    	        twist.angular.z = 0.5
		pub.publish(twist)
	    elif g_range_ahead >= 0.8:
		print g_range_ahead
		twist = Twist()
		twist.linear.x = 0.8
                twist.angular.z = 0 
		pub.publish(twist)
    	    rate.sleep()

    except rospy.ROSInterruptException:
	pass
