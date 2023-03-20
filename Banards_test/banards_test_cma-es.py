import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

from optimizers.cma_es import CMAESOptimizer
from optimizers.woa import WoaOptimizer
from banards import BarnardTest
from prettytable import PrettyTable


num_tests = 500

xmin, xmax = -1, 7
ymin, ymax = -3, 5

random_individuals = np.empty(num_tests, dtype=object)

bounds = [[xmin, xmax], [ymin, ymax]]
cmaes = CMAESOptimizer()
woa = WoaOptimizer()


m1 = (ymax - ymin)/(xmax-xmin)
b1 = (ymax - (m1*xmax))

x1 = np.linspace(xmin, xmax)
y1 = m1 * x1 + b1

m2 = -1 * m1
b2 = 0
x2 = np.linspace(xmin, xmax)
y2 = m2 * x2 + b2
# plt.plot(x2, y2, color="blue")


x3 = (b2-b1)/(m1-m2)
y3 = m1*x3 + b1

x3 = x3*2
y3 = y3*2


def bimodal_objective(x):
    """
    Computes the value of a bimodal objective function at point x.
    x: A numpy array of length 2, representing the coordinates (x, y) of the point.
    """
    x1, x2 = x
    f1 = (x1 - 0)**2 + (x2 - 0)**2
    f2 = (x1 - x3)**2 + (x2 - y3)**2
    f = np.minimum(f1, f2)
    return f


def graph(optimizer):

    for z in range(num_tests):
        random_individuals[z] = optimizer(bounds, bimodal_objective)

    # above = yes
    above_counter = 0

    # below = no
    below_counter = 0
    range_counter = 0

    above_points = np.empty((0, 2), float)
    below_points = np.empty((0, 2), float)

    t=0
    for point in random_individuals:
        x = point[0]
        y = point[1]

        if x>1.5:
            t=t+1
        expected_y = m1*x +b1

        if y > expected_y:
            above_counter = above_counter + 1
            above_points = np.append(above_points, [[x, y]], axis=0)
        elif y < expected_y:
            below_counter = below_counter + 1
            below_points = np.append(below_points, [[x, y]], axis=0)
        else:
            print("not in range")
            range_counter += 1

    print("above=", above_counter)
    print("below=", below_counter)
    print("t(below) =",t)
    # print("not in range =", range_counter)

    solutions = np.stack(random_individuals)
    xpoints = solutions[:, 0]
    ypoints = solutions[:, 1]

    plt.scatter(xpoints, ypoints)

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.plot(x1, y1, color="green")

    # plt.show()

    return np.array([below_points, above_points], dtype=object)


woa_res = graph(woa.woaOptimizer)
cma_res = graph(cmaes.cmaesOptimizer)
a = len(woa_res[0])
b = len(cma_res[0])
c = len(woa_res[1])
d = len(cma_res[1])

table = PrettyTable()
table.field_names = ["", "woa", "cma-es"]
table.add_row(["below", a, b])
table.add_row(["above", c, d])

ban = BarnardTest(a, b, c, d)
pval = ban.p_value()
p_val = stats.barnard_exact([[a, b], [c, d]])
print(table)
print("p-value= ", p_val.pvalue)
print("p-value= ", pval)


a = len(woa_res[0])
b = 250
c = len(woa_res[1])
d = 250

table = PrettyTable()
table.field_names = ["", "woa", "norm"]
table.add_row(["below", a, b])
table.add_row(["above", c, d])


ban = BarnardTest(a, b, c, d)
pval = ban.p_value()
p_val = stats.barnard_exact([[a, b], [c, d]])
print(table)
print("p-value= ", p_val.pvalue)
print("p-value= ", pval)


a = len(cma_res[0])
b = 250
c = len(cma_res[1])
d = 250

table = PrettyTable()
table.field_names = ["", "cma", "norm"]
table.add_row(["below", a, b])
table.add_row(["above", c, d])

ban = BarnardTest(a, b, c, d)
pval = ban.p_value()
p_val = stats.barnard_exact([[a, b], [c, d]])
print(table)
print("p-value= ", p_val.pvalue)
print("p-value= ", pval)

# graph(cmaes.cmaesOptimizer(bimodal_objective,bounds))
