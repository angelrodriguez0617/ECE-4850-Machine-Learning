import cv2
import os
import numpy as np
from djitellopy import Tello
import multiprocessing
import time
import matplotlib.pyplot as plt

class VideoStream:
    def __init__(self, drone):
          self.drone = drone
          self._queue = multiprocessing.Queue()
          self._drone_video_process_obj = multiprocessing.Process(target=self._init_drone_video_process, args=(self._queue,))
          self._drone_video_process_obj.start()
          self._my_photo = None

    def _init_drone_video_process(self, frame_queue):
        '''Continually pushes a photo to an available queue'''    
        while True:
            # empty the queue
            while not frame_queue.empty():
                frame_queue.get()
            print("sending frame")
            # push a photo from the tello to the frame
            frame_queue.put(self.drone.get_frame_read().frame)
            # delay so that we can send other commands to the tello
            time.sleep(1/60)

    def get_img(self):
        if not self._queue.empty():
            self._my_photo = self._queue.get()
        return self._my_photo
    
    def end(self):
        self._queue.close()
        self._drone_video_process_obj.close()
        print("Ending VideoStream")

if __name__ == "__main__":
    drone = Tello()
    drone.connect()
    drone.streamon()
    my_video_stream = VideoStream(drone)

    time.sleep(5)

    img = my_video_stream.get_img()
    
    print(img)

    plt.imshow(img)
    plt.show()
    my_video_stream.end()
    drone.streamoff()
    os._exit(0)

# def find_face(img):
#     '''Take an input image and searches for the target object using an xml file. 
#     Returns the inupt image with boundaries drawn around the detected object and the x and y values of the center of the target in the image
#     as well as the area of the detection boundary.'''

#     # Use Haar Cascades to detect objects using the built-in classifier tool
#     cascade = cv2.CascadeClassifier("Haarcascade_frontalface_default.xml")

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = cascade.detectMultiScale(gray, 1.2, 8)

#     faceListC = []
#     faceListArea = []
#     # turbineListW = []

#     for (x,y,w,h) in faces:
#         # draw a rectangle around the detected object
#         # code for creating a rectangle to see dectection boundaries --
#         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
#         # determine the center of the detection boundaries and the area
#         centerX = x + w // 2
#         centerY = y + h // 2
#         area = w * h
#         faceListC.append([centerX, centerY])
#         faceListArea.append(area)
#     if len(faceListArea) != 0:
#         # if there is items in the area list, find the maximum value and return
#         i = faceListArea.index(max(faceListArea))
#         return img, [faceListC[i], faceListArea[i], w]
#     else:
#         return img, [[0, 0], 0, 0]