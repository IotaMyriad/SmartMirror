# -*- coding: utf-8 -*-
import sys
import json

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Widgets.CollapsedWidgets.CollapsedWidget import CollapsedWidget
from Widgets.ExpandedWidgets.ExpandedWidget import ExpandedWidget

from Widgets.CollapsedWidgets import *
from Widgets.ExpandedWidgets import *

class MirrorWidget():
    class __MirrorWidget(QWidget):
        def __init__(self, app, collapsedWidgetConf):
            super(MirrorWidget.__MirrorWidget, self).__init__()

            self.installedCollapsedWidgets = {}
            self.installedExpandedWidgets = {}
            self.activeCollapsedWidgets = {}
            self.activeExpandedWidget = None

            self.loadInstalledWidgets()
            self.initActiveCollapsedWidgets(collapsedWidgetConf)
            self.initActiveExpandedWidget()
            self.initUI(app)

        def loadInstalledWidgets(self):
            for subclass in CollapsedWidget.__subclasses__():
                self.installedCollapsedWidgets[subclass.name()] = subclass

            for subclass in ExpandedWidget.__subclasses__():
                self.installedExpandedWidgets[subclass.name()] = subclass

        def initActiveCollapsedWidgets(self, collapsedWidgetConf):
            # Initializing the top widget
            if collapsedWidgetConf['top'] in self.installedCollapsedWidgets:
                self.activeCollapsedWidgets['top'] = \
                    self.installedCollapsedWidgets[collapsedWidgetConf['top']]()
            else:
                placeholderWidget = QWidget()
                placeholderWidget.setStyleSheet("background-color:black;}")
                self.activeCollapsedWidgets['top'] = placeholderWidget

            # Initializing the left widget
            if collapsedWidgetConf['left'] in self.installedCollapsedWidgets:
                self.activeCollapsedWidgets['left'] = \
                    self.installedCollapsedWidgets[collapsedWidgetConf['left']]()
            else:
                placeholderWidget = QWidget()
                placeholderWidget.setStyleSheet("background-color:black;}")
                self.activeCollapsedWidgets['left'] = placeholderWidget

            # Initializing the right widget
            if collapsedWidgetConf['right'] in self.installedCollapsedWidgets:
                self.activeCollapsedWidgets['right'] = \
                    self.installedCollapsedWidgets[collapsedWidgetConf['right']]()

            else:
                placeholderWidget = QWidget()
                placeholderWidget.setStyleSheet("background-color:black;}")
                self.activeCollapsedWidgets['right'] = placeholderWidget

        def initActiveExpandedWidget(self):
            placeholderWidget = QWidget()
            placeholderWidget.setStyleSheet("background-color:black;}")
            self.activeExpandedWidget = placeholderWidget

        def initUI(self, app):
            grid = QGridLayout()

            print (self.activeCollapsedWidgets)

            grid.addWidget(self.activeCollapsedWidgets['top'], 0, 30, 30, 90)
            grid.addWidget(self.activeCollapsedWidgets['left'], 0, 0, 130, 30)
            grid.addWidget(self.activeExpandedWidget, 30, 30, 100, 90)
            grid.addWidget(self.activeCollapsedWidgets['right'], 0, 120, 130, 30)

            geometry = app.desktop().availableGeometry()
            self.setLayout(grid)
            self.setStyleSheet("background-color:black;}")
            self.setGeometry(geometry)

    instance = None
    def __init__(self, app, collapsedWidgetConf):
        if not MirrorWidget.instance:
            MirrorWidget.instance = MirrorWidget.__MirrorWidget(app, collapsedWidgetConf)
        else:
            pass

    def __getattr__(self, name):
        return getattr(self.instance, name)



def main():
    app = QApplication(sys.argv)

    collapsedWidgetConf = json.load(open("CollapsedWidgetConf.json"))
    widget = MirrorWidget(app, collapsedWidgetConf)
    widget.show()
    #mainWidget.showFullScreen()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



