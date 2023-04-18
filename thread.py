import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)

from PyQt5.QtCore import *
from asymmetry_test.asymmetry_test import Asymmetry_tester
from optimizers.cma_es import CMAESOptimizer
from optimizers.EvoloPy_optimzers import EvoloPy_otimizers

tester = Asymmetry_tester()

cmaes = CMAESOptimizer()
bat = EvoloPy_otimizers('BAT')
cs = EvoloPy_otimizers('CS')
de = EvoloPy_otimizers('DE')
ffa = EvoloPy_otimizers('FFA')
hho = EvoloPy_otimizers('HHO')
jaya = EvoloPy_otimizers('JAYA')
woa = EvoloPy_otimizers('WOA')



class WorkerThread(QObject):
    finished = pyqtSignal(object)
    asymmetry_test = Asymmetry_tester()
    alg = ''

    def setAlg(self, alg):
        self.alg = alg

    def run(self):
        selected_alg = self.alg.lower()
        obj = globals()[selected_alg]
        method = getattr(obj, "optimize")
        print("inside thread")
        fig, p_value = tester.asymmetry_test(method)
        print('done')
        print(self.finished)
        self.finished.emit()
