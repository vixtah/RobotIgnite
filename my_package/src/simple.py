#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

rospy.init_node('ObiWan')
pub = rospy.Publisher('/cmd_vel', Twist)

rate = rospy.Rate(2)
twist = Twist()
twist.linear.x = 2


while not rospy.is_shutdown():
    pub.publish(twist)
    rate.sleep()