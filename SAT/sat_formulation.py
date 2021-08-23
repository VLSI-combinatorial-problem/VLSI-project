import re
from itertools import combinations
from timeit import default_timer as timer
import numpy as np
from z3 import And, Or, Bool, Solver, Not, sat, Xor, unsat
import matplotlib.pyplot as plt


class SAT:
    def __init__(self, data_n):
        self.cells = None
        self.solver = None
        self.prob_num = data_n
        self.max_h = None
        self.min_h = None
        self.w = None
        self.chips_w = None
        self.chips_h = None
        self.n = None
        self.load_data()

    def load_data(self):
        f = open("../cp_utils/dzn_files/ins_" + str(self.prob_num) + ".dzn", "r")
        lines = f.readlines()
        self.w = int(re.findall(r'\d+', lines[0])[0])
        self.chips_w = self.grab_data(lines[2])
        self.chips_h = self.grab_data(lines[3])
        self.n = len(self.chips_h)
        self.min_h = sum([self.chips_w[k] * self.chips_h[k] for k in range(self.n)]) // self.w
        self.max_h = sum(self.chips_h)

    def grab_data(self, line):
        line = line.split('[')[1]
        line = line.split(']')[0]
        line = line.split(',')
        return [int(n) for n in line]

    @staticmethod
    def at_most_one(bool_vars):
        res = []
        for pair in combinations(bool_vars, 2):
            res.append(Not(And(pair[0], pair[1])))
        return res

    @staticmethod
    def at_least_one(bool_vars):
        return Or(bool_vars)

    def display_solution(self, model, h):
        print("SUCCESS")
        print("h: " + str(h))
        grid = np.zeros((h, self.w))
        for i in range(h):
            for j in range(self.w):
                for k in range(self.n):
                    if model[self.cells[i][j][k]]:
                        grid[i, j] = k + 1
                        break
        print(grid)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        plt.imshow(grid, cmap='tab20c', extent=(0, self.w, 0, h))
        ax.set_xticks(range(self.w + 1))
        ax.set_yticks(range(h + 1))
        ax.grid(which='major', alpha=0.5)
        plt.xlabel("x coordinates")
        plt.ylabel("y coordinates")
        plt.tight_layout()
        plt.show()

    def solve_problem(self):
        for h in range(self.min_h, self.max_h):
            # VARIABLES
            self.cells = [[[Bool(f"cell{i}{j}{k}") for k in range(self.n)] for j in range(self.w)] for i in range(h)]
            print("current h: ", h)
            # SOLVER
            self.solver = Solver()

            # CONSTRAINTS
            # c1) DO NOT OVERLAP
            for i in range(h):
                for j in range(self.w):
                    self.solver.add(self.at_most_one(self.cells[i][j][:]))

            # C2) CHIPS CONSISTENCY
            # loop over levels
            for k in range(self.n):
                possible_plates = []
                for x in range(self.w - self.chips_w[k] + 1):
                    for y in range(h - self.chips_h[k] + 1):
                        rectangle = []
                        background = []
                        for i in range(h):  # rows
                            for j in range(self.w):  # cols
                                if y <= i < y + self.chips_h[k] and x <= j < x + self.chips_w[k]:
                                    rectangle.append(self.cells[i][j][k])
                                else:
                                    background.append(Not(self.cells[i][j][k]))
                        possible_plates.append(And(And(rectangle), And(background)))
                self.solver.add(self.at_least_one(possible_plates))
                self.solver.add(self.at_most_one(possible_plates))

            # RESOLUTION
            start = timer()
            outcome = self.solver.check()
            time = timer() - start
            if outcome == sat:
                print("Solving time: " + str(time))
                self.display_solution(self.solver.model(), h)
                return True
            print("FAILURE")
        return False


problem_number = 3
ss = SAT(problem_number)
ss.solve_problem()
