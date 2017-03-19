# user: smartmirror_elp
# pw: 12345678
# API-key: 68a61abe6601c18b8288c0e133ccaafb

import os,sys
import random
import pyowm
import datetime
from time import strftime
from datetime import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Widgets.ExpandedWidget import ExpandedWidget

API_key = "68a61abe6601c18b8288c0e133ccaafb"
place = "Toronto,Ca"
tor_lat = 43.6532
tor_long = -79.3832
day_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class DailyWeather(QWidget):
    date = ""

    def __init__(self, date):
        super(DailyWeather, self).__init__()
        self.date = date
        self.initUI()
        self.startTimer()

    def parse(self, string, start, end):
        strlist = string.split(start)
        ret = strlist[1].split(end)[0]
        ret = ret.split('}')[0]
        return ret
        
    def initUI(self):
        self.layout = QWidget(self)
        self.vbox = QVBoxLayout(self)  
         
        self.lbl1 = QLabel(self)
        self.lbl1.setStyleSheet("color : white")
        date = datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S+00")
        self.lbl1.setText(day_of_week[date.weekday()])
        self.vbox.addWidget(self.lbl1)
        
        self.lblp = QLabel(self)
        self.lblp.setScaledContents(True)
        self.vbox.addWidget(self.lblp)

        self.lbl2 = QLabel(self)
        self.lbl2.setStyleSheet("color : white")
        self.vbox.addWidget(self.lbl2)

        self.lbl3 = QLabel(self)
        self.lbl3.setStyleSheet("color : white")
        self.vbox.addWidget(self.lbl3)

        self.lbl4 = QLabel(self)
        self.lbl4.setStyleSheet("color : white")
        self.vbox.addWidget(self.lbl4)

        self.setWindowTitle('Weather')
        
        self.layout.setLayout(self.vbox)

        self.Update()
        
    def startTimer(self):
        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.Update)
        self.timer.start()
    
    def Update(self):
        owm = pyowm.OWM(API_key)
        fc = owm.daily_forecast(place)
        f = fc.get_forecast()
        w = f.get_weathers()[0]
        for weather in f:
            if self.date == weather.get_reference_time('iso'):
                w = weather
                break
        daily = w.get_temperature('celsius')
        temp_min = float(self.parse(str(daily), "'min': ", ","))
        temp_max = float(self.parse(str(daily), "'max': ", ","))
        observation = owm.weather_at_place(place)
        w = observation.get_weather()
        status = w.get_status()

        self.lblp.setPixmap(QPixmap(os.getcwd() + "/Widgets/InstalledWidgets/WeatherWidget/weather_icons/Expanded/" + w.get_weather_icon_name()))
        self.lbl2.setText("status: " + str(status) + "     ")
        self.lbl3.setText("daily min: " + str(int(round(temp_min))) + "°C     ")
        self.lbl4.setText("daily max: " + str(int(round(temp_max))) + "°C     ")

class ExpandedWeatherWidget(ExpandedWidget):

    def __init__(self):
        super(ExpandedWeatherWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.widget = QWidget()
        self.widget.setStyleSheet("background-color:black;}")

        owm = pyowm.OWM(API_key)  # You MUST provide a valid API key
        fc = owm.daily_forecast(place)
        f = fc.get_forecast()
        i = 0
        weather = f.get_weathers()[0]
        for weather in f:
            day = DailyWeather(weather.get_reference_time('iso'))
            day.setStyleSheet("background-color:black;");
            self.layout.addWidget(day,0,i)
            i += 1
        
        #self.layout.addWidget(self.widget)
        self.setLayout(self.layout)

    @staticmethod
    def name():
        return "WeatherWidget"
