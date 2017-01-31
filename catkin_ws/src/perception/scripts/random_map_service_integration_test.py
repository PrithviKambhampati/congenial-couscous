#!/usr/bin/env python
import rospy
import random
import sys
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from perception.srv import *
import time
import actionlib
from move_base_msgs.msg	import MoveBaseAction, MoveBaseGoal

def scan_callback(msg):
    global g_range_ahead
    g_range_ahead = min(msg.ranges)

def getTime(data):
    global last_time
    last_time = rospy.get_time()

def get_d3_points():
    rospy.wait_for_service('d3_points')
    try:
        get_d3_points = rospy.ServiceProxy('d3_points', D3Points)
        dest = get_d3_points(3)
        return dest.points
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def set_goal_pose(pose):
    goal_pose = MoveBaseGoal()
    goal_pose.target_pose = random.choice(pose)
    return goal_pose

if __name__ == "__main__":
    try:
        last_time=0.0
        g_range_ahead = 1.0
        rospy.init_node("random_map")
        dest = get_d3_points()
        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        #client.wait_for_server()
        rospy.Subscriber("/front/scan", LaserScan, scan_callback)
    	rate = rospy.Rate(50)
        pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        while not rospy.is_shutdown():
            if g_range_ahead >= 0.8:
                print g_range_ahead
    	        twist = Twist()
    	        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
    	        twist.angular.z = 0.5
                pub.publish(twist)
            elif g_range_ahead < 0.8:
                print g_range_ahead
                # twist = Twist()
                # twist.linear.x = 0.8; twist.linear.y = 0; twist.linear.z = 0
                # twist.angular.z = 0
                # pub.publish(twist)
                goal_dest = set_goal_pose(dest)
                client.send_goal(goal_dest)
                client.wait_for_result()
                rate.sleep()
    except rospy.ROSInterruptException:
        pass
