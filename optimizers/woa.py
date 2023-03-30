
import os
import sys

# Get the absolute path to the parent directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

# Add the parent directory and woa_pkg directory to the Python path
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, 'optimizers'))



# Add the parent directory of this script to the Python path
import numpy as np
from woa_pkg.whale_optimization import WhaleOptimization


def objective_function_wrapper(x, y, obj):
    x_ = np.array([x, y])
    return obj(x_)


class WoaOptimizer:
    def __init__(self, iterations=30):
        self.iterations = iterations

    def woaOptimizer(self, bounds, obj):

        a = 2
        a_step = a/self.iterations

        woa = WhaleOptimization(opt_func=lambda x, y: objective_function_wrapper(
            x, y, obj), constraints=bounds, nsols=50, b=1, a=a, a_step=a_step)
        for i in range(self.iterations):
            woa.optimize()
            solutions = woa.get_solutions()
        # print(solutions)
        # print(solutions[np.random.randint(len(solutions))])
            best_solutions = woa.print_best_solutions()

        # previous_best_solution = None
        # for i, (fitness, best_solution) in enumerate(best_solutions):

            
        #     if previous_best_solution is not None:
        #         # calculate distance between previous best solution and current best solution
        #         distance = np.linalg.norm(best_solution - previous_best_solution)
        #         print("Fitness value =",fitness,"coords = ",best_solution,f"Distance in iteration {i}: {distance}")

        #     previous_best_solution = best_solution

        return solutions[np.random.randint(len(solutions))],best_solutions

    @property
    def iterations(self):
        return self._iterations

    @iterations.setter
    def iterations(self, value):
        self._iterations = value
