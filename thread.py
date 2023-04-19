import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)

from PyQt5.QtCore import *
from asymmetry_test.asymmetry_test import Asymmetry_tester
from optimizers.cma_es import CMAESOptimizer
from optimizers.EvoloPy_optimzers import EvoloPy_otimizers


cmaes = CMAESOptimizer()
bat = EvoloPy_otimizers('BAT')
cs = EvoloPy_otimizers('CS')
de = EvoloPy_otimizers('DE')
ffa = EvoloPy_otimizers('FFA')
hho = EvoloPy_otimizers('HHO')
jaya = EvoloPy_otimizers('JAYA')
woa = EvoloPy_otimizers('WOA')



class WorkerThread(QObject):
    update_label = pyqtSignal(str)
    finished = pyqtSignal(object,object,object)
    progress = pyqtSignal(int)
    asymmetry_test = Asymmetry_tester()
    alg = ''
    iterations = 0
    numruns = 500
    popsize = 0

    def setAlg(self, alg):
        self.alg = alg
    def setIterations(self, iterations):
        self.iterations = iterations
    def setNumRuns(self, numruns):
        self.numruns = numruns
    def setPopsize(self, popsize):
        self.popsize = popsize

    def run(self):
        self.asymmetry_test.runs = self.numruns
        selected_alg = self.alg.lower()
        obj = globals()[selected_alg]
        obj.iterations = int(self.iterations)
        method = getattr(obj, "optimize")
        try:
            obj.popsize = int(self.popsize)
            self.update_label.emit(f"running {self.alg} {self.numruns} times with {self.iterations} iterations and {self.popsize} popsize, remember that running evolo optimzers with custom popsize does not work yet")
        except ValueError:
            self.update_label.emit(f"running {self.alg} {self.numruns} times with {self.iterations} iterations and default popsize")
        try:
            fig, p_value = self.asymmetry_test.asymmetry_test(method)
            self.finished.emit(fig,p_value,selected_alg)
        except TypeError:
            self.update_label.emit("It looks like every run of the algorithm tended to the same maxima!!")
            self.finished.emit(0,0,0)