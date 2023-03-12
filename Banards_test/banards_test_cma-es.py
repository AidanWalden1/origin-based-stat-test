import numpy as np
import matplotlib.pyplot as plt
from cma.fitness_functions import ff
from optimizers.cma_es import CMAESOptimizer

iterations = 150
num_tests = 150


random_individuals = np.empty(num_tests,dtype=object)

def dummy_objective_function(x):
    return 0


xmin, xmax = -10, 25
ymin, ymax = -8, 15

bounds = [[xmin, xmax], [ymin, ymax]]
cmaesOptimizer = CMAESOptimizer()


for z in range(num_tests):
    random_individuals[z] = cmaesOptimizer.CMAESOptimizer(dummy_objective_function,bounds)


# print(random_individuals)
solutions = np.stack(random_individuals)



x = solutions[:, 0]
y = solutions[:, 1]
plt.scatter(x, y)

plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax)


########################################

m = (ymax - ymin)/(xmax-xmin)
print('m = ', m )
b = (ymax - (m*xmax))
print('b = ', b)

x = np.linspace(xmin, xmax)
y = m * x + b
plt.plot(x, y, color="green")

# above = yes
above_counter = 0

# below = no
below_counter = 0

for point in random_individuals:

    x = point[0]
    y = point[1]

    if y > m * x + b:
        above_counter += 1
    elif y < m * x + b:
        below_counter += 1


print("above=", above_counter)
print("below=", below_counter)


# print("p-val?=", abs_num_above / abs_num_below)
# print("p-val?=", abs_num_below / abs_num_above)
plt.show()
