# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtWrapperType


class CollapsedWidgetMeta(pyqtWrapperType, ABCMeta):
    pass


class CollapsedWidget(QWidget, metaclass=CollapsedWidgetMeta):

    def __init__(self):
        super(CollapsedWidget, self).__init__()

    def keyPressUsed(self, direction) -> bool:
        return False

    @staticmethod
    @abstractmethod
    def name(self) -> str:
        '''
        Return the name of the widget
        !!! IMPORTANT: The name that is returned must match the one in
                       WidgetConf.json !!!"
        '''


