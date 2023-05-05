import numpy as np


class Obj_function:
    def __init__(self, bounds):
        self.bounds = bounds 
        # Extract xmin, xmax, ymin, ymax values from bounds array
        xmin, xmax, ymin, ymax = bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1]

        # Calculate slope and y-intercept for the line passing through (xmin, ymin) and (xmax, ymax)
        m1 = (ymax - ymin) / (xmax - xmin)
        b1 = (ymax - (m1 * xmax))

        # Generate an array of x values from xmin to xmax using linspace function from numpy
        x1 = np.linspace(xmin, xmax)

        # Calculate corresponding y values for the line passing through (xmin, ymin) and (xmax, ymax)
        y1 = m1 * x1 + b1

        # Calculate slope and y-intercept for the line perpendicular to the previous line, passing through (xmin, 0)
        m2 = -1 * m1
        b2 = 0

        # Generate an array of x values from xmin to xmax using linspace function from numpy
        x2 = np.linspace(xmin, xmax)

        # Calculate corresponding y values for the perpendicular line passing through (xmin, 0)
        y2 = m2 * x2 + b2

        # Calculate the intersection point of the two lines using the slope-intercept form of the equations
        x3 = (b2 - b1) / (m1 - m2)
        y3 = m1 * x3 + b1

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
        # Returns bi modal objective function based on bounds
        x1, x2 = x
        x3 = self.x3
        y3 = self.y3
        f1 = (x1 - 0)**2 + (x2 - 0)**2
        f2 = (x1 - x3)**2 + (x2 - y3)**2
        f = np.minimum(f1, f2)
        return f