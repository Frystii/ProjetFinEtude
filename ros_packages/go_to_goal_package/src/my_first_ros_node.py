#!/usr/bin/env python
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String
import actionlib
import json

FILE_PATH = "positions.json"

def load_positions_from_file():
    try:
        with open(FILE_PATH, "r") as f:
            positions = json.load(f)
            return positions
    except Exception as e:
         rospy.loginfo(e)

def send_goal(position):
    client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = position["x"]
    goal.target_pose.pose.position.y = position["y"]
    goal.target_pose.pose.position.z = position["z"]
    goal.target_pose.pose.orientation.x = position["qx"]
    goal.target_pose.pose.orientation.y = position["qy"]
    goal.target_pose.pose.orientation.z = position["qz"]
    goal.target_pose.pose.orientation.w = position["qw"]

    client.send_goal(goal)
    client.wait_for_result()

def position_callback(msg):
    global positions
    positions = load_positions_from_file()
    position_name = msg.data
    if position_name in positions:
        send_goal(positions[position_name])


if __name__ == "__main__":

    rospy.init_node('go_to_node')
    
    positions = load_positions_from_file()
    rospy.Subscriber('/go_to_position', String, position_callback)
    rospy.spin()
