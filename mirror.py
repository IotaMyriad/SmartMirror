# -*- coding: utf-8 -*-
import sys
import json
import os
import importlib

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# Importing the widget base classes
from Widgets.CollapsedWidget import CollapsedWidget
from Widgets.ExpandedWidget import ExpandedWidget


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

            self.displayedExpandedWidgetOwner = None
            self.displayedExpandedWidget = None

            self.placeholderExpandedWidget = QWidget()
            self.placeholderExpandedWidget.setStyleSheet("background-color:black;}");

            self.grid = QGridLayout()
            self.loadInstalledWidgets()
            self.initActiveCollapsedWidgets(collapsedWidgetConf)
            self.initActiveExpandedWidget()
            self.initUI(app)

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

        '''
        Initializes the collapsed widgets selected by the user to be displayed.
        '''
        def initActiveCollapsedWidgets(self, collapsedWidgetConf):
            # Initializing the top widget
            if collapsedWidgetConf['top'] in self.installedCollapsedWidgets:
                self.activeCollapsedWidgets['top'] = \
                    self.installedCollapsedWidgets[collapsedWidgetConf['top']]()
            else:
                placeholderWidget = QWidget()
                placeholderWidget.setStyleSheet("background-color:black;}")
                self.activeCollapsedWidgets['top'] = placeholderWidget


            if collapsedWidgetConf['top'] in self.installedExpandedWidgets:
                self.activeExpandedWidgets['top'] = \
                    self.installedExpandedWidgets[collapsedWidgetConf['top']]()
            else:
                self.activeExpandedWidgets['top'] = None

            # Initializing the left widget
            if collapsedWidgetConf['left'] in self.installedCollapsedWidgets:
                self.activeCollapsedWidgets['left'] = \
                    self.installedCollapsedWidgets[collapsedWidgetConf['left']]()
            else:
                placeholderWidget = QWidget()
                placeholderWidget.setStyleSheet("background-color:black;}")
                self.activeCollapsedWidgets['left'] = placeholderWidget

            if collapsedWidgetConf['left'] in self.installedExpandedWidgets:
                self.activeExpandedWidgets['left'] = \
                    self.installedExpandedWidgets[collapsedWidgetConf['left']]()
            else:
                self.activeExpandedWidgets['left'] = None

            # Initializing the right widget
            if collapsedWidgetConf['right'] in self.installedCollapsedWidgets:
                self.activeCollapsedWidgets['right'] = \
                    self.installedCollapsedWidgets[collapsedWidgetConf['right']]()
            else:
                placeholderWidget = QWidget()
                placeholderWidget.setStyleSheet("background-color:black;}")
                self.activeCollapsedWidgets['right'] = placeholderWidget

            if collapsedWidgetConf['right'] in self.installedExpandedWidgets:
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
        def initUI(self, app):
            self.grid.addWidget(self.activeCollapsedWidgets['top'], 0, 30, 30, 90)
            self.grid.addWidget(self.activeCollapsedWidgets['left'], 0, 0, 130, 30)
            self.grid.addWidget(self.displayedExpandedWidget, 30, 30, 100, 90)
            self.grid.addWidget(self.activeCollapsedWidgets['right'], 0, 120, 130, 30)

            self.activeCollapsedWidgets['top'].setFocusPolicy(Qt.NoFocus)
            geometry = app.desktop().availableGeometry()
            self.setLayout(self.grid)
            self.setStyleSheet("background-color:black;}")
            self.setGeometry(geometry)

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
                print ("HERE")
                return True
            return QWidget.eventFilter(self, obj, event)


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
