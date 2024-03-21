import math
import random as ran
import numpy as np 
import matplotlib.pyplot as plot


x = [57, 16, 14, 47, 90, 55, 3, 5, 80, 45, 38, 78, 36, 53, 71, 87, 32, 65, 97, 7, 57]
y = [80, 42, 72, 49, 80, 35, 7, 59, 91, 19, 43, 74, 3, 94, 76, 55, 18, 49, 51, 99, 80]
global final_path
global current_lowest

used_permutations =[]
energy_array =[]
new_path=[]
temperature_list = []
current_lowest = []

def calc_distance(x, y, index):
    overalldist = 0
    for i in range(1,len(index)):
        ec = 0
        ec = np.sqrt(np.abs(((x[index[i]] - x[index[i-1]])**2)+((y[index[i]] - y[index[i-1]])**2)))
        overalldist +=ec
    return overalldist

def compare_results(ec, ep,temp, temperature, iteration):
    global final_path
    global current_lowest
    delta = ec - ep
    if delta < 0:
        energy_array.append(ec)
        new_path.append(temp)
        final_path = temp
        return True
    else:
        u = ran.random()
        alpha = math.exp(-delta/temperature)
        if alpha > u:
            return True
        else:
            return False

def switch_indexes(to_switch):
    temp_index = to_switch.copy()
    temp_index_1 = temp_index[ran.randrange(1, len(to_switch)-1)]
    temp_index_2 = temp_index[ran.randrange(1, len(to_switch)-1)]

    val1 = temp_index[temp_index_1]
    val2 = temp_index[temp_index_2]
    
    temp_index[temp_index_1] = val2
    temp_index[temp_index_2] = val1
    used_permutations.append(temp_index)

    index = temp_index
    return temp_index

def find_minimum(ec, ep, temperature, temp, decrement_value, current_lowest):
    energy_array.clear()
    temperature_list.clear()
    for i in range(2000):
        if compare_results(ec, ep, temp, temperature, i) == True:
            temperature_list.append(temperature)
            temp = switch_indexes(temp)
            ep = ec
            ec = calc_distance(x, y, temp)
            if len(current_lowest) > 0 and current_lowest[0] > ec:
                current_lowest = [ec, temp, i]
            temperature *= decrement_value
        else:
            temp = switch_indexes(temp)
            ec = calc_distance(x, y, temp)
        
        if current_lowest[2] < i - 5 and ec > current_lowest[0]:
            temperature += 1.0
            temp = current_lowest[1]
            ec = current_lowest[0]
    return current_lowest

def main():
    global current_lowest
    index = []
    for i in range(len(x)):
        index.append(i)
    ep = calc_distance(x,y,index)
    temp = switch_indexes(index)
    temperature = 100.0
    decrement_value = 0.99
    ec = calc_distance(x,y,temp)
    test_list = [ep, index, 0]
    current_lowest = test_list
    temp2 = test_list
    while 1:
        temp2 = find_minimum(ec, ep, temperature, temp, decrement_value, test_list)
        while temp2[0] >= current_lowest[0]:
            temp2 = find_minimum(ec, ep, temperature, temp, decrement_value, test_list)
        current_lowest = temp2
        #test_list = current_lowest
        temperature = 100
        print(current_lowest)
        if current_lowest[0] <= 420:
            break
        

    font1 = {'family':'serif', 'color':'black','size':10}
    plot.plot(energy_array)
    plot.title("Overall Energy for Accepted Path", fontdict= font1)
    plot.xlabel("Iteration", fontdict= font1)
    plot.ylabel("Energy of Path", fontdict= font1)
    plot.show()

    plot.plot(temperature_list)
    plot.title("Tempurature over Time", fontdict= font1)
    plot.xlabel("Iteration", fontdict= font1)
    plot.ylabel("Tempurature", fontdict= font1)
    plot.show()

    print(current_lowest[0])
    for j in range(len(current_lowest[1])):
        if len(temp) > j+1:
            plot.plot([x[current_lowest[1][j]], x[current_lowest[1][j+1]]], [y[current_lowest[1][j]], y[current_lowest[1][j+1]]])

    plot.show()
    plot.close()


if __name__ == "__main__":
    main()
