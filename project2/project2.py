import numpy as np
import matplotlib.pyplot as plt
import random
import time

xpos = np.array([57, 16, 14, 47, 90, 55, 35, 80, 45, 38, 78, 36, 53, 71, 87, 32, 65, 97, 7])
ypos = np.array([80, 42, 72, 49, 80, 35, 7, 59, 91, 19, 43, 74, 3, 94, 76, 55, 18, 49, 51, 99])

# These arrays will be the starting order of travel
# The end of the paths will be the same as the starting point
# xpath = np.append(xpos, xpos[0])
# ypath = np.append(ypos, ypos[0])

# Define iterator, second parameter is the step size
# The first and the last coordinates in the paths will never be chosen
iterator = np.arange(1,xpos.size-1,1)

def get_distance(x1,y1,x2,y2):
    """x1/y1 correspond to first coordinate
    and x2/y2 correspond to second coordinate"""
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)

def total_energy(x,y,iter):
    """x is the array path of x coordinates
    y is the array path of y coordinates"""
    total_energy = get_distance(x[0],y[0],x[iter[0]],y[iter[0]])
    for i in range(1, iter.size):
        energy = get_distance(x[iter[i]],y[iter[i]],x[iter[i-1]],y[iter[i-1]])
        total_energy += energy     
    # Get energy from last point to starting point
    energy = get_distance(x[iter.size],y[iter.size],x[0],y[0])
    total_energy += energy
    return total_energy

def swap(iter):
    rand_int = random.randrange(0, iterator.size - 2)
    iter[rand_int], iter[rand_int-1] = iter[rand_int-1], iter[rand_int]
    return iter


energy_list = np.array([])
energy_list = np.append(energy_list, total_energy(xpos,ypos,iterator))

# enable interactive mode
plt.ion()
# creating subplot and figure
fig = plt.figure()
ax = fig.add_subplot(111)
xpath = np.append(np.append(xpos[0],xpos[iterator]),xpos[0])
ypath = np.append(np.append(ypos[0],ypos[iterator]),ypos[0])
line1, = ax.plot(xpath, ypath)
# data[0] = xpath
# data[1] = ypath
plt.title("Traveling Salesman Path")
# plt.text(xpos[0],ypos[0],'Start and Finish')
plt.text(15, 90, f'Total Energy: {int(energy_list[0])}', fontsize='medium', weight="bold")
ax.quiver(xpath[:-1], ypath[:-1], xpath[1:]-xpath[:-1], 
                   ypath[1:]-ypath[:-1],scale_units='xy', angles='xy', scale=1, color='teal', width=0.005)
ax.clear()

loop_counter = 1
T = 10
while T > 0:
    print(F"Iteration inside while loop: {loop_counter}")
    loop_counter += 1
    temp_iterator = swap(iterator)
    energy = total_energy(xpos,ypos, temp_iterator)

    # delta E = E_i - E_i-1 where E_i is current energy and E_i-1  is previous energy
    # if delta E < 0, accept the current path
    if energy < energy_list[-1]:
        energy_list = np.append(energy_list, energy)
        iterator = temp_iterator
        T -= 0.01
    else: # else, accept current path if e^(-delta_E/T) > u
        u = random.uniform(0, 1)
        delta_E = energy - energy_list[-1]
        if np.exp(-delta_E/T) > u: # accept path
            energy_list = np.append(energy_list, energy)
            iterator = temp_iterator
            T -= 0.01
        else: # This is when we do not want to update the iterator
            continue
        

    # Plot time
    # updating the value of x and ys
    xpath = np.append(np.append(xpos[0],xpos[iterator]),xpos[0])
    ypath = np.append(np.append(ypos[0],ypos[iterator]),ypos[0])
    line1.set_xdata(xpath)
    line1.set_ydata(ypath)
    ax.quiver(xpath[:-1], ypath[:-1], xpath[1:]-xpath[:-1], 
                   ypath[1:]-ypath[:-1],scale_units='xy', angles='xy', scale=1, color='teal', width=0.005)
    # re-drawing the figure
    plt.title("Traveling Salesman Path")
    # plt.text(xpos[0],ypos[0],'Start and Finish')
    plt.text(15, 90, f'Total Energy: {int(energy)}', fontsize='medium', weight="bold")
    format_T = "{:.2f}".format(T)
    plt.text(15, 85, f'Tempurature: {format_T}', fontsize='medium', weight="bold")
    fig.canvas.draw()
    # to flush the GUI events
    fig.canvas.flush_events()
    ax.clear()
    time.sleep(0.1)


plt.ioff()
plt.plot(energy_list)
plt.title("Energy of Chosen Paths")
plt.text(0, 800, f'Lowest Energy Value: {int(energy_list[-1])}', fontsize='medium', weight="bold")
plt.show()

