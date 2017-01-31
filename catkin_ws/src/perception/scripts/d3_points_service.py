#!/usr/bin/env python
import roslib; roslib.load_manifest('perception')
from perception.srv import *
from move_base_msgs.msg import MoveBaseGoal
import rospy
import tf
import math

def generate_d3_points(req):
    rospy.logdebug('Got a request')

    tf_list = tf.TransformListener()
    trans = None
    rot = None
    radius = 1
    dest = []

    while not (trans and rot):
        try:
            (trans, rot) = tf_list.lookupTransform('/map', '/base_link',
                                                   rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

    for i in xrange(0, req.points):
        pt = MoveBaseGoal()
        pt.target_pose.header.frame_id = 'map'

        pt.target_pose.pose.position.x = math.cos(2 * math.pi / req.points * i) * radius + trans[0]
        pt.target_pose.pose.position.y = math.sin(2 * math.pi / req.points * i) * radius + trans[1]
        pt.target_pose.pose.position.z = 0

        pt.target_pose.pose.orientation.x = 0
        pt.target_pose.pose.orientation.y = 0
        pt.target_pose.pose.orientation.z = 0
        pt.target_pose.pose.orientation.w = 1

        dest.append(pt)
    rospy.logdebug('Responding with: ', dest)
    return D3PointsResponse(destinations=dest)

def D3Points_server():
    rospy.init_node('d3_points_server')

    s = rospy.Service('d3_points', D3Points, generate_d3_points)
    rospy.loginfo("Ready to generate D3 points.")

    rospy.spin()

if __name__ == "__main__":
    D3Points_server()
