import cma
import numpy as np
import matplotlib.pyplot as plt
from cmaes import CMA
from cma.fitness_functions import ff

iterations = 1500
random_individuals = [[0] * 3 for i in range(iterations)]
num_tests = 150

abs_num_above = 0

abs_num_below = 0


def objective_function(x):
    return np.abs(x[0] + 1j * x[1]) ** 2


def elli(x):
    cond = 1000000.0
    ff.elli(x, cond)


def dummy_objective_function(x):
    return 0


def quadratic(x1, x2):
    return (x1 - 3) ** 2 + (10 * (x2 + 2)) ** 2


for z in range(num_tests):
    start_point = ([np.random.uniform(low=-6, high=10), np.random.uniform(low=-2, high=12)])

    options = {'maxiter': 50, 'verbose': -9, 'maxfevals': 1000, 'bounds': ([-6, -2], [10, 12])}

    optimizer = cma.CMAEvolutionStrategy(start_point, 7, options)
    print(start_point)
    for i in range(iterations):
        solutions = optimizer.ask()
        random_individual = solutions[np.random.randint(len(solutions))]
        # print(i, random_individual)
        random_individuals[i] = random_individual
        optimizer.tell(solutions, [dummy_objective_function(x) for x in solutions])
        optimizer.logger.add()  # write data to disc to be plotted
        optimizer.disp()

    solutions = np.array(random_individuals)
    x = solutions[:, 0]
    y = solutions[:, 1]

    x1, y1 = [-7, 11], [-2.875, 12.875]
    plt.plot(x1, y1, color="green")

    plt.plot()
    plt.scatter(x, y)
    plt.xlim(-6, 10)
    plt.ylim(-2, 12)
    # plt.show()

    ########################################

    m = 14 / 16
    b = 3.25

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

    if above_counter > below_counter:
        abs_num_above += 1
    elif above_counter < below_counter:
        abs_num_below += 1

    print(z)
    print("above=", above_counter)
    print("below=", below_counter)

print("abs above= ", abs_num_above)
print("abs below=", abs_num_below)
print("p-val?=", abs_num_above / abs_num_below)
print("p-val?=", abs_num_below / abs_num_above)
