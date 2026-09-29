import cv2
import numpy as np
import glob

# 1. Setup the ArUco Dictionary and Board (Matching your 4x4 setup)
# Adjust the numbers below to match your exact printed board layout
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
# Example: 5x7 ChArUco board, 0.04m square, 0.02m marker
board = cv2.aruco.CharucoBoard((7, 10), 0.0217, 0.01287, aruco_dict)
charuco_detector = cv2.aruco.CharucoDetector(board)


# Arrays to store detected data from all images
all_obj_points = []
all_img_points = []
image_size = None

# 2. Load your images from the SD card folder
# Change 'gopro_photos/*.jpg' to your actual folder path
image_files = glob.glob('gopro_photos_2/*.JPG')

if not image_files:
    print("Error: No images found in the specified directory.")
    exit()

print(f"Processing {len(image_files)} images...")

for fname in image_files:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if image_size is None:
        image_size = gray.shape[::-1] # Save (width, height)
        
    # Detect ArUco markers and interpolate the chessboard corners for high accuracy
    charuco_corners, charuco_ids, marker_corners, marker_ids = charuco_detector.detectBoard(gray)
    
    # Require a minimum number of detected corners to use the frame
    if charuco_ids is not None and len(charuco_ids) > 4:
        obj_points, img_points = board.matchImagePoints(charuco_corners, charuco_ids)
        all_obj_points.append(obj_points)
        all_img_points.append(img_points)

print(f"Successfully extracted corners from {len(all_obj_points)} frames.")

# 3. Run Camera Calibration
print("Calibrating camera... (this may take a moment)")
retval, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    all_obj_points,
    all_img_points,
    image_size,
    None,
    None
)

# 4. Print results
print("\n=== Calibration Complete ===")
print(f"Reprojection Error: {retval:.4f} pixels (Aim for < 1.0, ideally < 0.5)")
print("\nCamera Matrix (K):")
print(camera_matrix)
print("\nDistortion Coefficients (D):")
print(dist_coeffs)

# Optional: Save matrices to a file for your tracking script
np.savez("gopro_calibration.npz", mtx=camera_matrix, dist=dist_coeffs)
print("\nSaved calibration data to 'gopro_calibration.npz'")
total_error = 0
total_points = 0

for i in range(len(all_obj_points)):
    projected, _ = cv2.projectPoints(
        all_obj_points[i],
        rvecs[i],
        tvecs[i],
        camera_matrix,
        dist_coeffs
    )

    img_points = all_img_points[i].reshape(-1, 2)
    projected = projected.reshape(-1, 2)

    error = cv2.norm(
        img_points,
        projected,
        cv2.NORM_L2
    )

    total_error += error**2
    total_points += len(img_points)

    image_rms = error / np.sqrt(len(img_points))

    print(f"Image {i}: {image_rms:.3f} px")

overall_rms = np.sqrt(total_error / total_points)

print(f"\nOverall RMS: {overall_rms:.3f} px")