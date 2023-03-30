import cma
import numpy as np


class CMAESOptimizer:
    def __init__(self, iterations=100):
        self.iterations = iterations

    def cmaesOptimizer(self, bounds, obj_function):
        best_fit =[]
        start_points = [np.random.uniform(low=bounds[0][0], high=bounds[0][1]), np.random.uniform(low=bounds[1][0], high=bounds[1][1])]
        options = {'maxiter': 50, 'verbose': -9, 'bounds': ([bounds[0][0], bounds[1][0]], [bounds[0][1], bounds[1][1]]), 'maxfevals': 1000}
        sigma = (bounds[0][1] - bounds[0][0])/2
        optimizer = cma.CMAEvolutionStrategy(start_points, sigma, options)
        for i in range(self.iterations):
            solutions = optimizer.ask()
            fitness = [obj_function(x) for x in solutions]
            best_solution =np.min(fitness)
            best_fit.append(best_solution)
            optimizer.tell(solutions, fitness)


            # if previous_best_solution is not None:
            #     # calculate distance between previous best solution and current best solution
            #     distance = np.linalg.norm(best_solution - previous_best_solution)
            #     print("Fitness value =",min(fitness),"coords = ",best_solution,f"Distance in iteration {i}: {distance}")
            
            # previous_best_solution = best_solution

            if i == self.iterations - 1:
                return solutions[np.random.randint(len(solutions))],best_fit
            
            
    @property
    def iterations(self):
        return self._iterations

    @iterations.setter
    def iterations(self, value):
        self._iterations = value