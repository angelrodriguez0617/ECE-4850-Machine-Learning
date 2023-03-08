import numpy as np
from check_camera import check_camera
import time
import movement as mov
from mission import recordVideo


# Initialize drone object and take off
drone = mov.movement()

if __name__ == "__main__":
    
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
    recordVideo(drone, faces[0], angles[0])

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
        print("----------------------------------------")
        print(f"{drone.get_location()}")

    print("OUTSIDE OF THE WHILE LOOP")
    drone.land()

      
        
        