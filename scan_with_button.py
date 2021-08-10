from qtpy.QtWidgets import *
import ophyd

import sys
from bluesky_widgets.models.auto_plot_builders import AutoLines

from bluesky.plans import scan
from ophyd.sim import motor, det, det1
from ophyd import EpicsMotor
from ophyd import Device, EpicsSignal, EpicsSignalRO
from bluesky_widgets.utils.streaming import stream_documents_into_runs
from bluesky import RunEngine
from bluesky_widgets.qt.figures import QtFigures
from bluesky_widgets.qt.threading import wait_for_workers_to_quit


testdevice1 = ophyd.Device(name="det")

keithley6517_current = EpicsSignal("EMILEL:test:rdCurE3", name="keithley6517_current", labels=("detectors"))
geek_list = ["Select one...", testdevice1.name, keithley6517_current.name]
m1_sim = EpicsMotor('IOCsim:m1', name='m1', labels=("motors",))

app = QApplication(["Scan App Version 1"])
def plan():
    yield from scan([det], motor, -1, 1, 4)
    
def plan1():
    yield from scan([keithley6517_current], m1_sim, -10, 10, 10)
    
class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button = QPushButton("Scan")
        self.button.clicked.connect(self.on_clicled)   
       
        #lable = QLabel()
        #lable.setText("TutorialsPoint")
        
        self.lineEdit = QLineEdit()
        self.current_text = None                                                         # +++
        
        self.combo = QComboBox(self)
        self.combo.addItems(geek_list)
        self.combo.currentTextChanged.connect(self.on_combobox_func)       
 
        
        v_box = QVBoxLayout()
        v_box.addWidget(self.button)
        v_box.addStretch()
        v_box.addWidget(self.combo)
         

        self.h_box = QHBoxLayout(self)
        self.h_box.addLayout(v_box)
        self.h_box.addWidget(self.lineEdit)  
        
    def on_combobox_func(self, text):                                                    # +++
        self.current_text  = text 
        
    def on_clicled(self):    
    # Add a tabbed pane of figures to the app.
        
    # When the model receives data or is otherwise updated, any changes to
    # model.figures will be reflected in changes to the view.

    # Just for this example, generate some data before starting this app.
    # Again, in practice, this should happen in a separate process and send
    # the results over a network.   
        app.aboutToQuit.connect(wait_for_workers_to_quit)
        if self.current_text == "det":
            print("det is chosen, scan det")
            self.lineEdit.setText("scan det, please wait..") 
            self.h_box.addWidget(view)
            RE(plan())
        elif self.current_text == "keithley6517_current":
            print("det1 is chosen, scan keithley7517 current")
            self.lineEdit.setText("scan keithley6517 current, please wait...")
            self.h_box.addWidget(view)
            RE(plan1())
        
        else:
            self.lineEdit.setText("Select one detector...") 
if __name__ == '__main__':
    demo = Widget()
    
    model = AutoLines(max_runs=1)
    RE = RunEngine()
    RE.subscribe(stream_documents_into_runs(model.add_run))
    view = QtFigures(model.figures) 
    
   
    demo.show()
    sys.exit(app.exec_())


