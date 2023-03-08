import math
import numpy as np
import matplotlib.pyplot as plt
import random
from check_camera import check_camera
import time
import csv
import movement as mov
import random
from datetime import datetime

# Initialize drone object and take off
drone = mov.movement()
# Get the start time of flight
start_time = time.time()

def take_photo():
    # Take 10 images to find the location of the target and do the mission if it is found
    info = check_camera(camera)      

if __name__ == "__main__":
    
    camera = drone.get_drone()

    if camera.get_battery() < 20: # if battery is under 20%
        print("\n" + ">>>>>>>>>>>>>>>> DRONE BATTERY LOW. CHANGE BATTERY!")

    x_step = 120 # Steps the drone takes fowards and backwards
    y_step = 120 # Steps the drone takes left and right
    x_boundary = 900 # X-axis boundary of experiment
    y_boundary = 600 # Y-axis boundary of experiment
    turbine_quantity = 1 # Quantity of fans in the mission

    while drone.get_y_location() <= y_boundary: # The snake path progressively moves towards the y_boundary which should be the end of its mission
        print("----------------------------------------")
        print(f"{drone.get_location()}") 
        while drone.get_x_location() + x_step <= x_boundary: # Keep moving forward until the x_boundary is reached
            drone.move(fwd=x_step)
            # Check for fans
            # check_for_turbines()
        if drone.get_y_location() + y_step <= y_boundary: # We should pass into here every time except when we are on the y_boundary
            # Continue to the next row of the snake path search algorithm
            drone.move(left=y_step)
        else: # When here, we should be done with the mission, so exit the while loop
            break
        while drone.get_x_location() > 0: # Move all the way back to x=0
            drone.move(back=x_step)
            # check_for_turbines()
        if drone.get_y_location() + y_step <= y_boundary: # We should pass into here every time except when we are on the y_boundary
            # Continue to the next row of the snake path search algorithm
            drone.move(left=y_step)
        else: # When here, we should be done with the mission, so exit the while loop
            break
        print("----------------------------------------")
        print(f"{drone.get_location()}")

    print("OUTSIDE OF THE WHILE LOOP")

      
        
        