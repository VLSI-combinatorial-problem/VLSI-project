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


data_num = 15
h = 24
x_array = [16, 0, 3, 19, 19, 16, 19, 13, 16, 13, 3, 0, 10, 6, 6, 0]
y_array = [0, 14, 0, 0, 6, 3, 13, 12, 11, 0, 5, 0, 0, 19, 0, 18]
plot_solution(data_num, x_array, y_array, h)
