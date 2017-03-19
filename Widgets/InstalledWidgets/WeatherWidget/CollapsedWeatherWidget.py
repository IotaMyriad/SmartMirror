# user: smartmirror_elp
# pw: 12345678
# API-key: 68a61abe6601c18b8288c0e133ccaafb

import os,sys
import random
import pyowm
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Widgets.CollapsedWidget import CollapsedWidget

API_key = "68a61abe6601c18b8288c0e133ccaafb"
place = "Toronto,Ca"
tor_lat = 43.6532
tor_long = -79.3832

class CollapsedWeatherWidget(CollapsedWidget):

    def __init__(self):
        super(CollapsedWeatherWidget, self).__init__()
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
        
        self.lblp = QLabel(self)
        self.lblp.setScaledContents(True)
        self.lblp.setPixmap(QPixmap(os.getcwd() + "/Widgets/InstalledWidgets/WeatherWidget/weather_icons/01d.png"))
        self.vbox.addWidget(self.lblp)

        self.lbl1 = QLabel(self)
        self.lbl1.setStyleSheet("QLabel { color : white; }")
        self.lbl1.setFont(QFont("Helvetica",32))
        self.vbox.addWidget(self.lbl1)
        
        self.lbl2 = QLabel(self)
        self.lbl2.setStyleSheet("QLabel { color : white; }");
        self.vbox.addWidget(self.lbl2)
        
        self.lbl3 = QLabel(self)
        self.lbl3.setStyleSheet("QLabel { color : white; }");
        self.vbox.addWidget(self.lbl3)
        
        self.lbl4 = QLabel(self)
        self.lbl4.setStyleSheet("QLabel { color : white; }");
        self.vbox.addWidget(self.lbl4)
        
        self.lbl5 = QLabel(self)
        self.lbl5.setStyleSheet("QLabel { color : white; }");
        self.vbox.addWidget(self.lbl5)
        
        self.lbl6 = QLabel(self)
        self.lbl6.setStyleSheet("QLabel { color : white; }");
        self.vbox.addWidget(self.lbl6)
        
        self.lblp.setAlignment(Qt.AlignRight)
        self.lbl1.setAlignment(Qt.AlignRight)
        self.lbl2.setAlignment(Qt.AlignRight)
        self.lbl3.setAlignment(Qt.AlignRight)
        self.lbl4.setAlignment(Qt.AlignRight)
        self.lbl5.setAlignment(Qt.AlignRight)
        self.lbl6.setAlignment(Qt.AlignRight)

        self.setWindowTitle('Weather')
        
        self.layout.setLayout(self.vbox)
        self.Update()

    def startTimer(self):
        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.Update)
        self.timer.start()
        self.show()
    
    def Update(self):
        owm = pyowm.OWM(API_key)
        fc = owm.daily_forecast(place)
        f = fc.get_forecast()
        w = f.get_weathers()[0]
        daily = w.get_temperature('celsius')
        temp_min = float(self.parse(str(daily), "'min': ", ","))
        temp_max = float(self.parse(str(daily), "'max': ", ","))
        observation = owm.weather_at_place(place)
        w = observation.get_weather()
        status = w.get_status()
        wind_spd = float(self.parse(str(w.get_wind()), "'speed': ", ","))*3.6
        humidity = w.get_humidity()
        temp = float(self.parse(str(w.get_temperature('celsius')), "'temp': ", ","))

        self.lblp.setPixmap(QPixmap(os.getcwd() + "/Widgets/InstalledWidgets/WeatherWidget/weather_icons/" + w.get_weather_icon_name()))
        self.lbl1.setText(str(int(round(temp))) + "°C")
        self.lbl2.setText("status: " + str(status) + "")
        self.lbl3.setText("daily min: " + str(int(round(temp_min))) + "°C")
        self.lbl4.setText("daily max: " + str(int(round(temp_max))) + "°C")
        self.lbl5.setText("wind: " + str(int(round(wind_spd))) + " km/h")
        self.lbl6.setText("humidity: " + str(humidity) + "%")

    @staticmethod
    def name():
        return "WeatherWidget" 
