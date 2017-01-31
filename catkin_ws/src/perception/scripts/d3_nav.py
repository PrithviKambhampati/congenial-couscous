#!/usr/bin/env python
import rospy
import actionlib
import random
from perception.srv import *
from move_base_msgs.msg	import MoveBaseAction

def D3Points_nav():
    rospy.init_node('d3_nav')

    DestSrv = rospy.ServiceProxy('d3_points', D3Points)
    mvbs = actionlib.SimpleActionClient('move_base', MoveBaseAction)

    mvbs.wait_for_server()
    rospy.loginfo("D3 Nav ready.")

    while not rospy.is_shutdown():
        dest = random.choice(DestSrv(8, 1.5).destinations)
        rospy.loginfo(dest)

        mvbs.send_goal(dest)
        mvbs.wait_for_result()
        rospy.loginfo("Nav goal met, setting another one...")

if __name__ == "__main__":
    D3Points_nav()
