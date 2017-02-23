# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *

from Widgets.CollapsedWidget import CollapsedWidget


class ExampleCollapsedWidget1(CollapsedWidget):

    def __init__(self, msg_callback=None):
        super(ExampleCollapsedWidget1, self).__init__()
        print (msg_callback(widget_name='ExampleWidget1', msg='hi'))
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color:green;}")
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)

    @staticmethod
    def name():
        return "ExampleWidget1"
