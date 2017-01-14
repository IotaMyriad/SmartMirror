# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *

from Widgets.ExpandedWidget import ExpandedWidget


class ExampleExpandedWidget3(ExpandedWidget):

    def __init__(self):
        super(ExampleExpandedWidget3, self).__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color:blue;}")
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)

    @staticmethod
    def name():
        return "ExampleWidget3"