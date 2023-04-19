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

num_tests = 500

xmin, xmax = -10, 10
ymin, ymax = -8, 15
bounds = [[xmin, xmax], [ymin, ymax]]

cmaes = CMAESOptimizer()
original_woa = WoaOptimizer()
wooa = WoaOptimizer()

# BAT/CS/DE/FFA/HHO/JAYA/WOA
bat = EvoloPy_otimizers('BAT')
cs = EvoloPy_otimizers('CS')
de = EvoloPy_otimizers('DE')
ffa = EvoloPy_otimizers('FFA')
hho = EvoloPy_otimizers('HHO')
jaya = EvoloPy_otimizers('JAYA')
evolo_woa = EvoloPy_otimizers('WOA')
obj_fun = Obj_function(bounds)

random_individuals = np.empty(num_tests, dtype=object)
best_fit = np.empty(num_tests, dtype=object)


# fig, (abv, bel) = plt.subplots(2, 1)
class Asymmetry_tester(QObject):
    progress_update = pyqtSignal(int)
    def asymmetry_test(self, optimizer):
        
        below_arr = []
        above_arr =[]

        for i in range(num_tests):
            progress = int((i+1)/num_tests * 100)  # Calculate progress as a percentage
            print(progress)
            self.progress_update.emit(progress)  # Emit progress signal

            random_individuals[i], best_fit[i] = optimizer(bounds, obj_fun.bimodal_objective)
        

        for i,(point) in enumerate(random_individuals):
            x = point[0]
            y = point[1]
            expected_y = obj_fun.get_expected_y(x)

            indices = range(len(best_fit[i]))
            log_arr = np.log(best_fit[i])

            # Add labels and title
            # abv.set_ylabel('fitness')
            # abv.set_title('Plot when optimzer tends to other maxima')

            # bel.set_ylabel('fitness')
            # bel.set_title('Plot when optimzer tends to 0,0')

            # Display the plot


            if y > expected_y:
                above_arr.append(log_arr)
                # abv.plot(indices,log_arr)
            elif y < expected_y:
                below_arr.append(log_arr)
                # bel.plot(indices, log_arr)



        above_reordered_list = [list(x) for x in zip(*above_arr)]
        # print(above_reordered_list)
        below_reordered_list = [list(x) for x in zip(*below_arr)]
        # print("/////////////////////////////////////////////////////////")
        # print(below_reordered_list)

        abv_len = len(above_reordered_list[0])
        bel_len = len(below_reordered_list[0])

        # print(bel_len)
        # print(abv_len)

        for i in range(len(above_reordered_list)):
            if abv_len>bel_len:
                length = bel_len
            elif bel_len>abv_len:
                length = abv_len
            else:
                break

        

            above_reordered_list[i] = above_reordered_list[i][:length]

    
            below_reordered_list[i] = below_reordered_list[i][:length]

        # print('//////////////////////edited///////////////////////////////')
        # print(above_reordered_list)
        # print("/////////////////////////////////////////////////////////")
        # print(below_reordered_list)



        # Compute the rank sum test
        comparisons = len(above_reordered_list)

        p_values = [ranksums(above_reordered_list[i], below_reordered_list[i]).pvalue for i in range(comparisons)]
        log_p_values = -np.log10(p_values)

        adjusted_p_values = np.minimum(1, np.array(p_values) * comparisons) # adjust p-values
        min_p_value = np.min(adjusted_p_values) 

        # plt.plot(log_p_values)
        # plt.ylabel('-log10(p)')
        # plt.xlabel('t')
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.plot(log_p_values)
        ax.set_ylabel('-log10(p)')
        ax.set_xlabel('t')
        

        return fig, min_p_value
    
    
    
        

# bat = EvoloPy_otimizers('BAT')
# cs = EvoloPy_otimizers('CS')
# de = EvoloPy_otimizers('DE')
# ffa = EvoloPy_otimizers('FFA')
# hho = EvoloPy_otimizers('HHO')
# jaya = EvoloPy_otimizers('JAYA')
# woa = EvoloPy_otimizers('WOA')

# for i in range(1): 
#     print(f"woa - {asymmetry_test(original_woa.woaOptimizer)}")
#     print(f"cmaes - {asymmetry_test(cmaes.cmaesOptimizer)}")
#     print(f"Evolo woa - {asymmetry_test(evolo_woa.optimize)}")
#     print(f"Evolo cs - {asymmetry_test(cs.optimize)}")
#     print(f"Evolo de - {asymmetry_test(de.optimize)}")
#     print(f"Evolo ffa - {asymmetry_test(ffa.optimize)}")
#     print(f"Evolo hho - {asymmetry_test(hho.optimize)}")
#     print(f"Evolo jaya - {asymmetry_test(jaya.optimize)}")
#     print(f"Evolo woa - {asymmetry_test(woa.optimize)}")
# # print(f"woa - {asymmetry_test(woa.woaOptimizer)}")
# # print(f"cmaes - {asymmetry_test(cmaes.cmaesOptimizer)}")


