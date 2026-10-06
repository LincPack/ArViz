"""The purpose of this node is to take in either a mpv4 data file, or a link to the
camera device, and then process that data frame by frame, publishing the transformation
matrix for each of the tags that are detected in teh image. I should be able to duplicate
this node in order to run multiple cameras at once. From the command line, I should be able
to put in either the pathway to the mp4 file, or the camera device number and a pathway to
its calibration file."""


import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import cv2
import numpy as np
import scipy as sp
from scipy.spatial.transform import Rotation as rot

class CameraVisionNode(Node):
    def __init__(self):
        super().__init__('camera_vision_node')

        # The camera configuration file needs to be in a .npz format

        self.pub = self.create_publisher(PoseStamped, 'tag_pose', 10)

        self.declare_parameter('camera_config', 'ArViz/gopro_calibration.npz')
        self.declare_parameter('vid_source', '0')

        vid_source = self.get_parameter('vid_source').get_parameter_value().string_value

        if vid_source.isdigit():
            source = int(vid_source)
            self.get_logger.info("Obtaining video feed from a camera.")

        else:
            source = vid_source
            self.get_logger().info("Obtaining video feed from recording.")


        camera_config = np.load(self.get_parameter('camera_config').get_parameter_value().string_value)
        self.get_logger().info(f'Loading camera information from {camera_config}')

        self.camera_matrix = camera_config['mtx']
        self.camera_dist_coeffs = camera_config['dist']

        self.cam = cv2.VideoCapture(source)

        if not self.cam.isOpened():
            self.get_logger().error("Failed to open video source")

        fps = self.cam.get(cv2.CAP_PROP_FPS)
        if fps <=0 or fps > 200:
            fps = 30.0 # This could be the source of error in the future if I decide to do a high frame rate

        timer_period = 1.0/fps
        self.get_logger().info(f"Processing camera feed at {fps} fps.")

        self.timer = self.create_timer(timer_period, self.frame_process_callback)

        arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4x4_50)
        arucoParams = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.arucoDict, self.arucoParams)
        self.tag_size = 0.0194 ## Input tag length in m here

    def frame_process_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warn('No fram received, or end of file')
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = self.detector.detectMarkers(gray)

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            for markerCorners, markerID in zip(corners, ids):
                half = self.tag_size/2

                objectPoints = np.array([
                        [-half,  half, 0],
                        [ half,  half, 0],
                        [ half, -half, 0],
                        [-half, -half, 0]
                    ], dtype=np.float32)
                imagePoints = markerCorners.reshape(4,2)

                success, rvec, tvec = cv2.solvePnP(
                    objectPoints,
                    imagePoints,
                    self.camera_matrix,
                    self.camera_dist_coeffs,
                    flags=cv2.SOLVEPNP_IPPE_SQUARE
                )

                if success:
                    R, _ = cv2.Rodrigues(rvec)
                    rotation = rot.from_matrix(R)

                    quat = rotation.as_quat()

                #TODO publish all tags at once, not just one at a time

                    self.publish_tag_pose(markerID, quat, tvec.flatten())

        return
    def publish_tag_pose(self, idx, quat, tvec):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = f'tag_{idx}'
        msg.pose.position.x = tvec[0]
        msg.pose.position.y = tvec[1]
        msg.pose.position.z = tvec[2]

        msg.pose.quaternion.x = quat[0]
        msg.pose.quaternion.y = quat[1]
        msg.pose.quaternion.z = quat[2]
        msg.pose.quaternion.w = quat[3]

        self.pub.publish(msg)


def main(args = None):
    rclpy.init(args=args)
    camera_vision_node = CameraVisionNode
    rclpy.spin(camera_vision_node)
    camera_vision_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
