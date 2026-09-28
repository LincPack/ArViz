import cv2

# Use the 4x4 dictionary with 50 markers
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# Create a ChArUco board: 7 squares wide, 10 squares high
# Physical size recommendations: Squares = 40mm, Markers = 24mm (adjust to fit an A4 or Letter page)
square_length_m = 0.040
marker_length_m = 0.024
board = cv2.aruco.CharucoBoard((7, 10), square_length_m, marker_length_m, aruco_dict)

# Generate a high-resolution image for sharp printing (2100 x 3000 pixels)
board_image = board.generateImage((2100, 3000), marginSize=50, borderBits=1)

# Save the target image
cv2.imwrite("best_calibration_charuco_4x4.png", board_image)
print("Calibration board saved! Print this with zero scaling ('Actual Size').")
