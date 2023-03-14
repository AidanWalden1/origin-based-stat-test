import sys
sys.path.append('c:/Users/Aidan/OneDrive/Documents/MMP/Banards_test/optimizers/')
from woa_pkg.whale_optimization import WhaleOptimization
import numpy as np


def objective_function_wrapper(x, y,obj):
    x_ = np.array([x, y])
    return obj(x_)

class WoaOptimizer:
    def __init__(self, iterations=100):
        self.iterations = iterations


    def woaOptimizer(self, bounds, obj):
        # optimizer = cma.CMAEvolutionStrategy(start_points, 8, options)
        
        woa = WhaleOptimization(opt_func=lambda x, y: objective_function_wrapper(x, y, obj), constraints=bounds, nsols=10, b=1, a=2, a_step=0.01)

        for i in range(self.iterations):
            woa.optimize()
            solutions = woa.get_solutions()
        # print(solutions)
        # print(solutions[np.random.randint(len(solutions))])
        return solutions[np.random.randint(len(solutions))]
            
    @property
    def iterations(self):
        return self._iterations

    @iterations.setter
    def iterations(self, value):
        self._iterations = value