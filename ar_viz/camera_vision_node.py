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
from scipy.spatial.transform import Rotation as rot
import yaml
from custom_interfaces.msg import ArUcoArray, ArUcoDetection

class CameraVisionNode(Node):
    def __init__(self):
        super().__init__('camera_vision_node')

        # The camera configuration file needs to be in a .npz format

        self.pub = self.create_publisher(ArUcoArray, 'tag_pose_array', 10)
        

        self.declare_parameter('camera_config', 'ArViz/gopro_calibration.npz')
        self.declare_parameter('vid_source', '0')

        vid_source = self.get_parameter('vid_source').get_parameter_value().string_value


        if vid_source.isdigit():
            self.source = int(vid_source)
            self.get_logger().info("Obtaining video feed from a camera.")

        else:
            self.source = vid_source
            self.get_logger().info("Obtaining video feed from recording.")


        camera_config = np.load(self.get_parameter('camera_config').get_parameter_value().string_value)
        
        self.get_logger().info(f'Loading camera information from {camera_config}')

        self.camera_matrix = camera_config['mtx']
        self.camera_dist_coeffs = camera_config['dist']

        self.cam = cv2.VideoCapture(self.source)

        if not self.cam.isOpened():
            self.get_logger().error("Failed to open video source")

        fps = self.cam.get(cv2.CAP_PROP_FPS)
        if fps <=0 or fps > 200:
            fps = 30.0 # This could be the source of error in the future if I decide to do a high frame rate

        timer_period = 1.0/fps
        self.get_logger().info(f"Processing camera feed at {fps} fps.")

        self.timer = self.create_timer(timer_period, self.frame_process_callback) # This is the actual subscriber/publisher type thing

        arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        arucoParams = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
        self.tag_size = 0.0194 ## Input tag length in m here

    def frame_process_callback(self):
        ret, frame = self.cam.read()
        if not ret:
            self.get_logger().warn('No fram received, or end of file')
            self.cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = self.detector.detectMarkers(gray)

        

        if ids is not None:
            # cv2.aruco.drawDetectedMarkers(frame, corners, ids) # -- This may not be strictly necessary, especially if I am using RVIZ

            msg = ArUcoArray()
            # msg.header.frame_id = str(self.source)

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
                    tvec_flat = tvec.flatten()
                    rvec_flat = rvec.flatten()
                    R, _ = cv2.Rodrigues(rvec_flat)
                    rotation = rot.from_matrix(R)

                    quat = rotation.as_quat()

                    reprojected_points, _ = cv2.projectPoints(objectPoints, rvec_flat, tvec_flat, self.camera_matrix, self.camera_dist_coeffs)
                    reprojected_points = reprojected_points.reshape((4, 2))
            
                    # Compute the 2D Euclidean distance for each corner correctly
                    # As noted by users on the OpenCV Forums, do not treat it as a single high-dimensional vector;
                    # calculate the Euclidean distance per corner and then take the average.
                    errors = np.linalg.norm(imagePoints - reprojected_points, axis=1)
                    mean_reprojection_error = np.mean(errors)

                #TODO publish all tags at once, not just one at a time
                    tag = ArUcoDetection()
                    tag.id = int(markerID)
                    tag.reprojection_error = float(mean_reprojection_error)
            
                    tag.pose.position.x = float(tvec_flat[0])
                    tag.pose.position.y = float(tvec_flat[1])
                    tag.pose.position.z = float(tvec_flat[2])
            
                    tag.pose.orientation.x = float(quat[0])
                    tag.pose.orientation.y = float(quat[1])
                    tag.pose.orientation.z = float(quat[2])
                    tag.pose.orientation.w = float(quat[3])

                    msg.detections.append(tag)

            msg.header.stamp = self.get_clock().now().to_msg()
            self.pub.publish(msg)

        return
  


def main(args = None):
    rclpy.init(args=args)
    camera_vision_node = CameraVisionNode()
    rclpy.spin(camera_vision_node)
    camera_vision_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
