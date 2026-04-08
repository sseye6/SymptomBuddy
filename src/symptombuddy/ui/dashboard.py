# Import necessary pyqt5 modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QLineEdit, QTextEdit, QComboBox, QSlider, QCheckBox, QScrollArea
from .widgets import NotesWidget, TrackerWidget, TreatmentWidget, MoodWidget, SymptomsWidget

class Dashboard(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.initUI()
        

    def initUI(self):
        # Set up the dashboard UI
        self.setWindowTitle('Symptom Buddy - Dashboard')
        self.setGeometry(100, 100, 400, 300)

        # Create layout
        main_layout = QVBoxLayout()
        
        frame_layout = QGridLayout()
        frame_layout.setSpacing(10)

        # Add sample trackers and notes to the dashboard
        sample_symptom = {
            "Headache": f"5% increase",
            "Fatigue": f"3% increase"
        }
        symptom_tracker = SymptomsWidget(False, sample_symptom)
        frame_layout.addWidget(symptom_tracker, 0, 0)

        water_tracker = TrackerWidget('Water Intake', 'glasses', self.db_manager)
        frame_layout.addWidget(water_tracker, 1, 0)

        sleep_tracker = TrackerWidget('Sleep', 'hours', self.db_manager)
        frame_layout.addWidget(sleep_tracker, 2, 0)

        exercise_tracker = TrackerWidget('Exercise', 'minutes', self.db_manager)
        frame_layout.addWidget(exercise_tracker, 3, 0)

        notes_widget = NotesWidget(self.db_manager)
        frame_layout.addWidget(notes_widget, 1, 1)

        sample_treatment = {
            "Medication A": {"time": "08:00", "dosage": 2, "units": "pills"},
            "Medication B": {"time": "12:00", "dosage": 1, "units": "tablet"}
        }
        treatment_widget = TreatmentWidget(sample_treatment)
        frame_layout.addWidget(treatment_widget, 2, 1)

        mood_widget = MoodWidget()
        frame_layout.addWidget(mood_widget, 3, 1)

        main_layout.addLayout(frame_layout)

        edit_dashboard_button = QPushButton('+ Edit Dashboard')
        main_layout.addWidget(edit_dashboard_button)

        self.setLayout(main_layout)

