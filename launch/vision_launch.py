from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Define camera configs outside LaunchDescription
    cameras = [
        {
            'vid_source': '/dev/video42',
            'camera_config': 'ArViz/left_gopro.npz',
            'index': 0
        },
        {
            'vid_source': '/dev/video43',
            'camera_config': 'ArViz/right_gopro.npz',
            'index': 1
        },
    ]

    nodes = [
        Node(
            package='ar_viz',
            executable='camera_vision_node',  # this is the entry point name from setup.py, not setup.py itself
            name=f'camera_vision_node_{cam["index"]}',
            parameters=[{
                'vid_source': cam['vid_source'],
                'camera_config': cam['camera_config'],
                'output_topic': f'/raw_tag_array_{cam["index"]}'
            }],
            output='screen'
        )
        for cam in cameras
        
    ]

    nodes.append(
        Node(
                    package='ar_viz',
                    executable='data_meshing_node',
                    name='data_meshing_node',
                    parameters=[{
                        'num_cameras': len(cameras)
                    }]
        
                )
    )

    return LaunchDescription(nodes)