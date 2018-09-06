#! /usr/bin/env python

import sys, rospy, tf, actionlib, moveit_comamnder
from constrom_msgs.msg import (GripperCommandAction, GripperCommandGoal)
from geometry_msgs.msg import *
from tf.transformations import quaternion_from_euler
from look_at_bin import look_at_bin
from std_srvs.srv import Empty
from moveit_msgs.msg import CollisionObject
from moveit_python import PlanningSceneInterface

if __name__ == '__main__':
	moveit_commander.roscpp_initialize(sys.argv)
	rospy.init_node('pick_up_item')
	args = rospy.myargv(argv = sys.argv)
	if len(args) != 2:
		print("usage: pick_up_item.py BIN_NUMBER")
		sys.exit(1)
	item_frame = "item_%d" % int(args[1])

	rospy.wait_for_service("/clear_octomap")
	clear_octomap = rospy.ServiceProxy("/clear_octomap", Empty)

	gripper = actionlib.SimpleActionClient("gripper_controller/gripper_action", 
		GripperCommandAction)
	gripper.wait_for_server()

	arm = moveit_commander.MoveGroupCommander("arm")
	arm.allow_replanning(True)
	tf_listener = tf.TransformListener()
	rate = rospy.Rate(10)
	
