#! /usr/bin/env python
import rospy
import actionlib
from actionlib.msg import TestFeedback, TestResult, TestAction
from geometry_msgs.msg import Twist
import time


class QuadSquareActionServer(object):
    
  # create messages that are used to publish feedback/result
  _feedback = TestFeedback()
  _result   = TestResult()

  def __init__(self):
    # creates the action server
    self._as = actionlib.SimpleActionServer("quad_square_as", TestAction, self.goal_callback, False)
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
  
  def move_x_time(self, move_time, linearX, linearY):
    cmd = Twist()
    cmd.linear.x = linearX
    cmd.linear.y = linearY
    
    self.publish_once_in_cmd_vel(cmd)
    time.sleep(move_time)
    self.stop()
    
  def goal_callback(self, goal):
    # helper variables
    r = rospy.Rate(1)
    success = True
    
    square_size = goal.goal
    
    i = 0
    directions = [[1,0],
                  [0,1],
                  [-1,0],
                  [0,-1]]
    #preemptive exit
    while i < 4:
      if self._as.is_preempt_requested():
        rospy.loginfo('The goal has been cancelled/preempted')
        # the following line, sets the client in preempted state (goal cancelled)
        self._as.set_preempted()
        success = False
        # we end the calculation of the Fibonacci sequence
        break
    
    
      # Move Forwards
      self.move_x_time(move_time=2.0*square_size, linearX=directions[i][0], linearY=directions[i][1])
      self.move_x_time(move_time=2.0*square_size, linearX=0, linearY=0)

      self._feedback.feedback = i
      self._as.publish_feedback(self._feedback)
      i += 1
      
    if success:
      self._result.result = success
      rospy.loginfo('Succeeded traveling in a square')
      self._as.set_succeeded(self._result)
    
      
if __name__ == '__main__':
  rospy.init_node('quad_square_as')
  QuadSquareActionServer()
  rospy.spin()