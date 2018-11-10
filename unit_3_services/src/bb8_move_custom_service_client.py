#! /usr/bin/env python

import rospy
from unit_3_services.srv import BB8CustomServiceMessage, BB8CustomServiceMessageRequest

rospy.init_node('move_bb8_in_square_custom_client')
rospy.wait_for_service('/move_bb8_in_square_custom')
move_in_square_service = rospy.ServiceProxy('/move_bb8_in_square_custom', BB8CustomServiceMessage)
kk = BB8CustomServiceMessageRequest()
kk.side = 1
kk.repetitions = 2
result = move_in_square_service(kk)
print result