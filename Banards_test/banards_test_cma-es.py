# import numpy as np
# import cma
# from scipy import stats

# x0 = np.array([10, 0])
# num_runs = 1
# max_evals = 10

# def optimze(startpoint):
#     results = np.zeros((num_runs), float)
#     print("start points = ", startpoint)
#     # run the CMA-ES optimizer with the given parameters
#     for i in range(num_runs):
#         result = cma.fmin(activation_function, startpoint, 0.1, {'maxfevals': max_evals})
#         print(result)

import numpy as np
import cma

# define the objective function
def quadratic(x):
    return 0

# set up the CMA-ES optimizer
es = cma.CMAEvolutionStrategy(np.zeros(10), 0.5)

# run the optimization
while not es.stop():
    solutions = es.ask()
    fitness = [quadratic(x) for x in solutions]
    es.tell(solutions, fitness)

print(es.result)