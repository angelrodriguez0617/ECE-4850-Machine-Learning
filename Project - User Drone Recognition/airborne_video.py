import numpy as np
from check_camera import check_camera
import movement as mov
import cv2 as cv
from time import sleep
import cv2 as cv
import shutil
import threading
import os

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
    # Initialize drone object and take off
    drone = mov.movement(height=120)
    # Austin says this might work
    sleep(0.1)

    camera = drone.get_drone()
    if camera.get_battery() < 20: # if battery is under 20%
        print("\n" + ">>>>>>>>>>>>>>>> DRONE BATTERY LOW. CHANGE BATTERY!")

    x_step = 30 # Steps the drone takes fowards and backwards
    y_step = 30 # Steps the drone takes left and right
    z_step = 30 # Steps the drone takes up
    x_boundary = 200 # X-axis boundary of path
    y_boundary = 150 # Y-axis boundary of path
    z_boundary = 200 # Z-axis boundary of path

    # Record video and pictures
    
    try:
        
        frame_read = camera.get_frame_read()
        height, width, _ = frame_read.frame.shape
        video = cv.VideoWriter(f'{faces[face]}_{angles[angle]}_video.mp4', cv.VideoWriter_fourcc(*'mp4v'), 30, (width, height))
        video_thread = threading.Thread(target=recordVideo, args=(video, faces[face], angles[angle],))
        video_thread.start()
        # img_num should equal 10 after this meaning 10 photos were taken
        
        temp_x_coordinate = drone.get_x_location()
        temp_y_coordinate = drone.get_y_location()
        print(drone.get_z_location())
        while drone.get_z_location() + z_step <= z_boundary: # Keep going until we hit the ceiling boundary specified
            while drone.get_y_location() <= y_boundary: # The snake path progressively moves towards the y_boundary which should be the end of its mission 
                while drone.get_x_location() + x_step <= x_boundary: # Keep moving forward until the x_boundary is reached
                    drone.move(fwd=x_step)
                if drone.get_y_location() + y_step <= y_boundary: # We should pass into here every time except when we are on the y_boundary
                    # Continue to the next row of the snake path search algorithm
                    drone.move(left=y_step)
                else: # When here, we should be done with the mission, so exit the while loop
                    break
                while drone.get_x_location() > 0: # Move all the way back to x=0, we are okay with the drone being a step behind x=0
                    drone.move(back=x_step)
                if drone.get_y_location() + y_step <= y_boundary: # We should pass into here every time except when we are on the y_boundary
                    # Continue to the next row of the snake path search algorithm
                    drone.move(left=y_step)
                else: # When here, we should be done with the mission, so exit the while loop
                    break
            # Move up and repeat the process
            drone.move(up=z_step)
            # Go to orignal location to repeat path
            drone.x_go_to(temp_x_coordinate)
            drone.y_go_to(temp_y_coordinate)
 
        print("\n >>>>>>>>>>>>>>>> OUTSIDE OF THE WHILE LOOP\n")
        video.release()
        drone.land(turn_off=True)
    except KeyboardInterrupt:
        video.release()
        drone.land(turn_off=True)

      
        
        