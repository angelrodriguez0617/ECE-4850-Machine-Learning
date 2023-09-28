# -*- coding: utf-8 -*-
"""
# Kalman filter example Estimating a Random Constant

# A Python implementation of the example given in pages 11-15 of "An
# Introduction to the Kalman Filter" by Greg Welch and Gary Bishop,
# University of North Carolina at Chapel Hill, Department of Computer
# Science, TR 95-041,
# https://www.cs.unc.edu/~welch/media/pdf/kalman_intro.pdf
# by Andrew D. Straw

@author George Rudolph 1/17/2019
I've made some minor changes to Andrew Straw's demo code.
1. Added explanatory comments.
2. Seed the random number generator for consistency

@author George Rudolph 7 Nov 2020
1. change subscript k to t for time
"""

import numpy as np
import matplotlib.pyplot as plt

# intial parameters
# size of array, number of samples
n_iter = 200
sz = (n_iter,)
# truth value (typo in example at top of p. 13 calls this z)
# truth value not used in filter, only to compare behavior of filter
x = -0.37727 
noise_stddev = 0.1
np.random.seed(20190117)
z = np.random.normal(x,noise_stddev,size=sz) # observations (normal about x, sigma=0.1)
print(z)
# process variance
Q = 1e-5 

# allocate space for arrays
xhat=np.zeros(sz)      # a posteri estimate of x
P=np.zeros(sz)         # a posteri error estimate
xhatminus=np.zeros(sz) # a priori estimate of x
Pminus=np.zeros(sz)    # a priori error estimate
K=np.zeros(sz)         # gain or blending factor

# estimate of measurement variance, change to see effect
# For example, try with R=0.01, R = 1, and R=0.0001 
R = 10e-4 

# intial guesses
xhat[0] = 0.0
P[0] = 1.0

for t in range(1,n_iter):
    # time update
    xhatminus[t] = xhat[t-1]
    Pminus[t] = P[t-1]+Q

    # measurement update
    K[t] = Pminus[t]/( Pminus[t]+R )
    xhat[t] = (1-K[t])*xhatminus[t]+K[t]*z[t]
    P[t] = (1-K[t])*Pminus[t]

###############
# Display the data
###############
plt.rcParams['figure.figsize'] = (10, 8)
plt.figure()
plt.plot(z,'k+',label='noisy measurements')
plt.plot(xhat,'b-',label='a posteri estimate')
plt.axhline(x,color='g',label='truth value')
plt.legend()
plt.title('Estimate vs. iteration step', fontweight='bold')
plt.xlabel('Iteration')
plt.ylabel('Voltage')

plt.figure()
# Pminus not valid at step 0
valid_iter = range(1,n_iter) 
plt.plot(valid_iter,Pminus[valid_iter],label='a priori error estimate')
plt.title('Estimated $\it{\mathbf{a \ priori}}$ error vs. iteration step', fontweight='bold')
plt.xlabel('Iteration')
plt.ylabel('$(Voltage)^2$')
plt.setp(plt.gca(),'ylim',[0,.01])
plt.show()