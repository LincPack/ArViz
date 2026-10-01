import cv2
import numpy as np

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

# Camera Calibration
calibration = np.load('gopro_calibration.npz')

cameraMatrix = calibration['mtx']
distCoeffs = calibration['dist']

#Take in an mp4
video = cv2.VideoCapture('GoProTest1.MP4')
if not video.isOpened():
    raise RuntimeError("Error: Video was not opened")

tag_size = 0.0194
while True:
    # Get video frame
    frame = 0
    #Adjust so it fits the cv2 detector. 
    ret, frame = video.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        for markerCorners, markerID in zip(corners, ids):
            half = tag_size / 2

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
                cameraMatrix,
                distCoeffs,
                flags=cv2.SOLVEPNP_IPPE_SQUARE
            )

            if success:
                # Convert rotation vector → rotation matrix
                R, _ = cv2.Rodrigues(rvec)

                # Print results
                print(f"\nMarker ID: {markerID}")

                print("Position [m]:")
                print(tvec.flatten())

                print("Rotation matrix:")
                print(R)

                # Draw coordinate axes on marker
                cv2.drawFrameAxes(
                    frame,
                    cameraMatrix,
                    distCoeffs,
                    rvec,
                    tvec,
                    tag_size
                )

# Show video
    cv2.imshow("ArUco Pose", frame)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


video.release()
cv2.destroyAllWindows()

#Ouput position and orientation as numpy matricies.