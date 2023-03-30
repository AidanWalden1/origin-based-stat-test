import numpy as np
class Obj_function:
    def __init__(self,bounds):
        self.bounds = bounds
        xmin, xmax, ymin, ymax = bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1]
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

        self.x1 = x1
        self.y1 = y1

        self.x3 = x3*2
        self.y3 = y3*2

        self.m1 = m1
        self.b1 = b1

    @property
    def x1_prop(self):
        return self.x1
    @property
    def y1_prop(self):
        return self.y1

    def get_expected_y(self,x):
        return self.m1 * x + self.b1

    def bimodal_objective(self, x):
        x1, x2 = x
        x3 = self.x3
        y3 = self.y3
        f1 = (x1 - 0)**2 + (x2 - 0)**2
        f2 = (x1 - x3)**2 + (x2 - y3)**2
        f = np.minimum(f1, f2)
        return f