import cv2
import numpy as np
import glob

# 1. Setup the ArUco Dictionary and Board (Matching your 4x4 setup)
# Adjust the numbers below to match your exact printed board layout
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
# Example: 5x7 ChArUco board, 0.04m square, 0.02m marker
board = cv2.aruco.CharucoBoard((5, 7), 0.04, 0.02, aruco_dict)

# Arrays to store detected data from all images
all_charuco_corners = []
all_charuco_ids = []
image_size = None

# 2. Load your images from the SD card folder
# Change 'gopro_photos/*.jpg' to your actual folder path
image_files = glob.glob('gopro_photos/*.jpg')

if not image_files:
    print("Error: No images found in the specified directory.")
    exit()

print(f"Processing {len(image_files)} images...")

for fname in image_files:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if image_size is None:
        image_size = gray.shape[::-1] # Save (width, height)
        
    # Detect raw ArUco markers
    corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict)
    
    # If markers are found, interpolate the chessboard corners for high accuracy
    if ids is not None and len(ids) > 0:
        retval, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(
            corners, ids, gray, board
        )
        
        # Require a minimum number of detected corners to use the frame
        if retval > 4:
            all_charuco_corners.append(charuco_corners)
            all_charuco_ids.append(charuco_ids)

print(f"Successfully extracted corners from {len(all_charuco_corners)} frames.")

# 3. Run Camera Calibration
print("Calibrating camera... (this may take a moment)")
retval, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
    charuco_corners=all_charuco_corners,
    charuco_ids=all_charuco_ids,
    board=board,
    imageSize=image_size,
    cameraMatrix=None,
    distCoeffs=None
)

# 4. Print results
print("\n=== Calibration Complete ===")
print(f"Repjection Error: {retval:.4f} pixels (Aim for < 1.0, ideally < 0.5)")
print("\nCamera Matrix (K):")
print(camera_matrix)
print("\nDistortion Coefficients (D):")
print(dist_coeffs)

# Optional: Save matrices to a file for your tracking script
np.savez("gopro_calibration.npz", mtx=camera_matrix, dist=dist_coeffs)
print("\nSaved calibration data to 'gopro_calibration.npz'")
