import random
import sys
import feedparser
import TextTeaser
from newspaper import Article
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

"""
installing feedparser: 
-sudo pip3 install feedparser

installing newspaper: 
-go to this website: https://pypi.python.org/pypi/newspaper3k/0.1.9
-download the .tar.gz
-unpack it
-go to the unpacked folder in terminal
-sudo pip3 install -r requirements.txt
-sudo python3 setup.py install

for the document: we switched from google news to yahoo news
-still fulfills criteria, easier to parse (only parsing yahoo website, not all of them, parsing all website is outside the scope of the project), better end user experience, less random text / missing text
"""

from Widgets.CollapsedWidget import CollapsedWidget

class NewsWidget(CollapsedWidget):

    Headlines = []
    Links = []
    Articles = []

    def __init__(self):
        super(NewsWidget, self).__init__()
        self.getHeadlinesAndLinks()
        self.getArticles()
        self.initializeUI()

    def getHeadlinesAndLinks(self):
        newsUrl = "http://news.yahoo.com/rss/"
        #newsUrl = "http://hosted2.ap.org/atom/APDEFAULT/3d281c11a76b4ad082fe88aa0db04909"
        #newsUrl = "http://news.google.com/?output=rss"
        #newsUrl = "http://www.cbn.com/cbnnews/us/feed/"

        newsFeed = feedparser.parse(newsUrl)
        newsStories = newsFeed['items']
        
        for counter in range(4):
            newsStory = newsStories[counter]
            self.Headlines.append(newsStory['title'])
            self.Links.append(newsStory['link'])

        return

    def getArticles(self):
        for url in self.Links:
            article = Article(url)
            article.download()
            article.parse()
            self.Articles.append(article)

        return 

    def initializeUI(self):

        table = QTableWidget(self)
        table.setGeometry(100, 50, 300, 300)
        table.setColumnCount(1)
        table.setMinimumSize(1000, 200)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setStyleSheet("border: 0px")

        for headline in self.Headlines:
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
