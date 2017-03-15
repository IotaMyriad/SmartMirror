# -*- coding: utf-8 -*-

from time import sleep

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Widgets.CollapsedWidget import CollapsedWidget


class ExampleCollapsedWidget1(CollapsedWidget):

    def __init__(self, msg_callback=None):
        super(ExampleCollapsedWidget1, self).__init__()
        self.initUI()

        self.WidgetCommunicator = WidgetCommunicator(self, msg_callback, \
            "ExampleWidget1 message")
        self.WidgetCommunicator.start()  

    def initUI(self):
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color:green;}")
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)

    @staticmethod
    def name():
        return "ExampleWidget1"

class WidgetCommunicator(QtCore.QThread):

    def __init__(self, widget, msg_callback, message):
        QtCore.QThread.__init__(self)
        self.widget = widget
        self.message = message
        self.msg_callback = msg_callback

    def run(self):
        #send the first message
        while not self.msg_callback(widget=self.widget, message=self.message):
            pass

        #continue sending messages
        while self.msg_callback(widget=self.widget, message=self.message):
            sleep(5)