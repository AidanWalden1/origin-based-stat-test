from asymmetry_test.asymmetry_test import Asymmetry_tester
import numpy as np
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import shutil
from add_alg_dialog import AddAlgorithmDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
import matplotlib.pyplot as plt
import importlib
from optimizers.EvoloPy_optimzers import EvoloPy_otimizers
from optimizers.cma_es import CMAESOptimizer
from optimizers.woa import WoaOptimizer
from thread import WorkerThread
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QWidget, QVBoxLayout
from obj_function import Obj_function
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)


global iterations


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        selected_alg = None
        iterations = 30
        individuals = []

        # initiates all of the GUI features
        self.xmin, self.xmax = -5, 15
        self.ymin, self.ymax = -15, 5
        self.bounds = [[self.xmin, self.xmax], [self.ymin, self.ymax]]

        self.validator = QIntValidator()
        self.canvas = FigureCanvas(plt.Figure())
        self.setCentralWidget(self.canvas)
        self.second_canvas = FigureCanvas(Figure())

        label2 = QLabel("Enter iterations:")
        self.iterationBox = QLineEdit(self)
        self.iterationBox.setValidator(self.validator)

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
        self.combobox.currentIndexChanged.connect(
            self.on_combo_box_index_changed)
        self.combobox.addItems(['CMAES', 'BAT', 'CS', 'DE', 'FFA', 'GA',
                               'GWO', 'HHO', 'JAYA', 'MFO', 'MVO', 'PSO', 'SCA', 'SSA', 'WOA',])

        self.label = QLabel(self)
        self.label2 = QLabel(self)

        self.button = QPushButton("Test for asymmetry", self)
        self.button.move(10, 10)
        self.button.clicked.connect(self.on_button_clicked)

        # self.addOptimizerBtn = QPushButton("Add optimizer", self)
        # self.addOptimizerBtn.clicked.connect(self.showDialog)

        self.progress_bar = QProgressBar(self)

        self.position_label = QLabel()
        self.statusBar().addWidget(self.position_label)

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
        # param_choosers.addWidget(self.addOptimizerBtn)

        canvas1 = QVBoxLayout()
        canvas1.addWidget(self.canvas)
        canvas1.addWidget(self.label)

        canvas2 = QVBoxLayout()
        canvas2.addWidget(self.second_canvas)
        canvas2.addWidget(self.label2)


        canvasLayout = QHBoxLayout()
        canvasLayout.addLayout(canvas1)
        canvasLayout.addLayout(canvas2)

        # add the Matplotlib canvas widget to the main window
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addLayout(param_choosers)
        layout.addLayout(canvasLayout)
        layout.addWidget(self.button)
        layout.addWidget(self.progress_bar)
        self.setCentralWidget(central_widget)

    def on_button_clicked(self):
        global selected_alg
        global iterations
        # starts worker thread to run tester function
        iterations = self.iterationBox.text()
        num_runs = int(self.NumRunsBox.text())
        popsize = self.popSizeBox.text()
        selected_alg = selected_alg.lower()

        self.label.setText("")
        self.label2.setText("")


        self.thread = QThread()
        self.worker = WorkerThread()
        self.worker.setAlg(selected_alg)
        self.worker.setIterations(iterations)
        self.worker.setNumRuns(num_runs)
        self.worker.setPopsize(popsize)
        self.button.setEnabled(False)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.asymmetry_test.progress_update.connect(self.update_progress_bar)
        self.worker.update_label.connect(self.update_label_text)
        self.worker.progress.connect(self.progress_bar.setValue)
        # Waits for thread to finish and then runs functions
        self.worker.finishedTest.connect(self.on_worker_finished)
        self.worker.finishedTest.connect(self.thread.quit)

        self.thread.start()

    def on_combo_box_index_changed(self, index):
        # Updates global variables when combo box changes
        global selected_alg
        global iterations

        selected_alg = self.combobox.currentText()

        selected = selected_alg.lower()

        self.thread = WorkerThread()

        iterations = self.thread.getIterations(selected)

        self.iterationBox.setText(str(iterations))

        self.popSizeBox.setText("")

    def on_figure_hover(self, event):
        # Keeps track of mouse when it hovers over an x value on the graph.
        x = event.xdata
        if x is not None:
            x = int(x)
            self.position_label.setText(
                f'press to see all best indivdual a t= {str(x)}')
        else:
            self.position_label.setText('')

    def on_figure_clicked(self, event):
        # sends x data to function that spawns grpah
        global individuals
        individuals_at_t = []
        x = event.xdata
        if x is not None:
            x = int(x)
            for i in individuals:
                individuals_at_t.append(i[x])
            self.create_second_canvas(individuals_at_t,x)
        else:
            pass

# Obsolete function. feature not finished
    def showDialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Select file', os.getenv('HOME'), 'Python files (*.py)')
        if filename:
            print('Selected file:', filename)
            algorithm_dialog = AddAlgorithmDialog(filename)
            if algorithm_dialog.exec_() == QDialog.Accepted:
                algorithm_name = algorithm_dialog.line_edit.text()
                dest_folder = parent_dir + '\\MMP\\AddOptimizers'
                dest_file = os.path.join(dest_folder, f'{algorithm_name}.py')
                try:
                    shutil.copy(filename, dest_file)
                    QMessageBox.information(
                        self, 'Success', 'File saved successfully.')
                    self.combobox.addItem(algorithm_name)

                except Exception as e:
                    QMessageBox.critical(
                        self, 'Error', f'Error saving file: {str(e)}')

    def on_worker_finished(self, fig, p_value, alg_name, all_individuals):
        # makes graph with data from thread whhen the worker is finished
        global individuals
        self.button.setEnabled(True)
        if fig == 0:
            return

        self.canvas.figure.clear()
        self.canvas.figure = fig
        self.canvas.draw()
        self.canvas.mpl_connect('motion_notify_event', self.on_figure_hover)
        self.canvas.mpl_connect('button_press_event', self.on_figure_clicked)
        self.label.setText(f"The p-value of {alg_name} is {str(p_value)}")
        individuals = all_individuals

        self.popSizeBox.setText("")

    def create_second_canvas(self,individuals_at_t,t): 
        # draws second canvas using values returned from thread that are held in a glboal variable

        obj_fun = Obj_function(self.bounds)

        above_counter = 0
        below_counter = 0
        range_counter = 0

        above_points = np.empty((0, 2), float)
        below_points = np.empty((0, 2), float)

        for point in individuals_at_t:
            x = point[0]
            y = point[1]
            expected_y = obj_fun.get_expected_y(x)

            if y > expected_y:
                above_counter = above_counter + 1
                above_points = np.append(above_points, [[x, y]], axis=0)
            elif y < expected_y:
                below_counter = below_counter + 1
                below_points = np.append(below_points, [[x, y]], axis=0)
            else:
                range_counter += 1
        self.label2.setText("")
        self.label2.setText(f"There is {above_counter} points above the line and {below_counter} points below the line at t={t}")
        solutions = np.stack(individuals_at_t)
        xpoints = solutions[:, 0]
        ypoints = solutions[:, 1]
          
        new_fig = plt.Figure()
        new_ax = new_fig.add_subplot(111)
        new_ax.scatter(xpoints, ypoints)
        new_ax.set_xlim(self.xmin, self.xmax)
        new_ax.set_ylim(self.ymin, self.ymax)
        new_ax.plot(obj_fun.x1, obj_fun.y1, color="green")
        self.second_canvas.figure.clear()
        self.second_canvas.figure = new_fig
        self.second_canvas.draw()

# updated progress bar
    @pyqtSlot(int)
    def update_progress_bar(self, progress):
        self.progress_bar.setValue(progress)
# updates label
    @pyqtSlot(str)
    def update_label_text(self, text):
        self.label.setText(text)


if __name__ == '__main__':
    global selected_alg
    selected_alg = ''
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.setFixedHeight(600)
    window.setGeometry(100, 100, 1200, 480)
    window.show()
    sys.exit(app.exec_())
