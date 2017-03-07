import random
import sys
from time import sleep
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

    def __init__(self):
        super(ExpandedNewsWidget, self).__init__()

        self.headlines = []
        self.articles = []
        self.articleCounter = 0

        self.initializeUI()

    def initializeUI(self):
        self.vbox = QVBoxLayout(self)

        self.title = QLabel(self)
        self.title.setStyleSheet("font-size: 16pt; color: white")
        self.title.setFixedWidth(1085)
        self.title.setAlignment(Qt.AlignHCenter)
        self.vbox.addWidget(self.title)

        self.text = QTextEdit(self)
        self.text.setTextColor(Qt.white)
        self.text.setGeometry(25, 0, 1050, 750)
        self.text.setReadOnly(True)
        self.vbox.addWidget(self.text)

    def updateData(self, headlinesAndArticles):
        self.headlines = headlinesAndArticles[0]
        self.articles = headlinesAndArticles[1]
        self.updateUI()

    def updateUI(self):
        self.title.setText(self.headlines[self.articleCounter])
        self.text.setPlainText(self.articles[self.articleCounter].text)
        self.update()

    def receive_message(self, message):
        self.dataThread = message
        self.dataThread.signal.connect(self.updateData)

    def keyPressUsed(self, e) -> bool:
        if e.key() == Qt.Key_D and self.articleCounter < 3:
            self.articleCounter = self.articleCounter + 1
            self.updateUI()
            return True
        elif e.key() == Qt.Key_A and self.articleCounter > 0:
            self.articleCounter = self.articleCounter - 1
            self.updateUI()
            return True
        elif e.key() == Qt.Key_S:
            currentValue = self.text.verticalScrollBar().value()
            self.text.verticalScrollBar().setValue(currentValue + self.text.verticalScrollBar().pageStep())
            return True    
        elif e.key() == Qt.Key_W and self.text.verticalScrollBar().value() != 0:
            currentValue = self.text.verticalScrollBar().value()
            self.text.verticalScrollBar().setValue(currentValue - self.text.verticalScrollBar().pageStep())
            return True    
        else:
            return False

    @staticmethod
    def name():
        return "NewsWidget"