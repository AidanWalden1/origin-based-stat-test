import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

x1 = x2 = np.linspace(-20, 20, 100)
X1, X2 = np.meshgrid(x1, x2)
Z = (X1 - 5)**2 + (X2 - 5)**2

ax.plot_surface(X1, X2, Z, cmap='viridis')
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('f(x1, x2)')
ax.set_title('Function f(x1, x2) = (x1 - 5)^2 + (x2 - 5)^2')

plt.show()