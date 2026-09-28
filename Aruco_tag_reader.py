import cv2
import numpy as np

arucoDict = cv2.aruco.DICT_4X4_50
arucoParams = cv2.aruco.DetectorParameters_create()
detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

#Take in an mp4
video = 
# Use the openCV library to get the ArUco tags position by looping through each frame of the video and scanning it for ArUco tags
while True:
    # Get video frame
    frame = 0
    #Adjust so it fits the cv2 detector. 
    corners, ids, rejected = detector.detectMarkers(frame, arucoDict, parameters=arucoParams)
#Ouput position and orientation as numpy matricies.