import numpy as np
from EvoloPy import *
from EvoloPy.optimizer import run

class EvoloPy_otimizers:
    def __init__(self,optimzer,popsize = 50,iterations=30):
        self.optimizer = optimzer
        self.popsize = popsize
        self.iterations = iterations

    @property
    def iterations(self):
        return self._iterations

    @iterations.setter
    def iterations(self, value):
        self._iterations = value

    @property
    def popsize(self):
        return self._popsize

    @popsize.setter
    def popsize(self, value):
        self._popsize = value
    


    # Select benchmark function"
    # "F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12","F13","F14","F15","F16","F17","F18","F19"
    # "Ca1","Ca2","Gt1","Mes","Mef","Sag","Tan","Ros"
    objectivefunc = ["objFunc"]

    # Select number of repetitions for each experiment.
    # To obtain meaningful statistical results, usually 30 independent runs are executed for each algorithm.
    NumOfRuns = 1

    # Select general parameters for all optimizers (population size, number of iterations) ....


    # Choose whether to Export the results in different formats
    export_flags = {
        "Export_avg": False,
        "Export_details": False,
        "Export_convergence": False,
        "Export_boxplot": False,
    }

    def optimize(self,bounds,obj_func):
        self.params = {"PopulationSize": self.popsize, "Iterations": self.iterations}
        # print(self.popsize)
        res = run([self.optimizer], self.objectivefunc, self.NumOfRuns, self.params, self.export_flags)
        return res[0][1],res[0][0]
 
        


       