# -*- coding: utf-8 -*-

from time import sleep
import threading

from PyQt5.QtWidgets import *

from Widgets.CollapsedWidget import CollapsedWidget


class ExampleCollapsedWidget1(CollapsedWidget):

    global callback 

    def __init__(self, msg_callback=None):
        super(ExampleCollapsedWidget1, self).__init__()
        global callback 
        callback = msg_callback
        #self.startMessaging()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color:green;}")
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)

    def sendToExpanded(self, msg_callback):
        while True:
            print("ExampleWidget1")
            print(msg_callback(widget=self, message='hello'))
            sleep(1)

    def startMessaging(self):
        thread = threading.Thread(target = self.sendToExpanded, args=[callback])
        thread.daemon = True
        thread.start()

    @staticmethod
    def name():
        return "ExampleWidget1"
