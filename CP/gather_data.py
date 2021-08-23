import copy
from datetime import timedelta
from timeit import default_timer as timer
from minizinc import Solver, Instance, Model
import matplotlib.pyplot as plt
import matplotlib.patches as ptc
import seaborn as sns
import pandas as pd
import numpy as np
import re


def grab_data(line):
    line = line.split('[')[1]
    line = line.split(']')[0]
    line = line.split(',')
    return [int(n) for n in line]


def load_data(prob_num):
    f = open("../utils/dzn_files/ins_" + str(prob_num) + ".dzn", "r")
    lines = f.readlines()
    w = int(re.findall(r'\d+', lines[0])[0])
    chips_w = grab_data(lines[2])
    chips_h = grab_data(lines[3])
    n = len(chips_h)
    return w, n, chips_h, chips_w


def gather_times(rotation):
    results = np.full((40, 3), fill_value='', dtype=object)

    for prob_num in [22, 25, 30, 32]:
        w, n, chips_h, chips_w = load_data(prob_num)
        model = Model(f"cp_formulation{'_rotation' if rotation else ''}.mzn")
        solver = Solver.lookup("chuffed")

        inst = Instance(solver, model)
        inst["w"] = w
        inst["n"] = n
        inst["chips_w"] = chips_w
        inst["chips_h"] = chips_h

        start_time = timer()
        inst.solve(timeout=timedelta(seconds=241), free_search=True)
        solve_time = timer() - start_time

        results[prob_num - 1, 0] = str(int(prob_num))
        results[prob_num - 1, 1] = str(round(solve_time, 3))
        results[prob_num - 1, 2] = 'rotation' if rotation else 'no_rotation'

        print("Solve time: ", round(solve_time, 3))

    # np.savetxt(f"results{'_rotation' if rotation else ''}.csv", results, fmt="%s", delimiter=',')
    print(results)
    return results


if __name__ == '__main__':
    # no_rotation = gather_times(rotation=False)
    # rotation = gather_times(rotation=True)

    no_rotation = np.loadtxt("results.csv", delimiter=',', dtype=str)
    rotation = np.loadtxt("results_rotation.csv", delimiter=',', dtype=str)

    full_data = np.vstack((no_rotation, rotation))
    full_data[:, 0] = np.array(full_data[:, 0], dtype=int)

    full_data_df = pd.DataFrame(data=full_data,
                                columns=["instance", "seconds", "rotation"])
    full_data_df["instance"] = pd.to_numeric(full_data_df["instance"], downcast='signed')
    full_data_df["seconds"] = pd.to_numeric(full_data_df["seconds"], downcast="float")

    fig = plt.figure(figsize=(11, 5))
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(x="instance", y="seconds", hue="rotation", data=full_data_df)

    ch = ax.get_children()
    bars = [c for c in ch if type(c) is ptc.Rectangle]

    for b in bars:
        if b._height >= 240:
            b._alpha = 0.2
            b._hatch = '/'

    plt.tight_layout()
    ax.set_yscale("symlog")
    ax.set_yticks([0, 1, 10, 100, 240])
    plt.savefig("../utils/images/cp_plot.png")
    plt.show()
