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
        self.addTrackerTable()
        self.addMoodTable()

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
        # query = QSqlQuery(db)
        # query.exec(
        #     f"""
        #     SELECT id, widget_name FROM widgets;
        #     """
        # )
        # id, name= range(2)
        # while query.next():
        #     print(query.value(id), query.value(name))
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
            notes.append({'time': query.value(time), 'note': query.value(note)})
        db.close()
        return notes
    
    def addTrackerTable(self):
        # create a table to keep track of various tracked
        # values from tracker widget
        db = QSqlDatabase.database(self.connection_name)
        query = QSqlQuery(db)
        if not query.exec(
            f"""
            CREATE TABLE IF NOT EXISTS tracker_logs
            (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
            widget_id INTEGER,
            date TEXT NOT NULL,
            time TEXT,
            tracker_type TEXT UNIQUE NOT NULL,
            value INTEGER, 
            units TEXT); 
            """
        ):
            print("Error: Unable to initiate trackers table")
        db.close()

    def addTrackerEntry(self, widget_name, date, time, tracker_type, value, units):
        # print(widget_name, date, time, tracker_type, value, units)
        widget_id = self.findWidgetId(widget_name)
        db = QSqlDatabase.database(self.connection_name)
        query = QSqlQuery(db)
        if not query.exec(
            f"""
            INSERT INTO tracker_logs (widget_id, date, time, tracker_type, value, units)
            VALUES ({widget_id}, '{date}', '{time}', '{tracker_type}', {value}, '{units}');
            """
        ):
            print('Error: cannot add tracker entry', db.lastError().databaseText())
        
        db.close()

    def getTrackerByType(self, tracker_type, date = None):
        db = QSqlDatabase.database(self.connection_name)
        query = QSqlQuery(db)
        if date:
            query.exec(
                f"""
                SELECT date, time, value, units FROM tracker_logs WHERE tracker_type='{tracker_type}' 
                AND date='{date}' ORDER BY date, time;
                """
            )
        else:
            query.exec(
                f"""
                SELECT date, time, value, units FROM tracker_logs WHERE tracker_type='{tracker_type}' 
                ORDER BY date, time;
                """
            )

        d, t, v, u = range(4)
        values = []
        while query.next():
            values.append({'date': query.value(d), 'time': query.value(t), 'value': query.value(v),
                            'units':query.value(u)})

        db.close()
        return values
    
    def updateTrackerValue(self, widget_name, date, time, value):
        widget_id = self.findWidgetId(widget_name)
        db = QSqlDatabase.database(self.connection_name)
        query = QSqlQuery(db)
        if not query.exec(
            f"""
            UPDATE tracker_logs
            SET time='{time}', value ='{value}'
            WHERE widget_id='{widget_id}' AND date='{date}';
            """
        ):
            print("Error: can't update tracker vlaue")

        db.close()

    def initTrackerValue(self, widget_name, date, tracker_type, units):
        widget_id = self.findWidgetId(widget_name)
        db = QSqlDatabase.database(self.connection_name)
        query = QSqlQuery(db)
        if not query.exec(
            f"""
            SELECT value FROM tracker_logs WHERE widget_id={widget_id} AND date='{date}';
            """
        ):
            print("Error: can't find tracker value")
        value = 0
        if query.next():
            value = query.value(0)
            db.close()
        else:
            db.close()
            self.addTrackerEntry(widget_name, date, "00:00", tracker_type, 0, units)
        return value
    
    def addMoodTable(self):
        # create a table to keep track of mood
        # values from mood widget
        db = QSqlDatabase.database(self.connection_name)
        query = QSqlQuery(db)
        if not query.exec(
            f"""
            CREATE TABLE IF NOT EXISTS mood_logs
            (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
            widget_id INTEGER,
            date TEXT NOT NULL,
            time TEXT,
            value INTEGER); 
            """
        ):
            print("Error: Unable to initiate mood table")
        db.close()

    def addMoodEntry(self, widget_name, date, time, value):
        widget_id = self.findWidgetId(widget_name)
        db = QSqlDatabase.database(self.connection_name)
        query = QSqlQuery(db)
        if not query.exec(
            f"""
            INSERT INTO mood_logs (widget_id, date, time, value)
            VALUES ({widget_id}, '{date}', '{time}', {value});
            """
        ):
            print("Error: Unable to initiate trackers table")
        db.close()

    def initMoodValue(self, widget_name, date):
        widget_id = self.findWidgetId(widget_name)
        db = QSqlDatabase.database(self.connection_name)
        query = QSqlQuery(db)
        if not query.exec(
            f"""
            SELECT value FROM mood_logs WHERE date='{date}' ORDER BY time DESC;
            """
        ):
            print("Error: Unable to initiate trackers table")
        value = 3
        if query.next():
            value = query.value(0)
        db.close()
        return value