import sys
import random
from PyQt5 import QtWidgets,uic
from PyQt5.QtCore import QThread

import flask
import time

class FlaskServer(QThread):
    app = flask.Flask(__name__)
    app.config["DEBUG"] = False

    def run(self):
       self.app.run(host='0.0.0.0')

    @app.route('/', methods=['GET'])
    def Home():
        return "<h1>Hello, World!</h1><p>This webserver is working!</p>"

    @app.route('/time', methods=['GET'])
    def Get_Time():
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        return flask.jsonify(Current_Time=current_time)

    @app.route('/set_text', methods=['POST'])
    def Set_Text():
        print (flask.request.json)
        UI.btnCalculate.setText(flask.request.json['button']) # Get the text for the field 'button'
        UI.statusbar.showMessage(flask.request.json['status']) # Get the text for the field 'status'
        UI.lblOutput.setText("Ah Count: " + flask.request.json['ahCount']) # Get the text for the field 'ahCount'
        return flask.jsonify(flask.request.json)

    @app.route('/set_color', methods=['POST'])
    def Set_Color():
        BG_Color = "rgb(" + str(flask.request.json['red']) + "," + str(flask.request.json['green']) + "," + str(flask.request.json['blue']) + ");"
        FG_Color = "rgb(255,255,255);"

        UI.lblOutput.setStyleSheet("QLabel {background-color :" + BG_Color + "color : " + FG_Color + "}")
        return flask.jsonify(flask.request.json)


Click_Count = 0

def Quit():
    thread.terminate()
    thread.wait()
    App.quit()

def Handle_Click():
    global Click_Count
    Click_Count = Click_Count + 1

    BG_Color = "rgb(" + str(random.randint(0,255)) + "," + str(random.randint(0,255)) + "," + str(random.randint(0,255)) + ");"
    FG_Color = "rgb(255,255,255);"

    UI.lblOutput.setText("Clicked " + str(Click_Count) + " times")
    UI.lblOutput.setStyleSheet("QLabel {background-color :" + BG_Color + "color : " + FG_Color + "}")

App = QtWidgets.QApplication([])
UI=uic.loadUi("demo_flask_server.ui")

UI.btnCalculate.clicked.connect(Handle_Click)
UI.actionCalculate.triggered.connect(Handle_Click)
UI.actionQuit.triggered.connect(Quit)

UI.show()

thread = FlaskServer()
thread.start()

sys.exit(App.exec_())