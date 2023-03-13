import sys
sys.path.append('c:/Users/Aidan/OneDrive/Documents/MMP/Banards_test/optimizers/')
from woa_pkg.whale_optimization import WhaleOptimization
import numpy as np

# # define the objective function that always returns 0
# def objective(x, y):
#     return 0


# # define the constraints for the optimization problem
# constraints = [(-5, 5), (-5, 5)]

# # create an instance of the WhaleOptimization class
# woa = WhaleOptimization(opt_func=objective, constraints=constraints, nsols=10, b=1, a=2, a_step=0.01)

# # run the optimization algorithm for 100 iterations
# for i in range(100):
#     woa.optimize()
#     print(woa.get_solutions())
    

# import cma
# import numpy as np


class WoaOptimizer:
    def __init__(self, iterations=100):
        self.iterations = iterations

    def woaOptimizer(self, obj_function, bounds):
        # optimizer = cma.CMAEvolutionStrategy(start_points, 8, options)
        woa = WhaleOptimization(opt_func=obj_function, constraints=bounds, nsols=10, b=1, a=2, a_step=0.01)

        for i in range(self.iterations):
            woa.optimize()
            solutions = woa.get_solutions()
        print(solutions[np.random.randint(len(solutions))])
        return solutions[np.random.randint(len(solutions))]
            
    @property
    def iterations(self):
        return self._iterations

    @iterations.setter
    def iterations(self, value):
        self._iterations = value