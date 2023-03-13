import numpy as np
import matplotlib.pyplot as plt
from cma.fitness_functions import ff
from optimizers.cma_es import CMAESOptimizer
from optimizers.woa import WoaOptimizer

iterations = 150
num_tests = 150


def eggholder(X, Y):
    """constraints=512, minimum f(512, 414.2319)=-959.6407"""
    y = Y+47.0
    a = (-1.0)*(y)*np.sin(np.sqrt(np.absolute((X/2.0) + y)))
    b = (-1.0)*X*np.sin(np.sqrt(np.absolute(X-y)))
    return a+b

random_individuals = np.empty(num_tests,dtype=object)

def dummy_objective_function(x):
    return 0


xmin, xmax = -10, 25
ymin, ymax = -8, 15

bounds = [[xmin, xmax], [ymin, ymax]]
cmaes = CMAESOptimizer()
woa = WoaOptimizer()


for z in range(num_tests):
    random_individuals[z] = woa.woaOptimizer(eggholder,bounds)
    random_individuals[z] = cmaes.cmaesOptimizer(dummy_objective_function,bounds)





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
