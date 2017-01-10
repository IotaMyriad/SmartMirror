# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *

from Widgets.CollapsedWidgets.CollapsedWidget import CollapsedWidget


class ExampleCollapsedWidget3(CollapsedWidget):

    def __init__(self):
        super(ExampleCollapsedWidget3, self).__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color:purple;}")
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)

    @staticmethod
    def name():
        return "ExampleWidget3"