"""The goal of this node is to take in the number of cameras used in the detection, and then 
output a filter measurement of each node. Each ArUco tag would have its own kalman filter allowing
the system to combine two measurements based on the confidence of the measurement from the ArUco tags
"""

from geometry_msgs.msg import PoseStamped
from custom_interfaces import ArUcoArray, ArUcoDetection
import rclpy 
import sys
from rclpy.node import Node
import yaml

# Somehow I need to figure out how to confligrate multiple
# camera's pose estimations for the aruco tag

class DataMeshingNode(Node):
    def __init__(self):

        super().__init__('data_processing_node')

        self.sub = self.create_subscription(ArUcoArray, 'tag_pose_array', self.process_tagData_callback)


    def process_tagData_callback(self):
        pass




def main(args = None):
    rclpy.init(args=args)
    data_meshing_node = DataMeshingNode()
    rclpy.spin(data_meshing_node)
    data_meshing_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


