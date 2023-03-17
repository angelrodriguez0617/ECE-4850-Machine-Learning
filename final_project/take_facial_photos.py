import numpy as np
from check_camera import check_camera
import movement as mov
import cv2 as cv
from time import sleep
import cv2 as cv
import shutil
import threading
import os
from djitellopy import Tello
import sys


# This will be used to specify which person the recording will be of
faces = ["Angel", "Austin", "Shekaramiz"] 
# This will be used to specify which facial angle will be recorded
angles = ["front", "left", "right"]
# These are variable to adjust depending on whose face we are recording and which angle it is
face = 1
angle = 0

path = "Default"
parent_directory = os.getcwd()
directory = str(faces[face] + "_" + angles[angle])
path = os.path.join(parent_directory, directory)
if os.path.isdir(directory):
    shutil.rmtree(directory)
os.mkdir(path)
os.chdir(path)

def recordVideo(video, face, angle, img_num=1):
    '''File each step of the path
    img_num represents the number of the photo that is being taken since program start'''    
    #record = 150
    # IDK why, but *'XVID' is no longer working, instead I am using *'mp4v'
    # video = cv.VideoWriter(f'{face}_{angle}_{img_num}.mp4', cv.VideoWriter_fourcc(*'XVID'), 30, (width, height))
    count = 0
    while True: #record > 0:
        if count%30 == 0:
            cv.imwrite(f'{face}_{angle}_img{img_num}.png', frame_read.frame)
            img_num += 1
        count += 1
        video.write(frame_read.frame)
        sleep(1/60)
        #record -= 1
    #return img_num

if __name__ == "__main__":
    # Initialize drone object and turn on
    drone = Tello()
    drone.connect()
    drone.streamon()
    # Austin says this might work
    sleep(0.1)

    camera = drone
    if camera.get_battery() < 20: # if battery is under 20%
        print("\n" + ">>>>>>>>>>>>>>>> DRONE BATTERY LOW. CHANGE BATTERY!")

    # Record video and pictures
    
    try:
        frame_read = camera.get_frame_read()
        height, width, _ = frame_read.frame.shape
        video = cv.VideoWriter(f'{faces[face]}_{angles[angle]}_video.mp4', cv.VideoWriter_fourcc(*'mp4v'), 30, (width, height))
        video_thread = threading.Thread(target=recordVideo, args=(video, faces[face], angles[angle],))
        video_thread.start()
        # img_num should equal 10 after this meaning 10 photos were taken 

        while True:
            frame_read = camera.get_frame_read()
            img = frame_read.frame
            cv.imshow("Output", img)
            cv.waitKey(1)

        # video.release()
        # sys.exit()

    except KeyboardInterrupt:
        video.release()
        sys.exit()

      
        
        