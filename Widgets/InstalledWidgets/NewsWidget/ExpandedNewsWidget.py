import random
import sys
import feedparser
from newspaper import Article
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

"""
from summarizer import summarize
from sumy.parsers.plaintext import PlaintextParser #We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer
#sudo pip3 install sumy
#python -c "import nltk; nltk.download('punkt')"
#sudo pip3 install numpy

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

from Widgets.ExpandedWidget import ExpandedWidget

class ExpandedNewsWidget(ExpandedWidget):

    Headlines = []
    Articles = []
    ArticleCounter = 0

    def __init__(self):
        super(ExpandedNewsWidget, self).__init__()
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
        self.text = QTextEdit(self)
        self.text.setGeometry(25, 0, 1050, 750)
        self.text.setReadOnly(True)
        self.updateText()

    def updateText(self):
        self.text.setPlainText(self.Headlines[self.ArticleCounter] + "\n\n\n" + \
            self.Articles[self.ArticleCounter].text)

    def keyPressUsed(self, e) -> bool:
        if e.key() == Qt.Key_D and self.ArticleCounter < 3:
            self.ArticleCounter = self.ArticleCounter + 1
            self.updateText()
            return True
        elif e.key() == Qt.Key_A and self.ArticleCounter > 0:
            self.ArticleCounter = self.ArticleCounter - 1
            self.updateText()
            return True
        elif e.key() == Qt.Key_S:
            self.text.verticalScrollBar().setValue(self.text.verticalScrollBar().maximum())
            return True    
        elif e.key() == Qt.Key_W and self.text.verticalScrollBar().value() != 0:
            self.text.verticalScrollBar().setValue(self.text.verticalScrollBar().minimum())
            return True    
        else:
            return False

    @staticmethod
    def name():
        return "NewsWidget"

if __name__ == '__main__':
    main()

"""    def printArticle(self): 
        print(self.Articles[0].text)
        print("Summary: ")
        
        parser = PlaintextParser.from_string(self.Articles[0].text, Tokenizer("english"))
        sumarizer = LexRankSummarizer()
        summary = sumarizer(parser.document, 0.25)
        for sentence in summary: 
            print(sentence)
"""