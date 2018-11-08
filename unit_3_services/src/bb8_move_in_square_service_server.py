#! /usr/bin/env python

import rospy
from move_bb8 import MoveBB8
from std_srvs.srv import Empty, EmptyResponse # you import the service message python classes generated from Empty.srv.


def my_callback(request):
    print "My_callback has been called"
    x = MoveBB8()
    x.move_square()
    
    return EmptyResponse() # the service Response class, in this case EmptyResponse
    #return MyServiceResponse(len(request.words.split())) 

rospy.init_node('move_square_service_server') 
my_service = rospy.Service('/move_in_square_service', Empty , my_callback) # create the Service called my_service with the defined callback
rospy.spin() # mantain the service open.