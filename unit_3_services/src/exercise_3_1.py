#! /usr/bin/env python

import rospy
from iri_wam_reproduce_trajectory.srv import ExecTraj, ExecTrajRequest
import rospkg

rospack = rospkg.RosPack()

rospy.init_node('service_client')
rospy.wait_for_service('/execute_trajectory')
execute_trajectory_service = rospy.ServiceProxy('/execute_trajectory', ExecTraj)
kk = ExecTrajRequest()
kk.file = rospack.get_path('iri_wam_reproduce_trajectory') + "/config/get_food.txt"
result = execute_trajectory_service(kk)
print result