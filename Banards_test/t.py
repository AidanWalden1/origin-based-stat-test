import numpy as np
import matplotlib.pyplot as plt
from cma import CMAEvolutionStrategy

def objective_function(x):
    return np.abs(x[0] + 1j*x[1])**2

def dummy_objective_function(x):
    return 0

num_runs =100
start_point = ([np.random.uniform(low=-6, high=10),np.random.uniform(low=-2, high=12)])


options = {'maxiter': 50, 'verbose': -1, 'maxfevals': 1000,'bounds':([-6, -2], [10, 12])}
cma_es = CMAEvolutionStrategy(start_point, 7, options)

solutions = []

for i in range(num_runs):
    new_individuals = cma_es.ask()
    cma_es.tell(new_individuals, [dummy_objective_function(x) for x in new_individuals])
    random_individual = new_individuals[np.random.randint(len(new_individuals))]
    solutions.append(random_individual)
    
solutions = np.array(solutions)
x = solutions[:, 0]
y = solutions[:, 1]


plt.scatter(x, y)
plt.xlim(-6,10)
plt.ylim(-2,12)
plt.show()
