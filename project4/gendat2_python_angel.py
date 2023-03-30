import numpy as np
import random
import math

def gendat2_angel(class_num, num_points):
    '''class_num: 0 or 1 depending on which class is desired'''

        # First array contains x-coordinates and seconds array contains corresponding y-coordinates, for test data
    m0 = np.array([[-0.132, 0.320, 1.672, 2.230, 1.217, -0.819, 3.629, 0.8210, 1.808, 0.1700],
                     [-0.711, -1.726, 0.139, 1.151, -0.373, -1.573, -0.243, -0.5220, -0.511, 0.5330]])
    m1 = np.array([[-1.169, 0.813, -0.859, -0.608, -0.832, 2.015, 0.173, 1.432, 0.743, 1.0328],
                   [2.065, 2.441, 0.247, 1.806, 1.286, 0.928,1.923, 0.1299, 1.847, -0.052]])
    
    x = np.array([[],[]])
    for i in range(num_points):
        idx = math.floor(10 * (random.random())) # indexes 0-9
        if class_num:
            m = m0[:,idx]
        else:
            m = m1[:,idx]
        # my_array = np.array([[m[0] + random.random() / math.sqrt(5)], 
        #                       [m[1] + random.random() / math.sqrt(5)]])
        my_array = ([[],[]])
        my_array = np.array([np.add(m, np.random.random(size=(2)) / math.sqrt(5))]).T
        x = np.append(x, my_array, axis=1)
    return x

# For testing function
Ntest0 = 5000 # number of class 0 points to generate
Ntest1 = 5000 # number of class 1 points to generate
xtest0 = gendat2_angel(0,Ntest0) # generate the test data for class 0 
xtest1 = gendat2_angel(1,Ntest1) # generate the test data for class 1 
print(f'xtest0: {xtest0.shape}')
print(f'xtest1: {xtest1.shape}')