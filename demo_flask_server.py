import sys
import random
from PyQt5 import QtWidgets,uic
from PyQt5.QtCore import QThread

import flask
import time

class FlaskServer(QThread):
    app = flask.Flask(__name__) # instantiate the flask application
    app.config["DEBUG"] = False # Set DEBUG to False so others can access the web server

    def run(self):
       self.app.run(host='0.0.0.0') # Allow anyone on the network to connect to the web server

    @app.route('/', methods=['GET'])
    def Home():
        return "<h1>Hello, World!</h1><p>This webserver is working!</p>" # Output that verifies the webserver is working

    @app.route('/time', methods=['GET']) # run Get_Time when the client requests to post to http://10.0.2.5:5000/time
    # This function will return the current time from the web server
    def Get_Time():
        t = time.localtime() # get time from system
        current_time = time.strftime("%H:%M:%S", t)
        return flask.jsonify(Current_Time=current_time)


    @app.route('/set_text', methods=['POST']) # run Set_Text when the client requests to post to http://10.0.2.5:5000/set_text
    # This function will update the text fields for the server gui
    def Set_Text(): 
        print (flask.request.json) 
        UI.statusbar.showMessage(flask.request.json['status']) # Get the text for the field 'status'
        UI.lblOutput.setText("Ah Count: " + flask.request.json['ahCount']) # Get the text for the field 'ahCount'
        return flask.jsonify(flask.request.json) # return json object

    @app.route('/set_color', methods=['POST']) # run Set_Color when the client requests to post to http://10.0.2.5:5000/set_color
    # This function will update the lblOutput colors, based upon the values set by the client
    def Set_Color():
        redColorValue = flask.request.json['red'] # Get the current red rgb value from client
        greenColorValue = flask.request.json['green'] # Get the current green rgb value from client
        blueColorValue = flask.request.json['blue'] # Get the current blue rgb value from client
        BG_Color = "rgb(" + str(redColorValue) + "," + str(greenColorValue) + "," + str(blueColorValue) + ");" # set the background variable to the values read in from client
        FG_Color = "rgb(255,255,255);" # set the foreground variable to these values
        UI.lblOutput.setStyleSheet("QLabel {background-color :" + BG_Color + "color : " + FG_Color + "}") # Set the colors of the QLabel widget using values from BG_Color and FG_Color
        UI.redMagLabel.setText("Red:   " + str(redColorValue)) # Output the current value of red rgb background color from client
        UI.greenMagLabel.setText("Green: " + str(greenColorValue)) # Output the current value of green rgb background color from client
        UI.blueMagLabel.setText("Blue:  " + str(blueColorValue)) # Output the current value of blue rgb background color from client
        return flask.jsonify(flask.request.json) # return json object


ah_Count = 0 # This will hold the current ah_Count
redColorValue = 0 # This will hold the current value of red for the rgb background color
greenColorValue = 0 # This will hold the current value of green for the rgb background color
blueColorValue = 0 # This will hold the current value of blue for the rgb background color

# Function to stop the thread and quit the application
def Quit():
    thread.terminate()
    thread.wait()
    App.quit()


App = QtWidgets.QApplication([]) # instantiate application
UI=uic.loadUi("demo_flask_server.ui") # load in server ui

UI.actionQuit.triggered.connect(Quit) # connect quit function to action actionQuit

UI.show() # Display the user interface
UI.lblOutput.setText("Ah Counter Disconnected") # Set the initial text in lblOutput to indicate no client is connected
thread = FlaskServer() # instantiate a thread of FlaskServer
thread.start() # Begin processing the thread

sys.exit(App.exec_()) # Exit the program