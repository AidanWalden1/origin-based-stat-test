import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)

from PyQt5.QtCore import *
from asymmetry_test.asymmetry_test import Asymmetry_tester

# Finally, run your long-running function on a separate thread to prevent it from freezing your app. You can do this using the QThread class:

# python

#     from PyQt5.QtCore import QThread

#     class MyThread(QThread):
#         def run(self):
#             worker = Worker()
#             worker.progress.connect(progress_bar.setValue)
#             worker.run_algorithm()
            
#     thread = MyThread()
#     thread.start()

#     Here, we define a custom MyThread class that inherits from QThread. Inside the run() method, we create an instance of the Worker object and connect its progress signal to the progress bar's setValue() method. We then call the run_algorithm() method of the Worker object. Finally, we create an instance of the MyThread object and start it. This will run your long-running function on a separate thread, preventing it from freezing your app.

# That's it! With these steps, you should be able to track the progress of your long-running function and display it in your PyQt5 app using a progress bar.

class TestThread(QThread):
    result_ready = pyqtSignal(object)
    asymmetry_test = Asymmetry_tester()
    
    def __init__(self, obj_name, method_name, args=(), kwargs={}, parent=None):
        super().__init__(parent)
        self.obj_name = obj_name
        self.method_name = method_name
        self.result = None

    def run_optimize(obj, method):
        # get the function reference
        optimize_func = getattr(obj, method)
        
        # call the function
        fig, p_value = Asymmetry_tester.asymmetry_test(optimize_func)
        
        # return the result
        return (fig, p_value)

    def set_obj(self, obj_name):
        self._obj = globals()[obj_name]
    
    def set_method(self, method_name):
        self._method = getattr(self._obj, method_name)
    
    def run(self):
        result = self.run_optimize(self.obj, self.method)