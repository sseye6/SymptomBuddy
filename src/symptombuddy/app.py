# import necessary modules from PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from ui.dashboard import Dashboard
import datetime

class SymptomBuddyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Symptom Buddy')
        self.setGeometry(100, 100, 1200, 300)

        # Create layout
        main_layout = QHBoxLayout()

        # Create left panel for menu
        menu_layout = QVBoxLayout()
        self.menu_label = QLabel('Menu')
        self.menu_label.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        self.menu_dashboard_button = QPushButton('Dashboard')
        self.menu_track_new_button = QPushButton('Track New')
        self.menu_treatments_button = QPushButton('Treatments')
        self.menu_journal_button = QPushButton('Journal')
        self.menu_insights_button = QPushButton('Insights')
        self.menu_settings_button = QPushButton('Settings')

        menu_layout.addWidget(self.menu_label)
        menu_layout.addWidget(self.menu_dashboard_button)
        menu_layout.addWidget(self.menu_track_new_button)
        menu_layout.addWidget(self.menu_treatments_button)
        menu_layout.addWidget(self.menu_journal_button)
        menu_layout.addWidget(self.menu_insights_button)
        menu_layout.addWidget(self.menu_settings_button)

        # Create right panel for content
        self.content_layout = QVBoxLayout()
        self.content_label = QLabel('Welcome to Symptom Buddy!')
        self.content_label.setAlignment(Qt.AlignCenter)

        self.date_time_label = QLabel(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
        self.date_time_label.setAlignment(Qt.AlignCenter)

        self.dashboard = Dashboard()

        self.content_layout.addWidget(self.content_label)
        self.content_layout.addWidget(self.date_time_label)
        self.content_layout.addWidget(self.dashboard)

        # Add panels to main layout
        main_layout.addLayout(menu_layout)
        main_layout.addLayout(self.content_layout)
        self.setLayout(main_layout)


if __name__ == '__main__':
    app = QApplication([])
    symptom_buddy_app = SymptomBuddyApp()
    symptom_buddy_app.show()
    app.exec_()

        