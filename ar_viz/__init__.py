"""Just laying out my code
- Publisher node that starts up camera feeds, or takes them in and publishes them to a topic
- Subscriber node. Takes in image data and processes it with cv2. It should output the position
and orientation of the tags in the image. that would then be published to another topic
- A third subscriber node that takes in the position and orientation data, then does all the necessary calculations on it.

ros2 run my_package my_node --ros-args -r /old_topic:=/new_topic -r __node:=custom_node_name
"""