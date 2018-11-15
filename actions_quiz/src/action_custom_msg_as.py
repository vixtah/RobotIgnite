#! /usr/bin/env python
import rospy
import actionlib
# from actionlib.msg import TestFeedback, TestResult, TestAction
from actions_quiz.msg import CustomActionMsgAction, CustomActionMsgActionFeedback
from geometry_msgs.msg import Twist
import time


class QuadSquareActionServer(object):
    
  # create messages that are used to publish feedback/result
  _feedback = CustomActionMsgActionFeedback()
#   _result   = TestResult()

  def __init__(self):
    # creates the action server
    self._as = actionlib.SimpleActionServer("action_custom_msg_as", CustomActionMsgAction, self.goal_callback, False)
    self._as.start()
    
    self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    self.rate = rospy.Rate(10)
    
  def publish_once_in_cmd_vel(self, cmd):
    # while not self.ctrl_c:
    while 1:
        connections = self.vel_pub.get_num_connections()
        if connections > 0:
            self.vel_pub.publish(cmd)
            print("cmd published")
            break
        else:
            self.rate.sleep()
  
  def stop(self):
    cmd = Twist()
    cmd.linear.x = 0
    cmd.angular.z = 0
    self.publish_once_in_cmd_vel(cmd)
  
  def move_x_time(self, move_time, linearZ):
    cmd = Twist()
    cmd.linear.z = linearZ
    
    self.publish_once_in_cmd_vel(cmd)
    time.sleep(move_time)
    self.stop()
    
  def goal_callback(self, goal):
    # helper variables
    r = rospy.Rate(1)
    success = True
    
    direction = goal.direction.data
    print(direction=="UP")
    #preemptive exit
    if direction == "UP":
        self.move_x_time(move_time=2.0, linearZ=1)
        self.move_x_time(move_time=.1, linearZ=0)
        self._feedback.feedback.cur_direction.data = "Going up"

    elif direction == "DOWN":
        self.move_x_time(move_time=2.0, linearZ=-1)
        self.move_x_time(move_time=.1, linearZ=0)
        self._feedback.feedback.cur_direction.data = "Going down"

    self._as.publish_feedback(self._feedback)
    
      
if __name__ == '__main__':
  rospy.init_node('quad_square_as')
  QuadSquareActionServer()
  rospy.spin()