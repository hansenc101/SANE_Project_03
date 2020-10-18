import sys
import random
from PyQt5 import QtWidgets,uic
from PyQt5.QtCore import QThread
import requests
#r = requests.get('http://10.0.2.5:5000/time')
#print (r.json())

#r = requests.post('http://10.0.2.5:5000/set_text', json={"button":"OC", "status":"CENG 4113/5113"})
#if r.ok:
#    print (r.json())
    #====================== New Code =========================================
ah_Count = 0 # Number of ahs

class FlaskClient(QThread):
    def run(self):
        r = requests.post('http://10.0.2.5:5000/set_text', json={"button":"OC", "ahCount":str(ah_Count), "status":"CENG 4113/5113"})
        if r.ok:
            print(r.json())
        

def Quit():
    thread.terminate()
    thread.wait()
    App.quit()

def Handle_Increment_Click():
    global ah_Count
    ah_Count = ah_Count + 1

    UI.lblOutput.setText("Clicked " + str(ah_Count) + " times")
    r = requests.post('http://10.0.2.5:5000/set_text', json={"button":"OC", "ahCount":str(ah_Count), "status":"CENG 4113/5113"})

def Handle_Decrement_Click():
    global ah_Count
    ah_Count = ah_Count - 1

    BG_Color = "rgb(" + str(random.randint(0,255)) + "," + str(random.randint(0,255)) + "," + str(random.randint(0,255)) + ");"
    FG_Color = "rgb(255,255,255);"

    UI.lblOutput.setText("Clicked " + str(ah_Count) + " times")
    UI.lblOutput.setStyleSheet("QLabel {background-color :" + BG_Color + "color : " + FG_Color + "}")
    r = requests.post('http://10.0.2.5:5000/set_text', json={"button":"OC", "ahCount":str(ah_Count), "status":"CENG 4113/5113"})

def Handle_Color_Adjust():
    BG_Color = "rgb(" + str(UI.redSlider.value()) + "," + str(UI.greenSlider.value()) + "," + str(UI.blueSlider.value()) + ");"
    FG_Color = "rgb(255,255,255);"
    UI.lblOutput.setStyleSheet("QLabel {background-color :" + BG_Color + "color : " + FG_Color + "}")
    r = requests.post('http://10.0.2.5:5000/set_color', json={"red":str(UI.redSlider.value()), "green":str(UI.greenSlider.value()) , "blue":str(UI.blueSlider.value())})

App = QtWidgets.QApplication([]) # Instantiate the application
UI=uic.loadUi("demo_flask_client.ui") # Load in client user interface: demo_flask_client.ui

UI.incrementBtn.clicked.connect(Handle_Increment_Click) # Connect Handle_Increment_Click to incrementBtn
UI.decrementBtn.clicked.connect(Handle_Decrement_Click) # Connect Handle_Decrement_Click to decrementBtn
UI.actionQuit.triggered.connect(Quit) # Quit the application
UI.redSlider.valueChanged.connect(Handle_Color_Adjust)
UI.greenSlider.valueChanged.connect(Handle_Color_Adjust)
UI.blueSlider.valueChanged.connect(Handle_Color_Adjust)

UI.show() # Display the ui

thread = FlaskClient() # Instantiate the thread
thread.start() # Begin the thread

sys.exit(App.exec_()) # Exit