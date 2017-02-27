# user: smartmirror_elp
# pw: 12345678
# API-key: 68a61abe6601c18b8288c0e133ccaafb

import sys
import random
import pyowm
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

API_key = "68a61abe6601c18b8288c0e133ccaafb"
place = "Toronto,Ca"
tor_lat = 43.6532
tor_long = -79.3832

class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def parse(self, string, start, end):
        strlist = string.split(start)
        return strlist[1].split(end)[0]
        
    def initUI(self):

        owm = pyowm.OWM(API_key)  # You MUST provide a valid API key

        # Have a pro subscription? Then use:
        # owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')

        # Will it be sunny tomorrow at this time in Milan (Italy) ?
        #forecast = owm.daily_forecast("Milan,it")
        #tomorrow = pyowm.timeutils.tomorrow()
        #forecast.will_be_sunny_at(tomorrow)  # Always True in Italy, right? ;-)

        # weekly forcast
        fc = owm.daily_forecast(place)
        #fc = owm.three_hours_forecast(place)
        #fc = owm.daily_forecast_at_coords(tor_lat,tor_long)
        f = fc.get_forecast()
        w = f.get_weathers()[0]
        #print (w.get_reference_time('iso'),w.get_status())
        #print (weather.get_temperature('celsius'))
        daily = w.get_temperature('celsius')
        temp_min = float(self.parse(str(daily), "'min': ", ","))
        temp_max = float(self.parse(str(daily), "'max': ", ","))
        #print ("min: " + str(int(round(min_temp))) + "°C max: " + str(int(round(max_temp))) + "°C")

        # Search for current weather in place
        observation = owm.weather_at_place(place)
        w = observation.get_weather() # <Weather - reference time=2013-12-18 09:20,
                                      # status=Clouds>
        status = w.get_status()
        # Weather details
        #wind =  w.get_wind()                 # {'speed': 4.6, 'deg': 330}
        wind_spd = float(self.parse(str(w.get_wind()), "'speed': ", ","))*3.6
        humidity = w.get_humidity()              # 87
        temp = w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

        # Search current weather observations in the surroundings of
        # lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
        #observation_list = owm.weather_around_coords(-22.57, -43.12)
        temp_font = QFont ("Helvetica", 32)

        #self.lbl = QLabel(self)
        #self.lbl.setText(str(random.randint(0,9)))
        #self.lbl.move(0, 200)

        temp = float(self.parse(str(temp), "'temp': ", ","))
        self.lbl1 = QLabel(self)
        self.lbl1.setStyleSheet("QLabel { color : white; }");
        self.lbl1.setText(str(int(round(temp))) + "°C     ")
        self.lbl1.setFont(temp_font);
        self.lbl1.move(0, 0)

        self.lbl2 = QLabel(self)
        self.lbl2.setStyleSheet("QLabel { color : white; }");
        self.lbl2.setText("status: " + str(status) + "     ")
        self.lbl2.move(0, 60)

        self.lbl3 = QLabel(self)
        self.lbl3.setStyleSheet("QLabel { color : white; }");
        self.lbl3.setText("daily min: " + str(int(round(temp_min))) + "°C     ")
        self.lbl3.move(0, 80)

        self.lbl4 = QLabel(self)
        self.lbl4.setStyleSheet("QLabel { color : white; }");
        self.lbl4.setText("daily max: " + str(int(round(temp_max))) + "°C     ")
        self.lbl4.move(0, 100)

        self.lbl5 = QLabel(self)
        self.lbl5.setStyleSheet("QLabel { color : white; }");
        self.lbl5.setText("wind: " + str(int(round(wind_spd))) + " km/h     ")
        self.lbl5.move(0, 120)

        self.lbl6 = QLabel(self)
        self.lbl6.setStyleSheet("QLabel { color : white; }");
        self.lbl6.setText("humidity: " + str(humidity) + "%     ")
        self.lbl6.move(0, 140)

        self.setWindowTitle('Weather') 

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

        #self.lbl.setText(str(random.randint(0,9)))
        self.lbl1.setText(str(int(round(temp))) + "°C     ")
        self.lbl2.setText("status: " + str(status) + "     ")
        self.lbl3.setText("daily min: " + str(int(round(temp_min))) + "°C     ")
        self.lbl4.setText("daily max: " + str(int(round(temp_max))) + "°C     ")
        self.lbl5.setText("wind: " + str(int(round(wind_spd))) + " km/h     ")
        self.lbl6.setText("humidity: " + str(humidity) + "%     ")

def main():

    app = QApplication(sys.argv)
    ex = Example()
    ex.setStyleSheet("background-color:black;");

    mainWidget = QWidget()
    vbox = QVBoxLayout()
    vbox.addWidget(ex)

    mainWidget.setLayout(vbox)
    mainWidget.setGeometry(0, 0, 130, 800)
    mainWidget.setStyleSheet("background-color:black;");
    mainWidget.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


