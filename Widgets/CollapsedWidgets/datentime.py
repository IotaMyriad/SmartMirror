# see : http://stackoverflow.com/questions/10421166/how-to-attach-appointments-to-a-calender-widget-pyqt-and-python
# for how to include appointments

import random
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Widgets.CollapsedWidget import CollapsedWidget

class CalendarWidget(CollapsedWidget):

    def __init__(self):
        super(CalendarWidget, self).__init__()
        self.initUI()

    def initUI(self):
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(20, 20)
        cal.clicked[QDate].connect(self.showDate)

        self.lbl = QLabel(self)
        date = cal.selectedDate()
        self.lbl.setText("Selected date: " + date.toString() + "     ")
        self.lbl.move(20, 200)

        self.setGeometry(100,100,300,300)
        self.setWindowTitle('Calendar')

        self.lbl2 = QLabel(self)
        datetime = QDateTime.currentDateTime()
        self.lbl2.setText(datetime.toString() + "     ")
        self.lbl2.move(20, 220)

        self.lcd = QLCDNumber(self)
        self.lcd.setDigitCount(8)
        self.lcd.display(QTime.currentTime().toString())
        self.lcd.move(20, 240)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.Time)
        self.timer.timeout.connect(self.displayOSDateTime)
        self.timer.start()

        self.show()

    def Time(self):
        self.lcd.display(QTime.currentTime().toString())

    def displayOSDateTime(self):
        self.lbl2.setText(QDateTime.currentDateTime().toString())

    def showDate(self, date):
        self.lbl.setText("Selected date: " + date.toString())

    @staticmethod
    def name():
        return "CalendarWidget"

def main():

    app = QApplication(sys.argv)
    ex = CalendarWidget()

    mainWidget = QWidget()
    vbox = QVBoxLayout()
    vbox.addWidget(ex)

    mainWidget.setLayout(vbox)
    mainWidget.setGeometry(300, 300, 400, 320)
    mainWidget.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


