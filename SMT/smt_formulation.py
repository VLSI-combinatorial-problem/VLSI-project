import re
from itertools import combinations
from timeit import default_timer as timer


import numpy as np
from z3 import And, Or, Bool, Int, Solver, Not, sat, Xor, unsat, If, ForAll, Implies, Sum
import matplotlib.pyplot as plt


class SMT:
    def __init__(self, data_n):
        self.x_positions = None
        self.y_positions = None
        self.solver = None
        self.prob_num = data_n
        self.max_h = None
        self.min_h = None
        self.w = None
        self.chips_w = None
        self.chips_h = None
        self.n = None
        self.load_data()

    @staticmethod
    def at_most_one(bool_vars):
        res = []
        for pair in combinations(bool_vars, 2):
            res.append(Not(And(pair[0], pair[1])))
        return res

    @staticmethod
    def at_least_one(bool_vars):
        return Or(bool_vars)

    @staticmethod
    def grab_data(line):
        line = line.split('[')[1]
        line = line.split(']')[0]
        line = line.split(',')
        return [int(n) for n in line]

    def load_data(self):
        f = open("../cp_utils/dzn_files/ins_" + str(self.prob_num) + ".dzn", "r")
        lines = f.readlines()
        self.w = int(re.findall(r'\d+', lines[0])[0])
        self.chips_w = self.grab_data(lines[2])
        self.chips_h = self.grab_data(lines[3])
        self.n = len(self.chips_h)
        self.min_h = sum([self.chips_w[k] * self.chips_h[k] for k in range(self.n)]) // self.w
        self.max_h = sum(self.chips_h) - max(self.chips_h)

    def display_solution(self, model, h):
        print("SUCCESS")
        print("h: ", h)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        position_x = [int(model.evaluate(self.x_positions[i]).as_string()) for i in range(self.n)]
        position_y = [int(model.evaluate(self.y_positions[i]).as_string()) for i in range(self.n)]
        line_width = 2
        for i in range(self.n):
            plt.plot((position_x[i], position_x[i] + self.chips_w[i]),
                     (position_y[i], position_y[i]),
                     color='orange', linewidth=line_width)
            plt.plot((position_x[i] + self.chips_w[i], position_x[i] + self.chips_w[i]),
                     (position_y[i], position_y[i] + self.chips_h[i]),
                     color='orange', linewidth=line_width)
            plt.plot((position_x[i], position_x[i] + self.chips_w[i]),
                     (position_y[i] + self.chips_h[i], position_y[i] + self.chips_h[i]),
                     color='orange', linewidth=line_width)
            plt.plot((position_x[i], position_x[i]), (position_y[i], position_y[i] + self.chips_h[i]),
                     color='orange', linewidth=line_width)
        plt.scatter(position_x, position_y, zorder=10)
        ax.set_xticks(np.arange(0, self.w + 1, 1))
        ax.set_yticks(np.arange(0, h + 1, 1))
        ax.grid(which='major', alpha=0.5)
        plt.show()

    def solve_problem(self):
        # VARIABLES
        self.x_positions = [Int(f"x_pos{i}") for i in range(self.n)]
        self.y_positions = [Int(f"y_pos{i}") for i in range(self.n)]

        for h in range(self.min_h + 1, self.max_h):
            print("current h: ", h - 1)
            # SOLVER
            self.solver = Solver()

            # CONSTRAINTS

            # c1) NOT EXCEED, DOMAINS
            self.solver.add([And(0 <= self.x_positions[i], self.x_positions[i] <= self.w - self.chips_w[i])
                             for i in range(self.n)])

            self.solver.add([And(0 <= self.y_positions[i], self.y_positions[i] < h - self.chips_h[i])
                             for i in range(self.n)])

            # c2) SUM OVER ROWS
            for u in range(h):
                self.solver.add(self.w >= Sum([If(And(self.y_positions[i] <= u, u < self.y_positions[i] + self.chips_h[i]),
                        self.chips_w[i], 0) for i in range(self.n)]))

            # c3) DO NOT OVERLAP
            for i in range(1, self.n):
                for j in range(0, i):
                    self.solver.add(Or(self.y_positions[i] + self.chips_h[i] <= self.y_positions[j],
                                       self.y_positions[j] + self.chips_h[j] <= self.y_positions[i],
                                       self.x_positions[i] + self.chips_w[i] <= self.x_positions[j],
                                       self.x_positions[j] + self.chips_w[j] <= self.x_positions[i]))

            # c4) SUM OVER COLUMNS
            for u in range(self.w):
                self.solver.add(h >= Sum([If(And(self.x_positions[i] <= u, u < self.x_positions[i] + self.chips_w[i]),
                                             self.chips_h[i], 0) for i in range(self.n)]))

            # this constraint would be redundant since it is already satisfied by c2
            # self.solver.add(self.max([self.chips_w[i] + self.x_positions[i] for i in range(self.n)]) <= self.w)


            # SOLVER
            start = timer()
            outcome = self.solver.check()
            time = timer() - start
            if outcome == sat:
                print("Solving time: " + str(time))
                self.display_solution(self.solver.model(), h - 1)
                return True
            print("FAILURE ", h - 1)
        return False


if __name__ == '__main__':
    problem_number = 33
    ss = SMT(problem_number)
    ss.solve_problem()
