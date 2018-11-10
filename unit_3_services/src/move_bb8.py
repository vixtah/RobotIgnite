#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import time

class MoveBB8:
    
    def __init__(self):
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.ctrl_c = False
        rospy.on_shutdown(self.shutdownhook)
        self.rate = rospy.Rate(10)
        
        print("inited")
        
        
    def shutdownhook(self): 
        self.stop()
        self.ctrl_c = True
        
    def stop(self):
        cmd = Twist()
        cmd.linear.x = 0
        cmd.angular.z = 0
        self.publish_once_in_cmd_vel(cmd)
    
    def publish_once_in_cmd_vel(self, cmd):
        while not self.ctrl_c:
            connections = self.vel_pub.get_num_connections()
            if connections > 0:
                self.vel_pub.publish(cmd)
                print("cmd published")
                break
            else:
                self.rate.sleep()
    
    def move_x_time(self, move_time, linear, angular):
        cmd = Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular
        
        self.publish_once_in_cmd_vel(cmd)
        time.sleep(move_time)
        self.stop()
        
    def move_square(self, side = 1, repetitions = 1):
        k = 0
        while not self.ctrl_c and k < repetitions:
            k += 1
            i = 0
            while not self.ctrl_c and i < 4:
                i += 1
                # Move Forwards
                self.move_x_time(move_time=2.0*side, linear=0.2, angular=0.0)
                # Stop
                self.move_x_time(move_time=4.0, linear=0.0, angular=0.0)
                # Turn 
                self.move_x_time(move_time=3.5, linear=0.0, angular=0.2)
                # linear
                self.move_x_time(move_time=0.1*side, linear=0.0, angular=0.0)
           
        
    
        
print("imported")

if __name__ == '__main__':
    print("hi")
    rospy.init_node('move_bb8_test', anonymous=True)
    movebb8 = MoveBB8()
    try:
        movebb8.move_square()
    except rospy.ROSInterruptException:
        pass