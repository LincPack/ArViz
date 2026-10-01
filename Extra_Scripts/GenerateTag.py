#%%
import cv2

# 1. Select a predefined ArUco dictionary 
# (DICT_6X6_250 means a 6x6 grid with 250 unique available IDs)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50) # There are tens of thousands of options for a 4x4 grid, but this library narrows it down to the 50 most reliable

# 2. Define the marker parameters
marker_id = 0       # The unique ID of the marker (must be within 0-49)
pixel_size = 400     # The size of the output image in pixels (400x400) Higher pixels = higher resolution for a larger image. This is 

# 3. Generate the ArUco marker image
# The function automatically applies a 1-bit thick black border


for i in range(7):
    marker_id = i

    marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id, pixel_size)

# 4. Save the generated marker to a file
    cv2.imwrite(f"aruco_marker_{marker_id}.pdf", marker_image)

    print(f"ArUco tag successfully generated and saved as 'aruco_marker_{i}.png'")


