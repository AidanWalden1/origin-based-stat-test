import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)


import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import random
from matplotlib.figure import Figure


from optimizers.cma_es import CMAESOptimizer
from optimizers.woa import WoaOptimizer

from optimizers.EvoloPy_optimzers import EvoloPy_otimizers

from prettytable import PrettyTable
from obj_function import Obj_function
from scipy.stats import wilcoxon

from scipy.stats import ranksums, combine_pvalues,mannwhitneyu

from PyQt5.QtCore import *


xmin, xmax = -5, 15
ymin, ymax = -15, 5
bounds = [[xmin, xmax], [ymin, ymax]]
obj_fun = Obj_function(bounds)

# fig, (abv, bel) = plt.subplots(2, 1)
class Asymmetry_tester(QObject):

    def __init__(self, runs = 500):
        super().__init__()
        self.runs = runs

    @property
    def runs(self):
        return self._runs

    @runs.setter
    def runs(self, value):
        self._runs = value

    # Define a progress update signal
    progress_update = pyqtSignal(int)

    # Define a function for asymmetry testing using a given optimizer
    def asymmetry_test(self, name, optimizer):
        
        num_tests = self.runs
        
        # Initialize arrays for storing test results
        all_individuals = np.empty(num_tests, dtype=object)
        individuals = np.empty(num_tests, dtype=object)
        best_fit = np.empty(num_tests, dtype=object)
        below_arr = []
        above_arr =[]

        with open(name + ".csv", "w") as output:
            output.write("test,iteration,x,y,side,f\n")
            # Run optimization for the given number of tests
            for i in range(num_tests):
                # Calculate progress as a percentage
                progress = int((i+1)/num_tests * 100)
                # Emit progress signal
                self.progress_update.emit(progress)
                # Run optimization and store the results
                all_individuals[i], best_fit[i] = optimizer(bounds, obj_fun.bimodal_objective)
                for j in range(len(all_individuals[i])):
                    x = all_individuals[i][j][0]
                    y = all_individuals[i][j][1]
                    exp_y = 0 if obj_fun.get_expected_y(x) < y else 1
                    output.write(str(i) + "," + str(j) + "," + str(x) + "," + str(y) + "," + str(exp_y) + "," + str(best_fit[i][j]) + "\n")
                individuals[i] = all_individuals[i][-1]

        # Separate the test results based on their location relative to the expected value
        for i,(point) in enumerate(individuals):
            x = point[0]
            y = point[1]
            expected_y = obj_fun.get_expected_y(x)
            arr = np.log(best_fit[i])
            if y > expected_y:
                above_arr.append(arr)
            elif y < expected_y:
                below_arr.append(arr)

        # Reorder the arrays for statistical testing
        above_reordered_list = [list(x) for x in zip(*above_arr)]
        below_reordered_list = [list(x) for x in zip(*below_arr)]

        abv_len = len(above_reordered_list[0])
        bel_len = len(below_reordered_list[0])

        # Ensure that the two arrays have the same length for statistical testing

        for i in range(len(above_reordered_list)):
            if abv_len>bel_len:
                length = bel_len
            elif bel_len>abv_len:
                length = abv_len
            else:
                break

            above_reordered_list[i] = above_reordered_list[i][:length]
            below_reordered_list[i] = below_reordered_list[i][:length]



        # Compute the rank sum test
        comparisons = len(above_reordered_list)

        p_values = [ranksums(above_reordered_list[i], below_reordered_list[i]).pvalue for i in range(comparisons)]
        log_p_values = -np.log10(p_values)
        
        #adjusted using beferonnis then we get min p-value
        adjusted_p_values = np.minimum(1, np.array(p_values) * comparisons) # adjust p-values
        min_p_value = np.min(adjusted_p_values) 

        fig = Figure()
        ax = fig.add_subplot(111)
        ax.plot(log_p_values)
        ax.set_ylabel('-log10(p)')
        ax.set_xlabel('t')
        

        return fig, min_p_value,all_individuals
    
