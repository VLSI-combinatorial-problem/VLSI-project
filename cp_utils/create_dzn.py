import re
import copy
import numpy as np


for i in range(1, 41):
    f = open("../cp_utils/raw_instances/ins-" + str(i) + ".txt", "r")
    lines = f.readlines()
    new_lines = ['w = ' + re.sub(r'\n', ';\n', copy.deepcopy(lines[0])), 'n = ' + re.sub(r'\n', ';\n', copy.deepcopy(lines[1]))]
    lines = lines[2:]
    x_data = []
    y_data = []
    for l in lines:
        values = l.split(' ')
        x_data.append(int(values[0]))
        y_data.append(int(re.sub(r'\n', '', values[1])))
    sorting_array = (np.vstack((np.array(x_data), np.array(y_data)))).T
    sorting_array = sorting_array[sorting_array[:, 0].argsort()]
    new_lines.append('chips_w = ' + re.sub(r'\'', '', re.sub(r'[ ]+', ',', str(np.flip(sorting_array[:, 0])))) + ';')
    new_lines.append('\n')
    new_lines.append('chips_h = ' + re.sub(r'\[,', '[', re.sub(r'\'', '', re.sub(r'[ ]+', ',', str(np.flip(sorting_array[:, 1]))))) + ';')

    output = open("../cp_utils/dzn_files/ins_" + str(i) + ".dzn", "w+")
    output.writelines(new_lines)

    f.close()
    output.close()
