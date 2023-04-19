import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)

from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from thread import WorkerThread
from asymmetry_test.asymmetry_test import Asymmetry_tester 
from optimizers.woa import WoaOptimizer
from optimizers.cma_es import CMAESOptimizer
from optimizers.EvoloPy_optimzers import EvoloPy_otimizers

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import QThread

tester = Asymmetry_tester()


cmaes = CMAESOptimizer()
bat = EvoloPy_otimizers('BAT')
cs = EvoloPy_otimizers('CS')
de = EvoloPy_otimizers('DE')
ffa = EvoloPy_otimizers('FFA')
hho = EvoloPy_otimizers('HHO')
jaya = EvoloPy_otimizers('JAYA')
woa = EvoloPy_otimizers('WOA')

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        selected_alg = None

        # create a Matplotlib canvas widget
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.label = QLabel(self)
        self.combobox = QComboBox(self)
        self.combobox.currentIndexChanged.connect(self.on_combo_box_index_changed)
        self.combobox.addItems(['CMAES', 'BAT', 'CS','DE','FFA','HHO','JAYA','WOA'])


        self.button = QPushButton("Test for asymmetry", self)
        self.button.move(10, 10)
        self.button.clicked.connect(self.on_button_clicked)

        self.progress_bar = QProgressBar(self)

        # add the Matplotlib canvas widget to the main window
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.combobox)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        self.setCentralWidget(central_widget)

        tester.progress_update.connect(self.progress_bar.setValue)

    def on_button_clicked(self):
        global selected_alg
        selected_alg = selected_alg.lower()
        # self.thread = QThread()
        # self.worker = WorkerThread()
        # self.worker.setAlg(selected_alg)

        # self.worker.moveToThread(self.thread)
        # self.thread.started.connect(self.worker.run)
        # self.worker.finished.connect(self.thread.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(self.progress_bar.setValue)
        # self.thread.start()
            
        obj = globals()[selected_alg]
        method = getattr(obj, "optimize")
        fig, p_value = tester.asymmetry_test(method)

        # clear the canvas and redraw the new graph
        self.canvas.figure.clear()
        self.canvas.figure = fig
        self.canvas.draw()
        self.label.setText(f"The p-value of {selected_alg} is {str(p_value)}")
        
        
    def on_combo_box_index_changed(self,index):
    # update the label when the combo box selection changes
        global selected_alg
        selected_alg = self.combobox.currentText()


if __name__ == '__main__':
    global selected_alg
    selected_alg = ''
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
