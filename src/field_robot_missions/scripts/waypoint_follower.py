#!/usr/bin/env python
import rospy, actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
def send_goal(cli,x,y,yaw,frame="map"):
    q = quaternion_from_euler(0,0,yaw)
    g = MoveBaseGoal()
    g.target_pose.header.frame_id = frame
    g.target_pose.header.stamp    = rospy.Time.now()
    g.target_pose.pose.position.x = x
    g.target_pose.pose.position.y = y
    g.target_pose.pose.orientation.x, g.target_pose.pose.orientation.y, g.target_pose.pose.orientation.z, g.target_pose.pose.orientation.w = q
    cli.send_goal(g); cli.wait_for_result()
if __name__ == "__main__":
    rospy.init_node("waypoint_follower")
    wps = rospy.get_param("~waypoints", [])
    cli = actionlib.SimpleActionClient("move_base", MoveBaseAction)
    rospy.loginfo("Waiting for move_base..."); cli.wait_for_server()
    for wp in wps: send_goal(cli, wp["x"], wp["y"], wp["yaw"])
    rospy.loginfo("Mission complete.")
