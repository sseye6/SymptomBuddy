# Import necessary pyqt5 modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QLineEdit, QTextEdit, QComboBox, QSlider, QCheckBox, QScrollArea
import datetime

class NotesWidget(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        db_manager.addWidget("Notes")
        self.initUI()    

    def initUI(self):
        # Set up the notes widget UI
        self.setWindowTitle('Symptom Buddy - Notes')
        self.setGeometry(100, 100, 20, 20)

        notes_frame = QFrame()
        notes_frame.setFrameShape(QFrame.StyledPanel)

        frame_layout = QVBoxLayout()
        notes_label = QLabel('Notes')
        frame_layout.addWidget(notes_label)

        notes_text_edit = QTextEdit()
        frame_layout.addWidget(notes_text_edit)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_note)
        frame_layout.addWidget(save_button)

        notes_frame.setLayout(frame_layout)
        main_layout = QVBoxLayout()
        main_layout.addWidget(notes_frame)
        self.setLayout(main_layout)


    def save_note(self):
        # save notes to database for lookup later
        note_contents = str(self.findChild(QTextEdit).toPlainText())
        self.db_manager.addNote("Notes", datetime.datetime.now().strftime("%Y-%m-%d"), datetime.datetime.now().strftime("%H:%M"), note_contents)
        self.findChild(QTextEdit).setText("")
        

class TrackerWidget(QWidget):
    def __init__(self, tracker_type, units):
        super().__init__()
        self.tracker_type = tracker_type
        self.units = units
        self.initUI()

    def initUI(self):
        # Set up the tracker widget UI
        self.setWindowTitle(f'Symptom Buddy - {self.tracker_type} Tracker')
        self.setGeometry(100, 100, 20, 20)

        tracker_frame = QFrame()
        tracker_frame.setFrameShape(QFrame.StyledPanel)

        frame_layout = QVBoxLayout()
        tracker_label = QLabel(self.tracker_type)
        tracker_label.setAlignment(Qt.AlignCenter)
        adjust_layout = QHBoxLayout()
        decrease_button = QPushButton('-')
        decrease_button.clicked.connect(self.decrease_value)
        input_field = QLineEdit()
        input_field.setText('0')
        input_field.textChanged.connect(self.validate_input)
        increase_button = QPushButton('+')
        increase_button.clicked.connect(self.increase_value)
        adjust_layout.addWidget(decrease_button)
        adjust_layout.addWidget(input_field)
        adjust_layout.addWidget(increase_button)
        units_label = QLabel(self.units)
        units_label.setAlignment(Qt.AlignCenter)
        
        frame_layout.addWidget(tracker_label)
        frame_layout.addLayout(adjust_layout)
        frame_layout.addWidget(units_label)
        tracker_frame.setLayout(frame_layout)
        main_layout = QVBoxLayout()
        main_layout.addWidget(tracker_frame)
        self.setLayout(main_layout)

    def update_value(self, new_value):
        # Update the value in the input field
        self.findChild(QLineEdit).setText(str(new_value))

    def get_value(self):
        # Get the current value from the input field
        return self.findChild(QLineEdit).text()
    
    def set_units(self, new_units):
        # Update the units label
        self.findChild(QLabel, self.units).setText(new_units)
    
    def increase_value(self):
        # Increase the value by 1
        current_value = int(self.get_value())
        self.update_value(current_value + 1)
    
    def decrease_value(self):
        # Decrease the value by 1
        current_value = int(self.get_value())
        self.update_value(current_value - 1)

    def validate_input(self):
        # Validate that the input is a number
        try:
            self.update_value(max(0, int(self.get_value())))
            return True
        except ValueError:
            self.update_value(0)
            return False

class TreatmentWidget(QWidget):
    def __init__(self, treatment_details = {}):
        super().__init__()
        self.treatment_details = treatment_details
        self.initUI()

    def initUI(self):
        # Set up the treatment widget UI
        self.setWindowTitle('Symptom Buddy - Treatments')
        self.setGeometry(100, 100, 20, 20)

        treatment_frame = QFrame()
        treatment_frame.setFrameShape(QFrame.StyledPanel)

        frame_layout = QVBoxLayout()
        treatment_label = QLabel('Treatments')
        frame_layout.addWidget(treatment_label)

        for treatment in self.treatment_details.keys():
            treatment_info = self.treatment_details[treatment]
            treatment_entry_layout = QGridLayout()
            treatment_time_label = QLabel(treatment_info['time'])
            treatment_taken_checkbox = QCheckBox()
            treatment_name_label = QLabel(treatment)
            treatment_dosage_label = QLabel(f"{treatment_info['dosage']} {treatment_info['units']}")
            treatment_entry_layout.addWidget(treatment_time_label, 0, 0)
            treatment_entry_layout.addWidget(treatment_taken_checkbox, 1, 0)
            treatment_entry_layout.addWidget(treatment_name_label, 1, 1)
            treatment_entry_layout.addWidget(treatment_dosage_label, 1, 2)

            frame_layout.addLayout(treatment_entry_layout)

        add_treatment_button = QPushButton('Add Treatment')
        frame_layout.addWidget(add_treatment_button)

        treatment_frame.setLayout(frame_layout)
        main_layout = QVBoxLayout()
        main_layout.addWidget(treatment_frame)
        self.setLayout(main_layout)

class MoodWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the mood widget UI
        self.setWindowTitle('Symptom Buddy - Mood')
        self.setGeometry(100, 100, 20, 20)

        mood_frame = QFrame()
        mood_frame.setFrameShape(QFrame.StyledPanel)

        frame_layout = QVBoxLayout()
        mood_label = QLabel('Mood')
        mood_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(mood_label)

        mood_slider = QSlider(Qt.Horizontal)
        mood_slider.setMinimum(1)
        mood_slider.setMaximum(5)
        mood_slider.setValue(3)
        mood_slider.setTickPosition(QSlider.TicksBelow)
        mood_slider.setTickInterval(1)
        mood_slider.valueChanged.connect(self.update_mood_description)
        frame_layout.addWidget(mood_slider)

        self.mood_desc_label = QLabel('Neutral')
        self.mood_desc_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.mood_desc_label)

        submit_mood_button = QPushButton('Submit Mood')
        frame_layout.addWidget(submit_mood_button)

        mood_frame.setLayout(frame_layout)
        main_layout = QVBoxLayout()
        main_layout.addWidget(mood_frame)
        self.setLayout(main_layout)

    def update_mood_description(self):
        # Update the mood description based on the slider value
        descriptions = {
            1: 'Very Bad',
            2: 'Bad',
            3: 'Neutral',
            4: 'Good',
            5: 'Very Good'
        }
        self.mood_desc_label.setText(descriptions.get(self.get_mood_value(), 'Neutral'))

    def get_mood_value(self):
        # Get the current mood value from the slider
        return self.findChild(QSlider).value()

class SymptomsWidget(QWidget):
    def __init__(self, checkin_complete = False, trends_data = {}):
        super().__init__()
        self.checkin_complete = checkin_complete
        self.trends_data = trends_data
        self.initUI()


    def initUI(self):
        # Set up the symptoms widget UI
        self.setWindowTitle('Symptom Buddy - Symptoms')
        self.setGeometry(100, 100, 20, 20)
        
        main_layout = QVBoxLayout()
        symptoms_frame = QFrame()
        symptoms_frame.setFrameShape(QFrame.StyledPanel)

        frame_layout = QVBoxLayout()
        if self.checkin_complete:
            track_symptoms_button = QPushButton('Daily Symptom Check-in Complete')
        else:
            track_symptoms_button = QPushButton('Complete Daily Symptom Check-in')
        frame_layout.addWidget(track_symptoms_button)

        trends_layout = QHBoxLayout()
        for trend in self.trends_data.keys():
            trend_button = QPushButton(f"{trend}: {self.trends_data[trend]}")
            trends_layout.addWidget(trend_button)

        frame_layout.addLayout(trends_layout)

        to_insights_button = QPushButton('View Insights')
        frame_layout.addWidget(to_insights_button)

        symptoms_frame.setLayout(frame_layout)
        main_layout.addWidget(symptoms_frame)
        self.setLayout(main_layout)

    def update_checkin_status(self, value):
        self.checkin_complete = value
