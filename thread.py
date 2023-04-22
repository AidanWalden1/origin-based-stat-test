import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)

from PyQt5.QtCore import *
from asymmetry_test.asymmetry_test import Asymmetry_tester
from optimizers.cma_es import CMAESOptimizer
from optimizers.EvoloPy_optimzers import EvoloPy_otimizers
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt


cmaes = CMAESOptimizer()
bat = EvoloPy_otimizers('BAT')
cs = EvoloPy_otimizers('CS')
de = EvoloPy_otimizers('DE')
ffa = EvoloPy_otimizers('FFA')
ga = EvoloPy_otimizers('GA')
gwo = EvoloPy_otimizers('GWO')
hho = EvoloPy_otimizers('HHO')
jaya = EvoloPy_otimizers('JAYA')
mfo = EvoloPy_otimizers('MFO')
mvo = EvoloPy_otimizers('MVO')
pso = EvoloPy_otimizers('PSO')
sca = EvoloPy_otimizers('SCA')
ssa = EvoloPy_otimizers('SSA')
woa = EvoloPy_otimizers('WOA')



class WorkerThread(QObject):
    update_label = pyqtSignal(str)
    finishedTest = pyqtSignal(object,object,object,object)
    progress = pyqtSignal(int)
    data_ready = pyqtSignal(str)
    asymmetry_test = Asymmetry_tester()
    alg = ''
    iterations = 0
    numruns = 500
    popsize = 0

    def setAlg(self, alg):
        self.alg = alg
    def setIterations(self, iterations):
        self.iterations = iterations
    def getIterations(self,optimizer):
        obj = globals()[optimizer]
        return obj.iterations
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
            self.update_label.emit(f"running {self.alg} {self.numruns} times with {self.iterations} iterations and {self.popsize} popsize")
        except ValueError:
            self.update_label.emit(f"running {self.alg} {self.numruns} times with {self.iterations} iterations and default popsize")
        try:
            fig, p_value, individuals = self.asymmetry_test.asymmetry_test(method)
            self.finishedTest.emit(fig,p_value,selected_alg,individuals)
        except Exception as e:
            if type(e) == IndexError or IndexError:
                self.update_label.emit("It looks like every run of the algorithm tended to the same maxima!!")
                self.finishedTest.emit(0,0,0,0)
            else:
                self.update_label.emit(e)
                self.finishedTest.emit(0,0,0,0)

    def stop(self):
        self.running = False
        self.quit()