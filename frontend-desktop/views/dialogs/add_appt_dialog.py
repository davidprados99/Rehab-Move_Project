from PySide6.QtWidgets import QComboBox, QCompleter, QDialog, QFormLayout, QHBoxLayout, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class AddApptDialog(QDialog):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("Agregar Cita")
        self.setWindowIcon(QIcon("assets/logo_Rehab&Move.png"))
        self.resize(350, 500)
        self.init_ui()
        
    def init_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel("Nueva Cita")
        title.setObjectName("QLabelFormTitle")
        layout.addWidget(title)

        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)

        self.name_patient = QComboBox()
        self.name_patient.setEditable(True)
        self.name_patient.setPlaceholderText("Nombre del paciente")
        self.name_patient.completer().setFilterMode(Qt.MatchContains)
        self.name_patient.completer().setCompletionMode(QCompleter.PopupCompletion)

        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Notas adicionales para la cita")

        self.form_layout.addRow("Paciente:", self.name_patient)
        self.form_layout.addRow("Notas:", self.notes_input)
        layout.addLayout(self.form_layout)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Guardar Cita")
        self.save_btn.setObjectName("LoginBtn")
        self.cancel_btn = QPushButton("Cancelar") 
        self.cancel_btn.setObjectName("CancelBtn")
        
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)

        self.save_btn.clicked.connect(self.accept) # Close with accept code to indicate success
        self.cancel_btn.clicked.connect(self.reject) # Close with reject code to indicate cancellation
    
    def accept(self):
        # Basic validation: Ensure patient is selected
        if not self.name_patient.currentText().strip():
            QMessageBox.critical(self, "Error", "El paciente es obligatorio.")
            self.name_patient.setFocus()
            return    
        super().accept()  # Call the base class accept to close the dialog with success code
    
    def load_data_api(self):
        # Load patients and exercises from the API to populate the combo boxes
        self.name_patient.clear()
        success_patients, patients = self.api_client.get_patients()


        if success_patients:
            for patient in patients:
                self.name_patient.addItem(f"{patient.get('id_patient', 'N/A')} - {patient.get('name', 'N/A')} {patient.get('surnames', 'N/A')}")
        else:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los pacientes: {patients}")

    def get_data(self):
        """Return the data entered by the user as a dictionary."""
        return {
            "date": self.date_str,  # This should be set when opening the dialog
            "state": "pendiente",  # Default state for new appointments
            "notes": self.notes_input.text().strip() if self.notes_input.text().strip() else None,
            "id_patient": int(self.name_patient.currentText().split(" - ")[0]),
            "id_physio": None  # This should be set by the controller based on the logged-in physio
        }