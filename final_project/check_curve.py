import coordinate_management as cm
from time import sleep
import numpy as np
import math
import sys

drone = cm.drone_object()
drone.takeoff()
sleep(1)
move_position = np.array([100, 0, 100])
drone.move_arc(move_position)
sleep(1)
move_position = np.array([100, math.pi, 100])
sleep(1)
sys.exit()