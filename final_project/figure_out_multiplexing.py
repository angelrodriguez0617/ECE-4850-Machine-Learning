import multiprocessing
import numpy as np
from djitellopy import Tello
import time
import cv2
import os

class DroneObject:
    def __init__(self, enable_camera):
        self._drone = Tello()
        self._drone.connect()
        print(self._drone.query_wifi_signal_noise_ratio())
        self._enable_camera = enable_camera
        self._drone_camera_process = None
        self._drone_camera_img = None
        self._drone_camera_lock = None
        self._image_size = 2073600
        self._image_shape = (720, 960, 3)
        if enable_camera:
            self._init_drone_camera()

    def __del__(self):
        self.close()
    
    def _init_drone_camera(self):
        if self._enable_camera:
            self._drone.streamon()
            time.sleep(self._drone.TIME_BTW_COMMANDS)
            self._drone_camera_lock = multiprocessing.Lock()
            self._drone_camera_img = multiprocessing.Array('i', self._image_size, lock=False)
            self._drone_camera_process = multiprocessing.Process(target=self._update_drone_img)
            self._drone_camera_process.start()

    def _update_drone_img(self):
        while True:
            self._drone_camera_lock.acquire()
            try:
                self._drone_camera_img[:] = self._drone.get_frame_read().frame.flatten().tolist()
            finally:
                self._drone_camera_lock.release()
                time.sleep((1/(self._drone.FRAME_GRAB_TIMEOUT))+self._drone.TIME_BTW_COMMANDS)

    def get_img(self):
        self._drone_camera_lock.acquire()
        try:
            img = np.array(self._drone_camera_img[:]).reshape(self._image_shape).astype(np.uint8)
        finally:
            self._drone_camera_lock.release()
            return img
        
    def close(self):
        self._drone_camera_process.terminate()
        self._drone.end()



my_drone = DroneObject(enable_camera=True)

T = 100
while T > 0:
    img = my_drone.get_img()
    print(T)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
    T -= 1
    time.sleep(1/60)

my_drone.close()
os._exit(0)