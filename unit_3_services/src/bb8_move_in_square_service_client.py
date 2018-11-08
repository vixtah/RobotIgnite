#! /usr/bin/env python

import rospy
from std_srvs.srv import Empty, EmptyResponse, EmptyRequest

rospy.init_node('move_square_service_client')
rospy.wait_for_service('/move_in_square_service')
move_in_square_service = rospy.ServiceProxy('/move_in_square_service', Empty)
kk = EmptyRequest()
result = move_in_square_service(kk)
print result