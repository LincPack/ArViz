"""The purpose of this node is to take in either a mpv4 data file, or a link to the
camera device, and then process that data frame by frame, publishing the transformation
matrix for each of the tags that are detected in teh image. I should be able to duplicate
this node in order to run multiple cameras at once. """

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

