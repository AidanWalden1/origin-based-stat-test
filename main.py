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
from PyQt5.QtCore import pyqtSlot

global iterations

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
        iterations = 30
        self.validator = QIntValidator()

        # create a Matplotlib canvas widget
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        label2 = QLabel("Enter iterations:")
        self.iterationBox = QLineEdit(self)
        self.iterationBox.setValidator(self.validator)
        self.iterationBox.setText(str(cmaes.iterations))
        
        label3 = QLabel("Enter population size:")
        self.popSizeBox = QLineEdit(self)
        self.popSizeBox.setValidator(self.validator)
        self.popSizeBox.setText("")

        label4 = QLabel("Enter number of runs:")
        self.NumRunsBox = QLineEdit(self)
        self.NumRunsBox.setValidator(self.validator)
        self.NumRunsBox.setText("500")

        label1 = QLabel("Choose algorithm:")
        self.combobox = QComboBox(self)
        self.combobox.currentIndexChanged.connect(self.on_combo_box_index_changed)
        self.combobox.addItems(['CMAES', 'BAT', 'CS','DE','FFA','HHO','JAYA','WOA'])

        self.label = QLabel(self)

        
        self.button = QPushButton("Test for asymmetry", self)
        self.button.move(10, 10)
        self.button.clicked.connect(self.on_button_clicked)

        self.progress_bar = QProgressBar(self)

        param1_layout = QHBoxLayout()
        param1_layout.addWidget(label1)
        param1_layout.addWidget(self.combobox)

        param2_layout = QHBoxLayout()
        param2_layout.addWidget(label2)
        param2_layout.addWidget(self.iterationBox)

        param3_layout = QHBoxLayout()
        param3_layout.addWidget(label3)
        param3_layout.addWidget(self.popSizeBox)

        param4_layout = QHBoxLayout()
        param4_layout.addWidget(label4)
        param4_layout.addWidget(self.NumRunsBox)

        param_choosers = QHBoxLayout()
        param_choosers.addLayout(param1_layout)
        param_choosers.addLayout(param2_layout)
        param_choosers.addLayout(param3_layout)
        param_choosers.addLayout(param4_layout)

        # add the Matplotlib canvas widget to the main window
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addLayout(param_choosers)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        self.setCentralWidget(central_widget)
    



    def on_button_clicked(self):
        global selected_alg
        global iterations
        iterations = self.iterationBox.text()
        num_runs = int(self.NumRunsBox.text())
        popsize = self.popSizeBox.text()
        selected_alg = selected_alg.lower() 
        self.thread = QThread()
        self.worker = WorkerThread()
        self.worker.setAlg(selected_alg)
        self.worker.setIterations(iterations)
        self.worker.setNumRuns(num_runs)
        self.worker.setPopsize(popsize)



        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.asymmetry_test.progress_update.connect(self.update_progress_bar)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.update_label.connect(self.update_label_text)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.on_worker_finished)
        
        self.thread.start()
        
    def on_combo_box_index_changed(self,index):
        global selected_alg
        global iterations 
        selected_alg = self.combobox.currentText()

        selected = selected_alg.lower()
        obj = globals()[selected]
    
        iterations = obj.iterations
        self.iterationBox.setText(str(iterations))

        self.popSizeBox.setText("")

    def on_worker_finished(self, fig, p_value,alg_name):
        if fig == 0:
            return
        
        self.canvas.figure.clear()
        self.canvas.figure = fig
        self.canvas.draw()
        self.label.setText(f"The p-value of {alg_name} is {str(p_value)}")

        self.popSizeBox.setText("")

    @pyqtSlot(int)
    def update_progress_bar(self, progress):
        self.progress_bar.setValue(progress)

    @pyqtSlot(str)
    def update_label_text(self, text):
        self.label.setText(text)



if __name__ == '__main__':
    global selected_alg
    selected_alg = ''
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.setFixedHeight(700)
    window.setGeometry(100, 100, 640, 480)
    window.show()
    sys.exit(app.exec_())
