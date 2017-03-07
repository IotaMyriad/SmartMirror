# see : http://stackoverflow.com/questions/10421166/how-to-attach-appointments-to-a-calender-widget-pyqt-and-python
# for how to include appointments

import random
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Widgets.CollapsedWidget import CollapsedWidget

class CollapsedDateTimeWidget(CollapsedWidget):

    def __init__(self):
        super(CollapsedDateTimeWidget, self).__init__()

        self.layout = QWidget(self)
        self.vbox = QVBoxLayout(self)
        self.dateLabel = QLabel(self)
        self.date = QDate()
        self.timeLabel = QLabel(self)
        self.time = QTime()
        self.timer = QTimer(self)

        self.initialize_UI()
        self.start_update_timer()

    def initialize_UI(self):
        self.dateLabel.setText(self.date.currentDate().toString())
        self.dateLabel.setStyleSheet("font-size: 24pt; color: white")
        self.vbox.addWidget(self.dateLabel)

        self.timeLabel.setText(self.time.currentTime().toString())
        self.timeLabel.setStyleSheet("font-size: 24pt; color: white")
        self.vbox.addWidget(self.timeLabel)

        self.layout.setLayout(self.vbox)

    def start_update_timer(self):
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time)
        self.timer.timeout.connect(self.update_date)
        self.timer.start()

    def update_time(self):
        self.timeLabel.setText(self.time.currentTime().toString())

    def update_date(self):
        self.dateLabel.setText(self.date.currentDate().toString())

    @staticmethod
    def name():
        return "DateTimeWidget"


