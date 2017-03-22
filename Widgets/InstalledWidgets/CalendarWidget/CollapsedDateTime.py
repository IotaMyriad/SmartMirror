import os
import httplib2
import datetime
from datetime import timedelta

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Widgets.CollapsedWidget import CollapsedWidget

"""
pip3 install --upgrade google-api-python-client
"""


class CollapsedDateTimeWidget(CollapsedWidget):

    CALENDAR_SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    TASKS_SCOPES = 'https://www.googleapis.com/auth/tasks.readonly'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'SmartMirror'

    def __init__(self):
        super(CollapsedDateTimeWidget, self).__init__()

        self.layout = QWidget(self)
        self.vbox = QVBoxLayout(self)
        self.dateLabel = QLabel(self)
        self.date = QDate()
        self.timeLabel = QLabel(self)
        self.time = QTime()
        self.emptyLabel = QLabel(self)
        self.eventsLabel = QLabel(self)
        self.eventsTable = QTableWidget(self)
        self.tasksLabel = QLabel(self)
        self.tasksTable = QTableWidget(self)
        self.time_timer = QTimer(self)
        self.events_timer = QTimer(self)
        self.calendar_date = datetime.datetime.now()
        self.events = []
        self.tasks = []

        self.update_events()
        self.update_tasks()
        self.initialize_user_interface()
        self.start_timers()

    def initialize_user_interface(self):
        self.dateLabel.setText(self.date.currentDate().toString())
        self.dateLabel.setStyleSheet("font-size: 24pt; color: white")
        self.vbox.addWidget(self.dateLabel)

        self.timeLabel.setText(self.time.currentTime().toString())
        self.timeLabel.setStyleSheet("font-size: 24pt; color: white")
        self.vbox.addWidget(self.timeLabel)

        self.vbox.addWidget(self.emptyLabel)

        self.eventsLabel.setText("Events:")
        self.eventsLabel.setStyleSheet("font-size: 24pt; color: white")
        self.vbox.addWidget(self.eventsLabel)

        self.eventsTable .setColumnCount(2)
        self.eventsTable.verticalHeader().setVisible(False)
        self.eventsTable.horizontalHeader().setVisible(False)
        self.eventsTable.setStyleSheet("border: 0px; font-size: 20pt; color: white")
        self.vbox.addWidget(self.eventsTable)
        self.update_displayed_events()

        self.tasksLabel.setText("Tasks:")
        self.tasksLabel.setStyleSheet("font-size: 24pt; color: white")
        self.vbox.addWidget(self.tasksLabel)

        self.tasksTable.setColumnCount(1)
        self.tasksTable.verticalHeader().setVisible(False)
        self.tasksTable.horizontalHeader().setVisible(False)
        self.tasksTable.setStyleSheet("border: 0px; font-size: 20pt; color: white")
        self.vbox.addWidget(self.tasksTable)
        self.update_displayed_tasks()

        self.layout.setLayout(self.vbox)

    def start_timers(self):
        self.time_timer.setInterval(1000)
        self.time_timer.timeout.connect(self.update_displayed_time)
        self.time_timer.timeout.connect(self.update_displayed_date)
        self.time_timer.start()

        self.events_timer.setInterval(300000)
        self.events_timer.timeout.connect(self.update_displayed_events)
        self.events_timer.timeout.connect(self.update_displayed_tasks)
        self.events_timer.start()

    def update_displayed_time(self):
        self.timeLabel.setText(self.time.currentTime().toString())

    def update_displayed_date(self):
        self.dateLabel.setText(self.date.currentDate().toString())

    def update_displayed_events(self):
        row = 0
        self.eventsTable.setRowCount(0)
        for event in self.events:
            event_date_time_string = event['start'].get('dateTime').split("T")
            event_date_string = event_date_time_string[0]
            event_date_datetime = datetime.datetime.strptime(event_date_string, '%Y-%m-%d')
            if event_date_datetime.date() == self.calendar_date.date():
                self.eventsTable.insertRow(row)
                table_item_time = QTableWidgetItem(event_date_time_string[1].split("-")[0])
                table_item_title = QTableWidgetItem(event['summary'])
                self.eventsTable.setItem(row, 0, table_item_time)
                self.eventsTable.setItem(row, 1, table_item_title)
                self.eventsTable.resizeColumnsToContents()
                row = row + 1
        self.eventsTable.update()

    def update_displayed_tasks(self):
        row = 0
        self.tasksTable.setRowCount(0)
        for task in self.tasks:
            task_date_time_string = task['due'].split("T")
            task_date_string = task_date_time_string [0]
            task_date_datetime = datetime.datetime.strptime(task_date_string, '%Y-%m-%d')
            if task_date_datetime.date() == self.calendar_date.date():
                self.tasksTable.insertRow(row)
                table_item_title = QTableWidgetItem(task['title'])
                self.tasksTable.setItem(row, 0, table_item_title)
                self.tasksTable.resizeColumnsToContents()
                row = row + 1
        self.tasksTable.update()

    def get_credentials(self, type):
        """
        Citation for this function:
        "Python Quickstart", Google Calendar API, 2017. [Online]. Available:
        https://developers.google.com/google-apps/calendar/quickstart/python. [Accessed: 22-Mar-2017]
        """
        current_dir = os.getcwd()
        credential_dir = os.path.join(current_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        if type == "events":
            credential_path = os.path.join(credential_dir,
                                           'events-credidentials.json')
        elif type == "tasks":
            credential_path = os.path.join(credential_dir,
                                           'tasks-credidentials.json')

        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            if type == "events":
                flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.CALENDAR_SCOPES)
            else:
                flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.TASKS_SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            credentials = tools.run_flow(flow, store, None)
        return credentials

    def update_events(self):
        """
        Citation for this function:
        "Python Quickstart", Google Calendar API, 2017. [Online]. Available:
        https://developers.google.com/google-apps/calendar/quickstart/python. [Accessed: 22-Mar-2017]
        """
        credentials = self.get_credentials("events")
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        self.events = service.events().list(calendarId='primary',
                                            singleEvents=True, orderBy='startTime').execute().get('items', [])

    def update_tasks(self):
        """
        Citation for this function:
        "Python Quickstart", Google Tasks API, 2017. [Online]. Available:
        https://developers.google.com/google-apps/tasks/quickstart/python. [Accessed: 22-Mar-2017]
        """
        self.tasks = []
        credentials = self.get_credentials("tasks")
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('tasks', 'v1', http=http)

        taskLists = service.tasklists().list().execute().get('items', [])

        for tasklist in taskLists:
            tasks = service.tasks().list(tasklist=tasklist['id']).execute()
            for task in tasks['items']:
                self.tasks.append(task)

    def keyPressUsed(self, e) -> bool:
        if e.key() == Qt.Key_S:
            self.calendar_date = self.calendar_date + timedelta(1)
            self.update_displayed_events()
            self.update_displayed_tasks()
            return True
        elif e.key() == Qt.Key_W:
            self.calendar_date = self.calendar_date + timedelta(-1)
            self.update_displayed_events()
            self.update_displayed_tasks()
            return True
        elif e.key() == Qt.Key_D:
            self.update_events()
            self.update_displayed_events()
            self.update_tasks()
            self.update_displayed_tasks()
            return True

        return False

    @staticmethod
    def name():
        return "DateTimeWidget"


