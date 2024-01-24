import cma
import numpy as np


class CMAESOptimizer:
    def __init__(self, iterations=100,popsize=0):
        self.iterations = iterations
        self.popsize = popsize

    @property
    def iterations(self):
        return self._iterations

    @iterations.setter
    def iterations(self, value):
        self._iterations = value

    @property
    def popsize(self):
        return self._popsize

    @popsize.setter
    def popsize(self, value):
        self._popsize = value

    def optimize(self, bounds, obj_function):
        t =[]
        best_fit =[]
        #Start points randomly distributed thorugh search spoace
        start_points = [np.random.uniform(low=bounds[0][0], high=bounds[0][1]), np.random.uniform(low=bounds[1][0], high=bounds[1][1])]
        options = {'maxiter': self._iterations, 'verbose': -9 } #, 'bounds': ([bounds[0][0], bounds[1][0]], [bounds[0][1], bounds[1][1]])}
        if self.popsize != 0:
            options['popsize'] = self.popsize
        sigma = (bounds[0][1] - bounds[0][0])/2
        optimizer = cma.CMAEvolutionStrategy(start_points, sigma, options)
        # uses ask-tell interface to get results after each iteration
        for i in range(self._iterations):
            solutions = optimizer.ask()
            fitness = [obj_function(x) for x in solutions]
            best_solution =np.min(fitness)
            best_fit.append(best_solution)
            optimizer.tell(solutions, fitness)

            t.append(solutions[np.random.randint(len(solutions))])
            #  checks to see if we are on the last iteration. If we are return all the values we need for testing.
            if i == self._iterations - 1:
                return t,best_fit
