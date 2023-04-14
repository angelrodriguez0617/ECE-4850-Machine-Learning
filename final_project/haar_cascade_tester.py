'''Haar Cascade detection tester. This version will be used to test different Cascade Classifiers without taking off the drone
By Angel Rodriguez and Austin Philips 2023'''

from haar_cascade import find_face
import cv2 as cv
from djitellopy import Tello
import movement as mov

if __name__ == "__main__":
    drone = Tello()
    drone.connect()
    drone.streamon()

    # Display battery level
    battery = drone.get_battery()
    print(f'>>>>>>>>>> DRONE BATTERY: {battery}')
    if battery < 20:
        print('>>>>>>>>>> CHANGE DRONE BATTERY')

    # We want to detect a face a certain number of times just to be sure
    count = 10

    # While loop to output the live video feed
    while count > 0: # Output live video feed of the drone to user until face has been detected a certein number of times    
        frame = drone.get_frame_read()
        img = frame.frame
        img, info = find_face(img)
        # Display output window showing the drone's camera frames
        cv.imshow("Output", img)
        cv.waitKey(1)

        x, y = info[0]  # The x and y location of the center of the bounding box in the frame
        area = info[1]  # The area of the bounding box
        width = info[2] # The width of the bounding box

        if info[0][0]:
            print('>>>>>>>>>> FACE DETECTED')
            count -= 1
    
    # Close the window
    cv.destroyWindow("Output")

    # Set height of drone to match height of person's face to track
    drone = mov.movement(tello=drone)
    drone.move(fwd=20)

    


