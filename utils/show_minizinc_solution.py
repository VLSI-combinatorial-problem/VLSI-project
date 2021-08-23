import matplotlib.pyplot as plt
import numpy as np
import re


def grab_data(line):
    line = line.split('[')[1]
    line = line.split(']')[0]
    line = line.split(',')
    return [int(n) for n in line]


def plot_solution(data_n, position_x, position_y, max_h):
    f = open("../cp_utils/dzn_files/ins_" + str(data_n) + ".dzn", "r")
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    lines = f.readlines()
    w = int(re.findall(r'\d+', lines[0])[0])
    data_x = grab_data(lines[2])
    data_y = grab_data(lines[3])
    for i in range(len(position_x)):
        plt.plot((position_x[i], position_x[i] + data_x[i]), (position_y[i], position_y[i]), color='orange')
        plt.plot((position_x[i] + data_x[i], position_x[i] + data_x[i]), (position_y[i], position_y[i] + data_y[i]), color='orange')
        plt.plot((position_x[i], position_x[i] + data_x[i]), (position_y[i] + data_y[i], position_y[i] + data_y[i]), color='orange')
        plt.plot((position_x[i], position_x[i]), (position_y[i], position_y[i] + data_y[i]), color='orange')
    plt.scatter(position_x, position_y, zorder=10)
    ax.set_xticks(np.arange(0, w + 1, 1))
    ax.set_yticks(np.arange(0, max_h + 1, 1))
    ax.grid(which='major', alpha=0.5)
    plt.show()


def plot_dual(dual_array, h):
    w = len(dual_array[0][:])
    data_x = []
    data_y = []
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for j in range(w):
        for i in range(h):
            if dual_array[i][j] == 'true':
                data_x.append(j + 0.5)
                data_y.append(i + 0.5)
    plt.scatter(data_x, data_y)
    ax.set_xticks(np.arange(0, w + 1, 1))
    ax.set_yticks(np.arange(0, h + 1, 1))
    ax.grid(which='major', alpha=0.5)
    plt.show()


data_num = 5
h = 13
x_array = [0, 0, 9, 6, 3, 6, 9, 3]
y_array = [9, 0, 0, 0, 0, 7, 8, 6]
plot_solution(data_num, x_array, y_array, h)

# plot_dual(data, h)