#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from std_msgs.msg import String
import json

positions = {}

current_pose = None

def pose_callback(msg):
    global current_pose
    current_pose = msg.pose.pose

def save_position_callback(msg):
    global positions, current_pose
    if current_pose is None:
        return

    position_name = msg.data
    
    positions[position_name] = {
        "x": current_pose.position.x,
        "y": current_pose.position.y,
        "z": current_pose.position.z,
        "qx": current_pose.orientation.x,
        "qy": current_pose.orientation.y,
        "qz": current_pose.orientation.z,
        "qw": current_pose.orientation.w
    }
    save_positions_to_file()

def save_positions_to_file():
    try:
        with open("positions.json", "w") as f:
            json.dump(positions, f, indent=4)
    except Exception as e:
        rospy.loginfo(e)


if __name__ == "__main__":

    rospy.init_node('save_positions_node')
    
    try:
        with open("positions.json", "r") as f:
           positions = json.load(f)
    except Exception as e:
        rospy.loginfo("ah")
    rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, pose_callback)
    rospy.Subscriber('/save_position', String, save_position_callback)
    rospy.spin()
