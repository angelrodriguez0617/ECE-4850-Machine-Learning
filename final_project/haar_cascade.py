'''Haar Cascade detection through OpenCV using the OpenCV documentation. This version will detect the facials of the general popuation
By Angel Rodriguez and Austin Philips 2023'''

import cv2 as cv
import os
import numpy as np
from djitellopy import Tello
import movement as mov
import threading

CWD = os.getcwd()

def find_face(img):
    '''Take an input image and searches for the target object using an xml file. 
    Returns the inupt image with boundaries drawn around the detected object and the x and y values of the center of the target in the image
    as well as the area of the detection boundary.'''

    # Use Haar Cascades to detect objects using the built-in classifier tool
    cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.2, 8)

    faceListC = []
    faceListArea = []
    # turbineListW = []

    for (x,y,w,h) in faces:
        # draw a rectangle around the detected object
        # code for creating a rectangle to see dectection boundaries --
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # determine the center of the detection boundaries and the area
        centerX = x + w // 2
        centerY = y + h // 2
        area = w * h
        faceListC.append([centerX, centerY])
        faceListArea.append(area)
    if len(faceListArea) != 0:
        # if there is items in the area list, find the maximum value and return
        i = faceListArea.index(max(faceListArea))
        return img, [faceListC[i], faceListArea[i], w]
    else:
        return img, [[0, 0], 0, 0]

class MyVideoStream:
    def __init__(self, drone):
          self.drone = drone
          self.frame = 0
          self.info = np.array(([0],[0]))
          self.image = None

    def output_video(self):
        '''Output live video feed of the drone to user'''    
        while True: # Infinite while loop to output the live video feed indefinetly 
            self.frame = self.drone.get_frame_read()
            img = self.frame.frame
            self.img, self.info = find_face(img)
            # Display output window showing the drone's camera frames
            cv.imshow("Output", img)
            cv.waitKey(1)

if __name__ == "__main__":
    drone = Tello()
    drone.connect()
    drone.streamon()

    my_video_stream = MyVideoStream(drone)

    # Show the user the video stream using threading
    video_thread = threading.Thread(target=my_video_stream.output_video)
    video_thread.start()

    img, info = my_video_stream.image, my_video_stream.info
    
    x, y = info[0]  # The x and y location of the center of the bounding box in the frame
    area = info[1]  # The area of the bounding box
    width = info[2] # The width of the bounding box

    while True:
        if info[0][0]: # Face is detected
            drone.takeoff()

