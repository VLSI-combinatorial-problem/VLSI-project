import copy
from datetime import timedelta
from timeit import default_timer as timer
from minizinc import Solver, Instance, Model
import matplotlib.pyplot as plt
import matplotlib.patches as ptc
import seaborn as sns
import pandas as pd
import numpy as np
import argparse
import re


def grab_data(line):
    line = line.split('[')[1]
    line = line.split(']')[0]
    line = line.split(',')
    return [int(n) for n in line]


def load_data(prob_num):
    f = open("../CP/resources/ins_" + str(prob_num) + ".dzn", "r")
    lines = f.readlines()
    w = int(re.findall(r'\d+', lines[0])[0])
    chips_w = grab_data(lines[2])
    chips_h = grab_data(lines[3])
    n = len(chips_h)
    return w, n, chips_h, chips_w


def gather_times(rotation, start_inst, end_inst, save_times=False, verbose=False):
    if save_times:
        assert end_inst - start_inst == 40, "Saving allowed only on all instances"
        times = np.full((40, 3), fill_value='', dtype=object)

    for prob_num in range(start_inst, end_inst + 1):
        w, n, chips_h, chips_w = load_data(prob_num)
        model = Model(f"../CP/src/cp_formulation{'_rotation' if rotation else ''}.mzn")
        solver = Solver.lookup("chuffed")

        inst = Instance(solver, model)
        inst["w"] = w
        inst["n"] = n
        inst["chips_w"] = chips_w
        inst["chips_h"] = chips_h

        start_time = timer()
        inst.solve(timeout=timedelta(seconds=241), free_search=True)
        solve_time = timer() - start_time

        x_pos = mznout.solution.x_positions
        y_pos = mznout.solution.y_positions
        h = mznout.solution.h
        if rotation:
            rotations = mznout.solution.rotations

        with open(f"../CP/out/out{'_rotation' if rotation else '_no_rotation'}_{prob_num}.txt", 'w') as f:
            f.writelines(f"{w} {h}\n")
            f.writelines(f"{n}\n")
            for i in range(n):
                if rotation:
                    f.writelines(f"{chips_w[i]} {chips_h[i]} {x_pos[i]} {y_pos[i]} "
                                 f"{'rotated' if rotations[i] else 'not_rotated'}\n")
                else:
                    f.writelines(f"{chips_w[i]} {chips_h[i]} {x_pos[i]} {y_pos[i]}\n")

        if save_times:
            times[prob_num - 1, 0] = str(int(prob_num))
            times[prob_num - 1, 1] = str(round(solve_time, 3))
            times[prob_num - 1, 2] = 'rotation' if rotation else 'no_rotation'

        if verbose:
            print("Solve time: ", round(solve_time, 3))

    if save_times:
        np.savetxt(f"times{'_rotation' if rotation else '_no_rotation'}.csv", times, fmt="%s", delimiter=',')


def plot_times():
    no_rotation = np.loadtxt("../CP/out/times_no_rotation.csv", delimiter=',', dtype=str)
    rotation = np.loadtxt("../CP/out/times_rotation.csv", delimiter=',', dtype=str)

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
        if b._height >= 300:
            b._alpha = 0.2
            b._hatch = '/'

    plt.tight_layout()
    ax.set_yscale("symlog")
    ax.set_yticks([0, 1, 10, 100, 300])
    plt.savefig("../utils/images/cp_plot.png")
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-si", "--Start", help="Start Instance number", type=int, default=1)
    parser.add_argument("-ei", "--End", help="End Instance", type=int, default=40)
    parser.add_argument("-v", "--Verbose", help="Verbose", type=bool, default=False)
    parser.add_argument("-s", "--Save", help="Saves Results", type=bool, default=False)
    parser.add_argument("-p", "--Plot", help="Plot Results", type=bool, default=False)

    args = parser.parse_args()

    gather_times(rotation=False, start_inst=args.Start, end_inst=args.End, save_times=args.Save, verbose=args.Verbose)
    gather_times(rotation=True, start_inst=args.Start, end_inst=args.End, save_times=args.Save, verbose=args.Verbose)

    if args.Plot:
        plot_times()