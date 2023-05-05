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
    


    objectivefunc = ["objFunc"]

    # Select number of repetitions for each experiment.
    # Number of runs choesn in tester class not here. This is requred for package to work
    NumOfRuns = 1

    # Select general parameters for all optimizers (population size, number of iterations) ....

    # Choose whether to Export the results in different formats
    export_flags = {
        "Export_avg": False,
        "Export_details": False,
        "Export_convergence": False,
        "Export_boxplot": False,
    }

    # Runs algorithm once

    def optimize(self,bounds,obj_func):
        self.params = {"PopulationSize": self.popsize, "Iterations": self.iterations}
        res = run([self.optimizer], self.objectivefunc, self.NumOfRuns, self.params, self.export_flags)
        return res[0][1],res[0][0]
 
        


       