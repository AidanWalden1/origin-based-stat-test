import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import time
import random
from prettytable import PrettyTable
from obj_function import Obj_function
from scipy.stats import wilcoxon, ranksums, combine_pvalues, mannwhitneyu


from optimizers.cma_es import CMAESOptimizer
from optimizers.woa import WoaOptimizer


from optimizers.EvoloPy_optimzers import EvoloPy_otimizers

# Set the number of tests to run and the bounds for the objective function
num_tests = 10
xmin, xmax = -5, 15
ymin, ymax = -15, 5
bounds = [[xmin, xmax], [ymin, ymax]]

# Create an array to hold the random individuals for each test
individuals = np.empty(num_tests, dtype=object)

# Create instances of each optimizer to be tested
cmaes = CMAESOptimizer()
woa_original = WoaOptimizer()
woa = EvoloPy_otimizers('WOA')
bat = EvoloPy_otimizers('BAT')
cs = EvoloPy_otimizers('CS')
de = EvoloPy_otimizers('DE')
ffa = EvoloPy_otimizers('FFA')
hho = EvoloPy_otimizers('HHO')
jaya = EvoloPy_otimizers('JAYA')
evolo_woa = EvoloPy_otimizers('WOA')
ga = EvoloPy_otimizers('GA')

# Create an instance of the objective function class
obj_fun = Obj_function(bounds)

# Create arrays to hold all individuals, random individuals, and best fitness for each test
all_individuals = np.empty(num_tests, dtype=object)
individuals = np.empty(num_tests, dtype=object)
best_fit = np.empty(num_tests, dtype=object)

# Define a function to perform the Barnard's test on the results of an optimizer
def banard_test(optimizer):

    # Run the optimizer on the objective function and save the results for each test
    for i in range(num_tests):
        all_individuals[i], best_fit[i] = optimizer(bounds, obj_fun.bimodal_objective)
        individuals[i] = all_individuals[i][-1]

    # Initialize counters and arrays to store above and below points
    above_counter = 0
    below_counter = 0
    range_counter = 0
    above_points = np.empty((0, 2), float)
    below_points = np.empty((0, 2), float)

    # Iterate through the random individuals and count the number of points above and below the expected value
    for point in individuals:
        x = point[0]
        y = point[1]
        expected_y = obj_fun.get_expected_y(x)

        if y > expected_y:
            above_counter = above_counter + 1
            above_points = np.append(above_points, [[x, y]], axis=0)
        elif y < expected_y:
            below_counter = below_counter + 1
            below_points = np.append(below_points, [[x, y]], axis=0)
        else:
            # If the point is within the expected range, increment the range counter
            print("not in range")
            range_counter += 1

    # Create arrays to store x and y points for all random


    solutions = np.stack(individuals)
    xpoints = solutions[:, 0]
    ypoints = solutions[:, 1]

    # Plot graph 
    plt.scatter(xpoints, ypoints)

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.plot(obj_fun.x1, obj_fun.y1, color="green")

    # Set up Barnards test using num_test/2 as values for group2
    a = len(below_points)
    b = num_tests/2
    c = len(above_points)
    d = num_tests/2

    table = PrettyTable()
    table.field_names = ["", "optimizer", "norm"]
    table.add_row(["below", a, b])
    table.add_row(["above", c, d])


    p_val = stats.barnard_exact([[a, b], [c, d]])
    print(table)
    print("p-value= ", p_val.pvalue)



    plt.show()

    return np.array([below_points, above_points], dtype=object)

banard_test(cmaes.optimize)
