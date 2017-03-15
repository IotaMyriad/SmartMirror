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
        for weather in f:
        #print (weather.get_reference_time('iso'))
            if self.date == weather.get_reference_time('iso'):
                #print ("ya: ", date)
                w = weather
                break

        date = datetime.strptime(w.get_reference_time('iso'), "%Y-%m-%d %H:%M:%S+00")
        #print (day_of_week[date.weekday()])

        daily = w.get_temperature('celsius')
        temp_min = float(self.parse(str(daily), "'min': ", ","))
        temp_max = float(self.parse(str(daily), "'max': ", ","))
        #print ("min: " + str(int(round(min_temp))) + "°C max: " + str(int(round(max_temp))) + "°C")

        # Search for current weather in place
        observation = owm.weather_at_place(place)
        w = observation.get_weather() # <Weather - reference time=2013-12-18 09:20,
        status = w.get_status()    # status=Clouds>
          
        self.lbl1 = QLabel(self)
        self.lbl1.setStyleSheet("QLabel { color : white; }");
        self.lbl1.setText(day_of_week[date.weekday()])
        self.lbl1.move(0, 0)


        self.lblp = QLabel(self)
        self.lblp.setScaledContents(True);
        self.lblp.setGeometry(0, 20, 120, 80)
        #use full ABSOLUTE path to the image, not relative
        #print (w.get_weather_icon_name())
        self.lblp.setPixmap(QPixmap(os.getcwd() + "/weather_icons/" + w.get_weather_icon_name()))

        self.lbl2 = QLabel(self)
        self.lbl2.setStyleSheet("QLabel { color : white; }");
        self.lbl2.setText("status: " + str(status) + "     ")
        self.lbl2.move(0, 100)

        self.lbl3 = QLabel(self)
        self.lbl3.setStyleSheet("QLabel { color : white; }");
        self.lbl3.setText("daily min: " + str(int(round(temp_min))) + "°C     ")
        self.lbl3.move(0, 120)

        self.lbl4 = QLabel(self)
        self.lbl4.setStyleSheet("QLabel { color : white; }");
        self.lbl4.setText("daily max: " + str(int(round(temp_max))) + "°C     ")
        self.lbl4.move(0, 140)

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

        #self.lbl.setText(str(random.randint(0,9)))
        self.lbl2.setText("status: " + str(status) + "     ")
        self.lbl3.setText("daily min: " + str(int(round(temp_min))) + "°C     ")
        self.lbl4.setText("daily max: " + str(int(round(temp_max))) + "°C     ")

def main():

    app = QApplication(sys.argv)
    #ex = WeeklyWeather()
    #ex.setStyleSheet("background-color:black;");

    mainWidget = QWidget()

    grid = QGridLayout()
    owm = pyowm.OWM(API_key)  # You MUST provide a valid API key
    fc = owm.daily_forecast(place)
    f = fc.get_forecast() 
    i = 0
    for weather in f:
        day = DailyWeather(weather.get_reference_time('iso'))
        day.setStyleSheet("background-color:black;");
        grid.addWidget(day,0,i)
        i += 1

    mainWidget.setLayout(grid)
    mainWidget.setGeometry(0, 0, 1200, 200)
    mainWidget.setStyleSheet("background-color:black;");
    mainWidget.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


