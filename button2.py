import sys

from qtpy.QtWidgets import *
from widget_xafs import *

from bluesky_widgets.models.auto_plot_builders import AutoLines
from bluesky.plans import scan
from bluesky_widgets.utils.streaming import stream_documents_into_runs
from bluesky import RunEngine
from bluesky_widgets.qt.figures import QtFigures
from bluesky_widgets.qt.threading import wait_for_workers_to_quit

import ophyd
from ophyd.sim import det, det1
from ophyd import EpicsMotor
from ophyd import Device, EpicsSignal, EpicsSignalRO
def getResult(widget):
    text = widget.text() 
    print("text: ", text)
    print(type(text))
    print(text.encode('utf-8'))
    #return text.encode('utf-8')
    return text

testdevice1 = ophyd.Device(name="det")
keithley6517_current = EpicsSignal("EMILEL:test:rdCurE3", name="keithley6517_current", labels=("detectors"))
geek_list = ["Select one...", testdevice1.name, keithley6517_current.name]

m1 = EpicsMotor('IOCsim:m1', name="m1", labels=("motors",))
app = QApplication(["Scan App Version 1"])

def plan():
    yield from scan([det], motor, -1, 1, 4)
    
def plan1():
    #yield from scan([keithley6517_current], m1_sim, -10, 10, 10)
    yield from scan([keithley6517_current], motor, -10, 10, 10)


def getPlanEditor():
    plan_editor = PlanEditorXafs(model)
    vbox.addWidget(plan_editor, stretch=1)

class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button = QPushButton("Scan")
        self.button.clicked.connect(self.on_clicled)   

        
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
        
        
        self.lableLayout = QVBoxLayout()
        self.parametersLayout= QVBoxLayout()
        self.h_box.addLayout(self.lableLayout)
        self.h_box.addLayout(self.parametersLayout)
        
        l_det = QLabel('Detectors')
        l_mot = QLabel('Motors')
        l1 = QLabel('Start position')
        l2= QLabel('Final position')
        l3= QLabel('Numbers')

        
        self.lableLayout.addWidget(l_det)
        self.lableLayout.addWidget(l_mot)
        self.lableLayout.addWidget(l1)
        self.lableLayout.addWidget(l2)
        self.lableLayout.addWidget(l3)


        self.w1 = QLineEdit()
        self.w2 = QLineEdit()
        self.w3 = QLineEdit()
        self.w4 = QLineEdit()
        self.w5 = QLineEdit()

        self.parametersLayout.addWidget(self.w1)
        self.parametersLayout.addWidget(self.w2)
        self.parametersLayout.addWidget(self.w3)
        self.parametersLayout.addWidget(self.w4)
        self.parametersLayout.addWidget(self.w5)
  
       
        
    def on_combobox_func(self, text):                                                  
        self.current_text  = text 
        
    def on_clicled(self):    
    # Add a tabbed pane of figures to the app.
        
    # When the model receives data or is otherwise updated, any changes to
    # model.figures will be reflected in changes to the view.

    # Just for this example, generate some data before starting this app.
    # Again, in practice, this should happen in a separate process and send
    # the results over a network.   

        if self.current_text == "det":
            print("det is chosen, scan det")
            self.lineEdit.setText("scan det, please wait..") 
            RE(plan())

        elif self.current_text == "keithley6517_current":
            print("det1 is chosen, scan keithley7517 current")
            self.lineEdit.setText("scan keithley6517 current, please wait...")

            RE(plan1())
              
        else:
            det_name = getResult(self.w1)
            mot_name = getResult(self.w2)
            start = getResult(self.w3)
            stop =   getResult(self.w4)
            number = getResult(self.w5)
   
            def plan_custom():
                device_custom = ophyd.Signal(name=det_name)
                motor_custom = EpicsMotor('IOCsim:m1', name=mot_name, labels=("motors",))
                start = getResult(self.w3)
                stop =   getResult(self.w4)
                number = getResult(self.w5)
                yield from scan([device_custom], motor_custom, float(start), float(stop), int(number))

            RE(plan_custom())

            #self.lineEdit.setText("scan {}, please wait...".format(self.detectors))
        self.h_box.addWidget(view)
            
            
if __name__ == '__main__':
    demo = Widget()
    app.aboutToQuit.connect(wait_for_workers_to_quit)
    model = AutoLines(max_runs=2)
  
    RE = RunEngine()
    RE.subscribe(stream_documents_into_runs(model.add_run))
       
    view = QtFigures(model.figures) 
    
    demo.show()
    sys.exit(app.exec_())


