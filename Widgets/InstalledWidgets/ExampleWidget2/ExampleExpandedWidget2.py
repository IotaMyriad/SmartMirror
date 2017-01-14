# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *

from Widgets.ExpandedWidget import ExpandedWidget


class ExampleExpandedWidget2(ExpandedWidget):

    def __init__(self):
        super(ExampleExpandedWidget2, self).__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color:red;}")
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)

    @staticmethod
    def name():
        return "ExampleWidget2"