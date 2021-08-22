from datetime import timedelta
from minizinc import Solver, Instance, Model

model = Model("cp_formulation.mzn")
solver = Solver.lookup("chuffed")

inst = Instance(solver, model)

# Solve the instance
result = inst.solve(timeout=timedelta(seconds=20), free_search=True)
print(result)