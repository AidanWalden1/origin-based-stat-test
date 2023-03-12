import cma
import numpy as np

iterations = 150

class CMAESOptimizer:
    def __init__(self, iterations=100):
        self.iterations = iterations

    def CMAESOptimizer(self, obj_function, bounds):
        start_points = [np.random.uniform(low=bounds[0][0], high=bounds[0][1]), np.random.uniform(low=bounds[1][0], high=bounds[1][1])]
        options = {'maxiter': 50, 'verbose': -9, 'bounds': ([bounds[0][0], bounds[1][0]], [bounds[0][1], bounds[1][1]]), 'maxfevals': 1000}
        optimizer = cma.CMAEvolutionStrategy(start_points, 8, options)
        for i in range(iterations):
            solutions = optimizer.ask()
            optimizer.tell(solutions, [obj_function(x) for x in solutions])
            optimizer.logger.add()  # write data to disc to be plotted
            optimizer.disp()
            if i == iterations - 1:
                return solutions[np.random.randint(len(solutions))]
            
    @property
    def iterations(self):
        return self._iterations

    @iterations.setter
    def iterations(self, value):
        self._iterations = value