import matplotlib.pyplot as plt
import matplotlib.patches as ptc
import seaborn as sns
import pandas as pd
import numpy as np
import smt_formulation, smt_formulation_rotation


def gather_times(rotation):
    results = np.full((40, 3), fill_value='', dtype=object)

    for prob_num in range(1, 41):
        if rotation:
            solve_time = smt_formulation_rotation.main(prob_num)
        else:
            solve_time = smt_formulation.main(prob_num)

        results[prob_num - 1, 0] = str(int(prob_num))
        results[prob_num - 1, 1] = str(round(solve_time, 3))
        results[prob_num - 1, 2] = 'rotation' if rotation else 'no_rotation'

        print("Solve time: ", round(solve_time, 3))

    np.savetxt(f"results{'_rotation' if rotation else ''}.csv", results, fmt="%s", delimiter=',')
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
    plt.savefig("../utils/images/smt_plot.png")
    plt.show()
