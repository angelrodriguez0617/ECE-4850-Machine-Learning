import numpy as np
import matplotlib.pyplot as plt
import random
import time
import copy

xpos = np.array([57, 16, 14, 47, 90, 55, 35, 80, 45, 38, 78, 36, 53, 71, 87, 32, 65, 97, 7])
ypos = np.array([80, 42, 72, 49, 80, 35, 7, 59, 91, 19, 43, 74, 3, 94, 76, 55, 18, 49, 51, 99])

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
    new_iter = iter
    new_iter[rand_int], new_iter[rand_int-1] = new_iter[rand_int-1], new_iter[rand_int]
    return new_iter


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
plt.title("Traveling Salesman Path")
plt.text(15, 90, f'Total Energy: {int(energy_list[0])}', fontsize='medium', weight="bold")
ax.quiver(xpath[:-1], ypath[:-1], xpath[1:]-xpath[:-1], 
                   ypath[1:]-ypath[:-1],scale_units='xy', angles='xy', scale=1, color='teal', width=0.005)
ax.clear()

# We will use this to graph the minimum path later
best_iterator = copy.deepcopy(iterator)
loop_counter = 1
T = 2
T_stop = 0.00001
T_decimation = 0.9999 
while T > T_stop:
    loop_counter += 1
    iterator = swap(iterator)
    energy = total_energy(xpos,ypos, iterator)

    # delta E = E_i - E_i-1 where E_i is current energy and E_i-1  is previous energy
    # if delta E < 0, accept the current path
    if energy < energy_list[-1]:
        energy_list = np.append(energy_list, energy)
        best_iterator = copy.deepcopy(iterator)

    else: # else, accept current path if e^(-delta_E/T) > u
        u = random.uniform(0, 1)
        delta_E = energy - energy_list[-1]
        if np.exp(-delta_E/T) > u: # accept path
            energy_list = np.append(energy_list, energy)
        else: # This is when we do not want to update the iterator/path
            # Always update T
            T *= T_decimation
            continue
    # Always update T
    T *= T_decimation
    print(f"Accepted energy: {energy_list[-1]}")

    # Plot 
    # updating the values of x and y
    xpath = np.append(np.append(xpos[0],xpos[iterator]),xpos[0])
    ypath = np.append(np.append(ypos[0],ypos[iterator]),ypos[0])
    line1.set_xdata(xpath)
    line1.set_ydata(ypath)
    ax.quiver(xpath[:-1], ypath[:-1], xpath[1:]-xpath[:-1], 
                   ypath[1:]-ypath[:-1],scale_units='xy', angles='xy', scale=1, color='teal', width=0.005)
    # re-drawing the figure
    plt.title("Traveling Salesman Path")
    for i, j in zip(xpath, ypath): # Writes the (x,y) coordinates above the coordinate location
            plt.text(i-4, j+1, '({}, {})'.format(i, j), fontsize='small')
    plt.text(10, 90, f'Energy: {int(energy)}', fontsize='medium', weight="bold")
    format_T = "{:.3f}".format(T)
    plt.text(10, 85, f'Temperature: {format_T}', fontsize='medium', weight="bold")
    fig.canvas.draw()
    # to flush the GUI events
    fig.canvas.flush_events()
    ax.clear()
    time.sleep(0.1)

# print(f"best_iterator: {best_iterator}")
lowest_energy = total_energy(xpos,ypos,best_iterator)
print(f"lowest_energy: {lowest_energy}")
print(f"min value in energy_list: {np.amin(energy_list)}")
energy = total_energy(xpos,ypos,best_iterator)

# Turn off the fast updating plot
plt.ioff()
ax.remove()

# Plot the energy decrease over time
plt.subplot(2, 1, 1)
plt.plot(energy_list)
plt.title("Energy of Chosen Paths")
plt.text(0, 650, f'Lowest Energy Value: {int(np.amin(energy_list))}', fontsize='medium', weight="bold")

# Plot the ending path
plt.subplot(2, 1, 2)
xpath = np.append(np.append(xpos[0],xpos[best_iterator]),xpos[0])
ypath = np.append(np.append(ypos[0],ypos[best_iterator]),ypos[0])
plt.plot(xpath,ypath)
plt.quiver(xpath[:-1], ypath[:-1], xpath[1:]-xpath[:-1], 
                   ypath[1:]-ypath[:-1],scale_units='xy', angles='xy', scale=1, color='teal', width=0.003)
plt.title("Shortest Traveling Salesman Path Found")
for i, j in zip(xpath, ypath): # Writes the (x,y) coordinates above the coordinate location
            plt.text(i-2, j+2, '({}, {})'.format(i, j), fontsize='small')
plt.text(15, 90, f'Energy: {int(energy)}', fontsize='medium', weight="bold")
plt.subplots_adjust(left=0.125, bottom=0.044, right=0.589, top=0.943, wspace=0.2, hspace=0.291)
manager = plt.get_current_fig_manager()
manager.full_screen_toggle() # Make full screen for better view, Alt-F4 to exit full screen
plt.show()

