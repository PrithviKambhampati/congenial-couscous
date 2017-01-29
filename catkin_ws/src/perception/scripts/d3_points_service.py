#!/usr/bin/env python
import roslib; roslib.load_manifest('perception')
from perception.srv import *
from geometry_msgs.msg import PoseStamped
import rospy
import tf
import math


def generate_d3_points(req):
    print('Got a request')

    tf_list = tf.TransformListener()
    trans = None
    rot = None
    radius = 1

    while not (trans and rot):
        try:
            (trans, rot) = tf_list.lookupTransform('/map', '/base_link',
                                                   rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

    dest = [PoseStamped()] * (req.points)
    for i, p in enumerate(dest):
        p.header.frame_id = '/base_link'
        p.header.stamp = rospy.Time.now()

        p.pose.position.x = math.cos(2 * math.pi / req.points * i) * radius
        p.pose.position.y = math.sin(2 * math.pi / req.points * i) * radius
        p.pose.position.z = 0

        p.pose.orientation.x = 0
        p.pose.orientation.y = 0
        p.pose.orientation.z = 0
        p.pose.orientation.w = 1

    return D3PointsResponse(destinations=dest)

def D3Points_server():
    rospy.init_node('d3_points_server')

    s = rospy.Service('d3_points', D3Points, generate_d3_points)
    print("Ready to generate D3 points.")

    rospy.spin()

if __name__ == "__main__":
    D3Points_server()
