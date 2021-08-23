import re
from timeit import default_timer as timer

import numpy as np
from z3 import And, Or, Bool, Int, Solver, Not, sat, Xor, If, Sum
import matplotlib.pyplot as plt


class SMT:
    def __init__(self, data_n):
        self.x_positions = None
        self.y_positions = None
        self.rotations = None
        self.solver = None
        self.prob_num = data_n
        self.max_h = None
        self.min_h = None
        self.w = None
        self.chips_w = None
        self.chips_h = None
        self.chips_w_true = None
        self.chips_h_true = None
        self.n = None
        self.load_data()

    @staticmethod
    def grab_data(line):
        line = line.split('[')[1]
        line = line.split(']')[0]
        line = line.split(',')
        return [int(n) for n in line]

    def load_data(self):
        f = open("../utils/dzn_files/ins_" + str(self.prob_num) + ".dzn", "r")
        lines = f.readlines()
        self.w = int(re.findall(r'\d+', lines[0])[0])
        self.chips_w = self.grab_data(lines[2])
        self.chips_h = self.grab_data(lines[3])
        self.n = len(self.chips_h)
        self.min_h = sum([self.chips_w[k] * self.chips_h[k] for k in range(self.n)]) // self.w
        self.max_h = sum(self.chips_h)

    def display_solution(self, model, h):
        print("SUCCESS")
        print("h: ", h)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        position_x = [int(model.evaluate(self.x_positions[i]).as_string()) for i in range(self.n)]
        position_y = [int(model.evaluate(self.y_positions[i]).as_string()) for i in range(self.n)]
        chips_w_true = [int(model.evaluate(self.chips_w_true[i]).as_string()) for i in range(self.n)]
        chips_h_true = [int(model.evaluate(self.chips_h_true[i]).as_string()) for i in range(self.n)]
        rotations = [model[self.rotations[i]] for i in range(len(self.rotations))]

        for i in range(self.n):
            color = 'green' if rotations[i] else 'orange'
            zorder = 9 if rotations[i] else 5
            line_width = 2
            plt.plot((position_x[i], position_x[i] + chips_w_true[i]), (position_y[i], position_y[i]),
                     color=color, zorder=zorder, linewidth=line_width)
            plt.plot((position_x[i] + chips_w_true[i], position_x[i] + chips_w_true[i]),
                     (position_y[i], position_y[i] + chips_h_true[i]),
                     color=color, zorder=zorder, linewidth=line_width)
            plt.plot((position_x[i], position_x[i] + chips_w_true[i]),
                     (position_y[i] + chips_h_true[i], position_y[i] + chips_h_true[i]),
                     color=color, zorder=zorder, linewidth=line_width)
            plt.plot((position_x[i], position_x[i]), (position_y[i], position_y[i] + chips_h_true[i]),
                     color=color, zorder=zorder, linewidth=line_width)
        plt.scatter(position_x, position_y, zorder=10)
        plt.axis('scaled')
        plt.tight_layout()
        ax.set_xticks(np.arange(0, self.w + 1, 1))
        ax.set_yticks(np.arange(0, h + 1, 1))
        ax.grid(which='major', alpha=0.5)
        plt.show()

    def solve_problem(self):
        # VARIABLES
        self.x_positions = [Int(f"x_pos{i}") for i in range(self.n)]
        self.y_positions = [Int(f"y_pos{i}") for i in range(self.n)]
        self.rotations = [Bool(f"rotations{i}") for i in range(self.n)]
        self.chips_h_true = [Int(f"chips_h_true{i}") for i in range(self.n)]
        self.chips_w_true = [Int(f"chips_w_true{i}") for i in range(self.n)]

        self.solver = Solver()
        self.solver.set('timeout', 240000)

        for h in range(self.min_h + 1, self.min_h + 2):
            print("current h: ", h - 1)
            # CONSTRAINTS

            # c0) ROTATION
            self.solver.add([Xor(
                And(self.rotations[i],
                    self.chips_w_true[i] == self.chips_h[i],
                    self.chips_h_true[i] == self.chips_w[i]),
                And(Not(self.rotations[i]),
                    self.chips_w_true[i] == self.chips_w[i],
                    self.chips_h_true[i] == self.chips_h[i]))
                for i in range(self.n)])

            # c1) NOT EXCEED, DOMAINS
            self.solver.add([And(0 <= self.x_positions[i], self.x_positions[i] <= self.w - self.chips_w_true[i])
                             for i in range(self.n)])

            self.solver.add([And(0 <= self.y_positions[i], self.y_positions[i] < h - self.chips_h_true[i])
                             for i in range(self.n)])

            # c2) SUM OVER ROWS
            for u in range(h):
                self.solver.add(
                    self.w >= Sum([If(And(self.y_positions[i] <= u, u < self.y_positions[i] + self.chips_h_true[i]),
                                      self.chips_w_true[i], 0) for i in range(self.n)]))

            # c3) DO NOT OVERLAP
            for i in range(1, self.n):
                for j in range(0, i):
                    self.solver.add(Or(self.y_positions[i] + self.chips_h_true[i] <= self.y_positions[j],
                                       self.y_positions[j] + self.chips_h_true[j] <= self.y_positions[i],
                                       self.x_positions[i] + self.chips_w_true[i] <= self.x_positions[j],
                                       self.x_positions[j] + self.chips_w_true[j] <= self.x_positions[i]))

            # c4) SUM OVER COLUMNS
            for u in range(self.w):
                self.solver.add(
                    h >= Sum([If(And(self.x_positions[i] <= u, u < self.x_positions[i] + self.chips_w_true[i]),
                                 self.chips_h_true[i], 0) for i in range(self.n)]))

            # this constraint would be redundant since it is already satisfied by c2
            # self.solver.add([self.chips_h_true[i] + self.y_positions[i] <= h for i in range(self.n)])
            # self.solver.add([self.chips_w_true[i] + self.x_positions[i] <= self.w for i in range(self.n)])

            # SOLVER
            start = timer()
            outcome = self.solver.check()
            time = timer() - start
            if outcome == sat:
                print("Solving time: " + str(time))
                # self.display_solution(self.solver.model(), h - 1)
                return time
            print("FAILURE ", h - 1)
        return 241


def main(problem_number):
    ss = SMT(problem_number)
    solve_time = ss.solve_problem()
    return solve_time
