from woa_pkg.whale_optimization import WhaleOptimization
import numpy as np


def objective_function_wrapper(x, y,obj):
    x_ = np.array([x, y])
    return obj(x_)

class WoaOptimizer:
    def __init__(self, iterations=30):
        self.iterations = iterations


    def woaOptimizer(self, bounds, obj):
        
        a=2
        a_step = a/self.iterations
        
        woa = WhaleOptimization(opt_func=lambda x, y: objective_function_wrapper(x, y, obj), constraints=bounds, nsols=50, b=1, a=a, a_step=a_step)

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
