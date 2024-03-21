import coordinate_management as cm
from time import sleep
import numpy as np
import math
import sys

drone = cm.drone_object()
print(">>>>>>>>>>takeoff")
drone.takeoff()
sleep(1)
print(">>>>>>>>>>moving up")
move_position = np.array([100, 0, 100])
drone.move_arc(move_position)
sleep(1)
print(">>>>>>>>>>semicircle")
# TODO: semicircle OoR for some reason: generated Send command: 'go 20 0 0 50'
move_position = np.array([100, math.pi, 100])
drone.move_arc(move_position)
sleep(1)
sys.exit()