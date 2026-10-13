from setuptools import find_packages, setup
from glob import glob
import os
import sys

scripts_python = sys.executable

package_name = 'ar_viz'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools',
                      'numpy',
                      'opencv-python',
                      'scipy'],
    zip_safe=True,
    maintainer='lincolnpacker',
    maintainer_email='lincolnkingsday@gmail.com',
    description='This ROS2 package provides a way for multiple cameras to be set up to get an object\'s pose from ArUco tags.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'data_meshing_node = ar_viz.data_meshing_node:main',
            'camera_vision_node = ar_viz.camera_vision_node:main'
        ],
    },
)
