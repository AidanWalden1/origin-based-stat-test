import numpy as np
import matplotlib.pyplot as plt
import cma

# Define the objective function to optimize
def objective_function(x):
    return np.abs(x[0] + 1j*x[1])**2

# Define the callback function to record the best point in each iteration
random_individuals = []
def callback_function(cma_es):
    new_individuals = cma_es.ask()
    random_individual = new_individuals[np.random.randint(len(new_individuals))]
    random_individuals.append(random_individual)

def dummy_objective_function(x):
    return 0

# Define the initial guess for the optimization
initial_guess = np.array([5.0, 5.0])

# Define the options for the optimization
options = {'maxiter': 50, 'verbose': -1, 'maxfevals': 1000}

cma_es = cma.CMAEvolutionStrategy(initial_guess, 0.5, options)

# Optimize the objective function using the CMA-ES algorithm
cma_es.optimize(objective_function, callback=callback_function)

# Print the result of the optimization
result = cma_es.best.get()[0]
print('Best point found: {}'.format(result))

# Generate a graph showing the best point in each iteration
random_individuals = np.array(random_individuals)
fig, ax = plt.subplots()
# ax.plot(initial_guess)
ax.plot(random_individuals[:, 0], random_individuals[:, 1], 'bo-', linestyle='none')
# ax.plot(result[0], result[1], 'r*', markersize=10)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('CMA-ES Optimization')
plt.show()
