'''Haar Cascade detection tester. This version will be used to test different Cascade Classifiers without taking off the drone
By Angel Rodriguez and Austin Philips 2023'''

from haar_cascade import find_face
import cv2 as cv
from djitellopy import Tello

if __name__ == "__main__":
    drone = Tello()
    drone.connect()
    drone.streamon()

    # Output live video feed of the drone to user    
    while True: # Infinite while loop to output the live video feed indefinetly 
        frame = drone.get_frame_read()
        img = frame.frame
        img, info = find_face(img)
        # Display output window showing the drone's camera frames
        cv.imshow("Output", img)
        cv.waitKey(1)