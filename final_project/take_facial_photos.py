import numpy as np
from check_camera import check_camera
import movement as mov
import cv2 as cv
from time import sleep
import cv2 as cv
import shutil
from time import sleep
import os

path = "Default"

def recordVideo(mv, face, angle):
    '''File each step of the path'''
    parent_directory = os.getcwd()
    directory = face
    path = os.path.join(parent_directory, directory)
    if os.path.isdir(directory):
        shutil.rmtree(directory)
    os.mkdir(path)
    os.chdir(path)
    drone = mv.get_drone()
    count = 0
    img_num = 1
    frame_read = drone.get_frame_read()
    height, width, _ = frame_read.frame.shape
    record = 300
    video = cv.VideoWriter(f'{face}_{angle}.mp4', cv.VideoWriter_fourcc(*'XVID'), 30, (width, height))
    while record > 0:
        if count%30 == 0:
            cv.imwrite(f'{face}_{angle}_img{img_num}.png', frame_read.frame)
            img_num += 1
        count += 1
        video.write(frame_read.frame)
        sleep(1/60)
        record -= 1
    video.release()

if __name__ == "__main__":
    # Initialize drone object and take off
    drone = mov.movement()

    camera = drone.get_drone()
    if camera.get_battery() < 20: # if battery is under 20%
        print("\n" + ">>>>>>>>>>>>>>>> DRONE BATTERY LOW. CHANGE BATTERY!")

    x_step = 30 # Steps the drone takes fowards and backwards
    y_step = 30 # Steps the drone takes left and right
    x_boundary = 200 # X-axis boundary of path
    y_boundary = 200 # Y-axis boundary of path
    z_boundary = 200 # Z-axis boundary of path

    # This will be used to specify which person the recording will be of
    faces = ["Angel", "Austin", "Shekaramiz"] 
    # This will be used to specify which facial angle will be recorded
    angles = ["front", "left", "right"]
    # Record
    video = recordVideo(drone, faces[0], angles[0])

    while drone.get_y_location() <= y_boundary: # The snake path progressively moves towards the y_boundary which should be the end of its mission 
        while drone.get_x_location() + x_step <= x_boundary: # Keep moving forward until the x_boundary is reached
            drone.move(fwd=x_step)
        if drone.get_y_location() + y_step <= y_boundary: # We should pass into here every time except when we are on the y_boundary
            # Continue to the next row of the snake path search algorithm
            drone.move(left=y_step)
        else: # When here, we should be done with the mission, so exit the while loop
            break
        while drone.get_x_location() > 0: # Move all the way back to x=0
            drone.move(back=x_step)
        if drone.get_y_location() + y_step <= y_boundary: # We should pass into here every time except when we are on the y_boundary
            # Continue to the next row of the snake path search algorithm
            drone.move(left=y_step)
        else: # When here, we should be done with the mission, so exit the while loop
            break

    print("\n >>>>>>>>>>>>>>>>OUTSIDE OF THE WHILE LOOP\n")
    drone.land()

      
        
        