from cmaes import CMA
import numpy as np

import matplotlib.pyplot as plt

# target = np.array((0.75,0.75))
# def evaluate(point):
#     return np.sqrt(((point-target)**2).sum())

# optimizer = CMA(mean=np.array([0.5,0.5]),bounds=np.array([[0,1],[0,1]]),sigma=0.5,n_max_resampling=1)
# generations = 16
# sqrt = int(np.sqrt(generations))
# fig, axs = plt.subplots(sqrt,sqrt,num="CMA-ES",sharex=True,sharey=True)
# points = np.ndarray((generations,optimizer.population_size,2))
# for g in range(generations):
#     solutions = []
#     for i in range(optimizer.population_size):
#         point = optimizer.ask()
#         points[g,i] = point
#         score = evaluate(point)
#         solutions.append((point,score))
#     optimizer.tell(solutions)

# for i in range(generations):
#     ax = axs[i//sqrt,i%sqrt]
#     ax.scatter(*zip(*points[i]),c="b")
#     ax.scatter(*target,c="r")
#     ax.set_xlim([0,1])
#     ax.set_ylim([0,1])

# plt.show()

# optimizer = CMA(mean=np.array([0.5,0.5]),bounds=np.array([[0,1],[0,1]]),sigma=0.5,n_max_resampling=1)
# for i in range(optimizer.population_size):
#     point = optimizer.ask()
#     print(point,evaluate(point), end= '\n')

def quadratic(x1, x2):
    return (x1 - 3) ** 2 + (10 * (x2 + 2)) ** 2

if __name__ == "__main__":
    optimizer = CMA(mean=np.zeros(2), sigma=1.3)

    for generation in range(50):
        solutions = []
        for _ in range(optimizer.population_size):
            x = optimizer.ask()
            value = quadratic(x[0], x[1])
            solutions.append((x, value))
            print(f"#{generation} {value} (x1={x[0]}, x2 = {x[1]})")
        optimizer.tell(solutions)