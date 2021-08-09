import re
import copy


for i in range(1, 41):
    f = open("../cp_utils/raw_instances/ins-" + str(i) + ".txt", "r")
    lines = f.readlines()
    new_lines = ['w = ' + re.sub(r'\n', ';\n', copy.deepcopy(lines[0])), 'n = ' + re.sub(r'\n', ';\n', copy.deepcopy(lines[1]))]
    lines = lines[2:]
    x_data = []
    y_data = []
    for l in lines:
        values = l.split(' ')
        x_data.append(values[0])
        y_data.append(re.sub(r'\n', '', values[1]))
    new_lines.append('circuits_w = ' + re.sub(r'\'', '', str(x_data)) + ';')
    new_lines.append('\n')
    new_lines.append('circuits_h = ' + re.sub(r'\'', '', str(y_data)) + ';')

    output = open("../cp_utils/dzn_files/ins_" + str(i) + ".dzn", "w+")
    output.writelines(new_lines)

    f.close()
    output.close()
