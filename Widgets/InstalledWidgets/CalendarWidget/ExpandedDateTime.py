# see : http://stackoverflow.com/questions/10421166/how-to-attach-appointments-to-a-calender-widget-pyqt-and-python
# for how to include appointments

import random
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Widgets.ExpandedWidget import ExpandedWidget

class ExpandedDateTimeWidget(ExpandedWidget):

    def __init__(self):
        super(ExpandedDateTimeWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.calendar = QCalendarWidget(self)
        self.calendar.setGeometry(0, 0, 1100, 750)
        self.calendar.setVerticalHeaderFormat(0)
        self.calendar.setStyleSheet("font-size: 30pt")

    def keyPressUsed(self, direction) -> bool:
        if direction == 'down':
            currentDate = self.calendar.selectedDate()
            newDate = currentDate.addDays(1)
            self.calendar.setSelectedDate(newDate)
            return True
        elif direction == 'up':
            currentDate = self.calendar.selectedDate()
            newDate = currentDate.addDays(-1)
            self.calendar.setSelectedDate(newDate)
            return True
        elif direction == 'right':
            return True
        return False

    @staticmethod
    def name():
        return "DateTimeWidget"

