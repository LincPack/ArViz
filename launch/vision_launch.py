from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        
        # --- LEFT CAMERA NODE ---
        Node(
            package='your_package_name',       # <-- Replace with your ROS2 package name
            executable='your_executable_name', # <-- Replace with your node's setup.py/CMake entry
            name='camera_vision_node',
            namespace='left_camera',           # <-- Automatically prefixes topics with /left_camera/
            parameters=[{
                'vid_source': '0',
                'camera_config': 'ArViz/left_gopro.npz',
                'camera_frame_id': 'left_camera_optical_frame'
            }],
            output='screen'
        ),

        # --- RIGHT CAMERA NODE ---
        Node(
            package='your_package_name',       # <-- Replace with your ROS2 package name
            executable='your_executable_name', # <-- Replace with your node's setup.py/CMake entry
            name='camera_vision_node',
            namespace='right_camera',          # <-- Automatically prefixes topics with /right_camera/
            parameters=[{
                'vid_source': '2',
                'camera_config': 'ArViz/right_gopro.npz',
                'camera_frame_id': 'right_camera_optical_frame'
            }],
            output='screen'
        )
        
    ])
