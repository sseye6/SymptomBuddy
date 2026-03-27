# import neccessary pyqt modules
import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox
import datetime

class DatabaseManager():
    def __init__(self, connection_name):
        self.connection_name = connection_name
        self.addWidgetsTable()
        self.addNotesTable()

    def addWidgetsTable(self):
        # create a table to keep track of active widgets
        db = QSqlDatabase.database(self.connection_name)
        query = QSqlQuery(db)
        if not query.exec(
            f"""
            CREATE TABLE IF NOT EXISTS widgets
            (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
            widget_name TEXT UNIQUE NOT NULL); 
            """
        ):
            print("Error: AddWidgetTable", db.lastError().databaseText())
        db.close()


    def addWidget(self, widget_name):
        #add a widget to keep track of to widgets table
        db = QSqlDatabase.database(self.connection_name)
        query = QSqlQuery(db)
        query.exec(
            f"""
            INSERT INTO widgets (widget_name)
            VALUES ('{widget_name}');
            """
        )
        db.close()

    def findWidgetId(self, widget_name):
        #lookup widgetid from name
        db = QSqlDatabase.database(self.connection_name)
        query = QSqlQuery(db)
        if not query.exec(
            f"""
            SELECT id FROM widgets WHERE widget_name='{widget_name}';
            """
        ): 
            print("error:Find Widget ID")
        if not query.first():
            print("error:Find Widget ID")
            db.close()
            return -1
        id = query.value(0)
        db.close()
        return id

    def addNotesTable(self):
        # create a table to keep track of saved notes 
        # from notes widget
        db = QSqlDatabase.database(self.connection_name)
        query = QSqlQuery(db)
        if not query.exec(
            f"""
            CREATE TABLE IF NOT EXISTS notes
            (note_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
            widget_id INTEGER,
            date TEXT NOT NULL,
            time TEXT,
            note TEXT); 
            """
        ):
            print("Error: add Notes Table")
        print(db.tables())
        db.close()

    def addNote(self, widget_name, date, time, note):
        #save a note to notes table
        widget_id = self.findWidgetId(widget_name)
        db = QSqlDatabase.database(self.connection_name)
        query = QSqlQuery(db)
        query.exec(
            f"""
            INSERT INTO notes (widget_id, date, time, note)
            VALUES ({widget_id}, '{date}','{time}', '{note}');
            """
        )
        query = QSqlQuery(db)
        query.exec('SELECT note_id, date, time, note FROM notes')
        note_id, date, time, note = range(4)
        while query.next():
            print(query.value(note_id), query.value(date), query.value(time), query.value(note))
        db.close()

    def getNotesByDate(self, widget_name, date=None):
        #lookup all notes from a date, organized by time
        widget_id = self.findWidgetId(widget_name)
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        db = QSqlDatabase.database(self.connection_name)
        query = QSqlQuery(db)
        query.exec(
            f"""
            SELECT time, note FROM notes WHERE date='{date}' ORDER BY time;
            """
        )
        time, note = range(2)
        notes = []
        while query.next:
            notes.append((query.value(time), query.value(note)))
        db.close()
        return notes