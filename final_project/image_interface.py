'''The main object detection and drone flight module.
By Angel Rodriguez and Austin Philips 2023'''
from downvision_calibration import calibrate
from time import sleep
import math
import cv2 as cv
from check_camera import check_camera
import haar_cascade as hc
import mission
import math
import movement as mov
import numpy
import csv
import time
from djitellopy import Tello

fbRange = [62000,82000] # [32000, 52000] # preset parameter for detected image boundary size
w, h = 720, 480         # display size of the screen
location = [0, 0, 0, 0] # Initialized list of x, y and angle coordinates for the drone.


def trackObject(drone, info, starting_location, flag_rotate=0, flag_shift=0, flag_shift_direction = "none"):
    '''Take the variable for the drone, the output array from calling findTurbine in haar_cascade.py, and the current drone x,y location and relative angle (initialized as [0, 0, 0]).
    It scans for the target object of find_face and approaches the target.'''
    # if the object is no longer detected, attempt to find it with 10 more frames
    camera = drone.get_drone()
    if info[0][0] == 0:
        for i in range(100): #Orignally 10
            if info[0][0] == 0:
                frame = camera.get_frame_read()
                img = frame.frame
                img = cv.resize(img, (w, h))
                img, info = hc.find_face(img)
            else:
                break

    # if we did not find the center after finding it previously and our last command was a rotate. Rotate the same degree in the opposite direction
    if info[0][0] == 0 and flag_rotate != 0:
        drone.move(ccw=flag_rotate)
        trackObject(drone, info, starting_location, flag_rotate)
    # if we did not find the center after finding it previously and our last command was a shift left. Move right the same distance.
    elif info[0][0] == 0 and flag_shift != 0 and flag_shift_direction == "left":
        drone.move(right=flag_shift)
        trackObject(drone, info, starting_location, flag_shift)
    # if we did not find the center after finding it previously and our last command was a shift right. Move left the same distance.
    elif info[0][0] == 0 and flag_shift != 0 and flag_shift_direction == "right":
        drone.move(left=flag_shift)
        trackObject(drone, info, starting_location, flag_shift)
    elif info[0][0] == 0:
        return False

    area = info[1]  # The area of the bounding box
    x, y = info[0]  # The x and y location of the center of the bounding box in the frame
    width = info[2] # The width of the bounding box
    img_pass = 0    # Flag to determine if the drone is returning from a target to skip point distance calculations

    # How close to the drone are you comfortable with? 
    x_distance_cutoff = 100

    # object detected
    if(x != 0):
        # (Focal length of camera lense * Real-world width of object)/Width of object in pixels
        # About 22 cm correctly calculates the distance of my face, feel free to revise to work with you
        distance = int((650 * 22) / width) 
        if distance < 20:
            distance = 20

        if(0 < x <= 340):
            # The drone needs to angle to the left to center the target.
            new_angle = int(round(((360 - x) / 360) * 41.3))

            print("new_angle: " , new_angle)
            shift = numpy.abs(distance * numpy.sin(new_angle * numpy.pi/180))
            print("Shift Left: " , shift)
            # If our opposite O found from distance * sin(theta) < 20 rotate the drone counter-clockwise to center on the blue circle.
            if shift < 20:
                drone.move(ccw=new_angle)  
                flag_rotate = new_angle * -1
                flag_shift = 0
            else:
            # If our opposite O found from distance * sin(theta) > 20 shift the drone left by O to center on the blue circle.
                drone.move(left=shift)
                flag_shift = shift
                flag_rotate = 0
                flag_shift_direction = "left" 
            info = check_camera(camera)      
            target_found = trackObject(drone, info, starting_location, flag_rotate,  flag_shift, flag_shift_direction)
            print("Leaving trackObject function on line 109 in image_interface")
            img_pass = 1
            # Maybe this will work, we need to continue trying to find the turbine we missed by returning False
            if not target_found:
                return target_found

        elif(x >= 380):
            # The drone needs to angle to the right to center the target.
            new_angle = int(round(((x - 360) / 360) * 41.3))
            target_angle = drone.get_angle()-new_angle
            if target_angle < 0: target_angle += 360

            print("new_angle: " , new_angle)
            shift = numpy.abs(distance * numpy.sin(new_angle * numpy.pi/180))
            print("Shift Right: " , shift)
            # If our opposite O found from distance * sin(theta) < 20 rotate the drone clockwise to center on the blue circle.
            if shift < 20:
                drone.move(cw=new_angle)
                flag_rotate = new_angle
                flag_shift = 0
            # If our opposite O found from distance * sin(theta) > 20 shift the drone right by O to center on the blue circle.
            else:
                drone.move(right=shift)
                flag_shift = shift
                flag_rotate = 0
                flag_shift_direction = "right"  
            info = check_camera(camera)       
            target_found = trackObject(drone, info, starting_location, flag_rotate,  flag_shift, flag_shift_direction)
            print("Leaving trackObject function on line 144 in image_interface")
            img_pass = 1
            # Maybe this will work, we need to continue trying to find the turbine we missed by returning False
            if not target_found:
                return target_found

        if area > fbRange[0] and area < fbRange[1] and img_pass == 0:
            # The drone has approached the target and will stay put
            print(">>>>>>>>>> DRONE WILL STAY PUT")
            return target_found

        elif area > fbRange[1] and img_pass == 0:
            # The drone is too close to the target
            drone.move(back=20)
            info = check_camera(camera)
            trackObject(drone, info, starting_location)
            print("Leaving trackObject function on line 156 in image_interface")

        elif area < fbRange[0] and area != 0 and img_pass == 0:
            # The drone is too far from the target
            if distance <= 500:
                drone.move(fwd=distance - x_distance_cutoff)
            else:
                while distance != 0:
                    if distance > 500:
                        drone.move(fwd=500)
                        distance -= 500
                    else:
                        drone.move(fwd=distance)
                        distance -= distance
            try:
                flight_time = camera.get_flight_time()
                print(f"Flight time: {flight_time}")
            except:
                print("Printing statement failed")
            camera.flip('f')
            return True

   
        