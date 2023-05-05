import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QMessageBox, QDialog, QVBoxLayout, QLineEdit, QLabel

# added a class that spawns a diaglog for file upload
# Not used as add optimzer feature was not added
class AddAlgorithmDialog(QDialog,):
    def __init__(self,filename):
        super().__init__()
        self.filename = filename
        self.filename = self.filename.split('/')
        self.filename = self.filename[-1]
        self.filename = self.filename.split('.')[0]
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Enter Algorithm Name')
        self.layout = QVBoxLayout(self)
        self.label = QLabel('Algorithm Name (make sure the name is also the same as the class):', self)
        self.layout.addWidget(self.label)
        self.line_edit = QLineEdit(self)
        self.line_edit.setText(self.filename)
        self.layout.addWidget(self.line_edit)
        self.button_ok = QPushButton('OK', self)
        self.button_ok.clicked.connect(self.accept)
        self.layout.addWidget(self.button_ok)
