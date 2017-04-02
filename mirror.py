# -*- coding: utf-8 -*-
import sys
import json
import os
import numpy
import importlib
from inspect import signature
from inspect import ismethod

import cv2
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

# COMMENT THIS STUFF OUT IF NOT RUNNING ON PI 
from picamera.array import PiRGBArray
from picamera import PiCamera

class speechRecognitionThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        """
        citation for this function:
        A. Zhang, "Uberi/speech_recognition", Github, 2017. [Online]. Available:
        https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py.
        [Accessed: 22-Mar-2017]
        """
        r = sr.Recognizer()
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


class cameraThread(QThread):
    signal = pyqtSignal(object)

    def __init__(self):
        QThread.__init__(self)
        self.last_user = None

    def run(self):
        """ 
        citation for this function: 
        N. Ingham, "Face Detection and Recognition in Python with OpenCV",  
        Noahingham.com, 2017. [Online].  
        Available: https://noahingham.com/blog/facerec-python.html.  
        [Accessed: 23-Mar-2017]. 
        """

        size = 2
        fn_haar = 'haarcascade_frontalface_default.xml'
        fn_dir = 'att_faces'

        multiplePeopleCounter = 0
        infoShowing = True
        faceTimeCounter = 5
        widgetsShowing = True

        # Part 1: Create fisherRecognizer
        print('Training...')

        # Create a list of images and a list of corresponding names
        (images, lables, names, id) = ([], [], {}, 0)

        # Get the folders containing the training data
        for (subdirs, dirs, files) in os.walk(fn_dir):

            # Loop through each folder named after the subject in the photos
            for subdir in dirs:
                names[id] = subdir
                subjectpath = os.path.join(fn_dir, subdir)

                # Loop through each photo in the folder
                for filename in os.listdir(subjectpath):

                    # Skip non-image formates
                    f_name, f_extension = os.path.splitext(filename)
                    if (f_extension.lower() not in
                            ['.png', '.jpg', '.jpeg', '.gif', '.pgm']):
                        print("Skipping " + filename + ", wrong file type")
                        continue
                    path = subjectpath + '/' + filename
                    lable = id

                    # Add to training data
                    images.append(cv2.imread(path, 0))
                    lables.append(int(lable))
                id += 1
        (im_width, im_height) = (112, 92)

        # Create a Numpy array from the two lists above
        (images, lables) = [numpy.array(lis) for lis in [images, lables]]

        # OpenCV trains a model from the images
        # NOTE FOR OpenCV2: remove '.face'
        model = cv2.face.createFisherFaceRecognizer()
        model.train(images, lables)
        model.setThreshold(400)

        # Part 2: Use fisherRecognizer on camera stream
        haar_cascade = cv2.CascadeClassifier(fn_haar)
        #webcam = cv2.VideoCapture(0)

        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 16
        rawCapture = PiRGBArray(camera, size=(640, 480))

        for input_frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):        
        #while True:

            # Loop until the camera is working
            '''
            rval = False
            while (not rval):
                # Put the image from the webcam into 'frame'
                (rval, frame) = webcam.read()
                if (not rval):
                    print("Failed to open webcam. Trying again...")
            '''
            frame = input_frame.array

            # Flip the image (optional)
            frame = cv2.flip(frame, 1, 0)

            # Convert to grayscalel
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Resize to speed up detection (optinal, change size above)
            mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))

            # Detect faces
            faces = haar_cascade.detectMultiScale(mini)
            print('number of faces:' + str(len(faces)))

            information_to_send = []

            #sleep mode algorithm
            if len(faces) == 0:
                if faceTimeCounter > 0:
                    faceTimeCounter = faceTimeCounter - 1
            else:
                if faceTimeCounter < 5:
                    faceTimeCounter = faceTimeCounter + 1

            print("faceTimeCounter: " + str(faceTimeCounter))
            if faceTimeCounter > 0 and widgetsShowing == False:
                widgetsShowing = True
                information_to_send.append('show widgets')
            elif faceTimeCounter == 0 and widgetsShowing == True:
                widgetsShowing = False
                information_to_send.append('hide widgets')
                information_to_send.append('hide info')
                self.last_user = None

            #multiple people algorithm
            if len(faces) == 0 or len(faces) == 1:
                if multiplePeopleCounter > 0:
                    multiplePeopleCounter = multiplePeopleCounter - 1
            else:
                if multiplePeopleCounter < 10:
                    multiplePeopleCounter = multiplePeopleCounter + 1

            print("multiplePeopleCounter: " + str(multiplePeopleCounter))
            if multiplePeopleCounter > 5 and infoShowing == True:
                infoShowing = False
                information_to_send.append('hide info')
                self.last_user = None
            elif multiplePeopleCounter < 5 and infoShowing == False:
                infoShowing = True

            #try to predict the face
            if len(faces) == 1 and infoShowing == True:
                face_i = faces[0]

                # Coordinates of face after scaling back by `size`
                (x, y, w, h) = [v * size for v in face_i]
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (im_width, im_height))

                prediction = model.predict(face_resize)
                if prediction[0] >= 0 and prediction[0] < len(names):
                    person = names[prediction]
                    print(person)
                    if self.last_user != person:
                        self.last_user = person
                        information_to_send.append(person)

            #send the information
            if len(information_to_send) > 0:
                print("information to send: " + str(information_to_send))
                self.signal.emit(information_to_send)
            
            rawCapture.truncate(0)
            #sleep
            sleep(1)

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

            self.cameraThread = cameraThread()
            self.cameraThread.signal.connect(self.cameraEvent)
            self.cameraThread.start()

            # CHANGE THIS TO startFacialDetection() IF NOT RUNNING ON PI
            #self.startPiFacialDetection()

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

        def cameraEvent(self, information_array):
            for information in information_array:
                if information == 'show widgets':
                    self.showWidgets()
                elif information == 'hide widgets':
                    self.hideWidgets()
                elif information == 'phil' or information == 'louis':
                    self.activeCollapsedWidgets['left'].user = information
                    self.activeCollapsedWidgets['left'].keyPressUsed('right')
                elif information == 'hide info':
                    self.activeCollapsedWidgets['left'].user = None
                    self.activeCollapsedWidgets['left'].keyPressUsed('right')

        def speechEvent(self, speech):
            print (speech)
            split_speech = speech.split(" ")
            if len(split_speech) == 2:
                character = list(split_speech[1])[0]

                if character == 'r':
                    self.user_interaction('right')
                elif character == 'd':
                    self.user_interaction('down')
                elif character == 'l':
                    self.user_interaction('left')
                elif character == 'u':
                    self.user_interaction('up')

        def keyPressEvent(self, e):
            if e.key() == Qt.Key_D:
                self.user_interaction('right')
            elif e.key() == Qt.Key_S:
                self.user_interaction('down')
            elif e.key() == Qt.Key_A:
                self.user_interaction('left')
            elif e.key() == Qt.Key_W:
                self.user_interaction('up')

        def user_interaction(self, direction):
            # Check if we can display an expanded widget
            if not self.displayedExpandedWidgetOwner:
                if direction == 'right':
                    self.displayedExpandedWidgetOwner = 'left'
                elif direction == 'down':
                    self.displayedExpandedWidgetOwner = 'top'
                elif direction == 'left':
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
            elif self.displayedExpandedWidgetOwner == 'top' and self.displayedExpandedWidget.keyPressUsed(direction):
                pass

                # Check if the expanded widget can use the event
            elif self.displayedExpandedWidgetOwner == 'left' and self.displayedExpandedWidget.keyPressUsed(direction):
                # pass the key press down to the collapsed widget
                self.activeCollapsedWidgets['left'].keyPressUsed(direction)
                pass

            # Check if we can close the expanded widget
            else:
                if (direction == 'right' and self.displayedExpandedWidgetOwner == 'right') \
                        or (direction == 'up' and self.displayedExpandedWidgetOwner == 'top') \
                        or (direction == 'left' and self.displayedExpandedWidgetOwner == 'left'):
                    self.grid.removeWidget(self.displayedExpandedWidget)
                    self.displayedExpandedWidget.setParent(None)
                    self.displayedExpandedWidget = self.placeholderExpandedWidget
                    self.displayedExpandedWidgetOwner = None
                    self.grid.addWidget(self.displayedExpandedWidget, 30, 30, 100, 90)

        def startFacialDetection(self):
            thread = threading.Thread(target = self.facialDetection)
            thread.daemon = True
            thread.start()

        def startPiFacialDetection(self):
            thread = threading.Thread(target = self.piFacialDetection)
            thread.daemon = True
            thread.start()
       
        def piFacialDetection(self):
            """
            Citation for this function:
            A. Rosebrock, "Accessing the Raspberry Pi Camera with OpenCV and Python", pyimagesearch, 2017. [Online]
            Available:
            http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python.
            [Accessed: 22-Mar-2017].
            """
            faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            camera = PiCamera()
            camera.resolution = (640, 480)
            camera.framerate = 16
            rawCapture = PiRGBArray(camera, size=(640, 480))

            faceTimeCounter = 5
            widgetsShowing = False
           
            time.sleep(0.1)
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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
                rawCapture.truncate(0)
                sleep(1)

        def facialDetection(self):
            """
            Citation for this function:
            S. Tiwari, "Face detection in Python using a webcam", Real Python, 2014. [Online]. Available:
            https://realpython.com/blog/python/face-detection-using-a-webcam. [Accessed: 22-Mar-2017].
            """

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
