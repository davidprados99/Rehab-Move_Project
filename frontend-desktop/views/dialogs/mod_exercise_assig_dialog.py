from PySide6.QtWidgets import QCheckBox, QComboBox, QCompleter, QDateEdit, QDialog, QMessageBox,QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
from PySide6.QtGui import QIcon, Qt
from PySide6.QtCore import QDate

class ModExerciseAssigDialog(QDialog):

    def __init__(self, api_client, exercise_assignment_data=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("Editar Plan de Ejercicio")
        self.setMinimumWidth(400)
        self.setWindowIcon(QIcon("assets/logo_Rehab_Move.png"))
        self.init_ui()
        self.load_data_api()
        if exercise_assignment_data:
            self.load_exercise_assignment_data(exercise_assignment_data)

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Editar Plan de Ejercicio")
        title.setObjectName("QLabelFormTitle")
        layout.addWidget(title)

        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)

        self.name_patient = QComboBox()
        self.name_patient.setEditable(True)
        self.name_patient.setPlaceholderText("Nombre del paciente")
        # Configure the completer to filter based on substring match and show a popup
        self.name_patient.completer().setFilterMode(Qt.MatchContains)
        self.name_patient.completer().setCompletionMode(QCompleter.PopupCompletion)

        self.name_exercise = QComboBox()
        self.name_exercise.setEditable(True)
        self.name_exercise.setPlaceholderText("Nombre del ejercicio")
        # Configure the completer to filter based on substring match and show a popup
        self.name_exercise.completer().setFilterMode(Qt.MatchContains)
        self.name_exercise.completer().setCompletionMode(QCompleter.PopupCompletion) 

        self.weekly_frequency_input = QLineEdit()
        self.weekly_frequency_input.setPlaceholderText("Frecuencia semanal")

        self.series_input = QLineEdit()
        self.series_input.setPlaceholderText("Número de series")

        self.repetitions_input = QLineEdit()
        self.repetitions_input.setPlaceholderText("Número de repeticiones")

        self.start_date_input = QDateEdit()
        self.start_date_input.setDisplayFormat("dd-MM-yyyy")
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())

        self.end_date_input = QDateEdit()
        self.end_date_input.setDisplayFormat("dd-MM-yyyy")
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate().addDays(7)) # Default to one week later

        self.form_layout.addRow("Paciente:", self.name_patient)
        self.form_layout.addRow("Ejercicio:", self.name_exercise)
        self.form_layout.addRow("Frecuencia semanal:", self.weekly_frequency_input)
        self.form_layout.addRow("Número de series:", self.series_input)
        self.form_layout.addRow("Número de repeticiones:", self.repetitions_input)
        self.form_layout.addRow("Fecha de inicio:", self.start_date_input)
        self.form_layout.addRow("Fecha de fin:", self.end_date_input)
        layout.addLayout(self.form_layout)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Guardar Cambios")
        self.save_btn.setObjectName("LoginBtn")
        
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setObjectName("CancelBtn")
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

        # Conexiones
        self.save_btn.clicked.connect(self.accept) # Close with accept code to indicate success
        self.cancel_btn.clicked.connect(self.reject) # Close with reject code to indicate cancellation
    
    def accept(self):
        if self.weekly_frequency_input.text().strip() and not self.weekly_frequency_input.text().strip().isdigit():
            QMessageBox.warning(self, "Datos inválidos", "Frecuencia semanal debe ser un número entero.")
            return
        if self.series_input.text().strip() and not self.series_input.text().strip().isdigit():
            QMessageBox.warning(self, "Datos inválidos", "Número de series debe ser un número entero.")
            return
        if self.repetitions_input.text().strip() and not self.repetitions_input.text().strip().isdigit():
            QMessageBox.warning(self, "Datos inválidos", "Número de repeticiones debe ser un número entero.")
            return
        if not self.start_date_input.date().isValid() or not self.end_date_input.date().isValid():
            QMessageBox.warning(self, "Datos inválidos", "Las fechas deben tener el formato DD-MM-YYYY.")
            return
        
        super().accept() # Close the dialog with accept code

    def load_data_api(self):
        # Load patients and exercises from the API to populate the combo boxes
        self.name_patient.clear()
        self.name_exercise.clear() 
        success_patients, patients = self.api_client.get_patients()
        success_exercises, exercises = self.api_client.get_exercises()

        if success_patients:
            for patient in patients:
                self.name_patient.addItem(f"{patient.get('id_patient', 'N/A')} - {patient.get('name', 'N/A')} {patient.get('surnames', 'N/A')}")
        else:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los pacientes: {patients}")

        if success_exercises:
            for exercise in exercises:
                self.name_exercise.addItem(f"{exercise.get('id_exercise', 'N/A')} - {exercise.get('name', 'N/A')}")
        else:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los ejercicios: {exercises}")
    
    def load_exercise_assignment_data(self, exercise_assignment_data):
        """Load existing exercise assignment data into the form."""
        if not exercise_assignment_data:
            return
        
        patient_id = exercise_assignment_data.get("id_patient")
        exercise = exercise_assignment_data.get("name_exercise")

        # Set the current index of the patient combo box based on the patient ID
        for i in range(self.name_patient.count()):
            if self.name_patient.itemText(i).startswith(f"{patient_id} -"):
                self.name_patient.setCurrentIndex(i)
                break

        # Set the current index of the exercise combo box based on the exercise name
        for i in range(self.name_exercise.count()):
            if self.name_exercise.itemText(i).endswith(f" - {exercise}"):
                self.name_exercise.setCurrentIndex(i)
                break

        self.weekly_frequency_input.setText(str(exercise_assignment_data.get("weekly_frequency", "")))
        self.series_input.setText(str(exercise_assignment_data.get("series", "")))
        self.repetitions_input.setText(str(exercise_assignment_data.get("repetitions", "")))

        start_date_str = exercise_assignment_data.get("start_date")
        end_date_str = exercise_assignment_data.get("end_date")

        if start_date_str:
            start_date = QDate.fromString(start_date_str, "yyyy-MM-dd")
            if start_date.isValid():
                self.start_date_input.setDate(start_date)


        if end_date_str:
            end_date = QDate.fromString(end_date_str, "yyyy-MM-dd")
            if end_date.isValid():
                self.end_date_input.setDate(end_date)

    def get_data(self):
        """Return the data entered by the user as a dictionary."""
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")

        return {
            "id_patient": self.name_patient.currentText().split(" - ")[0] if self.name_patient.currentText() else None,
            "id_exercise": self.name_exercise.currentText().split(" - ")[0] if self.name_exercise.currentText() else None,
            "weekly_frequency": self.weekly_frequency_input.text() if self.weekly_frequency_input.text().strip() else None,
            "series": self.series_input.text() if self.series_input.text().strip() else None,
            "repetitions": self.repetitions_input.text() if self.repetitions_input.text().strip() else None,
            "start_date": start_date if self.start_date_input.date().isValid() else None,
            "end_date": end_date if self.end_date_input.date().isValid() else None
        }