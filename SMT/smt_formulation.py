import re
from itertools import combinations

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
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        position_x = [int(model.evaluate(self.x_positions[i]).as_string()) for i in range(self.n)]
        position_y = [int(model.evaluate(self.y_positions[i]).as_string()) for i in range(self.n)]
        for i in range(self.n):
            plt.plot((position_x[i], position_x[i] + self.chips_w[i]), (position_y[i], position_y[i]), color='orange')
            plt.plot((position_x[i] + self.chips_w[i], position_x[i] + self.chips_w[i]),
                     (position_y[i], position_y[i] + self.chips_h[i]),
                     color='orange')
            plt.plot((position_x[i], position_x[i] + self.chips_w[i]),
                     (position_y[i] + self.chips_h[i], position_y[i] + self.chips_h[i]),
                     color='orange')
            plt.plot((position_x[i], position_x[i]), (position_y[i], position_y[i] + self.chips_h[i]), color='orange')
        plt.scatter(position_x, position_y, zorder=10)
        ax.set_xticks(np.arange(0, self.w + 1, 1))
        ax.set_yticks(np.arange(0, h + 1, 1))
        ax.grid(which='major', alpha=0.5)
        plt.show()

    # Return maximum of a vector; error if empty
    def max(self, vs):
        m = vs[0]
        for v in vs[1:]:
            m = If(v > m, v, m)
        return m

    def solve_problem(self):
        # VARIABLES
        self.x_positions = [Int(f"x_pos{i}") for i in range(self.n)]
        self.y_positions = [Int(f"y_pos{i}") for i in range(self.n)]

        for h in range(self.min_h, self.min_h + 2):
            # SOLVER
            self.solver = Solver()

            # CONSTRAINTS
            self.solver.add([And(0 <= self.x_positions[i], self.x_positions[i] <= self.w - self.chips_w[i])
                             for i in range(self.n)])

            self.solver.add([And(0 <= self.y_positions[i], self.y_positions[i] <= h - self.chips_h[i])
                             for i in range(self.n)])


            # Ale solution
            '''active_chip = [[Int(f"is_present") for _ in range(self.n)] for _ in range(h)] #  shape == (h, n)
            self.solver.add(
                [Xor(active_chip[i][j] == 1, active_chip[i][j] == 0) for i in range(h) for j in range(self.n)])

            for i in range(h):
                for j in range(self.n):
                    self.solver.add(If(And(self.y_positions[j] <= i, i < self.y_positions[j] + self.chips_h[j]),
                                            active_chip[i][j] == 1, active_chip[i][j] == 0))

            for i in range(h):
                self.solver.add(Sum([self.chips_w[j] * active_chip[i][j] for j in range(self.n)]) <= self.w)'''

            # general solution timerd
            ''''u = Int('u')
            self.solver.add(u >= 0, u < self.n)
            self.solver.add(ForAll(u, self.w >= Sum([If(And(self.y_positions[i] <= u, u < self.y_positions[i] + self.chips_h[i]),
                                           self.chips_w[i], 0) for i in range(self.n)])))'''

            # CUMULATIVE TASK-RD
            for ref_chip in range(self.n):
                concurrent_chips = [self.chips_w[ref_chip]]
                for different_chip in range(self.n):
                    if ref_chip != different_chip:
                        concurrent_chips.append(If(And([self.y_positions[different_chip] <= self.y_positions[ref_chip],
                                                        (self.y_positions[different_chip] + self.chips_h[
                                                            different_chip]) < self.y_positions[ref_chip]]),
                                                   self.chips_w[different_chip], 0))
                self.solver.add(Sum(concurrent_chips) <= self.w)

            for i in range(1, self.n):
                for j in range(0, i):
                    self.solver.add(Or(self.y_positions[i] + self.chips_h[i] <= self.y_positions[j],
                                       self.y_positions[j] + self.chips_h[j] <= self.y_positions[i],
                                       self.x_positions[i] + self.chips_w[i] <= self.x_positions[j],
                                       self.x_positions[j] + self.chips_w[j] <= self.x_positions[i]))

            self.solver.add(self.max([self.chips_h[i] + self.y_positions[i] for i in range(self.n)]) <= h)
            self.solver.add(self.max([self.chips_w[i] + self.x_positions[i] for i in range(self.n)]) <= self.w)

            # SOLVER

            if self.solver.check() == sat:
                print(self.solver.model())
                self.display_solution(self.solver.model(), h)
                return True
        print("FAILURE")
        return False


if __name__ == '__main__':
    problem_number = 3
    ss = SMT(problem_number)
    ss.solve_problem()
