import rclpy
from rclpy.node import Node


"""Just laying out my code
- Publisher node that starts up camera feeds, or takes them in and publishes them to a topic
- Subscriber node. Takes in image data and processes it with cv2. It should output the position
and orientation of the tags in the image. that would then be published to another topic
- A third subscriber node that takes in the position and orientation data, then does all the necessary calculations on it.
"""