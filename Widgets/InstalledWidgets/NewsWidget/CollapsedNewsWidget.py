import random
import sys

import feedparser
from time import sleep
from newspaper import Article
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

"""
installing feedparser: 
-sudo pip3 install feedparser

installing newspaper: 
-go to this website: https://pypi.python.org/pypi/newgit sspaper3k/0.1.9
-download the .tar.gz
-unpack it
-go to the unpacked folder in terminal
-sudo pip3 install -r requirements.txt
-sudo python3 setup.py install

for the document: we switched from google news to yahoo news
-still fulfills criteria, easier to parse (only parsing yahoo website, not all of them, parsing all website is outside the scope of the project), better end user experience, less random text / missing text
"""

from Widgets.CollapsedWidget import CollapsedWidget

class CollapsedNewsWidget(CollapsedWidget):

    def __init__(self, msg_callback=None):
        super(CollapsedNewsWidget, self).__init__()

        self.initializeUI()

        self.dataDownloader = DataDownloadThread()
        self.dataDownloader.signal.connect(self.updateUI)
        self.dataDownloader.start()

        self.WidgetCommunicator = WidgetCommunicator(self, msg_callback, \
            self.dataDownloader)
        self.WidgetCommunicator.start()       

    def initializeUI(self):
        self.table = QTableWidget(self)
        self.table.setGeometry(25, 30, 1000, self.height())
        self.table.setColumnCount(1)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setStyleSheet("border: 0px; font-size: 16pt;")

        for row in range(4):
            self.table.insertRow(row)
            self.table.setColumnWidth(row, 1000)

    def updateUI(self, headlinesAndArticles):
        Headlines = headlinesAndArticles[0]
        for row in range(4):
            headline = Headlines[row]
            item = QTableWidgetItem(headline)
            item.setTextAlignment(Qt.AlignHCenter)
            item.setForeground(Qt.white)
            self.table.setItem(row, 0, item)
        self.update()

    @staticmethod
    def name():
        return "NewsWidget"

class DataDownloadThread(QtCore.QThread):

    signal = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.newsUrl = "http://news.yahoo.com/rss/"
        self.refreshRate = 300 #5 minutes

    def getArticle(self, url):
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article
        except:
            return None

    def updateArticlesAndHeadlines(self):
        self.headlines = []
        self.articles = []

        newsFeed = feedparser.parse(self.newsUrl)
        newsStories = newsFeed['items']

        loopCounter = 0
        articleCounter = 0
        while loopCounter < 4:
            newsStory = newsStories[articleCounter]
            article = self.getArticle(newsStory['link'])
            if article is not None:
                self.headlines.append(newsStory['title'])
                self.articles.append(article)
                loopCounter = loopCounter + 1
            articleCounter = articleCounter + 1

    def run(self):
        while True:
            self.updateArticlesAndHeadlines()
            self.signal.emit([self.headlines, self.articles])
            sleep(self.refreshRate)

class WidgetCommunicator(QtCore.QThread):

    def __init__(self, widget, msg_callback, message):
        QtCore.QThread.__init__(self)
        self.widget = widget
        self.message = message
        self.msg_callback = msg_callback

    def run(self):
        while not self.msg_callback(widget=self.widget, message=self.message):
            pass