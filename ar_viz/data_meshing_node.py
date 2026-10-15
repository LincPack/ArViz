"""The goal of this node is to take in the number of cameras used in the detection, and then 
output a filter measurement of each node. Each ArUco tag would have its own kalman filter allowing
the system to combine two measurements based on the confidence of the measurement from the ArUco tags
"""

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PoseArray
from custom_interfaces.msg import ArUcoArray, ArUcoDetection
import rclpy 
import sys
from rclpy.node import Node
import numpy as np
import message_filters

# Somehow I need to figure out how to confligrate multiple
# camera's pose estimations for the aruco tag
# I think I need to create a kalman filter for each tag as it comes in. Then publish those to 

class DataMeshingNode(Node):
    def __init__(self):

        super().__init__('data_processing_node')

        self.filters = {}

        self.pub = self.create_publisher(PoseArray, 'tag_pose_array', 10)

        self.declare_parameter('num_cameras', 1)

        num_cameras = self.get_parameter('num_cameras').get_parameter_value().integer_value

        subscribers = [
            message_filters.Subscriber(self, ArUcoArray, f'tag_pose_array_{i}')
            for i in range(len(num_cameras))
        ]

        self.sync = message_filters.ApproximateTimeSynchronizer(
            subscribers,
            queue_size=10,
            slop= 0.001 # This may need to be changed. It is the allowable time difference between two combined video recordings
        )

        self.sync.registerCallback(self.callback)
        self.get_logger().info(f'Node initialized with {num_cameras} cameras')

    def callback(self, *msgs):
        """Extract cameras, then tags, and then id's. Maybe we make a list of """
        tag_list
        for tag in tag_list:
            if tag not in self.filters:
                self.filters[f'{tag}'] = KalmanFilter()
        pass

        # Create subscribers and kalman filters per tag detected dynamically

class KalmanFilter():
    def __init__(self, Q, R):
        pass
    def predict(self, u):
        pass
    def update(self, r):
        pass





def main(args = None):
    rclpy.init(args=args)
    data_meshing_node = DataMeshingNode()
    rclpy.spin(data_meshing_node)
    data_meshing_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


