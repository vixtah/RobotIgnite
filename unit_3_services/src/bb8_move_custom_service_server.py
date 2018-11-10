#! /usr/bin/env python

import rospy
from move_bb8 import MoveBB8

from unit_3_services.srv import BB8CustomServiceMessage, BB8CustomServiceMessageRequest, BB8CustomServiceMessageResponse

def my_callback(request):
    print "My_callback has been called"
    
    x = MoveBB8()
    x.move_square(request.side, request.repetitions)
    
    response = BB8CustomServiceMessageResponse()
    response.success = True 
    
    return response # the service Response class, in this case EmptyResponse
    #return MyServiceResponse(len(request.words.split())) 

rospy.init_node('move_bb8_in_square_custom') 
my_service = rospy.Service('/move_bb8_in_square_custom', BB8CustomServiceMessage , my_callback) # create the Service called my_service with the defined callback
rospy.spin() # mantain the service open.