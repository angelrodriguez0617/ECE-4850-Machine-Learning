from djitellopy import Tello
import numpy as np
import math
import threading

# we set the origin so that the human is always at (0, 0, 0).
# we also neet to track the position of the drone.
# the coordinate system will be cylindrical so that we have (rho, theta, z)

# this set of movements are to move the drone so that the camera is always facing the origin
class drone_object():
    def __init__(self, position=None, video_active=False, limits=None):
        self.drone = Tello()
        self.drone.connect()
        if position == None:
            self.position = np.array([0, 0, 0])
        else:
            self.position = position
        if video_active == True:
            self.video_active = True
            self.frame = None
            self.video_thread = None
            self.__initalize_video_stream()
        else:
            self.video_active = False
        if limits == None:
            self.limits = (1000, 1000, 5)
        else:
            self.limits = limits

    def deactivate(self):
        if self.video_active == True:
            self.drone.streamoff()

    def __initalize_video_stream(self):
        self.drone.streamon()
        self.video_thread = threading.Thread(target=self.__update_frame)

    def __update_frame(self):
        while True:
            self.frame = self.drone.get_frame_read().frame

    def takeoff(self, height=100):
        self.drone.takeoff()
        self.position[2] = height
        launch_height = self.drone.get_height()
        self.drone.move_up(height - launch_height)

    def land(self):
        self.drone.land()

    def move_arc(self, move_position, segmentation_num=None):
        # calculate how much distance the drone moves
        movement_distance = math.sqrt(self.position[0]**2 + move_position[0]**2 - 2*self.position[0]*move_position[0]*math.cos(self.position[1] - move_position[1]) + (self.position[2] - move_position[2])**2)
        # if we arent given how finely to chunck our movement up, chunck every 10cms
        if segmentation_num == None:
            segmentation_distance = 5
            segmentation_numb = math.floor(movement_distance / segmentation_distance)
        else:
            segmentation_numb = segmentation_num
            segmentation_distance = movement_distance / segmentation_numb
        # calculate the movement in each direction
        movements = (move_position - self.position) / segmentation_distance
        # move the equivalent number of chunks
        # we do a fake acceleration curve (TODO: implement a better acceleration curve)
        self.__move_drone_cylin(movements, 50)
        for i in range(segmentation_numb-1):
            self.__move_drone_cylin(movements, 100)
        # TODO : tail end code seems wrong, generates this: Send command: 'go -300 0 0 50'
        tail_movement = (move_position - self.position)
        self.__move_drone_cylin(tail_movement, 50)

    # moves the drone along a cylindrical vector in cm
    # converts to cartesian and uses the __move_drone_cart function
    def __move_drone_cylin(self, distance, speed=10):
        try:
            # adjust the position numerically first
            self.position = self.position + distance
            # check to see if it would go over our limits
            if self.position[2] <= self.limits[2] or self.position[1] >= self.limits[1] or self.position[0] >= self.limits[0]:
                raise Exception('Limit Error')
        except Exception as error:
            print(repr(error) + f': attempted position ({self.position[0]}, {self.position[1]}, {self.position[2]})')
        else:
            # cut down on repeat math
            sine_movements = math.sin(distance[1])
            cosine_movements = math.cos(distance[1])
            # convert to a cartesian vector
            movements = np.array([(distance[0]*cosine_movements - distance[1]*sine_movements), (distance[0]*sine_movements + distance[1]*cosine_movements), distance[2]])
            self.__move_drone_cart(movements, speed)


    # this function moves the drone along a cartesian vector
    # distance is a numpy array with [x, y, z] in cm
    def __move_drone_cart(self, distance, speed=10):
        self.drone.go_xyz_speed(round(distance[0]), round(distance[1]), round(distance[2]), speed)
