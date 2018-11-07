#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

rospy.init_node('avoid_wall')
pub = rospy.Publisher('/cmd_vel', Twist)

# rate = rospy.Rate(2)
twist = Twist()
twist.linear.x = 1


# while not rospy.is_shutdown():
#     print("hi")
#     pub.publish(twist)
#     rate.sleep()
    
    
    


    
def calcZ(avg):
    return (avg - 650)/30
    
def callback(msg): 
    ranges = msg.ranges
    weightedSum = 0
    totalWeights = 0
    for i, range in enumerate(ranges):
        if range < 3.0:
            weightedSum += i*range
            totalWeights += range
    weightedAvg = weightedSum / totalWeights
    twist.angular.z = calcZ(weightedAvg)
    print(weightedAvg, twist.angular.z)
    
    pub.publish(twist)
    
  
  
    
sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, callback)
rospy.spin()