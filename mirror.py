# -*- coding: utf-8 -*-
import sys
import json
import os
import importlib
from inspect import signature
from inspect import ismethod

#import cv2
#http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/
#used that to install opencv
#I did not use virtualenvs, and instead changed a line when you cmake
#-D PYTHON_EXECUTABLE=/usr/bin/python

from time import sleep
import threading

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# Importing the widget base classes
from Widgets.CollapsedWidget import CollapsedWidget
from Widgets.ExpandedWidget import ExpandedWidget

import speech_recognition as sr

class speechRecognitionThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        r = sr.Recognizer()
        m = sr.Microphone()
        r.energy_threshold = 5500
        r.non_speaking_duration = 0.2
        r.pause_threshold = 0.3

        while True:
            with sr.Microphone() as source:
                try:
                    audio = r.listen(source, phrase_time_limit=2)
                except sr.WaitTimeoutError as we:
                    continue
            BING_KEY = "11a5b6e3266f434ca89758db27105b2c" # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
            try:
                self.signal.emit(r.recognize_bing(audio, key=BING_KEY))
                #print("Microsoft Bing Voice Recognition thinks you said " + r.recognize_bing(audio, key=BING_KEY))
            except sr.UnknownValueError:
                pass
                #print("Microsoft Bing Voice Recognition could not understand audio")
            except sr.RequestError as e:
                pass
                #print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
                                

'''
Singleton class for the Mirror Widget. This is the main widget that displays
all of the other widgets.
'''
class MirrorWidget():
    class __MirrorWidget(QWidget):
        def __init__(self, app, collapsedWidgetConf):
            super(MirrorWidget.__MirrorWidget, self).__init__()

            self.installedCollapsedWidgets = {}
            self.installedExpandedWidgets = {}
            self.activeCollapsedWidgets = {}
            self.activeExpandedWidgets = {}
            self.activeExpandedWidgetsNames = set()
            self.respondingExpandedWidgets = set()
            
            self.displayedExpandedWidgetOwner = None
            self.displayedExpandedWidget = None

            self.placeholderExpandedWidget = QWidget()
            self.placeholderExpandedWidget.setStyleSheet("background-color:black;}");

            self.grid = QGridLayout()
            self.loadInstalledWidgets()
            self.initActiveCollapsedWidgets(collapsedWidgetConf)
            self.initActiveExpandedWidget()
            self.initUI(app, collapsedWidgetConf)

            self.speechThread = speechRecognitionThread()
            self.speechThread.signal.connect(self.speechEvent)
            self.speechThread.start()

            #self.startFacialDetection()

            ''' TODO: This is just a workaround so that the main application
                      gets all the keyboard events. Need to figure out how to
                      capture events of child events.
            '''
            self.setFocusPolicy(Qt.StrongFocus)
            self.setFocus()
        '''
        Maps widget name to the widget class.
        '''
        def loadInstalledWidgets(self):
            for subclass in CollapsedWidget.__subclasses__():
                self.installedCollapsedWidgets[subclass.name()] = subclass

            for subclass in ExpandedWidget.__subclasses__():
                self.installedExpandedWidgets[subclass.name()] = subclass
                if 'receive_message' in dir(subclass):
                    self.respondingExpandedWidgets.add(subclass.name())
                    

        '''
        Initializes the collapsed widgets selected by the user to be displayed.
        '''
        def initActiveCollapsedWidgets(self, collapsedWidgetConf):
            # Initializing the top widget
            if collapsedWidgetConf['top'] in self.installedCollapsedWidgets:
                widget_class = self.installedCollapsedWidgets[collapsedWidgetConf['top']]
                # If the widget indicates that it wants communication access
                if 'msg_callback' in str(signature(widget_class.__init__)):
                    widget = widget_class(msg_callback=self.widget_communication)
                else:
                    widget = widget_class()
                self.activeCollapsedWidgets['top'] = widget
            else:
                placeholderWidget = QWidget()
                placeholderWidget.setStyleSheet("background-color:black;}")
                self.activeCollapsedWidgets['top'] = placeholderWidget


            if collapsedWidgetConf['top'] in self.installedExpandedWidgets:
                self.activeExpandedWidgetsNames.add(collapsedWidgetConf['top'])
                self.activeExpandedWidgets['top'] = \
                    self.installedExpandedWidgets[collapsedWidgetConf['top']]()
            else:
                self.activeExpandedWidgets['top'] = None

            # Initializing the left widget
            if collapsedWidgetConf['left'] in self.installedCollapsedWidgets:
                widget_class = self.installedCollapsedWidgets[collapsedWidgetConf['left']]
                # If the widget indicates that it wants communication access
                if 'msg_callback' in str(signature(widget_class.__init__)):
                    widget = widget_class(msg_callback=self.widget_communication)
                else:
                    widget = widget_class()
                self.activeCollapsedWidgets['left'] = widget
            else:
                placeholderWidget = QWidget()
                placeholderWidget.setStyleSheet("background-color:black;}")
                self.activeCollapsedWidgets['left'] = placeholderWidget

            if collapsedWidgetConf['left'] in self.installedExpandedWidgets:
                self.activeExpandedWidgetsNames.add(collapsedWidgetConf['left'])
                self.activeExpandedWidgets['left'] = \
                    self.installedExpandedWidgets[collapsedWidgetConf['left']]()
            else:
                self.activeExpandedWidgets['left'] = None

            # Initializing the right widget
            if collapsedWidgetConf['right'] in self.installedCollapsedWidgets:
                widget_class = self.installedCollapsedWidgets[collapsedWidgetConf['right']]
                # If the widget indicates that it wants communication access
                if 'msg_callback' in str(signature(widget_class.__init__)):
                    widget = widget_class(msg_callback=self.widget_communication)
                else:
                    widget = widget_class()
                self.activeCollapsedWidgets['right'] = widget
            else:
                placeholderWidget = QWidget()
                placeholderWidget.setStyleSheet("background-color:black;}")
                self.activeCollapsedWidgets['right'] = placeholderWidget

            if collapsedWidgetConf['right'] in self.installedExpandedWidgets:
                self.activeExpandedWidgetsNames.add(collapsedWidgetConf['right'])
                self.activeExpandedWidgets['right'] = \
                    self.installedExpandedWidgets[collapsedWidgetConf['right']]()
            else:
                self.activeExpandedWidgets['right'] = None

        '''
        Initializes the expanded widget as a placeholder.
        '''
        def initActiveExpandedWidget(self):
            self.displayedExpandedWidget = self.placeholderExpandedWidget

        '''
        Draws the initial GUI for the collapsed and expanded widgets.
        '''
        def initUI(self, app, collapsedWidgetConf):
            self.grid.addWidget(self.activeCollapsedWidgets['top'], 0, 30, 30, 90)
            self.grid.addWidget(self.activeCollapsedWidgets['left'], 0, 0, 130, 30)
            self.grid.addWidget(self.displayedExpandedWidget, 30, 30, 100, 90)
            self.grid.addWidget(self.activeCollapsedWidgets['right'], 0, 120, 130, 30)

            self.activeCollapsedWidgets['top'].setFocusPolicy(Qt.NoFocus)
            geometry = app.desktop().availableGeometry()
            self.setLayout(self.grid)
            self.setStyleSheet("background-color:black;}")
            self.setGeometry(geometry)

        def showWidgets(self):
            for position, widget in self.activeCollapsedWidgets.items():
                widget.show()

            self.displayedExpandedWidget.show()

        def hideWidgets(self):
            for position, widget in self.activeCollapsedWidgets.items():
                widget.hide()

            self.displayedExpandedWidget.hide()

        def widget_communication(self, **kwargs):
            widget_name, widget, message = None, None, None
            for key, value in kwargs.items():
                if key == 'widget':
                    widget = value
                    widget_name = widget.name()
                elif key == 'message':
                    message = value

            # Check if expanded widget exists
            if not widget_name or widget_name not in self.respondingExpandedWidgets \
               or widget_name not in list(self.activeExpandedWidgetsNames) \
               or not self.activeExpandedWidgets:
                return False

            for key, value in self.activeCollapsedWidgets.items():
                if value == widget:
                    # Deliver the message
                    try:
                        self.activeExpandedWidgets[key].receive_message(message)
                        return True
                    except:
                        pass

            return False

        def speechEvent(self, event):
            print (event)	
            # Check if we can display an expanded widget		
            if not self.displayedExpandedWidgetOwner:
                if event == 'open one':
                    self.displayedExpandedWidgetOwner = 'left'
                elif event == 'open two':
                    self.displayedExpandedWidgetOwner = 'top'
                elif event == 'open three' or event == 'open free':
                    self.displayedExpandedWidgetOwner = 'right'

                # If the user has performed an accepted interaction and an expanded view exists for the widget
                if self.displayedExpandedWidgetOwner and \
                    self.activeExpandedWidgets[self.displayedExpandedWidgetOwner]:
                    # Remove the placeholder
                    self.grid.removeWidget(self.displayedExpandedWidget)
                    self.displayedExpandedWidget.setParent(None)
                    self.displayedExpandedWidget = self.activeExpandedWidgets[self.displayedExpandedWidgetOwner]
                    self.grid.addWidget(self.displayedExpandedWidget, 30, 30, 100, 90)
                # Reset displayedExpandedWidgetOwner if user performs illegal action or no expanded view exists
                else:
                    self.displayedExpandedWidgetOwner = None
            # Check if we can close the expanded widget
            else:
                if ((event == "close three" or event=="close free") and self.displayedExpandedWidgetOwner == 'right') \
                    or ((event == "close two" or event == "close to") and self.displayedExpandedWidgetOwner == 'top') \
                    or (event == "close one" and self.displayedExpandedWidgetOwner == 'left'):
                    self.grid.removeWidget(self.displayedExpandedWidget)
                    self.displayedExpandedWidget.setParent(None)
                    self.displayedExpandedWidget = self.placeholderExpandedWidget
                    self.displayedExpandedWidgetOwner = None
                    self.grid.addWidget(self.displayedExpandedWidget, 30, 30, 100, 90)

               
                   
                    
        
        def keyPressEvent(self, e):
            # Check if we can display an expanded widget
            if not self.displayedExpandedWidgetOwner:
                if e.key() == Qt.Key_D:
                    self.displayedExpandedWidgetOwner = 'left'
                elif e.key() == Qt.Key_S:
                    self.displayedExpandedWidgetOwner = 'top'
                elif e.key() == Qt.Key_A:
                    self.displayedExpandedWidgetOwner = 'right'

                # If the user has performed an accepted interaction and an expanded view exists for the widget
                if self.displayedExpandedWidgetOwner and \
                    self.activeExpandedWidgets[self.displayedExpandedWidgetOwner]:
                    # Remove the placeholder
                    self.grid.removeWidget(self.displayedExpandedWidget)
                    self.displayedExpandedWidget.setParent(None)
                    self.displayedExpandedWidget = self.activeExpandedWidgets[self.displayedExpandedWidgetOwner]
                    self.grid.addWidget(self.displayedExpandedWidget, 30, 30, 100, 90)

                # Reset displayedExpandedWidgetOwner if user performs illegal action or no expanded view exists
                else:
                    self.displayedExpandedWidgetOwner = None

            # Check if the expanded widget can use the event
            elif self.displayedExpandedWidgetOwner == 'top' and self.displayedExpandedWidget.keyPressUsed(e):
                pass

                # Check if the expanded widget can use the event
            elif self.displayedExpandedWidgetOwner == 'left' and self.displayedExpandedWidget.keyPressUsed(e):
                #pass the key press down to the collapsed widget
                self.activeCollapsedWidgets['left'].keyPressUsed(e)
                pass

            # Check if we can close the expanded widget
            else:
                if (e.key() == Qt.Key_D and self.displayedExpandedWidgetOwner == 'right') \
                    or (e.key() == Qt.Key_W and self.displayedExpandedWidgetOwner == 'top') \
                    or (e.key() == Qt.Key_A and self.displayedExpandedWidgetOwner == 'left'):
                    self.grid.removeWidget(self.displayedExpandedWidget)
                    self.displayedExpandedWidget.setParent(None)
                    self.displayedExpandedWidget = self.placeholderExpandedWidget
                    self.displayedExpandedWidgetOwner = None
                    self.grid.addWidget(self.displayedExpandedWidget, 30, 30, 100, 90)


        def eventFilter(self, object, event):
            if event.type() == QEvent.KeyPress:
                return True
            return QWidget.eventFilter(self, obj, event)

        def startFacialDetection(self):
            thread = threading.Thread(target = self.facialDetection)
            thread.daemon = True
            thread.start()

        def facialDetection(self):
            #https://realpython.com/blog/python/face-detection-in-python-using-a-webcam/
            #need to source code
            faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            video_capture = cv2.VideoCapture(0)

            #use counter to have time delay for when someone leaves
            faceTimeCounter = 5
            widgetsShowing = False

            while True:
                # Capture frame-by-frame
                ret, frame = video_capture.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

                if len(faces) == 0:
                    if faceTimeCounter > 0:
                        faceTimeCounter = faceTimeCounter - 1
                else:
                    if faceTimeCounter < 30:
                        faceTimeCounter = faceTimeCounter + 1

                print("faceTimeCounter: " + str(faceTimeCounter))
                if faceTimeCounter > 0 and widgetsShowing == False:
                    widgetsShowing = True
                    self.showWidgets()
                elif faceTimeCounter == 0 and widgetsShowing == True:
                    widgetsShowing = False
                    self.hideWidgets()

                sleep(1)

    instance = None
    def __init__(self, app, collapsedWidgetConf):
        if not MirrorWidget.instance:
            MirrorWidget.instance = \
                MirrorWidget.__MirrorWidget(app, collapsedWidgetConf)
        else:
            pass

    def __getattr__(self, name):
        return getattr(self.instance, name)

def main():
    app = QApplication(sys.argv)

    importInstalledWidgetModules()

    collapsedWidgetConf = json.load(open("CollapsedWidgetConf.json"))
    widget = MirrorWidget(app, collapsedWidgetConf)
    widget.show()
    #widget.showFullScreen()

    sys.exit(app.exec_())

'''
Imports all installed widgets so that they are visible to the main application.
'''
def importInstalledWidgetModules():
    # Package path to the installed widgets
    packagePath = 'Widgets.InstalledWidgets.'

    currDir = os.path.dirname(__file__)
    # File path to the installed widgets
    path = os.path.join(currDir, 'Widgets', 'InstalledWidgets')

    for fname in os.listdir(path):
        # Find all of the individual widget directories
        if os.path.isdir(os.path.join(path, fname)) and fname != '__pycache__':
            widgetPackagePath = packagePath + fname + "."
            widgetPath = os.path.join(path, fname)
            for widgetFile in os.listdir(widgetPath):
                # Import all of the modules needed for the widget
                if os.path.isfile(os.path.join(widgetPath, widgetFile)) \
                    and widgetFile != '__init__.py' and \
                    os.path.splitext(widgetFile)[1] == '.py':
                    importlib.import_module(widgetPackagePath
                    + str(os.path.splitext(widgetFile)[0]))

if __name__ == '__main__':
    main()
