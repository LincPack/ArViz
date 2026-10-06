import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped

class DataProcessingNode(Node):
    def __init__(self):

        super.__init__('data_processing_node')

        self.sub = self.create_subscription(PoseStamped, 'tag_pose', self.process_tagData_callback)


    def process_tagData_callback(self):
        pass




def main(args = None):
    rclpy.init(args=args)
    data_processing_node = DataProcessingNode
    rclpy.spin(data_processing_node)
    data_processing_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


