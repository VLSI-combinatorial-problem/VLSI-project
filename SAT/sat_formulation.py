"""

DO NOT OVERLAP -> only one True for each column array


"""
import re
from itertools import combinations

import numpy as np
from z3 import And, Or, Bool, Solver, Not, sat
import matplotlib.pyplot as plt


class SAT:
    def __init__(self, data_n, solution):
        self.solution = solution
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
        self.max_h = sum(self.chips_h) - max(self.chips_h)

    def grab_data(self, line):
        line = line.split('[')[1]
        line = line.split(']')[0]
        line = line.split(',')
        return [int(n) for n in line]

    def solve_problem(self):
        for h in range(self.min_h, self.min_h + 1):
            self.solver = Solver()
            if self.solve_vlsi_instace(h) == sat:
                self.display_solution(self.solver.model(), h)
                return True
        print("FAILURE")
        return False

    def solve_vlsi_instace(self, current_h):
        self.build_world(current_h)
        for k in range(self.n):
            k_constraints = []
            for x in range(self.w - self.chips_w[k] + 1):
                for y in range(current_h - self.chips_h[k] + 1):
                    k_constraints.append(self.check_rectangle(x, y, k, current_h))
            # self.solver.add(self.at_least_one(k_constraints))
        self.giochino_magico(self.solution)
        return self.solver.check()

    def build_world(self, current_h):
        self.cells = [[[Bool(f"cell_{i}{j}{k}") for k in range(self.n)] for j in range(self.w)] for i in
                      range(current_h)]
        for i in range(current_h):
            for j in range(self.w):
                # self.solver.add(self.at_most_one(self.cells[i][j]))  # no overlap
                pass

    def at_most_one(self, bool_vars):
        return [Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]

    def at_least_one(self, bool_vars):
        return Or(bool_vars)

    def check_rectangle(self, x, y, k, h):
        rectangle = []
        for i in range(h):
            for j in range(self.w):
                if y <= i < y + self.chips_h[k] and x <= j < x + self.chips_w[k]:
                    rectangle.append(self.cells[i][j][k])
                else:
                    rectangle.append(Not(self.cells[i][j][k]))
        return And(rectangle)

    def display_solution(self, model, h):
        print("SUCCESS")
        print("h: " + str(h))
        grid = np.zeros((h, self.w))
        for i in range(h):
            for j in range(self.w):
                for k in range(self.n):
                    if model.evaluate(self.cells[i][j][k]):
                        grid[i, j] = k + 1
                        break
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        plt.imshow(grid, cmap='tab20c')
        ax.set_xticks(np.arange(0.5, self.w, 1))
        ax.set_yticks(np.arange(0.5, h, 1))
        ax.grid(which='major', alpha=0.5)
        plt.show()

    def giochino_magico(self, solution):
        for i in range(12):
            for j in range(12):
                for k in range(8):
                    if solution[i][j][k]:
                        self.solver.add(self.cells[i][j][k])
                    else:
                        self.solver.add(Not(self.cells[i][j][k]))


solution_flatten = [[1, 1, 1, 1, 1, 1, 6, 6, 6, 7, 7, 7],
                    [1, 1, 1, 1, 1, 1, 6, 6, 6, 7, 7, 7],
                    [1, 1, 1, 1, 1, 1, 6, 6, 6, 7, 7, 7],
                    [2, 2, 2, 8, 8, 8, 6, 6, 6, 3, 3, 3],
                    [2, 2, 2, 8, 8, 8, 6, 6, 6, 3, 3, 3],
                    [2, 2, 2, 8, 8, 8, 4, 4, 4, 3, 3, 3],
                    [2, 2, 2, 5, 5, 5, 4, 4, 4, 3, 3, 3],
                    [2, 2, 2, 5, 5, 5, 4, 4, 4, 3, 3, 3],
                    [2, 2, 2, 5, 5, 5, 4, 4, 4, 3, 3, 3],
                    [2, 2, 2, 5, 5, 5, 4, 4, 4, 3, 3, 3],
                    [2, 2, 2, 5, 5, 5, 4, 4, 4, 3, 3, 3],
                    [2, 2, 2, 5, 5, 5, 4, 4, 4, 3, 3, 3]]

solution_3d = np.full((12, 12, 8), fill_value=False)
for i in range(12):
    for j in range(12):
        solution_3d[i, j, solution_flatten[i][j] - 1] = True


problem_number = 5
ss = SAT(problem_number, solution_3d)
ss.solve_problem()
