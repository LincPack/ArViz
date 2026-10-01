"""The purpose of this node is to take in either a mpv4 data file, or a link to the
camera device, and then process that data frame by frame, publishing the transformation
matrix for each of the tags that are detected in teh image. I should be able to duplicate
this node in order to run multiple cameras at once. From the command line, I should be able
to put in either the pathway to the mp4 file, or the camera device number and a pathway to
its calibration file."""


import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from geometry_msgs.msg import PoseStamped
import cv2
import numpy as np

class CameraVisionNode(Node):
    def __init__(self):
        super().__init__('camera_vision_node')

        # I need to input a bit of code to get a command line input for the camera configuration file
        # The camera configuration file needs to be in a .npz format

        self.pub = self.create_publisher(PoseStamped, 'tag_pose', 10)

        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4x4_50)
        self.arucoParams = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(self.arucoDict, self.arucoParams)




    def publish_tag_pose(self, idx, tag_pose):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = f'tag_{idx}'
        msg.pose.position.x = 
        msg.pose.position.y = 
        msg.pose.position.z = 

        msg.pose.quaternion.x = 
        msg.pose.quaternion.y = 
        msg.pose.quaternion.z = 
        msg.pose.quaternion.w = 

        self.pub.publish(msg)


def main(args = None):
    rclpy.init(args=args)
    camera_vision_node = CameraVisionNode
    rclpy.spin(camera_vision_node)
    camera_vision_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
