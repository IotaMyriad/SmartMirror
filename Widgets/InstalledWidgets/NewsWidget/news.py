import random
import sys
import feedparser
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Widgets.CollapsedWidget import CollapsedWidget

class NewsWidget(CollapsedWidget):

    def __init__(self):
        super(NewsWidget, self).__init__()
        headlines = self.getNewsHeadlines()
        self.initUI(headlines)

    def getNewsHeadlines(self):
        headlines = []
        #newsUrl = "http://hosted2.ap.org/atom/APDEFAULT/3d281c11a76b4ad082fe88aa0db04909"
        newsUrl = "http://news.google.com/?output=rss"
        #newsUrl = "http://news.yahoo.com/rss/"
        #newsUrl = "http://www.cbn.com/cbnnews/us/feed/"

        newsFeed = feedparser.parse(newsUrl)
        for counter in range(4):
            headlines.append(newsFeed['items'][counter]['title'])

        return headlines

    def initUI(self, headlines):

        for hl in headlines:
            print(hl)

        print(len(headlines))

        table = QTableWidget(self)
        table.setGeometry(100, 50, 300, 300)
        table.setColumnCount(1)
        table.setMinimumSize(1000, 200)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setStyleSheet("border: 0px")

        for headline in headlines:
            rowPosition = table.rowCount()
            table.insertRow(rowPosition)
            table.setItem(rowPosition,0, QTableWidgetItem(headline))
        table.resizeColumnsToContents()
        self.show()

    @staticmethod
    def name():
        return "NewsWidget"

if __name__ == '__main__':
    main()