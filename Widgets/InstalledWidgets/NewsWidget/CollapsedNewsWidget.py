import random
import sys
import feedparser
from newspaper import Article
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

    Headlines = []
    Articles = []

    def __init__(self):
        super(CollapsedNewsWidget, self).__init__()
        self.getHeadlinesAndArticles()
        self.initializeUI()

    def getHeadlinesAndArticles(self):
        newsUrl = "http://news.yahoo.com/rss/"

        newsFeed = feedparser.parse(newsUrl)
        newsStories = newsFeed['items']
        
        loopCounter = 0
        articleCounter = 0
        while loopCounter < 4:
            newsStory = newsStories[articleCounter]
            article = self.getArticle(newsStory['link'])
            if article is not None:
                self.Headlines.append(newsStory['title'])
                self.Articles.append(article)
                loopCounter = loopCounter + 1
            articleCounter = articleCounter + 1
        return

    def getArticle(self, url):
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article
        except:
            return None

    def initializeUI(self):

        table = QTableWidget(self)

        table.setGeometry(325, 30, 500, 500)
        table.setColumnCount(1)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setStyleSheet("border: 0px")

        for headline in self.Headlines:
            rowPosition = table.rowCount()
            table.insertRow(rowPosition)
            item = QTableWidgetItem(headline)
            item.setTextAlignment(Qt.AlignHCenter)
            table.setItem(rowPosition,0, item)
        table.resizeColumnsToContents()

    @staticmethod
    def name():
        return "NewsWidget"

if __name__ == '__main__':
    main()
